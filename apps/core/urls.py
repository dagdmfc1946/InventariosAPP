from django.urls import path

from .views import component_search

urlpatterns = [
    path('search/', component_search, name='component_search'),
]
