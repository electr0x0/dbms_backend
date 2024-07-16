from django.urls import path
from .views import PatientHealthRecordCreate, PatientHealthRecord, PatientHealthRecordByUser, create_or_update_health_record

urlpatterns = [
    path('patient/healtrecord/', PatientHealthRecordCreate.as_view(), name='hr-list-create'),
    path('patient/healtrecord/all/', PatientHealthRecord.as_view(), name='hr-detail'),
    path('healthrecord/<int:user_id>/', PatientHealthRecordByUser.as_view(), name='patient-health-record-by-user'),
    path('healthrecord/create/', create_or_update_health_record, name='create-or-update-health-record'),
]
