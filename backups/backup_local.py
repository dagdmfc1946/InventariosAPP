"""Snapshots verificados. Detener las escrituras antes de copiar base y media."""
from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
import tempfile
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from config.version import __version__


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _no_links(root):
    for path in [root, *root.rglob('*')]:
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('No se admiten enlaces ni rutas fuera del respaldo.')


def _check_sqlite(path):
    with closing(sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)) as database:
        if database.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
            raise ValueError('La base SQLite no pasó la comprobación de integridad.')


def validate_backup(backup_dir):
    root = Path(backup_dir).resolve()
    _no_links(root)
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    if not isinstance(manifest, dict):
        raise ValueError('Manifiesto de respaldo inválido.')
    files = manifest.get('files', {})
    if manifest.get('format') != 1 or not isinstance(files, dict) or 'db.sqlite3' not in files:
        raise ValueError('Formato de respaldo no reconocido o incompleto.')
    for name, digest in files.items():
        parts = PurePosixPath(name)
        if (parts.is_absolute() or '..' in parts.parts or '\\' in name or ':' in name
                or not (name in ('db.sqlite3', '.runtime-key') or name.startswith('media/'))):
            raise ValueError('El respaldo contiene una ruta no permitida.')
        path = root / name
        if not path.is_file() or file_hash(path) != digest:
            raise ValueError(f'Archivo ausente o alterado en el respaldo: {name}')
    actual = {path.relative_to(root).as_posix() for path in root.rglob('*') if path.is_file()}
    if actual != set(files) | {'manifest.json'}:
        raise ValueError('El contenido no coincide con el manifiesto del respaldo.')
    if not (root / 'media').is_dir():
        raise ValueError('Falta el directorio de documentos.')
    _check_sqlite(root / 'db.sqlite3')
    return manifest


def backup_project(project_root: str | Path, output_dir: str | Path | None = None) -> Path:
    root = Path(project_root).resolve()
    if not (root / 'db.sqlite3').is_file():
        raise FileNotFoundError('No existe una base para respaldar.')
    target = Path(output_dir).resolve() if output_dir else root / 'backups' / (
        'backup_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S') + '_' + uuid.uuid4().hex[:8])
    if target == root or root.is_relative_to(target) or target.is_relative_to(root / 'media'):
        raise ValueError('El respaldo debe estar separado de la base y de media.')
    if target.exists():
        raise FileExistsError('El destino ya existe; no se sobrescriben respaldos.')
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.backup-', dir=target.parent))
    try:
        with closing(sqlite3.connect((root / 'db.sqlite3').as_uri() + '?mode=ro', uri=True)) as source:
            with closing(sqlite3.connect(staging / 'db.sqlite3')) as copied:
                source.backup(copied)
                copied.execute('PRAGMA journal_mode=DELETE')
                copied.commit()
        _check_sqlite(staging / 'db.sqlite3')
        media = root / 'media'
        if media.exists():
            _no_links(media)
            shutil.copytree(media, staging / 'media')
        else:
            (staging / 'media').mkdir()
        key = root / '.runtime-key'
        if key.exists():
            if key.is_symlink():
                raise ValueError('La clave local no puede ser un enlace.')
            shutil.copy2(key, staging / key.name)
        manifest = {'format': 1, 'version': __version__, 'created_utc': datetime.now(timezone.utc).isoformat(),
                    'files': {path.relative_to(staging).as_posix(): file_hash(path)
                              for path in sorted(staging.rglob('*')) if path.is_file()}}
        (staging / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        validate_backup(staging)
        staging.rename(target)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return target


def restore_backup(backup_dir: str | Path, project_root: str | Path, *, return_previous=False):
    backup_root = Path(backup_dir).resolve()
    root = Path(project_root).resolve()
    if root == root.parent or (root / 'manage.py').exists() or (root / '.git').exists():
        raise ValueError('Restaurar únicamente en una carpeta de datos, nunca en la raíz del proyecto o del disco.')
    if Path(project_root).is_symlink():
        raise ValueError('El destino no puede ser un enlace.')
    validate_backup(backup_root)
    root.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f'.{root.name}.restore-', dir=root.parent))
    previous = root.with_name(root.name + '.previous-' + uuid.uuid4().hex[:12])
    moved = False
    try:
        shutil.copy2(backup_root / 'db.sqlite3', staging / 'db.sqlite3')
        shutil.copytree(backup_root / 'media', staging / 'media')
        if (backup_root / '.runtime-key').exists():
            shutil.copy2(backup_root / '.runtime-key', staging / '.runtime-key')
        # Validar nuevamente la copia antes de tocar el destino.
        shutil.copy2(backup_root / 'manifest.json', staging / 'manifest.json')
        validate_backup(staging)
        (staging / 'manifest.json').unlink()
        if root.exists():
            root.rename(previous)
            moved = True
        staging.rename(root)
    except Exception:
        if moved and not root.exists():
            previous.rename(root)
        if staging.exists():
            shutil.rmtree(staging)
        raise
    # La carpeta .previous-* conserva el estado anterior íntegro para volver atrás.
    return (root, previous if moved else None) if return_previous else root
