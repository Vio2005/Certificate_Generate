from django import template

register = template.Library()

@register.filter
def ordinal_superscript(date_obj):
    if not date_obj:
        return ""

    day = date_obj.day
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    # Wrap suffix in <sup>
    return f"{day}<sup>{suffix}</sup> {date_obj.strftime('%B %Y')}"
