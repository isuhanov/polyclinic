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
    adm_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    doctor = forms.ModelChoiceField(Doctors.objects.all())

    adm_date.widget.attrs.update({'class': 'form_input'})    
    doctor.widget.attrs.update({'class': 'form_input'})    

    def save(self, p_user):
        patient_user = Patients.objects.get(user = p_user)
        new_coupon = Coupons.objects.create(
            adm_date = self.cleaned_data['adm_date'],
            patient = patient_user,
            doctor = self.cleaned_data['doctor']
        )

        return new_coupon
        