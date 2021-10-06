from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Doctor,Patient,DoctorProfile,PatientProfile,Meeting,RegisteredEmail,DoctorTiming



class UserAdminConfig(UserAdmin):
    ordering = ('join_date',)
    list_display = ('username','is_active','is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'join_date','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
    )


admin.site.register(User,UserAdminConfig)
admin.site.register(Doctor,UserAdminConfig)
admin.site.register(Patient,UserAdminConfig)
admin.site.register([DoctorProfile,PatientProfile,Meeting,RegisteredEmail,DoctorTiming])