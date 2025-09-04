# apps/timetable/utils.py
import random
from collections import defaultdict
from django.db.models import Q
from .models import TimeSlot, Teacher, ClassRoom, Subject, Period, Class, ConflictLog

class ConflictDetector:
    """Utility class for detecting scheduling conflicts"""

    @staticmethod
    def check_slot_conflicts(time_slot):
        """Check for conflicts in a given time slot"""
        conflicts = []

        # Skip conflict checking for break periods
        if time_slot.period.is_break:
            return conflicts

        # Check teacher double booking
        if time_slot.teacher:
            teacher_conflicts = TimeSlot.objects.filter(
                teacher=time_slot.teacher,
                day_of_week=time_slot.day_of_week,
                period=time_slot.period,
                is_active=True
            ).exclude(id=time_slot.id if time_slot.id else None)

            if teacher_conflicts.exists():
                conflicts.append(f"Teacher {time_slot.teacher.user.get_full_name()} is already scheduled at this time")

        # Check classroom double booking
        if time_slot.classroom:
            room_conflicts = TimeSlot.objects.filter(
                classroom=time_slot.classroom,
                day_of_week=time_slot.day_of_week,
                period=time_slot.period,
                is_active=True
            ).exclude(id=time_slot.id if time_slot.id else None)

            if room_conflicts.exists():
                conflicts.append(f"Classroom {time_slot.classroom.name} is already booked at this time")

        # Check class double booking
        if time_slot.school_class:
            class_conflicts = TimeSlot.objects.filter(
                school_class=time_slot.school_class,
                day_of_week=time_slot.day_of_week,
                period=time_slot.period,
                is_active=True
            ).exclude(id=time_slot.id if time_slot.id else None)

            if class_conflicts.exists():
                conflicts.append(f"Class {time_slot.school_class.name} already has a period scheduled at this time")

        return conflicts

    @staticmethod
    def detect_class_conflicts(school_class):
        """Detect all conflicts for a specific class"""
        conflicts = []
        time_slots = TimeSlot.objects.filter(
            school_class=school_class,
            is_active=True
        ).select_related('teacher', 'classroom', 'period')

        for slot in time_slots:
            slot_conflicts = ConflictDetector.check_slot_conflicts(slot)
            if slot_conflicts:
                conflicts.extend(slot_conflicts)

        return conflicts

    @staticmethod
    def detect_all_conflicts():
        """Detect all conflicts in the system"""
        all_slots = TimeSlot.objects.filter(is_active=True).select_related('teacher', 'classroom', 'period', 'school_class')
        conflict_groups = defaultdict(list)

        # Group slots by day and period
        for slot in all_slots:
            if not slot.period.is_break:
                key = f"{slot.day_of_week}_{slot.period.id}"
                conflict_groups[key].append(slot)

        conflicts = []
        for key, slots in conflict_groups.items():
            if len(slots) > 1:
                # Check for teacher conflicts
                teachers = defaultdict(list)
                rooms = defaultdict(list)

                for slot in slots:
                    if slot.teacher:
                        teachers[slot.teacher.id].append(slot)
                    if slot.classroom:
                        rooms[slot.classroom.id].append(slot)

                # Report teacher conflicts
                for teacher_id, teacher_slots in teachers.items():
                    if len(teacher_slots) > 1:
                        teacher_name = teacher_slots[0].teacher.user.get_full_name()
                        conflicts.append(f"Teacher {teacher_name} has multiple classes at the same time")

                # Report room conflicts
                for room_id, room_slots in rooms.items():
                    if len(room_slots) > 1:
                        room_name = room_slots[0].classroom.name
                        conflicts.append(f"Room {room_name} is double-booked")

        return conflicts

