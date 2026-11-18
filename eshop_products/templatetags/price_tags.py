from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ENGLISH_DIGITS = "0123456789"


@register.filter
def toman(value):

    if value is None or value == "":
        return ""
    try:
        number = int(Decimal(value))
    except (InvalidOperation, ValueError, TypeError):
        return value

    formatted = f"{number:,}"   # → 48,000,000
    return formatted.translate(str.maketrans(ENGLISH_DIGITS, PERSIAN_DIGITS))


@register.filter
def fa_digits(value):

    if value is None:
        return ""
    return str(value).translate(str.maketrans(ENGLISH_DIGITS, PERSIAN_DIGITS))