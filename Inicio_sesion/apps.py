from django.apps import AppConfig


class InicioSesionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Inicio_sesion'
    
    def ready(self):
        import Inicio_sesion.signals
