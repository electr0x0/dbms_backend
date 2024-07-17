# appointments/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from connection import execute_raw_sql
from datetime import datetime
from django.utils import timezone
from .serializers import AppointmentSerializer

class AppointmentListView(APIView):
    def get(self, request, doctor_id):
        try:
            query = """
                SELECT 
                    a.id, 
                    a.title, 
                    a.description, 
                    a.ap_date, 
                    a.ap_start_time, 
                    a.ap_end_time, 
                    a.ap_type, 
                    a.google_meet_link, 
                    a.room_number, 
                    d.doctor_name, 
                    p.p_user_id_id, 
                    u.username as patient_username, 
                    a.completed,
                    CASE WHEN a.completed = FALSE AND a.ap_date < CURRENT_DATE THEN TRUE ELSE FALSE END as missed
                FROM appointment_appointment a
                JOIN doctor_doctordetails d ON a.doctor_id = d.doc_id_id
                JOIN patientInfo_patienthealthrecord p ON a.patient_id = p.p_user_id_id
                JOIN auth_user u ON p.p_user_id_id = u.id
                WHERE a.doctor_id = %s
            """
            params = [doctor_id]
            appointments = execute_raw_sql(query, params)
            return Response({'data': appointments}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentCreateView(APIView):
    def post(self, request):
        try:
            serializer = AppointmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Appointment created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateAppointmentStatusView(APIView):
    def post(self, request):
        try:
            doctor_id = request.data.get('doctor_id')
            patient_id = request.data.get('patient_id')
            ap_date = request.data.get('ap_date')
            ap_start_time = request.data.get('ap_start_time')
            completed = request.data.get('completed')

            if not all([doctor_id, patient_id, ap_date, ap_start_time, completed is not None]):
                return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

            query = """
                UPDATE appointment_appointment
                SET completed = %s
                WHERE doctor_id = %s
                AND patient_id = %s
                AND ap_date = %s
                AND ap_start_time = %s
            """
            params = [completed, doctor_id, patient_id, ap_date, ap_start_time]
            execute_raw_sql(query, params)

            return Response({'message': 'Appointment status updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteAppointmentView(APIView):
    def post(self, request):
        try:
            doctor_id = request.data.get('doctor_id')
            patient_id = request.data.get('patient_id')
            ap_date = request.data.get('ap_date')
            ap_start_time = request.data.get('ap_start_time')

            if not all([doctor_id, patient_id, ap_date, ap_start_time]):
                return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

            query = """
                DELETE FROM appointment_appointment
                WHERE doctor_id = %s
                AND patient_id = %s
                AND ap_date = %s
                AND ap_start_time = %s
            """
            params = [doctor_id, patient_id, ap_date, ap_start_time]
            execute_raw_sql(query, params)

            return Response({'message': 'Appointment deleted successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)