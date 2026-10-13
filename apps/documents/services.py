import logging
from django.db import transaction

logger = logging.getLogger(__name__)


def create_datasheet(sheet):
    sheet.full_clean()
    uploaded = not sheet.file._committed
    try:
        with transaction.atomic():
            sheet.save()
    except Exception:
        if uploaded and sheet.file._committed:
            try:
                sheet.file.storage.delete(sheet.file.name)
            except OSError:
                logger.exception('No se pudo limpiar la carga fallida de PDF.')
        raise
    return sheet
