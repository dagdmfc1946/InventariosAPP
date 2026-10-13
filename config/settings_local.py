"""Configuración del launcher local; secretos/datos definidos antes de importar Django."""
import sys
from .settings import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
STATIC_ROOT = BASE_DIR / 'collected_static'
if getattr(sys, 'frozen', False):
    STATICFILES_DIRS = []  # El .exe entrega los archivos ya recolectados.
MIDDLEWARE = [MIDDLEWARE[0], 'whitenoise.middleware.WhiteNoiseMiddleware', *MIDDLEWARE[1:]]
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
# Solo HTTP en loopback: cookies Secure/redirect HTTPS impedirían el acceso local.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
X_FRAME_OPTIONS = 'DENY'
