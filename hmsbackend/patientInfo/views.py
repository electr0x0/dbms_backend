from rest_framework import generics
from .models import PatientHealthRecord
from .serializers import PatientHealthRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .connection import execute_raw_sql
from rest_framework.decorators import api_view
from django.utils import timezone
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
    

class PatientHealthRecordByUser(generics.GenericAPIView):
    serializer_class = PatientHealthRecordSerializer

    def get(self, request, user_id):
        query = "SELECT * FROM `patientInfo_patienthealthrecord` WHERE p_user_id_id = %s"
        allPatients = execute_raw_sql(query, [user_id])
        serialized_patients = PatientHealthRecordSerializer(allPatients, many=True)
        return Response(serialized_patients.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_or_update_health_record(request):
    data = request.data
    user_id = data.get('p_user_id')
    date = data.get('date', timezone.now().date())
    blood_type = data.get('blood_type')
    bmi = data.get('bmi')
    height = data.get('height')
    weight = data.get('weight')
    blood_pressure = data.get('blood_pressure')
    heart_rate = data.get('heart_rate')
    cholesterol_level = data.get('cholesterol_level')
    sugar_level = data.get('sugar_level')
    
    select_query = "SELECT * FROM `patientInfo_patienthealthrecord` WHERE p_user_id_id = %s AND date = %s"
    existing_records = execute_raw_sql(select_query, [user_id, date])

    if existing_records:
        update_query = """
        UPDATE `patientInfo_patienthealthrecord`
        SET blood_type = %s, bmi = %s, height = %s, weight = %s, blood_pressure = %s,
            heart_rate = %s, cholesterol_level = %s, sugar_level = %s
        WHERE p_user_id_id = %s AND date = %s
        """
        params = [blood_type, bmi, height, weight, blood_pressure, heart_rate, cholesterol_level, sugar_level, user_id, date]
        execute_raw_sql(update_query, params)
        message = "Record updated successfully."
    else:
        insert_query = """
        INSERT INTO `patientInfo_patienthealthrecord` (blood_type, bmi, height, weight, blood_pressure, heart_rate, cholesterol_level, sugar_level, p_user_id_id, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [blood_type, bmi, height, weight, blood_pressure, heart_rate, cholesterol_level, sugar_level, user_id, date]
        execute_raw_sql(insert_query, params)
        message = "Record created successfully."

    return Response({'message': message}, status=status.HTTP_200_OK)