from django.urls import path
from . import views

app_name = 'Resultados'

urlpatterns = [
    path('', views.index, name='index'),
    path('resultadosUsuarios/', views.resultadosUsuarios, name='resultadosUsuarios'),
    path('resultadosEmpre/', views.resultadosEmpre, name='resultadosEmpre'),
]
