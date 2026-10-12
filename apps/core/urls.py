from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from apps.components.views import component_create

from .views import component_search, site_home

urlpatterns = [
    path('', site_home, name='site_home'),
    path('search/', component_search, name='component_search'),
    path('components/new/', component_create, name='component_create'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
