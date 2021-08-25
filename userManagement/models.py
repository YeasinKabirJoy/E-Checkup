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
        other_fields.setdefault('type', Types.Patient)
        return self.crete_user(username,password,**other_fields)


class User(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=50,unique=True)
    type = models.CharField(max_length=20,choices=Types.choices,default=Types.Admin)
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



