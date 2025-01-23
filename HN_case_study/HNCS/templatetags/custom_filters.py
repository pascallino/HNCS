from datetime import datetime
from django import template
from django.utils.timezone import make_aware, localtime
import pytz 

register = template.Library()

@register.filter
def format_timestamp(value):
    """
    Converts a timestamp string (e.g., "2025-01-21T18:00:42Z") to a formatted date string
    in the timezone of the server's location.
    """
    try:
        # Parse the timestamp string into a naive datetime object
        dt_object = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        # Make the datetime timezone-aware using UTC
        aware_datetime = make_aware(dt_object, pytz.UTC)
        # Convert to the local timezone (server's timezone)
        local_datetime = localtime(aware_datetime)
        # Format the localized datetime
        return local_datetime.strftime("%b %d %Y, %I:%M %p ")
    except (ValueError, TypeError):
        return value  # Return the original value if parsing fails
