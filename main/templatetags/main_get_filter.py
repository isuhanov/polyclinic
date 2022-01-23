from django import template
from django.template.defaulttags import register
from main.models import *

register = template.Library()

#функция для получения данных словаря
@register.filter
def is_empl(auth_user):
    return RegistryEmployee.objects.filter(user = auth_user)
