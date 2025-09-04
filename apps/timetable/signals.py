# apps/timetable/signals.py (FIXED)
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from .models import TimeSlot, ConflictLog

@receiver(post_save, sender=TimeSlot)
def detect_conflicts_on_save(sender, instance, created, **kwargs):
    """Detect conflicts when a time slot is saved"""
    if instance.period.is_break:
        return

    # Check for teacher conflicts
    teacher_conflicts = TimeSlot.objects.filter(
        teacher=instance.teacher,
        day_of_week=instance.day_of_week,
        period=instance.period,
        is_active=True
    ).exclude(id=instance.id)

    for conflict_slot in teacher_conflicts:
        ConflictLog.objects.get_or_create(
            conflict_type='TEACHER_DOUBLE_BOOK',
            time_slot1=instance,
            time_slot2=conflict_slot,
            defaults={
                'description': f"Teacher {instance.teacher.user.get_full_name()} is assigned to multiple classes at the same time"
            }
        )

    # Check for room conflicts  
    room_conflicts = TimeSlot.objects.filter(
        classroom=instance.classroom,
        day_of_week=instance.day_of_week,
        period=instance.period,
        is_active=True
    ).exclude(id=instance.id)

    for conflict_slot in room_conflicts:
        ConflictLog.objects.get_or_create(
            conflict_type='ROOM_DOUBLE_BOOK',
            time_slot1=instance,
            time_slot2=conflict_slot,
            defaults={
                'description': f"Room {instance.classroom.name} is booked for multiple classes at the same time"
            }
        )

@receiver(post_delete, sender=TimeSlot)
def resolve_conflicts_on_delete(sender, instance, **kwargs):
    """Resolve conflicts when a time slot is deleted"""
    ConflictLog.objects.filter(
        models.Q(time_slot1=instance) | models.Q(time_slot2=instance)
    ).update(is_resolved=True, resolved_at=timezone.now())
