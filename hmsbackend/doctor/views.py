from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .serializers import DoctorDetailSerializer
from .models import DoctorDetails, DoctorSpecialization
from connection import execute_raw_sql

class DoctorDetailView(View):
    def get(self, request, doctor_id):
        query = """
        SELECT dd.doc_id_id, dd.doctor_name, dd.department, dd.years_of_experience, dd.daily_hours, dd.room_number, ds.specialization
        FROM doctor_doctordetails dd
        LEFT JOIN doctor_doctorspecialization ds ON dd.doc_id_id = ds.doc_id_id
        WHERE dd.doc_id_id = %s
        """
        doctor_details = execute_raw_sql(query, [doctor_id])

        if doctor_details:
            serialized_data = DoctorDetailSerializer(doctor_details[0]).data
            return JsonResponse({'data': serialized_data}, status=200)
        else:
            return JsonResponse({'error': 'Doctor not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class DoctorUpdateView(View):
    def post(self, request, doctor_id):
        try:
            data = json.loads(request.body)
            serializer = DoctorDetailSerializer(data=data)
            print(serializer)
            if serializer.is_valid():
                # Update doctor details
                update_details_query = """
                UPDATE doctor_doctordetails 
                SET doctor_name = %s, department = %s, years_of_experience = %s, daily_hours = %s, room_number = %s
                WHERE doc_id_id = %s
                """
                execute_raw_sql(update_details_query, [
                    serializer.validated_data['doctor_name'],
                    serializer.validated_data['department'],
                    serializer.validated_data['years_of_experience'],
                    serializer.validated_data['daily_hours'],
                    serializer.validated_data['room_number'],
                    doctor_id
                ])
                
                # Update doctor specialization
                update_specialization_query = """
                UPDATE doctor_doctorspecialization 
                SET specialization = %s 
                WHERE doc_id_id = %s
                """
                execute_raw_sql(update_specialization_query, [
                    serializer.validated_data['specialization'],
                    doctor_id
                ])

                return JsonResponse({'message': 'Doctor details updated successfully'}, status=200)
            else:
                return JsonResponse({'error': serializer.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
