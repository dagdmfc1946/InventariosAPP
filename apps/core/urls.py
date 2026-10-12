from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

from apps.components.views_duplicate import component_duplicate
from apps.components.views import component_create, component_detail, component_edit
from apps.inventory.views_movement import component_movement
from apps.inventory.views import location_list, location_edit
from apps.suppliers.views import supplier_list, supplier_edit, offer_edit
from apps.documents.views import datasheet_upload, datasheet_download

from .views import component_search, site_home, profile_edit

urlpatterns = [
    path('', site_home, name='site_home'),
    path('search/', component_search, name='component_search'),
    path('components/new/', component_create, name='component_create'),
    path('components/<int:pk>/', component_detail, name='component_detail'),
    path('components/<int:pk>/duplicate/', component_duplicate, name='component_duplicate'),
    path('components/<int:pk>/edit/', component_edit, name='component_edit'),
    path('components/<int:pk>/movements/new/', component_movement, name='component_movement'),
    path('suppliers/', supplier_list, name='supplier_list'),
    path('suppliers/new/', supplier_edit, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', supplier_edit, name='supplier_edit'),
    path('components/<int:component_pk>/offers/new/', offer_edit, name='offer_create'),
    path('components/<int:component_pk>/offers/<int:pk>/edit/', offer_edit, name='offer_edit'),
    path('locations/', location_list, name='location_list'),
    path('locations/new/', location_edit, name='location_create'),
    path('locations/<int:pk>/edit/', location_edit, name='location_edit'),
    path('components/<int:pk>/datasheets/', datasheet_upload, name='datasheet_upload'),
    path('documents/<int:pk>/download/', datasheet_download, name='datasheet_download'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/password/', PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('accounts/password/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('accounts/profile/', profile_edit, name='profile_edit'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
