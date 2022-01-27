from distutils.command.clean import clean
from django import forms
from django.forms import widgets
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.core.exceptions import ValidationError, ObjectDoesNotExist

import datetime

set_number = {'1','2','3','4','5','6','7','8','9','0'}
set_letters_cir = {' ', 'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я' }
set_letters_lat = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
set_taboo_letters = {'?', '/', ',', '.', '!', '@', ';', ':', '<', '>', '=', '+', '"', "'", '%', '&', '|'}


class DateInput(forms.DateInput):#объявляю поле ввода даты
    input_type = 'date'

# ------------------------------------- проверки -------------------------------------------------------
# функция проверки даты рождаения
def check_bd(bd):
    if bd > datetime.date.today():
        raise ValidationError('Дата рождения не должна превышать настоящую')

# функция проверки даты приема
def check_adm_date(adm_date):
    if adm_date.timestamp() < datetime.datetime.now().timestamp():
        raise ValidationError('Неверная дата')
    # if Coupons.objects.filter(doctor=doctor).filter()

# функция проверки фио
def check_fio(fio):
    for i in fio.lower():
        if not(i in set_letters_cir or i in set_letters_lat):
            raise ValidationError('Поле содержит недопустимые символы')
    if len(fio) > 100:
        raise ValidationError('Кол-во символов превышает предел')

# функция проверки серии паспорта
def check_numfield(pasp_seria, am):
    for i in pasp_seria:
        if not(i in set_number):
            raise ValidationError('Поле содержит недопустимые символы')
    if len(pasp_seria) > am:
        raise ValidationError(f'В поле слишком много символов, необходимо {am}')
    if len(pasp_seria) < am:
        raise ValidationError(f'В поле недостаточно символов, необходимо {am}')

# функция проверки логина
def check_login(login):
    for i in login.lower():
        if i in set_letters_cir:
            raise ValidationError('Поле содержит недопустимые символы')

# функция проверки пароля
def check_pass(password):
    password.lower
    for i in password:
        if i in set_taboo_letters or i in set_letters_cir:
            raise ValidationError('Пароль содержит недопустимые символы')
    if len(password) > 30:
        raise ValidationError('В пароле слишком много символов, максимум 30')
    if len(password) < 8:
        raise ValidationError('В пароле недостаточно символов, минимум 8')

# функиция проверки существования логина
def check_login_exists(login):
    if User.objects.filter(username=login).exists():
        raise ValidationError('Такой пользователь уже существует')

# функиция проверки несуществования логина
def check_login_unexists(login):
    if not (User.objects.filter(username=login).exists()):
        raise ValidationError('Такой пользователь не существует')



class CreateCouponForm(forms.Form):
    adm_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    patient = forms.ModelChoiceField(Patients.objects.all(), empty_label='Выберите пациента', required=False)
    doctor = ''

    adm_date.widget.attrs.update({'class': 'form_input', 'autocomplete': 'off', 'placeholder': 'Время посещения...'})    
    patient.widget.attrs.update({'class': 'form_input'})  

    def clean_adm_date(self):
        new_adm_date = self.cleaned_data['adm_date']
        check_adm_date(new_adm_date)

        if Coupons.objects.filter(doctor = self.doctor).filter(adm_date=self.cleaned_data['adm_date']).exists():
            raise ValidationError('Дата занята')

        for coupons in  Coupons.objects.filter(doctor = self.doctor):
            if self.cleaned_data['adm_date'] > coupons.adm_date and self.cleaned_data['adm_date'] < coupons.adm_date_end:
                raise ValidationError('Время приема забронированно')

        delta = new_adm_date.timestamp() - datetime.datetime.now().timestamp()
        delat_days = (datetime.datetime.fromtimestamp(delta) - datetime.datetime.fromtimestamp(0)).days
        if  delat_days > 3:
            raise ValidationError('Можно записаться тольок на 3 дня вперед')

        return new_adm_date


    def save(self, p_user):
        patient_user = Patients.objects.get(user = p_user)
        new_coupon = Coupons.objects.create(
            adm_date = self.cleaned_data['adm_date'],
            adm_date_end = self.cleaned_data['adm_date'] + datetime.timedelta(minutes=15),
            patient = patient_user,
            doctor = self.doctor
        )
        return new_coupon

    def staff_save(self):
        new_coupon = Coupons.objects.create(
            adm_date = self.cleaned_data['adm_date'],
            adm_date_end = self.cleaned_data['adm_date'] + datetime.timedelta(minutes=15),
            patient = self.cleaned_data['patient'],
            doctor = self.doctor
        )
        return new_coupon

    def set_doctor(self, doctor):
        self.doctor = doctor


class FilterForm(forms.Form):
    DATE_CHOICES =(
        ('all', 'all'),
        ('active', 'active'),
        ('disabled ', 'disabled')
    )
    date_choice = forms.ChoiceField(choices = DATE_CHOICES, required=False)
    patient = forms.ModelChoiceField(Patients.objects.all(), empty_label='Выберите пациента', required=False)
    doctor = forms.ModelChoiceField(Doctors.objects.all(), empty_label='Выберите врача', required=False)
    

    def get_coupons(self):
        coupons = Coupons.objects.all()

        if self.cleaned_data['date_choice'] == 'active':
            coupons = coupons.filter(adm_date__gte=datetime.datetime.now())

        if self.cleaned_data['date_choice'] != 'all' and self.cleaned_data['date_choice'] != 'active':
            coupons = coupons.filter(adm_date__lt=datetime.datetime.now())
        
        if self.cleaned_data['patient'] != None:
            coupons = coupons.filter(patient=self.cleaned_data['patient'])
        
        if self.cleaned_data['doctor'] != None:
            coupons = coupons.filter(doctor=self.cleaned_data['doctor'])

        return coupons
        


