from django.shortcuts import render, redirect
from .forms import ClientSignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CustomUser
from appointments.models import Appointment
from django.utils import timezone

def register_client(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)  
    else:
        form = ClientSignUpForm()
    return render(request, 'users/register_client.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == CustomUser.Role.CLIENT:
                return redirect('client_dashboard')  
            elif user.role == CustomUser.Role.PSYCHOLOGIST:
                return redirect('psychologist_dashboard')
        else:
            error = 'Numele de utilizator sau parola sunt greșite.'
            return render(request, 'users/login.html', {'error': error})
    return render(request, 'users/login.html')


@login_required
def psychologist_dashboard(request):
    if request.user.role != CustomUser.Role.PSYCHOLOGIST:
        return HttpResponse("Acces interzis.", status=403)

    appointments = Appointment.objects.filter(psychologist=request.user)
    return render(request, 'users/psychologist_dashboard.html', {'appointments': appointments})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def client_dashboard(request):
    if request.user.role != CustomUser.Role.CLIENT:
        return HttpResponse("Acces interzis.", status=403)
    
    appointments = Appointment.objects.filter(
        client=request.user,
        datetime__date__gte=timezone.now().date()
    ).order_by('datetime')
    
    return render(request, 'users/client_dashboard.html', {
        'appointments': appointments
    })