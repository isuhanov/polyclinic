from re import L
import re
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect


from django.contrib.auth import authenticate, login, logout


from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'menu.html', context={'title': 'menu'})


class CouponView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            return HttpResponseRedirect('/login/')
        if user.is_staff:
            coupons = Coupons.objects.all()
        else:
            current_patient = Patients.objects.get(user = user)
            coupons = Coupons.objects.filter(patient = current_patient)
        return render(request, 'coupon.html', context={'coupons': coupons})


class CreateCoupon(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            return HttpResponseRedirect('/login/')
        coupon_form = CreateCouponForm()
        return render(request, 'add_coupon.html', context={'coupon_form': coupon_form, 'title': 'Запись к врачу'})

    def post(self, request):
        bound_form = CreateCouponForm(request.POST)

        if bound_form.is_valid():
            bound_form.save(request.user)
            return render(request, 'success.html')

        return render(request, 'add_coupon.html' ,context={'coupon_form': bound_form})


class UpdateCoupon(View):
    def get(self, request, coupon_id):
        coupon_form = CreateCouponForm()
        return render(request, 'add_coupon.html', context={'coupon_form': coupon_form, 'title': 'Изменение записи к врачу'})

    def post(self, request, coupon_id):
        bound_form = CreateCouponForm(request.POST)

        if bound_form.is_valid():
            coupon = Coupons.objects.get(coupons_id = coupon_id)
            coupon.adm_date = bound_form.cleaned_data['adm_date']
            coupon.doctor = bound_form.cleaned_data['doctor']
            coupon.save()
            return render(request, 'success.html')

        return render(request, 'add_coupon.html' ,context={'coupon_form': bound_form})


class DeleteCoupon(View):
    def get(self, request, coupon_id):
        return render(request, 'delete_ask.html')

    def post(self, request, coupon_id):
        Coupons.objects.get(coupons_id = coupon_id).delete()
        return render(request, 'success.html')
        

class AddPatientView(View):
    def get(self, request):
        return render(request, 'add_patient.html', context={'': ''})


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
            return HttpResponseRedirect('/login/')

        return render(request, 'register.html', context={'form': bound_form})