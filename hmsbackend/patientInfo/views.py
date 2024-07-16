from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import PatientHealthRecord
from .serializers import PatientHealthRecordSerializer
from .connection import execute_raw_sql

class PatientHealthRecordCreate(generics.ListCreateAPIView):
    serializer_class = PatientHealthRecordSerializer

    def get_queryset(self):
        query = "SELECT * FROM `patientInfo_patienthealthrecord`"
        queryset = execute_raw_sql(query)
        print(queryset)
        return queryset
    

class PatientHealthRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientHealthRecord.objects.all()
    serializer_class = PatientHealthRecordSerializer

class PatientHealthRecordList(APIView):
    def get(self, request):
        query = "SELECT * FROM `patientInfo_patienthealthrecord`"
        all_patients = execute_raw_sql(query)
        serialized_patients = PatientHealthRecordSerializer(all_patients, many=True)
        return Response(serialized_patients.data, status=status.HTTP_200_OK)

class PatientHealthRecordByUser(APIView):
    def get(self, request, user_id):
        query = "SELECT * FROM `patientInfo_patienthealthrecord` WHERE p_user_id_id = %s"
        all_patients = execute_raw_sql(query, [user_id])
        serialized_patients = PatientHealthRecordSerializer(all_patients, many=True)
        return Response(serialized_patients.data, status=status.HTTP_200_OK)
