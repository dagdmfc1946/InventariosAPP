import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import SimpleTestCase
from runtime_local import DataLock, configure_runtime
from launcher import parser


class LocalRuntimeTests(SimpleTestCase):
    def test_installation_key_is_persistent_and_debug_is_disabled(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ):
            directory = Path(temp) / 'installation'
            with DataLock(directory):
                configure_runtime(directory)
                first = os.environ['SECRET_KEY']
                self.assertGreaterEqual(len(first), 50)
                self.assertEqual(os.environ['DEBUG'], 'False')
                self.assertEqual(os.environ['ALLOWED_HOSTS'], '127.0.0.1,localhost')
                self.assertFalse((directory / 'db.sqlite3').exists())
                configure_runtime(directory)
                self.assertEqual(os.environ['SECRET_KEY'], first)

    def test_data_lock_blocks_second_process_handle_and_releases(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / 'installation'
            with DataLock(directory):
                with self.assertRaises(RuntimeError):
                    with DataLock(directory):
                        pass
            with DataLock(directory):
                pass

    def test_manage_arguments_and_loopback_only_configuration(self):
        parsed = parser().parse_args(['manage', 'createsuperuser'])
        self.assertEqual(parsed.arguments, ['createsuperuser'])
        with self.assertRaises(SystemExit):
            parser().parse_args(['serve', '--host', '0.0.0.0'])

    def test_invalid_key_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ):
            directory = Path(temp)
            (directory / '.runtime-key').write_text('short')
            with self.assertRaises(ValueError):
                configure_runtime(directory)
            self.assertEqual((directory / '.runtime-key').read_text(), 'short')
