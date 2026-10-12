from pathlib import PurePosixPath
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from apps.components.models import Component
from apps.core.access import inventory_read_required
from .forms import DatasheetUploadForm
from .models import Datasheet
from .services import create_datasheet


@inventory_read_required
@permission_required('documents.add_datasheet', raise_exception=True)
@require_http_methods(['POST'])
def datasheet_upload(request, pk):
    component = get_object_or_404(Component, pk=pk)
    form = DatasheetUploadForm(request.POST, request.FILES)
    if form.is_valid():
        sheet = form.save(commit=False)
        sheet.component = component
        try:
            create_datasheet(sheet)
        except (DatabaseError, OSError):
            messages.error(request, 'No se pudo guardar el PDF. Intenta nuevamente; la ficha del componente se conserva.')
            return redirect('component_detail', pk=pk)
        except ValidationError as error:
            form.add_error('file', error.messages)
        else:
            messages.success(request, 'Ficha técnica adjuntada.')
            return redirect('component_detail', pk=pk)
    return render(request, 'components/component_detail.html', {'component': component, 'upload_form': form})


def pdf_response(request, sheet):
    try:
        stream = sheet.file.open('rb')
    except OSError:
        return render(request, 'documents/file_unavailable.html', {'component': sheet.component}, status=404)
    response = FileResponse(stream, content_type='application/pdf', filename=PurePosixPath(sheet.file.name).name)
    response['X-Content-Type-Options'] = 'nosniff'
    response['Cache-Control'] = 'private, no-store'
    return response


@inventory_read_required
@permission_required('documents.view_datasheet', raise_exception=True)
@require_http_methods(['GET'])
def datasheet_download(request, pk):
    return pdf_response(request, get_object_or_404(Datasheet, pk=pk))


@inventory_read_required
@permission_required('documents.view_datasheet', raise_exception=True)
@require_http_methods(['GET'])
def protected_media(request, path):
    # Resolver por registro, nunca abrir una ruta arbitraria suministrada por el cliente.
    return pdf_response(request, get_object_or_404(Datasheet, file=path))
