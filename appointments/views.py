from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from appointments.forms import AppointmentForm 
from psychologists.models import Psychologist
from django.core.mail import send_mail
from django.conf import settings
from appointments.models import Appointment
from django.http import HttpResponseForbidden
from .forms import CancellationForm
@login_required
def book_appointment(request, psychologist_id):
    psychologist = get_object_or_404(Psychologist, id=psychologist_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, psychologist=psychologist.user) 
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.psychologist = psychologist.user 
            appointment.save()

         
            send_mail(
                subject='Confirmare programare',
                message=f'Ai programat o ședință cu {psychologist.user.get_full_name()} '
                        f'pe data de {appointment.datetime.date()} la ora {appointment.datetime.time()}.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

          
            send_mail(
                subject='Ai o programare nouă',
                message=f'{request.user.get_full_name()} s-a programat pe {appointment.datetime}.\n\n'
                        f'Mesajul: {appointment.message or "-"}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[psychologist.user.email],
                fail_silently=False,
            )

            return redirect('client_dashboard')
    else:
        form = AppointmentForm(psychologist=psychologist.user)  

    return render(request, 'appointments/book.html', {
        'form': form,
        'psychologist': psychologist
    })

def list_psychologists(request):
    psychologists = Psychologist.objects.all()
    return render(request, 'appointments/psychologists_list.html', {'psychologists': psychologists})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.client:
        return HttpResponseForbidden("Nu ai permisiunea să anulezi această programare.")

    appointment.delete()
    return redirect('client_dashboard')


@login_required
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.client:
        return HttpResponseForbidden("Nu ai permisiunea să reprogramezi această programare.")

    if request.method == 'POST':
        form = AppointmentForm(request.POST, psychologist=appointment.psychologist)
        if form.is_valid():
            new_datetime = form.cleaned_data['datetime']
            appointment.datetime = new_datetime
            appointment.message = form.cleaned_data.get('message', '')
            appointment.save()
            return redirect('client_dashboard')
    else:
        initial_datetime = appointment.datetime.strftime("%Y-%m-%dT%H:%M")
        form = AppointmentForm(initial={
            'datetime': initial_datetime,
            'message': appointment.message,
        })

    return render(request, 'appointments/reschedule.html', {'form': form})

@login_required
def client_appointments(request):
    print("USER:", request.user)
    print("AUTENTIFICAT:", request.user.is_authenticated)
    print("ROL:", request.user.role)
    appointments = Appointment.objects.filter(client=request.user)
    return render(request, 'appointments/client_appointments.html', {'appointments': appointments})

@login_required
def psychologist_appointments(request):
    appointments = Appointment.objects.filter(psychologist=request.user.psychologist)
    return render(request, 'appointments/psychologist_appointments.html', {'appointments': appointments})



@login_required
def cancel_appointment_by_psychologist(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.psychologist:
        return HttpResponseForbidden("Nu ai permisiunea să anulezi această programare.")

    if request.method == "POST":
        form = CancellationForm(request.POST)
        if form.is_valid():
            appointment.cancellation_reason = form.cleaned_data["cancellation_reason"]
            appointment.is_cancelled = True
            appointment.cancelled_by_psychologist = True
            appointment.save()
            return redirect("psychologist_dashboard")
    else:
        form = CancellationForm()

    return render(request, "appointments/cancel_by_psychologist.html", {"form": form})


@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)


    if request.user == appointment.client and appointment.is_cancelled:
        appointment.delete()
    
    return redirect('client_dashboard')