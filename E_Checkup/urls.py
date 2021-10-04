"""customUser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userManagement import views as userView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls, name='adminpanel'),
    path('',userView.viewHomePage, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', userView.registration, name='registration'),
    path('profile/', userView.show_profile, name='profile'),
    path('doctor_list/',userView.doctor_list,name='doctor_list'),
    path('contact_us/',userView.contact_us,name='contact_us'),
    path('scheduling/',userView.scheduling,name='scheduling'),
    # path('meeting/',userView.create_meeting,name='meeting'),
    path('doctor_list/<int:doc_id>',userView.create_meeting, name = 'meeting'),
    path('verify_profile/', userView.send_email, name='send_mail'),
    path('email_verification/', userView.verify_email, name='verification'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

