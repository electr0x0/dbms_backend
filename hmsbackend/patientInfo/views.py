from rest_framework import generics
from .models import PatientHealthRecord
from .serializers import PatientHealthRecordSerializer

class PatientHealthRecordCreate(generics.ListCreateAPIView):
    queryset = PatientHealthRecord.objects.all()
    serializer_class = PatientHealthRecordSerializer

class PatientHealthRecord(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientHealthRecord.objects.all()
    serializer_class = PatientHealthRecordSerializer

