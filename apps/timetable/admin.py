# apps/timetable/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import (
    School, Department, Subject, Teacher, ClassRoom, Class, 
    Period, TimeSlot, ConflictLog, TimetableTemplate
)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'established']
    search_fields = ['name', 'email']
    list_filter = ['established']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'head', 'school']
    list_filter = ['school']
    search_fields = ['name', 'code']
    ordering = ['code']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'credits', 'is_active']
    list_filter = ['department', 'is_active', 'credits']
    search_fields = ['name', 'code']
    ordering = ['code']
    list_editable = ['is_active']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'department', 'specialization', 'is_active', 'get_workload']
    list_filter = ['department', 'is_active']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'user__username']
    ordering = ['employee_id']
    list_editable = ['is_active']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'

    def get_workload(self, obj):
        """Show current workload"""
        total_periods = TimeSlot.objects.filter(teacher=obj, is_active=True).count()
        return f"{total_periods} periods/week"
    get_workload.short_description = 'Current Workload'

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'name', 'room_type', 'capacity', 'floor', 'building', 'get_features', 'is_active']
    list_filter = ['room_type', 'building', 'floor', 'is_active', 'has_projector', 'has_computer']
    search_fields = ['room_number', 'name', 'building']
    ordering = ['room_number']
    list_editable = ['is_active']

    def get_features(self, obj):
        """Display room features as badges"""
        features = []
        if obj.has_projector:
            features.append('📽️ Projector')
        if obj.has_computer:
            features.append('💻 Computer')
        if obj.has_whiteboard:
            features.append('📝 Whiteboard')
        return ' | '.join(features) if features else 'Basic'
    get_features.short_description = 'Features'

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'grade_level', 'department', 'class_teacher', 'total_students', 'academic_year', 'is_active']
    list_filter = ['grade_level', 'department', 'academic_year', 'is_active']
    search_fields = ['name', 'section']
    ordering = ['grade_level', 'section']
    list_editable = ['is_active', 'total_students']

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time', 'is_break', 'order']
    list_filter = ['is_break']
    ordering = ['order']
    list_editable = ['order']

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['school_class', 'day_of_week', 'period', 'subject', 'teacher', 'classroom', 'academic_year', 'is_active']
    list_filter = ['day_of_week', 'academic_year', 'is_active', 'school_class__department', 'period__is_break']
    search_fields = ['school_class__name', 'subject__name', 'teacher__user__first_name', 'teacher__user__last_name']
    ordering = ['day_of_week', 'period__order']
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('school_class', 'academic_year', 'day_of_week', 'period')
        }),
        ('Assignment', {
            'fields': ('subject', 'teacher', 'classroom')
        }),
        ('Additional', {
            'fields': ('notes', 'is_active'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'school_class', 'subject', 'teacher__user', 'classroom', 'period'
        )

@admin.register(ConflictLog)
class ConflictLogAdmin(admin.ModelAdmin):
    list_display = ['conflict_type', 'get_time_slots', 'is_resolved', 'created_at', 'resolved_at']
    list_filter = ['conflict_type', 'is_resolved', 'created_at']
    search_fields = ['description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'resolved_at']

    def get_time_slots(self, obj):
        """Display involved time slots"""
        return f"{obj.time_slot1} | {obj.time_slot2}"
    get_time_slots.short_description = 'Conflicting Time Slots'

@admin.register(TimetableTemplate)
class TimetableTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'grade_levels', 'is_default', 'created_by', 'created_at']
    list_filter = ['department', 'is_default', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

# Customize admin site
admin.site.site_header = "School Timetable Administration"
admin.site.site_title = "Timetable Admin"
admin.site.index_title = "Manage School Timetables"
