from django.shortcuts import redirect, render
from .registrationForm import RegistrationForm
from .models import PatientProfile



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