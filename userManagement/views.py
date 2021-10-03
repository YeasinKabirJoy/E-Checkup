import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .registrationForm import RegistrationForm
from .meetingForm import MeetingForm
from .models import PatientProfile, DoctorProfile,Types,Doctor


def registration(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = PatientProfile(user=user)
            profile.save()
            form = RegistrationForm()
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'userManagement/registration.html', context)


def viewHomePage(request):
    return render(request, 'home.html')

@login_required
def show_profile(request):
    if request.user.type == Types.Doctor:
        try:
            profile = DoctorProfile.objects.get(user=request.user)
        except DoctorProfile.DoesNotExist:
            profile = "Please complete your profile to view"
    else:
        try:
            profile = PatientProfile.objects.get(user=request.user)
        except PatientProfile.DoesNotExist:
            profile = "Please complete your profile to view"



    context = {
        'profile': profile
    }

    return render(request, 'userManagement/profile.html', context)


def doctor_list(request):
    doctors = DoctorProfile.objects.all()

    context={
        'doctors':doctors
    }

    return render(request, 'userManagement/doctorList.html', context)


def create_meeting(request,doc_id):
    form = MeetingForm()

    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            doc=Doctor.objects.get(id=doc_id)
            a=form.save(commit=False)
            a.doctor=doc
            a.patient=request.user

            delta = datetime.timedelta(minutes=15)
            t = a.s_time
            a.e_time=(datetime.datetime.combine(datetime.datetime.now().date(), t) + delta).time()
            # a.e_time= a.s_time+datetime.timedelta(hours=00,minutes=15,seconds=00)
            a.save()
            form = MeetingForm()
    context = {
        'form': form,
    }
    return render(request, 'userManagement/create_meeting.html', context)


def contact_us(request):
    return render(request, 'userManagement/contactUs.html')

def scheduling(request):
    return render(request, 'userManagement/scheduling.html')


