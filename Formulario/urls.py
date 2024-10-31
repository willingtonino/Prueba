from django.urls import path
from . import views

app_name = 'Formulario'

urlpatterns = [
    path('', views.index, name='index'),
    path('userView/', views.userView, name='userView'),
    path('companyView/', views.companyView, name='companyView'),
    path('createFormView/', views.createFormView, name='createFormView'),
    path('createForm/', views.createForm, name='createForm'),
    path('editUserProfileView/', views.editUserProfileView, name='editUserProfileView'),
    path('editCompanyProfileView/', views.editCompanyProfileView, name='editCompanyProfileView'),
    path('uploadProfilePicture/', views.uploadProfilePicture, name='uploadProfilePicture'),
    path('userFormView/', views.userFormView, name='userFormView'),
    path('submitForm/', views.submitForm, name='submitForm'),
]
