# apps/timetable/apps.py (QUICK FIX)  
from django.apps import AppConfig

class TimetableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.timetable'
    verbose_name = 'Timetable Management'

    # Comment out signals import until signals.py is created
    # def ready(self):
    #     import apps.timetable.signals
