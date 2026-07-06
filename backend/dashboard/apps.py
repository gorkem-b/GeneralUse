from django.apps import AppConfig
from django.apps import AppConfig
import os

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        # Background workers have been replaced by the Notification long-polling system.
        pass
