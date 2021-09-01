from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .registrationForm import RegistrationForm
from .models import PatientProfile, DoctorProfile, Types




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
