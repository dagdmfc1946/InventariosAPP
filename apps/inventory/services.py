from django.db import transaction
from apps.components.models import Component


@transaction.atomic
def assign_location_components(location, components):
    ids = [component.pk for component in components]
    Component.objects.filter(location=location).exclude(pk__in=ids).update(location=None)
    Component.objects.filter(pk__in=ids).update(location=location)
