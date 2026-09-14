from django.urls import path

from .views import component_search, site_home

urlpatterns = [
    path('', site_home, name='site_home'),
    path('search/', component_search, name='component_search'),
]