class LoginForm(forms.Form):#форма авторизации и аутентификации
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    login.widget.attrs.update({'class': 'form_input', 'placeholder': 'Логин (Почта)...'})
    password.widget.attrs.update({'class': 'form_input', 'placeholder': 'Пароль...'})

    def clean(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=login).exists():
            print(self.errors)
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

    def clean_first_name(self):
        new_first_name = self.cleaned_data['first_name']
        check_fio(new_first_name)
        return new_first_name

    def clean_last_name(self):
        new_last_name = self.cleaned_data['last_name']
        check_fio(new_last_name)
        return new_last_name

    def clean_bd(self):
        new_bd = self.cleaned_data['bd']
        check_bd(new_bd)
        return new_bd

    def clean_policy(self):
        new_policy = self.cleaned_data['policy']
        check_numfield(new_policy, 16)
        return new_policy

    def clean_passport(self):
        new_passport = self.cleaned_data['passport']
        check_numfield(new_passport, 10)
        return new_passport
    
    def clean_login(self):
        new_login = self.cleaned_data['login']
        check_login_exists(new_login)
        return new_login
    
    def clean_password(self):
        self.new_password = self.cleaned_data['password']
        check_pass(self.new_password)
        return self.new_password

    def clean_password2(self):
        if self.new_password != self.cleaned_data['password2']:
            raise ValidationError('Пароли не совпадают')
        return self.cleaned_data['password2']


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



class RegistrEmplForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    bd = forms.DateField(widget=DateInput)
    post = forms.CharField()
    login = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    first_name.widget.attrs.update({'class': 'form_input', 'placeholder': 'Имя...'})
    last_name.widget.attrs.update({'class': 'form_input', 'placeholder': 'Фамилия...'})
    bd.widget.attrs.update({'class': 'form_input', 'placeholder': 'Дата рождения...'})
    post.widget.attrs.update({'class': 'form_input', 'placeholder': 'Должность...'})
    login.widget.attrs.update({'class': 'form_input', 'placeholder': 'Почта...'})
    password.widget.attrs.update({'class': 'form_input', 'placeholder': 'Пароль...'})
    password2.widget.attrs.update({'class': 'form_input', 'placeholder': 'Повторите пароль...'})

    def clean_first_name(self):
        new_first_name = self.cleaned_data['first_name']
        check_fio(new_first_name)
        return new_first_name

    def clean_last_name(self):
        new_last_name = self.cleaned_data['last_name']
        check_fio(new_last_name)
        return new_last_name

    def clean_bd(self):
        new_bd = self.cleaned_data['bd']
        check_bd(new_bd)
        return new_bd

    def clean_post(self):
        new_post = self.cleaned_data['post']
        check_fio(new_post)
        return new_post
    
    def clean_login(self):
        new_login = self.cleaned_data['login']
        check_login_exists(new_login)
        return new_login
    
    def clean_password(self):
        self.new_password = self.cleaned_data['password']
        check_pass(self.new_password)
        return self.new_password

    def clean_password2(self):
        if self.new_password != self.cleaned_data['password2']:
            raise ValidationError('Пароли не совпадают')
        return self.cleaned_data['password2']


    def save_user(self):
        new_user = User.objects.create(
            username= self.cleaned_data['login'],
            first_name= self.cleaned_data['first_name'],
            last_name= self.cleaned_data['last_name'],
            password= make_password(self.cleaned_data['password']),
            email = self.cleaned_data['login']
        )
        return new_user

    def save_empl(self):
        user = User.objects.get(username=self.cleaned_data['login'])
        new_patient = RegistryEmployee.objects.create(
            bd = self.cleaned_data['bd'],
            post = self.cleaned_data['post'],
            user = user
        )


class RegistrDoctorForm(forms.Form):
    fio = forms.CharField()
    direction = forms.ModelChoiceField(DirectionDoctors.objects.all())
    cab = forms.CharField()

    fio.widget.attrs.update({'class': 'form_input', 'placeholder': 'ФИО...'})
    direction.widget.attrs.update({'class': 'form_input', 'placeholder': 'Должность...'})
    cab.widget.attrs.update({'class': 'form_input', 'placeholder': 'Кабинет...'})

    def clean_fio(self):
        new_fio = self.cleaned_data['fio']
        check_fio(new_fio)
        return new_fio

    def clean_cab(self):
        new_cab = self.cleaned_data['cab']
        for i in new_cab:
            if not(i in set_number):
                raise ValidationError('Поле содержит недопустимые символы')
        if len(new_cab) > 3:
            raise ValidationError('В поле слишком много символов')
        if new_cab == '0':
            raise ValidationError('Недопустимое значение')
        if Doctors.objects.filter(cab=new_cab).exists():
            raise ValidationError('Кабинет занят другим врачем')
        return new_cab

    def save_doctor(self):
        new_doctor = Doctors.objects.create(
            fio = self.cleaned_data['fio'],
            direction = self.cleaned_data['direction'],
            cab = self.cleaned_data['cab'],
        )
        return new_doctor