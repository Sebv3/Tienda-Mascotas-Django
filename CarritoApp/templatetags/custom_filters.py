from django import template
from babel.numbers import format_currency

register = template.Library()

@register.filter
def currency_format(value):
    try:
        # Formatear el valor como pesos chilenos
        return format_currency(value, 'CLP', locale='es_CL')
    except (ValueError, TypeError):
        return value