# apps/timetable/templatetags/timetable_extras.py
from django import template

register = template.Library()

@register.filter
def dict_item(dictionary, key):
    """Get item from dictionary by key"""
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None

@register.filter
def get_slot(organized_slots, day_period):
    """Get slot from organized slots"""
    try:
        day, period_id = day_period.split('|')
        return organized_slots.get(day, {}).get(int(period_id))
    except:
        return None

@register.simple_tag
def get_slot_by_day_period(organized_slots, day, period_id):
    """Template tag to get slot by day and period"""
    if organized_slots and day in organized_slots:
        return organized_slots[day].get(period_id)
    return None
