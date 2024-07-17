# appointments/urls.py

from django.urls import path
from .views import AppointmentListView, AppointmentCreateView, UpdateAppointmentStatusView, DeleteAppointmentView

urlpatterns = [
    path('appointments/', AppointmentCreateView.as_view(), name='create_appointment'),
    path('appointments/<int:doctor_id>/', AppointmentListView.as_view(), name='list_appointments'),
    path('appointments/update-status/', UpdateAppointmentStatusView.as_view(), name='appointment-update-status'),
    path('appointments/delete/', DeleteAppointmentView.as_view(), name='delete-appointment')
]
