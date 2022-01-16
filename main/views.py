from django.shortcuts import render, redirect
from django.views import View

from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'menu.html', context={'title': 'menu'})


class CreateCoupon(View):
    def get(self, request):
        coupon_form = CreateCouponForm()
        return render(request, 'add_coupon.html', context={'coupon_form': coupon_form})
