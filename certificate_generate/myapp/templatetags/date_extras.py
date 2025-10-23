from django import template
from datetime import datetime

register = template.Library()

@register.filter
def pretty_date(value):
    if not value:
        return ""
    
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return value

    day = value.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    formatted = f"{day}<sup>{suffix}</sup> {value.strftime('%B %Y')}"
    return formatted
