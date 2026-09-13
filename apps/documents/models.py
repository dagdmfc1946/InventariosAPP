from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class Datasheet(models.Model):
    MAX_FILE_SIZE = 20 * 1024 * 1024

    component = models.ForeignKey('components.Component', on_delete=models.CASCADE, related_name='datasheets')
    file = models.FileField(
        upload_to='datasheets/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        max_length=500,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def clean(self):
        if self.file and not self.file.name.lower().endswith('.pdf'):
            raise ValidationError({'file': 'Solo se permiten archivos PDF.'})

        if self.file and self.file.size > self.MAX_FILE_SIZE:
            raise ValidationError({'file': 'El datasheet no puede superar los 20 MB.'})

    def __str__(self):
        return f'{self.component.reference} - {self.file.name}'
