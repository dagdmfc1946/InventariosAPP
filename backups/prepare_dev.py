"""Crear una copia de desarrollo sin modificar ni sobrescribir datos existentes."""

import argparse
import shutil
import sqlite3
from contextlib import closing
from pathlib import Path


def prepare_development_copy(project_root, destination):
    root = Path(project_root).resolve()
    target = Path(destination).resolve()
    if target == root or root.is_relative_to(target):
        raise ValueError('La copia debe estar en un directorio separado del proyecto.')
    if target.exists():
        raise FileExistsError('El destino ya existe. No se sobrescribe una copia previa.')
    source_db = root / 'db.sqlite3'
    if not source_db.is_file():
        raise FileNotFoundError('No existe la base original; prepare una base nueva con migrate.')

    target.mkdir(parents=True)
    # La API backup obtiene un snapshot SQLite; no copia un archivo abierto a ciegas.
    with closing(sqlite3.connect(source_db.as_uri() + '?mode=ro', uri=True)) as source:
        with closing(sqlite3.connect(target / 'db.sqlite3')) as copied:
            source.backup(copied)
            if copied.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('La copia SQLite no pasó la comprobación de integridad.')
    if (root / 'media').exists():
        shutil.copytree(root / 'media', target / 'media')
    else:
        (target / 'media').mkdir()
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', default='.local/dev_v2')
    args = parser.parse_args()
    project = Path(__file__).resolve().parent.parent
    destination = Path(args.destination)
    if not destination.is_absolute():
        destination = project / destination
    print(prepare_development_copy(project, destination))
