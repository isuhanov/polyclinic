from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class RegistryEmployee(models.Model):
    red_empl_id = models.AutoField(primary_key=True, blank=False, verbose_name='ID сотрудника')
    bd = models.DateField(blank=False, verbose_name='Дата рождения сотрудника')
    post = models.CharField(max_length=100, blank=False, verbose_name='Должность сотрудника')
    user = models.ForeignKey(User,  on_delete=models.CASCADE, blank=False, null=True, verbose_name='пользователь')

    def __str__(self):
        return (self.user.first_name + ' ' + self.user.last_name)

    class Meta:
        verbose_name = 'Сотрудник регистратуры'
        verbose_name_plural = 'Сотрудники регистратуры'


class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True, blank=False, verbose_name='ID пациента')
    bd = models.DateField(blank=False, verbose_name='Дата рождения пациента')
    policy = models.CharField(max_length=16, blank=False, verbose_name='Полис')
    passport = models.CharField(max_length=10,blank=False, verbose_name='Паспорт')
    user = models.ForeignKey(User,  on_delete=models.CASCADE, blank=False, null=True, verbose_name='пользователь')

    def __str__(self):
        return (self.user.first_name + ' ' + self.user.last_name)

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class DirectionDoctors(models.Model):
    direction_id = models.AutoField(primary_key=True, blank=False, verbose_name='ID направления')
    direction_doctors = models.CharField(max_length=100, blank=False, verbose_name='Направление врача')

    def __str__(self):
        return self.direction_doctors

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


class Doctors(models.Model):
    doctor_id = models.AutoField(primary_key=True, blank=False, verbose_name='ID врача')
    fio = models.CharField(max_length=100, blank=False, verbose_name='ФИО врача')
    direction = models.ForeignKey(DirectionDoctors,  on_delete=models.CASCADE, blank=False, null=True, verbose_name='Напрвление врача')
    cab = models.CharField(max_length=3, blank=False, verbose_name='Номер кабинета', default='')

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'


class Coupons(models.Model):
    coupons_id = models.AutoField(primary_key=True, blank=False, verbose_name='ID талона')
    adm_date = models.DateTimeField(blank=False, verbose_name='Дата посещения')
    patient = models.ForeignKey(Patients,  on_delete=models.CASCADE, blank=False, null=True, verbose_name='Пациент')
    doctor = models.ForeignKey(Doctors,  on_delete=models.CASCADE, blank=False, null=True, verbose_name='Врач')
    
    def get_update_url(self):
        return reverse('update_coupon_url', kwargs={'coupon_id': self.coupons_id})
        
    def get_delete_url(self):
        return reverse('delete_coupon_url', kwargs={'coupon_id': self.coupons_id})

    def __str__(self):
        return str(self.coupons_id)

    class Meta:
        verbose_name = 'Талон'
        verbose_name_plural = 'Талоны'