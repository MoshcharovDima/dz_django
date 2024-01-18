from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Censor filter can only be applied to strings.")
    censored_words = ['badword1', 'badword2']  # Замените на ваш список слов
    for word in censored_words:
        pattern = r'\b' + word + r'\b'  # Ищет полное слово, игнорируя части слов
        value = re.sub(pattern, '*' * len(word), value, flags=re.IGNORECASE)
    return mark_safe(value)