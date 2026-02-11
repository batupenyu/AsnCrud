from django import template
import base64
import os
import logging
from datetime import datetime

register = template.Library()
logger = logging.getLogger(__name__)

def terbilang(n):
    """Convert number to Indonesian words"""
    if n == 0:
        return "nol"
    elif n == 1:
        return "satu"
    elif n == 2:
        return "dua"
    elif n == 3:
        return "tiga"
    elif n == 4:
        return "empat"
    elif n == 5:
        return "lima"
    elif n == 6:
        return "enam"
    elif n == 7:
        return "tujuh"
    elif n == 8:
        return "delapan"
    elif n == 9:
        return "sembilan"
    elif n == 10:
        return "sepuluh"
    elif n == 11:
        return "sebelas"
    elif n < 20:
        return terbilang(n - 10) + " belas"
    elif n < 100:
        return terbilang(n // 10) + " puluh" + (" " + terbilang(n % 10) if n % 10 != 0 else "")
    elif n < 200:
        return "seratus" + (" " + terbilang(n - 100) if n > 100 else "")
    elif n < 1000:
        return terbilang(n // 100) + " ratus" + (" " + terbilang(n % 100) if n % 100 != 0 else "")
    elif n < 2000:
        return "seribu" + (" " + terbilang(n - 1000) if n > 1000 else "")
    elif n < 1000000:
        return terbilang(n // 1000) + " ribu" + (" " + terbilang(n % 1000) if n % 1000 != 0 else "")
    elif n < 1000000000:
        return terbilang(n // 1000000) + " juta" + (" " + terbilang(n % 1000000) if n % 1000000 != 0 else "")
    else:
        return str(n)  # fallback for very large numbers

@register.filter
def terbilang_filter(value):
    """
    Convert number to Indonesian words
    Usage: {{ number|terbilang }}
    """
    try:
        n = int(value)
        return terbilang(n)
    except (ValueError, TypeError):
        return value

@register.filter
def image_to_base64(image_field):
    """
    Convert ImageField to base64 data URI
    Usage: {{ image_field|image_to_base64 }}
    """
    if not image_field:
        return ''
    
    try:
        # Pastikan file exists
        if not image_field.path or not os.path.exists(image_field.path):
            logger.warning(f"Image file not found: {image_field.path}")
            return ''
        
        # Baca file dan encode
        with open(image_field.path, 'rb') as f:
            image_data = f.read()
        
        encoded = base64.b64encode(image_data).decode('utf-8')
        
        # Determine MIME type
        ext = os.path.splitext(image_field.path)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg', 
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.bmp': 'image/bmp'
        }
        mime = mime_types.get(ext, 'image/jpeg')  # default to jpeg
        
        return f'data:{mime};base64,{encoded}'
        
    except Exception as e:
        logger.error(f"Error converting image to base64: {e}")
        return ''

@register.filter
def days_between(start_date, end_date):
    """
    Calculates the number of days between two dates.
    """
    if start_date and end_date:
        return (end_date - start_date).days + 1
    return 0

@register.filter
def split(value, delimiter):
    """
    Splits a string by a given delimiter.
    """
    return value.split(delimiter)
