from contextlib import closing
import json
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import SimpleTestCase
from backups.backup_local import backup_project, restore_backup, validate_backup


class BackupRecoveryTests(SimpleTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'data'
        self.root.mkdir()
        with closing(sqlite3.connect(self.root / 'db.sqlite3')) as database:
            database.execute('PRAGMA journal_mode=WAL')
            database.execute('CREATE TABLE sample (name TEXT)')
            database.execute("INSERT INTO sample VALUES ('original')")
            database.commit()
        (self.root / 'media').mkdir()
        (self.root / 'media' / 'saved.pdf').write_bytes(b'%PDF-original')
        (self.root / '.runtime-key').write_text('test-secret-key')

    def test_verified_snapshot_reads_committed_sqlite_and_refuses_overwrite(self):
        destination = Path(self.temp.name) / 'snapshot'
        snapshot = backup_project(self.root, destination)
        self.assertEqual(validate_backup(snapshot)['format'], 1)
        with closing(sqlite3.connect(snapshot / 'db.sqlite3')) as database:
            self.assertEqual(database.execute('SELECT name FROM sample').fetchone()[0], 'original')
        with self.assertRaises(FileExistsError):
            backup_project(self.root, destination)
        with self.assertRaises(ValueError):
            backup_project(self.root, self.root / 'media' / 'bad')

    def test_restore_replaces_media_and_preserves_prior_state(self):
        snapshot = backup_project(self.root, Path(self.temp.name) / 'snapshot')
        with closing(sqlite3.connect(self.root / 'db.sqlite3')) as database:
            database.execute("UPDATE sample SET name = 'changed'")
            database.commit()
        (self.root / 'media' / 'obsolete.pdf').write_bytes(b'%PDF-new')
        restore_backup(snapshot, self.root)
        self.assertFalse((self.root / 'media' / 'obsolete.pdf').exists())
        self.assertEqual((self.root / 'media' / 'saved.pdf').read_bytes(), b'%PDF-original')
        self.assertEqual((self.root / '.runtime-key').read_text(), 'test-secret-key')
        previous = list(self.root.parent.glob('data.previous-*'))
        self.assertEqual(len(previous), 1)
        self.assertTrue((previous[0] / 'media' / 'obsolete.pdf').exists())
        with closing(sqlite3.connect(self.root / 'db.sqlite3')) as database:
            self.assertEqual(database.execute('SELECT name FROM sample').fetchone()[0], 'original')

    def test_corrupt_snapshot_is_rejected_before_target_changes(self):
        snapshot = backup_project(self.root, Path(self.temp.name) / 'snapshot')
        (snapshot / 'media' / 'saved.pdf').write_bytes(b'altered')
        with self.assertRaises(ValueError):
            restore_backup(snapshot, self.root)
        self.assertEqual((self.root / 'media' / 'saved.pdf').read_bytes(), b'%PDF-original')
        self.assertFalse(list(self.root.parent.glob('data.previous-*')))

    def test_manifest_path_escape_and_extra_files_are_rejected(self):
        snapshot = backup_project(self.root, Path(self.temp.name) / 'snapshot')
        manifest = json.loads((snapshot / 'manifest.json').read_text())
        manifest['files']['../outside'] = 'bad'
        (snapshot / 'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            validate_backup(snapshot)

    def test_install_failure_restores_original_directory(self):
        snapshot = backup_project(self.root, Path(self.temp.name) / 'snapshot')
        rename = Path.rename
        def fail_install(path, target):
            if '.restore-' in path.name:
                raise OSError('simulated')
            return rename(path, target)
        with patch.object(Path, 'rename', fail_install):
            with self.assertRaises(OSError):
                restore_backup(snapshot, self.root)
        self.assertTrue((self.root / 'db.sqlite3').exists())
        self.assertTrue((self.root / 'media' / 'saved.pdf').exists())

    def test_project_directory_cannot_be_restore_destination(self):
        snapshot = backup_project(self.root, Path(self.temp.name) / 'snapshot')
        (self.root / 'manage.py').write_text('project')
        with self.assertRaises(ValueError):
            restore_backup(snapshot, self.root)
