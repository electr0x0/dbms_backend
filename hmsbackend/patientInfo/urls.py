from django.urls import path
from .views import PatientHealthRecordCreate, PatientHealthRecordList, PatientHealthRecordByUser

urlpatterns = [
    path('patient/healthrecord/create/', PatientHealthRecordCreate.as_view(), name='hr-list-create'),
    path('patient/healthrecord/all/', PatientHealthRecordList.as_view(), name='hr-detail'),
    path('patient/healthrecord/<int:user_id>/', PatientHealthRecordByUser.as_view(), name='patient-health-record-by-user')
]
