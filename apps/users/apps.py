# apps/users/apps.py (QUICK FIX)
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'User Management'

    # Comment out signals import until signals.py is created
    # def ready(self):
    #     import apps.users.signals
