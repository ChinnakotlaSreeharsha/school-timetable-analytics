# school_timetable/urls.py (MINIMAL WORKING VERSION)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('users/', include('apps.users.urls')),

    # Main timetable URLs  
    path('timetable/', include('apps.timetable.urls', namespace='timetable')),

    # Redirect root to timetable
    path('', RedirectView.as_view(url='/timetable/', permanent=False)),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site configuration
admin.site.site_header = "School Timetable Administration"
admin.site.site_title = "Timetable Admin"  
admin.site.index_title = "Welcome to School Timetable Administration"
