
# explanation: This file defines the configuration for the 'projects' app in a Django project. It specifies the default auto field type and the name of the app.

from django.apps import AppConfig

class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'