from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class Datasheet(models.Model):
    MAX_FILE_SIZE = 20 * 1024 * 1024

    component = models.ForeignKey('components.Component', verbose_name='Componente', on_delete=models.CASCADE, related_name='datasheets')
    file = models.FileField(verbose_name='Archivo PDF',
        upload_to='datasheets/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        max_length=500,
    )
    uploaded_at = models.DateTimeField(verbose_name='Fecha de carga', auto_now_add=True)

    class Meta:
        verbose_name = 'Ficha técnica'
        verbose_name_plural = 'Fichas técnicas'
        ordering = ['-uploaded_at']

    def clean(self):
        if self.file and not self.file.name.lower().endswith('.pdf'):
            raise ValidationError({'file': 'Solo se permiten archivos PDF.'})

        if self.file:
            try:
                size = self.file.size
            except OSError:
                raise ValidationError({'file': 'No se puede leer el archivo guardado. Vuelva a adjuntar el PDF.'})
            if size > self.MAX_FILE_SIZE:
                raise ValidationError({'file': 'La ficha técnica no puede superar los 20 MB.'})

    def __str__(self):
        return f'{self.component.reference} - {self.file.name}'
