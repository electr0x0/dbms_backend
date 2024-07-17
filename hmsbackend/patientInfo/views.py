from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import PatientHealthRecord
from .serializers import PatientHealthRecordSerializer, DiagnosisReportSerializer
from django.db import connection
from rest_framework.parsers import MultiPartParser, FormParser
import os
import uuid
from django.conf import settings

def execute_raw_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

class PatientHealthRecordCreate(generics.ListCreateAPIView):
    serializer_class = PatientHealthRecordSerializer

    def get_queryset(self):
        query = "SELECT * FROM patientInfo_patienthealthrecord"
        queryset = execute_raw_sql(query)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        query = """
            INSERT INTO patientInfo_patienthealthrecord (
                blood_type, bmi, height, weight, blood_pressure, heart_rate, cholesterol_level, sugar_level, date, p_user_id_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [
            data.get('blood_type'),
            data.get('bmi'),
            data.get('height'),
            data.get('weight'),
            data.get('blood_pressure'),
            data.get('heart_rate'),
            data.get('cholesterol_level'),
            data.get('sugar_level'),
            data.get('date'),
            data.get('p_user_id_id')
        ]
        
        print(params)
        
        try:
            execute_raw_sql(query, params)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, record_id, *args, **kwargs):
        
        print('the id values is',record_id)
        
        if not record_id:
            return Response({'error': 'ID parameter is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)
        
       

        query = "DELETE FROM patientInfo_patienthealthrecord WHERE id = %s"
        params = [record_id]

        try:
            execute_raw_sql(query, params)
            return Response({'message': f'Health record with ID {record_id} deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

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
    
    

class DiagnosisReportListCreate(generics.ListCreateAPIView):
    serializer_class = DiagnosisReportSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_queryset(self):
        query = "SELECT * FROM patientInfo_diagnosisreport"
        return execute_raw_sql(query)

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        file_type = request.data.get('file_type')
        user_id = request.data.get('user_id')
        report_id = str(uuid.uuid4())  # Generate a unique report ID

        if files:
            for file in files:
                file_extension = os.path.splitext(file.name)[1]
                file_name = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join(settings.MEDIA_ROOT, 'diagnosis_reports', file_name)

                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                query = """
                    INSERT INTO patientInfo_diagnosisreport (report_id, file, file_type, uploaded_at, user_id)
                    VALUES (%s, %s, %s, NOW(), %s)
                """
                params = [
                    report_id,
                    os.path.join('diagnosis_reports', file_name),
                    file_type,
                    user_id
                ]

                try:
                    execute_raw_sql(query, params)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Files uploaded successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)

class DiagnosisReportHistory(APIView):
    def get(self, request, user_id):
        query = "SELECT * FROM patientInfo_diagnosisreport WHERE user_id = %s"
        params = [user_id]
        result = execute_raw_sql(query, params)
        serialized_history = DiagnosisReportSerializer(result, many=True)
        return Response(serialized_history.data, status=status.HTTP_200_OK)
