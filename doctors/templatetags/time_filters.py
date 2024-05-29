from django import template
from datetime import datetime

register = template.Library()


@register.filter(name="time_12hr")
def time_12hr(value):
    """
    Convert a 24-hour time string or time object to 12-hour AM/PM format.
    """
    if isinstance(value, str):
        time_obj = datetime.strptime(value, "%H:%M:%S").time()
    else:
        time_obj = value

    return time_obj.strftime("%I:%M %p")
