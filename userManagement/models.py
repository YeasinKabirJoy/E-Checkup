from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.


class Types(models.TextChoices):
    Patient = 'PATIENT', 'Patient'
    Doctor = 'DOCTOR', 'Doctor'
    Admin = 'ADMIN', 'Admin'


class CustomUserManager(BaseUserManager):
    def crete_user(self,username,password,**other_fields):
        user = self.model(username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('type', Types.Admin)
        return self.crete_user(username,password,**other_fields)


class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=50,unique=True)
    type = models.CharField(max_length=20,choices=Types.choices,default=Types.Patient)
    join_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'


    def __str__(self):
        return self.username


class DoctorManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=Types.Doctor)


class Doctor(User):
    objects = DoctorManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Types.Doctor
        return super().save(*args, **kwargs)



class PatientManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=Types.Patient)


class Patient(User):
    objects = PatientManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Types.Patient
        return super().save(*args, **kwargs)


# days = (
#     ('Saturday','Saturday'),
#     ('Sunday','Sunday'),
#     ('Monday','Monday'),
#     ('Tuesday','Tuesday'),
#     ('Wednesday','Wednesday'),
#     ('Thursday','Thursday'),
#     ('Friday','Friday')
# )


class DoctorProfile(models.Model):
    image = models.ImageField(upload_to='doctor/', blank=True, null=True, default="doctor/default_icon.png",)
    user = models.ForeignKey(Doctor, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    status = models.BooleanField(blank=True,null=True,default=True)
    degree = models.CharField(max_length=500,blank=True,null=True)
    hospital_name = models.CharField(max_length=100,blank=True,null=True)
    speciality = models.CharField(max_length=100,blank=True,null=True)


    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created and instance.type == Types.Doctor:
            DoctorProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=Doctor)

class PatientProfile(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    user = models.ForeignKey(Patient, default=None, on_delete=models.CASCADE)
    status = models.BooleanField(blank=True,null=True,default=False)


class Meeting(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,related_name='Doctor')
    patient = models.ForeignKey(Patient,on_delete=models.DO_NOTHING,related_name='Patient')
    date = models.DateField(auto_now=True)
    s_time = models.TimeField()
    e_time = models.TimeField()

    def __str__(self):
        return str(self.date)



    def is_open(self):
        return self.s_time <= datetime.now().time() < self.e_time


# day = models.DateField(default=datetime.now().date().strftime('%d-%m-%y'))
#e_time = models.TimeField(default=datetime.now() + timedelta(minutes=15))


