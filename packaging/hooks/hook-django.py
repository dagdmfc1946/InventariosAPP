"""Hook explícito: nunca incorporar db.sqlite3 del proyecto al ejecutable."""
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = collect_data_files('django', include_py_files=True, includes=[
    '**/templates/**/*', '**/locale/**/*', '**/static/**/*', '**/migrations/*.py',
    'contrib/auth/common-passwords.txt.gz',
])
hiddenimports = collect_submodules('django', on_error='ignore',
    filter=lambda name: not ('.tests' in name or '.test.' in name or name.startswith('django.contrib.gis')))
