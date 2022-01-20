from email import policy
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

    adm_date.widget.attrs.update({'class': 'form_input', 'autocomplete': 'off'})    
    doctor.widget.attrs.update({'class': 'form_input'})    

    def save(self, p_user):
        patient_user = Patients.objects.get(user = p_user)
        new_coupon = Coupons.objects.create(
            adm_date = self.cleaned_data['adm_date'],
            patient = patient_user,
            doctor = self.cleaned_data['doctor']
        )

        return new_coupon



class LoginForm(forms.Form):#форма авторизации и аутентификации
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    login.widget.attrs.update({'class': 'form_input', 'placeholder': 'Логин (Почта)...'})
    password.widget.attrs.update({'class': 'form_input', 'placeholder': 'Пароль...'})

    def clean(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=login).exists():
            raise ValidationError('Пользователь не существует')
        user = User.objects.get(username=login)
        if user:
            if not user.check_password(password):
                raise ValidationError('Неверный пароль')

        return self.cleaned_data
        


class RegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    bd = forms.DateField(widget=DateInput)
    policy = forms.CharField()
    passport = forms.CharField()
    login = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    first_name.widget.attrs.update({'class': 'form_input', 'placeholder': 'Имя...'})
    last_name.widget.attrs.update({'class': 'form_input', 'placeholder': 'Фамилия...'})
    bd.widget.attrs.update({'class': 'form_input', 'placeholder': 'Дата рождения...'})
    policy.widget.attrs.update({'class': 'form_input', 'placeholder': 'Медицинский полис...'})
    passport.widget.attrs.update({'class': 'form_input', 'placeholder': 'Паспорт...'})
    login.widget.attrs.update({'class': 'form_input', 'placeholder': 'Почта...'})
    password.widget.attrs.update({'class': 'form_input', 'placeholder': 'Пароль...'})
    password2.widget.attrs.update({'class': 'form_input', 'placeholder': 'Повторите пароль...'})

    def save_user(self):
        new_user = User.objects.create(
            username= self.cleaned_data['login'],
            first_name= self.cleaned_data['first_name'],
            last_name= self.cleaned_data['last_name'],
            password= make_password(self.cleaned_data['password']),
            email = self.cleaned_data['login']
        )
        return new_user

    def save_patient(self):
        user = User.objects.get(username=self.cleaned_data['login'])
        new_patient = Patients.objects.create(
            bd = self.cleaned_data['bd'],
            policy = self.cleaned_data['policy'],
            passport = self.cleaned_data['passport'],
            user = user
        )