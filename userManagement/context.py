from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import User, DoctorProfile, PatientProfile


def verifiedUser(request):
    usertype = ''
    userStatus=''
    if request.user.is_authenticated:
        if request.user.type == 'DOCTOR':
            usertype = 'DOCTOR'
        elif request.user.type == 'PATIENT':
            usertype = 'PATIENT'
            try:
                user = get_object_or_404(PatientProfile, user=request.user)
                if user.status:
                    userStatus = 'Verified'
                else:
                    userStatus = 'notVerified'
            except Exception:
                usertype = "Error"
        else:
            usertype = "ADMIN"



    context = {
        'userStatus': userStatus,
        'usertype' : usertype
    }
    return context