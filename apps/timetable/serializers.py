# apps/timetable/serializers.py
from rest_framework import serializers
from .models import (
    School, Department, Subject, Teacher, ClassRoom, Class, 
    Period, TimeSlot, ConflictLog, TimetableTemplate
)

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'department', 'department_name', 'credits', 'description', 'is_active']

class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'employee_id', 'full_name', 'department', 'department_name', 'phone', 
                 'specialization', 'is_active', 'max_periods_per_day', 'max_periods_per_week']

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    class_teacher_name = serializers.CharField(source='class_teacher.user.get_full_name', read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'section', 'grade_level', 'department', 'department_name', 
                 'academic_year', 'class_teacher', 'class_teacher_name', 'total_students', 'is_active']

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    period_name = serializers.CharField(source='period.name', read_only=True)
    period_time = serializers.SerializerMethodField()
    class_name = serializers.CharField(source='school_class.name', read_only=True)

    class Meta:
        model = TimeSlot
        fields = ['id', 'school_class', 'class_name', 'subject', 'subject_name', 
                 'teacher', 'teacher_name', 'classroom', 'classroom_name', 
                 'period', 'period_name', 'period_time', 'day_of_week', 
                 'academic_year', 'is_active', 'notes']

    def get_period_time(self, obj):
        return f"{obj.period.start_time} - {obj.period.end_time}"

class ConflictLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConflictLog
        fields = '__all__'

class TimetableTemplateSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = TimetableTemplate
        fields = '__all__'
