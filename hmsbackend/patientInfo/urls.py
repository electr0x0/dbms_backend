from django.urls import path
from .views import PatientHealthRecordCreate, PatientHealthRecordList, PatientHealthRecordByUser, DiagnosisReportListCreate, DiagnosisReportHistory

urlpatterns = [
    path('patient/healthrecord/', PatientHealthRecordCreate.as_view(), name='hr-list-create'),
    path('patient/healthrecord/delete/<int:record_id>', PatientHealthRecordCreate.as_view(), name='hr-list-delete'),
    path('patient/healthrecord/all/', PatientHealthRecordList.as_view(), name='hr-detail'),
    path('patient/healthrecord/view/<int:user_id>', PatientHealthRecordByUser.as_view(), name='patient-health-record-by-user'),
    path('patient/diagnosisreport/', DiagnosisReportListCreate.as_view(), name='diagnosisreport-list-create'),
    path('patient/diagnosisreport/history/<int:user_id>', DiagnosisReportHistory.as_view(), name='diagnosisreport-history'),
]
