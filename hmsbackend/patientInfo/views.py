from rest_framework import generics
from .models import PatientHealthRecord
from .serializers import PatientHealthRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from connection import execute_raw_sql



class PatientHealthRecordCreate(generics.ListCreateAPIView):
    queryset = PatientHealthRecord.objects.all()
    serializer_class = PatientHealthRecordSerializer

class PatientHealthRecord(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientHealthRecord.objects.all()
    serializer_class = PatientHealthRecordSerializer

    def get(self, request):
        query = "SELECT * FROM `patientInfo_patienthealthrecord` "  
        allPatients = execute_raw_sql(query)
        print(allPatients)
        serialized_patients = PatientHealthRecordSerializer(allPatients, many=True)
        return Response(serialized_patients.data, status=status.HTTP_200_OK)


