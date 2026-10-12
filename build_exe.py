"""Generar distribución Windows sin datos del usuario: python build_exe.py."""
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from config.version import __version__


def build():
    if os.name != 'nt':
        raise SystemExit('Genera el ejecutable de Windows desde Windows.')
    root = Path(__file__).resolve().parent
    output = root / 'dist' / f'v{__version__}'
    output.mkdir(parents=True, exist_ok=True)
    commands = [
        [sys.executable, str(root / 'launcher.py'), '--data-dir', str(root / '.local' / 'build_profile'),
         'manage', 'collectstatic', '--noinput'],
        [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean',
         '--distpath', str(output), '--workpath', str(root / '.local' / 'pyinstaller_build'), str(root / 'InventariosAPP.spec')],
    ]
    for command in commands:
        subprocess.run(command, cwd=root, check=True)
    executable = output / 'InventariosAPP.exe'
    # Verificación de contenido sin ejecutar ni extraer datos privados.
    from PyInstaller.archive.readers import CArchiveReader
    archive = CArchiveReader(str(executable))
    prohibited = [name for name in archive.toc if Path(name).suffix.lower() in ('.db', '.sqlite3')
                  or Path(name).name in ('.env', '.runtime-key') or 'media' in Path(name).parts or '.local' in Path(name).parts]
    if prohibited:
        raise RuntimeError('El paquete contiene archivos privados: ' + ', '.join(prohibited))
    for name in ('DISTRIBUCION_Y_DESARROLLO.md', 'MANUAL_USUARIO.md', 'CHANGELOG.md', 'INFORME_VALIDACION_FASE4.md'):
        shutil.copy2(root / name, output / name)
    # Avisos de dependencias que deben acompañar la distribución.
    for package in ('Django', 'waitress', 'whitenoise', 'reportlab', 'pillow', 'python-decouple', 'asgiref', 'sqlparse', 'tzdata', 'charset-normalizer', 'pyinstaller'):
        distribution = importlib.metadata.distribution(package)
        for filename in distribution.files or []:
            if filename.name.lower().startswith(('license', 'licence', 'copying')):
                relative = Path(*[part for part in filename.parts if part not in ('..', '.')])
                destination = output / 'licenses' / package / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(distribution.locate_file(filename), destination)
    python_license = Path(sys.base_prefix) / 'LICENSE.txt'
    if python_license.exists():
        destination = output / 'licenses' / 'Python-LICENSE.txt'
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(python_license, destination)
    summary = {'version': f'v{__version__}', 'built_utc': datetime.now(timezone.utc).isoformat(),
               'sha256': hashlib.sha256(executable.read_bytes()).hexdigest(),
               'database_bundled': False, 'first_installation': 'Base nueva sin cuentas ni componentes; migrate al iniciar',
               'runtime': 'Windows x64; Waitress en 127.0.0.1',
               'python': sys.version.split()[0],
               'dependencies': {name: importlib.metadata.version(name) for name in ('Django','reportlab','waitress','whitenoise','pyinstaller')}}
    (output / 'BUILD_INFO.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Distribución generada: {output}', flush=True)


if __name__ == '__main__':
    build()
