from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def inventory_read_required(view):
    @login_required
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        # Mantener el acceso de los operadores con permisos individuales de Fase 1.
        if not (request.user.has_perm('components.view_component') or request.user.has_perm('components.add_component')):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapped
