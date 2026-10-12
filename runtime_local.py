"""Datos persistentes y bloqueo entre servidor y mantenimiento local."""
import os
import secrets
from pathlib import Path


class DataLock:
    def __init__(self, directory):
        directory = Path(directory).resolve()
        directory.parent.mkdir(parents=True, exist_ok=True)
        self.path = directory.parent / f'.{directory.name}.runtime.lock'
        self.stream = None

    def __enter__(self):
        self.stream = self.path.open('a+b')
        try:
            self.stream.seek(0)
            if not self.stream.read(1):
                self.stream.write(b'0')
                self.stream.flush()
            self.stream.seek(0)
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.stream.close()
            self.stream = None
            raise RuntimeError('Esta carpeta de datos está en uso. Detén la aplicación antes de continuar.') from None
        return self

    def __exit__(self, *args):
        if self.stream:
            self.stream.seek(0)
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream.fileno(), fcntl.LOCK_UN)
            self.stream.close()


def default_data_dir():
    local = os.environ.get('LOCALAPPDATA')
    return Path(local) / 'InventariosAPP' / 'data' if local else Path.home() / '.inventariosapp' / 'data'


def configure_runtime(directory):
    directory = Path(directory).expanduser().resolve()
    project = Path(__file__).resolve().parent
    if directory == directory.parent or directory == project or (directory / 'manage.py').exists():
        raise ValueError('Usa una carpeta de datos separada del código y de la raíz del disco.')
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'media').mkdir(exist_ok=True)
    key_path = directory / '.runtime-key'
    if not key_path.exists():
        # El bloqueo DataLock evita generar dos claves para una misma instalación.
        with key_path.open('x', encoding='utf-8') as stream:
            stream.write(secrets.token_urlsafe(64))
        try:
            key_path.chmod(0o600)
        except OSError:
            pass
    key = key_path.read_text(encoding='utf-8').strip()
    if len(key) < 50:
        raise ValueError('La clave de esta instalación no es válida. Recupera un respaldo; no la reemplaces a ciegas.')
    os.environ['INVENTARIOS_DATA_DIR'] = str(directory)
    os.environ['SECRET_KEY'] = key
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = '127.0.0.1,localhost'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_local'
    return directory
