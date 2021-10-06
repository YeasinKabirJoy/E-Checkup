import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .registrationForm import RegistrationForm
from .meetingForm import MeetingForm
from .models import PatientProfile, DoctorProfile,Types,Doctor,RegisteredEmail,DoctorTiming,Meeting
import random
import string


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

    timing = DoctorTiming.objects.get(doctor = Doctor.objects.get(id=doc_id))
    profile = DoctorProfile.objects.get(user = Doctor.objects.get(id=doc_id))
    scheduled_meeting = Meeting.objects.filter(doctor = Doctor.objects.get(id=doc_id),date=datetime.datetime.now().date().strftime("%Y-%m-%d"))
    context = {
        'form': form,
        'timing': timing,
        'profile': profile,
        'scheduled_meeting':scheduled_meeting,

    }
    return render(request, 'userManagement/create_meeting.html', context)



def contact_us(request):
    return render(request, 'userManagement/contactUs.html')

def scheduling(request):
    return render(request, 'userManagement/scheduling.html')

def id_generator(size=16, chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) :
    return ''.join(random.choice(chars) for _ in range(size))


@login_required
def send_email(request):
    recipient_list = []
    subject = ''
    message = ''
    status = PatientProfile.objects.get(user=request.user).status
    user_message = ''
    if status:
        user_message = 'Profile Verified'
        context = {
            'message': user_message
        }
        return render(request, 'registration /send_email.html', context)
    if request.method == 'POST':

        name =request.POST['name']
        gender =request.POST['gender']
        blood =request.POST['blood']
        email = request.POST['recipient']
        try:
            RegisteredEmail.objects.get(email=email)
            user_message ='Email alreday exists'
            context = {
                'message': user_message
            }
            return render(request, 'registration/send_email.html', context)
        except Exception:
            recipient_list.append( request.POST['recipient'])
            subject = 'E-checkup Verification'

            code = id_generator()
            # v_code = code
            request.session['v_code'] = code
            request.session['name'] = name
            request.session['gender'] = gender
            request.session['blood'] = blood
            request.session['email'] = email

            message += 'Do Not Share With Anyone'
            message += '\n Activation code: ' + code


            status = send_mail(
                subject = subject,
                message = message,
                from_email = 'contact.echeckup@gmail.com',
                recipient_list = recipient_list,
                fail_silently = True
            )
            if status == 1:

                user_message = 'Email sent successfully. Please enter the verification code.'
                context = {
                    'message': user_message
                }

                return redirect('verification')
            else:
                user_message = 'Failed! Try again please!'

    context = {
                'message' : user_message
            }
    return render(request, 'registration/send_email.html', context)



@login_required
def verify_email(request):
    message = ''

    if request.method == "POST":
        code = request.POST['code']
        message = 'Not matched!'

        if request.session['v_code'] == code:
            email=RegisteredEmail(email=request.session['email'])
            email.save()
            message = "Successful! Your account is activated now!"
            profile = PatientProfile.objects.get(user=request.user)
            profile.status = True
            profile.name = request.session['name']
            profile.gender = request.session['gender']
            profile.blood_group = request.session['blood']
            profile.email = request.session['email']
            profile.save()
            context = {
                'message': message
            }
            return render(request, 'registration/verification_success.html', context)

    context = {
        'message': message
    }
    return render(request, 'registration/email_verification.html', context)



