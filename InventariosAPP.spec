# PyInstaller onefile; código/recursos explícitos, sin datos de instalaciones.
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

root = Path(SPECPATH).resolve()
datas = [(str(root / 'templates'), 'templates'),
         (str(root / 'collected_static'), 'collected_static')]
datas += collect_data_files('apps', includes=['**/templates/**/*', '**/migrations/*.py'], include_py_files=True)
datas += collect_data_files('reportlab', includes=['fonts/*'])
hidden = []
for package in ('apps', 'config', 'backups'):
    hidden += collect_submodules(package, on_error='ignore',
        filter=lambda name: not any(part.startswith('test') for part in name.split('.')))
hidden += ['django.db.backends.sqlite3', 'django.contrib.auth.context_processors',
           'django.contrib.messages.context_processors', 'whitenoise.middleware', 'whitenoise.storage']

analysis = Analysis([str(root / 'launcher.py')], pathex=[str(root)], binaries=[], datas=datas,
                    hiddenimports=hidden, hookspath=[str(root / 'packaging' / 'hooks')],
                    runtime_hooks=[], excludes=['pytest', 'tkinter', 'django.contrib.gis'], noarchive=False)
# También comprobar lo agregado por hooks de terceros antes de crear el archivo.
for destination, source, kind in analysis.datas:
    target = Path(destination)
    if target.suffix.lower() in ('.sqlite3', '.db') or target.name in ('.env', '.runtime-key') or 'media' in target.parts or '.local' in target.parts:
        raise RuntimeError(f'Recurso privado prohibido en el paquete: {destination}')
pyz = PYZ(analysis.pure)
exe = EXE(pyz, analysis.scripts, analysis.binaries, analysis.datas, [('u', None, 'OPTION')],
          name='InventariosAPP', debug=False, strip=False, upx=False, console=True,
          disable_windowed_traceback=False)
