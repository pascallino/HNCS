from datetime import datetime
from django import template

register = template.Library()

@register.filter
def format_timestamp(value):
    """
    Converts a timestamp string (e.g., "2025-01-21T18:00:42Z") to a formatted date string.
    """
    try:
        dt_object = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        return dt_object.strftime("%b %d %Y, %I:%M %p")
    except (ValueError, TypeError):
        return value  # 