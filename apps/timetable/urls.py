# apps/timetable/urls.py (MINIMAL WORKING VERSION)
from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    # Basic URLs that work
    path('', views.dashboard_view, name='dashboard'),
    path('class/<int:class_id>/', views.timetable_grid_view, name='grid'),
    path('teacher/', views.teacher_schedule_view, name='teacher'),
    path('teacher/<int:teacher_id>/', views.teacher_schedule_view, name='teacher_detail'),
    path('conflicts/', views.conflict_report_view, name='conflicts'),

    # Comment out problematic URLs for now
    # path('generate/<int:class_id>/', views.auto_generate_timetable, name='generate'),
    # path('slot/add/', views.TimeSlotCreateView.as_view(), name='slot_add'),
    # path('slot/<int:pk>/edit/', views.TimeSlotUpdateView.as_view(), name='slot_edit'),
    # path('slot/<int:pk>/delete/', views.TimeSlotDeleteView.as_view(), name='slot_delete'),
    # path('conflict/<int:conflict_id>/resolve/', views.resolve_conflict, name='resolve_conflict'),
]
