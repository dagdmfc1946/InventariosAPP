"""Generar distribución Windows sin datos del usuario: python build_exe.py."""
import hashlib
import argparse
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from config.version import __version__


def reuse_verified_launcher(previous, executable):
    """Solo reutilizar bytes intactos cuando no cambió código, bootloader ni archivo embebido."""
    import pefile
    current = executable.read_bytes()
    image = pefile.PE(data=previous)
    fields = [(image.FILE_HEADER, 'TimeDateStamp'), (image.OPTIONAL_HEADER, 'CheckSum')]
    fields += [(entry.struct, 'TimeDateStamp') for entry in getattr(image, 'DIRECTORY_ENTRY_DEBUG', [])]
    metadata = set()
    for structure, name in fields:
        offset = structure.get_field_absolute_offset(name)
        metadata.update(range(offset, offset + 4))
    if len(previous) != len(current) or any(a != b and index not in metadata for index, (a, b) in enumerate(zip(previous, current))):
        raise RuntimeError('El lanzador anterior contiene código diferente; no se puede reutilizar. Conserva la nueva compilación para validar.')
    executable.write_bytes(previous)
    return {'verified_identical_code': True, 'new_build_sha256': hashlib.sha256(current).hexdigest(),
            'retained_sha256': hashlib.sha256(previous).hexdigest(), 'exe_modified': False}


def build(reuse_launcher=None):
    if os.name != 'nt':
        raise SystemExit('Genera el ejecutable de Windows desde Windows.')
    root = Path(__file__).resolve().parent
    # Leer antes de que COLLECT reemplace una carpeta de salida anterior.
    previous = Path(reuse_launcher).read_bytes() if reuse_launcher else None
    output = root / 'dist' / f'v{__version__}'
    output.mkdir(parents=True, exist_ok=True)
    commands = [
        [sys.executable, str(root / 'launcher.py'), '--data-dir', str(root / '.local' / 'build_profile'),
         'manage', 'collectstatic', '--noinput', '--clear'],
        [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
         '--distpath', str(output), '--workpath', str(root / '.local' / 'pyinstaller_build'), str(root / 'InventariosAPP.spec')],
    ]
    for command in commands:
        subprocess.run(command, cwd=root, check=True)
    package_root = output / 'InventariosAPP'
    executable = package_root / 'InventariosAPP.exe'
    reuse_info = reuse_verified_launcher(previous, executable) if previous is not None else None
    # Verificación de contenido sin ejecutar ni extraer datos privados.
    from PyInstaller.archive.readers import CArchiveReader
    archive = CArchiveReader(str(executable))
    prohibited = [name for name in archive.toc if Path(name).suffix.lower() in ('.db', '.sqlite3')
                  or Path(name).name in ('.env', '.runtime-key') or 'media' in Path(name).parts or '.local' in Path(name).parts]
    if prohibited:
        raise RuntimeError('El paquete contiene archivos privados: ' + ', '.join(prohibited))
    for path in package_root.rglob('*'):
        relative = path.relative_to(package_root)
        if (path.suffix.lower() in ('.db', '.sqlite3') or path.name in ('.env', '.runtime-key')
                or 'media' in relative.parts or '.local' in relative.parts):
            raise RuntimeError(f'Recurso privado prohibido en la carpeta distribuida: {relative}')
    for name in ('DISTRIBUCION_Y_DESARROLLO.md', 'MANUAL_USUARIO.md', 'CHANGELOG.md', 'INFORME_VALIDACION_FASE4.md'):
        shutil.copy2(root / name, package_root / name)
    # Avisos de dependencias que deben acompañar la distribución.
    for package in ('Django', 'waitress', 'whitenoise', 'reportlab', 'pillow', 'python-decouple', 'asgiref', 'sqlparse', 'tzdata', 'charset-normalizer', 'pyinstaller'):
        distribution = importlib.metadata.distribution(package)
        for filename in distribution.files or []:
            if filename.name.lower().startswith(('license', 'licence', 'copying')):
                relative = Path(*[part for part in filename.parts if part not in ('..', '.')])
                destination = package_root / 'licenses' / package / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(distribution.locate_file(filename), destination)
    python_license = Path(sys.base_prefix) / 'LICENSE.txt'
    if python_license.exists():
        destination = package_root / 'licenses' / 'Python-LICENSE.txt'
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(python_license, destination)
    summary = {'version': f'v{__version__}', 'built_utc': datetime.now(timezone.utc).isoformat(),
               'sha256': hashlib.sha256(executable.read_bytes()).hexdigest(),
               'format': 'onedir', 'database_bundled': False, 'first_installation': 'Base nueva sin cuentas ni componentes; migrate al iniciar',
               'runtime': 'Windows x64; Waitress en 127.0.0.1',
               'python': sys.version.split()[0],
               'dependencies': {name: importlib.metadata.version(name) for name in ('Django','reportlab','waitress','whitenoise','pyinstaller')}}
    if reuse_info:
        summary['launcher_reuse'] = reuse_info
    (package_root / 'BUILD_INFO.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    checksums = '\n'.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(package_root).as_posix()}'
                          for path in sorted(package_root.rglob('*')) if path.is_file() and path.name != 'SHA256SUMS.txt') + '\n'
    (package_root / 'SHA256SUMS.txt').write_text(checksums, encoding='utf-8')
    shutil.make_archive(str(output / f'InventariosAPP-v{__version__}-Windows-x64'), 'zip', output, package_root.name)
    print(f'Distribución generada: {package_root}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Construir distribución onedir limpia sin datos personales')
    parser.add_argument('--reuse-launcher', type=Path, help='Lanzador previo, solo para recursos si el código es exactamente el mismo')
    build(parser.parse_args().reuse_launcher)
