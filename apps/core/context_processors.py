from config.version import FECHA_VERSION, __version__


def software_version(request):
    return {'software_version': f'v{__version__}', 'software_date': FECHA_VERSION}
