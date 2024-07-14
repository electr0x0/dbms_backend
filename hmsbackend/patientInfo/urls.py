from django.urls import path
from .views import PatientHealthRecordCreate, PatientHealthRecord

urlpatterns = [
    path('patient/healtrecord/', PatientHealthRecordCreate.as_view(), name='hr-list-create'),
    path('patient/healtrecord/<int:pk>/', PatientHealthRecord.as_view(), name='hr-detail'),
]
