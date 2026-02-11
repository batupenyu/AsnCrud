from django import template
import datetime
from django.utils import formats # Still useful for general date formatting
from django.utils import timezone # For handling datetime objects

register = template.Library()

INDONESIAN_MONTHS_FULL = [
    '', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]

INDONESIAN_MONTHS_ABBR = [
    '', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',
    'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'
]

INDONESIAN_DAYS_FULL = [
    'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'
]

@register.filter
def indonesian_date(value, arg="%d %B %Y"):
    if not value:
        return ""
    
    # Ensure it's a date object, not datetime for date-only formatting
    if isinstance(value, datetime.datetime):
        value = value.date()

    day = value.day
    month_num = value.month
    year = value.year

    formatted_string = arg

    # Replace %d, %m, %Y, %y, etc.
    formatted_string = formatted_string.replace('%d', str(day))
    formatted_string = formatted_string.replace('%m', str(month_num).zfill(2))
    formatted_string = formatted_string.replace('%Y', str(year))
    formatted_string = formatted_string.replace('%y', str(year)[-2:])

    # Replace %B (Full month name)
    if '%B' in formatted_string:
        formatted_string = formatted_string.replace('%B', INDONESIAN_MONTHS_FULL[month_num])

    # Replace %b (Abbreviated month name)
    if '%b' in formatted_string:
        formatted_string = formatted_string.replace('%b', INDONESIAN_MONTHS_ABBR[month_num])

    return formatted_string

@register.filter
def indonesian_datetime(value, arg="%d %B %Y %H:%M"):
    if not value:
        return ""
    
    # Ensure it's a datetime object
    if isinstance(value, datetime.date):
        # Convert date to datetime if it's a date object to allow time formatting
        value = datetime.datetime(value.year, value.month, value.day, 0, 0, 0, tzinfo=timezone.get_current_timezone())


    day = value.day
    month_num = value.month
    year = value.year
    hour = value.hour
    minute = value.minute
    second = value.second
    weekday_num = value.weekday() # Monday is 0, Sunday is 6

    formatted_string = arg

    # Replace date components
    formatted_string = formatted_string.replace('%d', str(day).zfill(2))
    formatted_string = formatted_string.replace('%m', str(month_num).zfill(2))
    formatted_string = formatted_string.replace('%Y', str(year))
    formatted_string = formatted_string.replace('%y', str(year)[-2:])

    # Replace time components
    formatted_string = formatted_string.replace('%H', str(hour).zfill(2))
    formatted_string = formatted_string.replace('%M', str(minute).zfill(2))
    formatted_string = formatted_string.replace('%S', str(second).zfill(2))

    # Replace %B (Full month name)
    if '%B' in formatted_string:
        formatted_string = formatted_string.replace('%B', INDONESIAN_MONTHS_FULL[month_num])

    # Replace %b (Abbreviated month name)
    if '%b' in formatted_string:
        formatted_string = formatted_string.replace('%b', INDONESIAN_MONTHS_ABBR[month_num])
    
    # Replace %A (Full weekday name)
    if '%A' in formatted_string:
        # Weekday() returns 0 for Monday, 6 for Sunday.
        # INDONESIAN_DAYS_FULL is indexed from 0 for Monday.
        formatted_string = formatted_string.replace('%A', INDONESIAN_DAYS_FULL[weekday_num])

    return formatted_string