from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index_url'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', logout_view, name='logout_url'),
    path('registration/', RegistrView.as_view(), name='reg_url'),
    path('registration_empl/', RegistrEmplView.as_view(), name='reg_empl_url'),
    path('registration_doctor/', RegistrDoctorView.as_view(), name='reg_doctor_url'),
    path('coupon/', CouponView.as_view(), name='coupon_url'),
    path('doctor_choice/', doctor_choice, name='doctor_choice_url'),
    path('create_coupon/<int:doctor_id>/', CreateCouponView.as_view(), name='create_coupon_url'),
    path('update_coupon/<int:coupon_id>/', UpdateCoupon.as_view(), name='update_coupon_url'),
    path('delete_coupon/<int:coupon_id>/', DeleteCoupon.as_view(), name='delete_coupon_url'),
]