class TimetableGenerator:
    """Algorithm for automatically generating timetables"""

    def __init__(self):
        self.days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        self.periods = Period.objects.filter(is_break=False).order_by('order')
        self.max_attempts = 100

    def generate_for_class(self, school_class, subjects_per_week=None):
        """Generate timetable for a specific class"""
        if not subjects_per_week:
            # Default subject distribution
            subjects_per_week = self._get_default_subjects(school_class)

        generated_slots = []
        available_slots = self._get_available_slots()

        # Clear existing slots for this class
        TimeSlot.objects.filter(school_class=school_class).delete()

        for subject_id, periods_needed in subjects_per_week.items():
            subject = Subject.objects.get(id=subject_id)
            assigned_periods = 0
            attempts = 0

            while assigned_periods < periods_needed and attempts < self.max_attempts:
                slot = self._find_available_slot(
                    school_class, subject, available_slots
                )

                if slot:
                    generated_slots.append(slot)
                    # Remove this slot from available slots
                    slot_key = f"{slot['day_of_week']}_{slot['period'].id}"
                    if slot_key in available_slots:
                        available_slots[slot_key].remove((slot['teacher'].id, slot['classroom'].id))
                    assigned_periods += 1

                attempts += 1

            if assigned_periods < periods_needed:
                print(f"Warning: Could only assign {assigned_periods}/{periods_needed} periods for {subject.name}")

        return generated_slots

    def _get_default_subjects(self, school_class):
        """Get default subject distribution for a class"""
        subjects = Subject.objects.filter(
            department=school_class.department,
            is_active=True
        )

        # Simple distribution - each subject gets 4-6 periods per week
        subjects_per_week = {}
        for subject in subjects:
            subjects_per_week[subject.id] = random.randint(4, 6)

        return subjects_per_week

    def _get_available_slots(self):
        """Get all available time slots"""
        available_slots = defaultdict(list)

        # Get all teachers and rooms
        teachers = Teacher.objects.filter(is_active=True)
        rooms = ClassRoom.objects.filter(is_active=True)

        # Build available slots for each day/period combination
        for day in self.days:
            for period in self.periods:
                # Find teachers and rooms not busy at this time
                busy_teachers = TimeSlot.objects.filter(
                    day_of_week=day,
                    period=period,
                    is_active=True
                ).values_list('teacher_id', flat=True)

                busy_rooms = TimeSlot.objects.filter(
                    day_of_week=day,
                    period=period,
                    is_active=True
                ).values_list('classroom_id', flat=True)

                available_teachers = teachers.exclude(id__in=busy_teachers)
                available_rooms = rooms.exclude(id__in=busy_rooms)

                # Create combinations of available teachers and rooms
                slot_key = f"{day}_{period.id}"
                for teacher in available_teachers:
                    for room in available_rooms:
                        available_slots[slot_key].append((teacher.id, room.id))

        return available_slots

    def _find_available_slot(self, school_class, subject, available_slots):
        """Find an available slot for a subject"""
        # Shuffle days and periods for randomness
        shuffled_days = self.days.copy()
        random.shuffle(shuffled_days)

        shuffled_periods = list(self.periods)
        random.shuffle(shuffled_periods)

        for day in shuffled_days:
            for period in shuffled_periods:
                slot_key = f"{day}_{period.id}"

                if slot_key in available_slots and available_slots[slot_key]:
                    # Check if class is already busy at this time
                    existing_slot = TimeSlot.objects.filter(
                        school_class=school_class,
                        day_of_week=day,
                        period=period,
                        is_active=True
                    ).first()

                    if existing_slot:
                        continue

                    # Get a random available teacher and room
                    teacher_id, room_id = random.choice(available_slots[slot_key])
                    teacher = Teacher.objects.get(id=teacher_id)
                    classroom = ClassRoom.objects.get(id=room_id)

                    return {
                        'school_class': school_class,
                        'subject': subject,
                        'teacher': teacher,
                        'classroom': classroom,
                        'period': period,
                        'day_of_week': day,
                        'academic_year': '2024-2025',  # This should be dynamic
                        'is_active': True
                    }

        return None

class TimetableAnalyzer:
    """Analyze timetable efficiency and statistics"""

    @staticmethod
    def get_teacher_workload(teacher):
        """Calculate teacher workload statistics"""
        slots = TimeSlot.objects.filter(
            teacher=teacher,
            is_active=True
        ).exclude(period__is_break=True)

        workload = {
            'total_periods': slots.count(),
            'periods_per_day': {},
            'classes_taught': slots.values('school_class').distinct().count(),
            'subjects_taught': slots.values('subject').distinct().count(),
        }

        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        for day in days:
            workload['periods_per_day'][day] = slots.filter(day_of_week=day).count()

        return workload

    @staticmethod
    def get_room_utilization(classroom):
        """Calculate room utilization statistics"""
        slots = TimeSlot.objects.filter(
            classroom=classroom,
            is_active=True
        ).exclude(period__is_break=True)

        total_periods = Period.objects.filter(is_break=False).count() * 6  # 6 days
        utilization_rate = (slots.count() / total_periods) * 100 if total_periods > 0 else 0

        return {
            'total_bookings': slots.count(),
            'utilization_rate': round(utilization_rate, 2),
            'classes_using': slots.values('school_class').distinct().count(),
        }

    @staticmethod
    def get_class_statistics(school_class):
        """Get statistics for a specific class"""
        slots = TimeSlot.objects.filter(
            school_class=school_class,
            is_active=True
        ).exclude(period__is_break=True)

        return {
            'total_periods': slots.count(),
            'subjects_covered': slots.values('subject').distinct().count(),
            'teachers_involved': slots.values('teacher').distinct().count(),
            'rooms_used': slots.values('classroom').distinct().count(),
            'free_periods': self._count_free_periods(school_class),
        }

    @staticmethod
    def _count_free_periods(school_class):
        """Count free periods for a class"""
        total_periods = Period.objects.filter(is_break=False).count() * 6  # 6 days
        scheduled_periods = TimeSlot.objects.filter(
            school_class=school_class,
            is_active=True
        ).exclude(period__is_break=True).count()

        return total_periods - scheduled_periods
