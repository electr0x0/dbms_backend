from django.urls import path
from .views import DoctorDetailView, DoctorUpdateView

urlpatterns = [
    path('doctor/<int:doctor_id>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctor/update/<int:doctor_id>/', DoctorUpdateView.as_view(), name='doctor-update'),
]
