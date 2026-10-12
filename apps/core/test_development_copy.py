import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

from django.test import SimpleTestCase

from backups.prepare_dev import prepare_development_copy


class DevelopmentCopyTests(SimpleTestCase):
    def test_copy_is_independent_and_never_overwrites_existing_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with closing(sqlite3.connect(root / 'db.sqlite3')) as database:
                database.execute('CREATE TABLE sample (name TEXT)')
                database.execute("INSERT INTO sample VALUES ('original')")
                database.commit()
            (root / 'media').mkdir()
            (root / 'media' / 'sample.pdf').write_bytes(b'%PDF-test')
            destination = root / 'isolated'
            prepare_development_copy(root, destination)
            with closing(sqlite3.connect(destination / 'db.sqlite3')) as copied:
                copied.execute("UPDATE sample SET name = 'development'")
                copied.commit()
            with closing(sqlite3.connect(root / 'db.sqlite3')) as original:
                self.assertEqual(original.execute('SELECT name FROM sample').fetchone()[0], 'original')
            self.assertEqual((destination / 'media' / 'sample.pdf').read_bytes(), b'%PDF-test')
            with self.assertRaises(FileExistsError):
                prepare_development_copy(root, destination)

    def test_project_root_is_not_a_valid_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                prepare_development_copy(directory, directory)
