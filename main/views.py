from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'menu.html', context={'title': 'menu'})


class CouponView(View):
    def get(self, request):
        current_patient = Patients.objects.get(user = request.user)
        coupons = Coupons.objects.filter(patient = current_patient)
        return render(request, 'coupon.html', context={'coupons': coupons})


class CreateCoupon(View):
    def get(self, request):
        coupon_form = CreateCouponForm()
        return render(request, 'add_coupon.html', context={'coupon_form': coupon_form})

    def post(self, request):
        bound_form = CreateCouponForm(request.POST)

        if bound_form.is_valid():
            bound_form.save(request.user)
            return render(request, 'success.html')

        return render(request, 'add_coupon.html' ,context={'coupon_form': bound_form})
