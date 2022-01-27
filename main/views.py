from asyncio.windows_events import NULL
from datetime import timedelta
import json
from re import L
import re
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect


from django.contrib.auth import authenticate, login, logout
from matplotlib.style import context


from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'menu.html', context={'title': 'menu'})


class CouponView(View):
    def get(self, request):
        filter_form = FilterForm()
        if request.user.is_authenticated:
            user = request.user
        else:
            return HttpResponseRedirect('/login/')
        if user.is_staff or RegistryEmployee.objects.filter(user = request.user):
            coupons = Coupons.objects.all()
        else:
            current_patient = Patients.objects.get(user = user)
            coupons = Coupons.objects.filter(patient = current_patient)

        return render(request, 'coupon.html', context={'coupons': coupons, 'filter_form': filter_form})

    def post(self, request):
        bound_form = FilterForm(request.POST)
        if bound_form.is_valid():
            coupons = bound_form.get_coupons()
        return render(request, 'coupon.html', context={'coupons': coupons, 'filter_form': bound_form})


def doctor_choice(request):
    if request.user.is_authenticated:
            user = request.user
    else:
        return HttpResponseRedirect('/login/')
    doctors = Doctors.objects.all()
    return render(request, 'doctor_choice.html', context={'doctors':doctors, 'title': 'Выберите врача'})


class CreateCouponView(View):
    def get(self, request, doctor_id):
        dates = Coupons.objects.filter(doctor = doctor_id).filter(adm_date__gte=datetime.datetime.now())
        coupon_form = CreateCouponForm(initial = {'doctor': doctor_id})
        return render(request, 'add_coupon.html', context={'coupon_form': coupon_form, 'dates': dates, 'datetime': datetime, 'title': 'Запись к врачу'})

    def post(self, request, doctor_id):
        bound_form = CreateCouponForm(request.POST)
        doctor = Doctors.objects.get(doctor_id = doctor_id)
        bound_form.set_doctor(doctor)
        
        if bound_form.is_valid():
            if request.user.is_staff:
                new_coupon = bound_form.staff_save()
            else:
                new_coupon = bound_form.save(request.user)
            return render(request, 'success.html')
        
        return render(request, 'add_coupon.html' ,context={'coupon_form': bound_form})


class UpdateCoupon(View):
    def get(self, request, coupon_id):
        doctor = Coupons.objects.get(coupons_id = coupon_id).doctor
        dates = Coupons.objects.filter(doctor = doctor).filter(adm_date__gte=datetime.datetime.now())
        coupon_form = CreateCouponForm()
        return render(request, 'update_coupon.html', context={'coupon_form': coupon_form, 'dates': dates, 'title': 'Изменение записи к врачу'})

    def post(self, request, coupon_id):
        bound_form = CreateCouponForm(request.POST)
        coupon = Coupons.objects.get(coupons_id = coupon_id)
        bound_form.set_doctor(coupon.doctor)

        if bound_form.is_valid():
            coupon.adm_date = bound_form.cleaned_data['adm_date']
            coupon.adm_date_end = bound_form.cleaned_data['adm_date'] + datetime.timedelta(minutes=15)
            coupon.save()
            return render(request, 'success.html')

        return render(request, 'update_coupon.html' ,context={'coupon_form': bound_form})


class DeleteCoupon(View):
    def get(self, request, coupon_id):
        return render(request, 'delete_ask.html')

    def post(self, request, coupon_id):
        Coupons.objects.get(coupons_id = coupon_id).delete()
        return render(request, 'success.html')
        

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', context={'form': form})


    def post(self, request):
        bound_form = LoginForm(request.POST)

        if bound_form.is_valid():
            login_user = bound_form.cleaned_data['login']
            password = bound_form.cleaned_data['password']

            user = authenticate(username=login_user, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')

        return render(request, 'login.html', context={'form':bound_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class RegistrView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', context={'form': form})

    def post(self, request):
        bound_form = RegisterForm(request.POST)

        if bound_form.is_valid():
            new_user = bound_form.save_user()
            new_patient = bound_form.save_patient()
            if (request.user.is_staff):
                return render(request, 'success.html')
            else:
                return HttpResponseRedirect('/login/')

        return render(request, 'register.html', context={'form': bound_form})


class RegistrEmplView(View):
    def get(self, request):
        form = RegistrEmplForm()
        return render(request, 'register_empl.html', context={'form': form})

    def post(self, request):
        pass
        bound_form = RegistrEmplForm(request.POST)

        if bound_form.is_valid():
            new_user = bound_form.save_user()
            new_patient = bound_form.save_empl()
            return render(request, 'success.html')

        return render(request, 'register_empl.html', context={'form': bound_form})


class RegistrDoctorView(View):
    def get(self, request):
        form = RegistrDoctorForm()
        return render(request, 'register_doctor.html', context={'form': form})

    def post(self, request):
        pass
        bound_form = RegistrDoctorForm(request.POST)

        if bound_form.is_valid():
            new_doctor = bound_form.save_doctor()
            return render(request, 'success.html')

        return render(request, 'register_doctor.html', context={'form': bound_form})