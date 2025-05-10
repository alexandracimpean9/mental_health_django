from django.urls import path
from appointments import views
from appointments.models import Appointment

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('choose/', views.list_psychologists, name='choose_psychologist'),
    path('book/<int:psychologist_id>/', views.book_appointment, name='book_appointment'),
    path('psychologists/', views.list_psychologists, name='psychologist_list'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('client/my-appointments/', views.client_appointments, name='client_appointments'),
    path('cancel-by-psychologist/<int:appointment_id>/', views.cancel_appointment_by_psychologist, name='cancel_by_psychologist'),
    path('delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
]

