from django.contrib import admin

from main.models import Coupons, DirectionDoctors, Doctors, Patients, RegistryEmployee


admin.site.register(RegistryEmployee)
admin.site.register(Patients)
admin.site.register(DirectionDoctors)
admin.site.register(Doctors)
admin.site.register(Coupons)
