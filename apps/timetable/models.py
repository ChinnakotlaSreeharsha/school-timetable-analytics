# apps/timetable/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Core entities for timetable management

class School(models.Model):
    """School information"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    established = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"

class Department(models.Model):
    """Academic departments"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['code']

class Subject(models.Model):
    """Subjects/Courses offered"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    credits = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['code']

class Teacher(models.Model):
    """Teaching staff information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    phone = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    max_periods_per_day = models.PositiveIntegerField(default=6)
    max_periods_per_week = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ['employee_id']

class ClassRoom(models.Model):
    """Physical classrooms and their details"""
    ROOM_TYPES = [
        ('LECTURE', 'Lecture Hall'),
        ('LAB', 'Laboratory'), 
        ('COMPUTER', 'Computer Lab'),
        ('LIBRARY', 'Library'),
        ('AUDITORIUM', 'Auditorium'),
        ('SPORTS', 'Sports Hall'),
    ]

    name = models.CharField(max_length=50)
    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='LECTURE')
    capacity = models.PositiveIntegerField()
    floor = models.CharField(max_length=10, blank=True)
    building = models.CharField(max_length=50, blank=True)
    has_projector = models.BooleanField(default=False)
    has_computer = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} - {self.name} (Capacity: {self.capacity})"

    class Meta:
        verbose_name = "Class Room"
        verbose_name_plural = "Class Rooms"
        ordering = ['room_number']

class Class(models.Model):
    """Student classes/sections"""
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10, blank=True)
    grade_level = models.PositiveIntegerField()  # e.g., 9, 10, 11, 12
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='classes')
    academic_year = models.CharField(max_length=9)  # e.g., "2023-2024"
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    total_students = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Class {self.grade_level}{self.section} - {self.name}"

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        unique_together = ['name', 'section', 'academic_year']
        ordering = ['grade_level', 'section']

class Period(models.Model):
    """Time periods for scheduling"""
    name = models.CharField(max_length=20)  # e.g., "Period 1", "Morning Break"
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False)
    order = models.PositiveIntegerField()  # For sorting periods

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        ordering = ['order', 'start_time']

class TimeSlot(models.Model):
    """Individual timetable slots"""
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'), 
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    school_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='time_slots')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    academic_year = models.CharField(max_length=9)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Validate time slot constraints"""
        if self.period.is_break and (self.subject or self.teacher):
            raise ValidationError("Break periods cannot have subjects or teachers assigned")

        if not self.period.is_break and not (self.subject and self.teacher):
            raise ValidationError("Non-break periods must have both subject and teacher assigned")

    def __str__(self):
        if self.period.is_break:
            return f"{self.school_class} - {self.day_of_week} - {self.period.name}"
        return f"{self.school_class} - {self.day_of_week} - {self.period.name} - {self.subject} ({self.teacher})"

    class Meta:
        verbose_name = "Time Slot"
        verbose_name_plural = "Time Slots"
        unique_together = [
            ['school_class', 'day_of_week', 'period', 'academic_year'],
        ]
        ordering = ['day_of_week', 'period__order']

class ConflictLog(models.Model):
    """Log scheduling conflicts for analysis"""
    CONFLICT_TYPES = [
        ('TEACHER_DOUBLE_BOOK', 'Teacher Double Booking'),
        ('ROOM_DOUBLE_BOOK', 'Room Double Booking'),
        ('CLASS_DOUBLE_BOOK', 'Class Double Booking'),
    ]

    conflict_type = models.CharField(max_length=30, choices=CONFLICT_TYPES)
    time_slot1 = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='conflicts_as_slot1')
    time_slot2 = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='conflicts_as_slot2')
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.conflict_type} - {self.created_at.date()}"

    class Meta:
        verbose_name = "Conflict Log"
        verbose_name_plural = "Conflict Logs"
        ordering = ['-created_at']

class TimetableTemplate(models.Model):
    """Reusable timetable templates"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    grade_levels = models.CharField(max_length=50, help_text="Comma-separated grade levels, e.g., '9,10,11'")
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Timetable Template"
        verbose_name_plural = "Timetable Templates"
        ordering = ['-created_at']
