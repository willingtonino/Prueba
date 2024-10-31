from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

app_name = 'Inicio_sesion'

urlpatterns = [
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Inicio_sesion/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Inicio_sesion/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Inicio_sesion/password_reset_complete.html'), name='password_reset_complete'),
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signup_business/', views.signup_business, name='signup_business'),
    path('signout/', views.signout, name='signout'),  # URL para la función de logout
]
