from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index_url'),
    path('create_coupon/', CreateCoupon.as_view(), name='create_coupon_url'),
]