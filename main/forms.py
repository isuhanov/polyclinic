from django import forms
from django.forms import widgets
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.core.exceptions import ValidationError, ObjectDoesNotExist

import datetime

class DateInput(forms.DateInput):#объявляю поле ввода даты
    input_type = 'date'



class CreateCouponForm(forms.Form):
    adm_date = forms.DateTimeField()
    doctor = forms.CharField(max_length=100)

    