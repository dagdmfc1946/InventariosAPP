from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


def backup_project(project_root: str | Path, output_dir: str | Path | None = None) -> Path:
    root = Path(project_root).resolve()
    if output_dir is None:
        backup_root = root / 'backups' / f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    else:
        backup_root = Path(output_dir).resolve()

    backup_root.mkdir(parents=True, exist_ok=True)

    db_file = root / 'db.sqlite3'
    if db_file.exists():
        shutil.copy2(db_file, backup_root / 'db.sqlite3')

    media_dir = root / 'media'
    if media_dir.exists():
        target_media_dir = backup_root / 'media'
        target_media_dir.mkdir(parents=True, exist_ok=True)
        for child in media_dir.iterdir():
            if child.is_dir():
                shutil.copytree(child, target_media_dir / child.name, dirs_exist_ok=True)
            else:
                shutil.copy2(child, target_media_dir / child.name)

    return backup_root


def restore_backup(backup_dir: str | Path, project_root: str | Path) -> Path:
    backup_root = Path(backup_dir).resolve()
    root = Path(project_root).resolve()

    db_backup = backup_root / 'db.sqlite3'
    if db_backup.exists():
        shutil.copy2(db_backup, root / 'db.sqlite3')

    media_backup = backup_root / 'media'
    if media_backup.exists():
        media_root = root / 'media'
        media_root.mkdir(parents=True, exist_ok=True)
        for child in media_backup.iterdir():
            if child.is_dir():
                shutil.copytree(child, media_root / child.name, dirs_exist_ok=True)
            else:
                shutil.copy2(child, media_root / child.name)

    return root
