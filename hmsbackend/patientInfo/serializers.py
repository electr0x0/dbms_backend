from rest_framework import serializers
from .models import PatientHealthRecord, DiagnosisReport

class PatientHealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHealthRecord
        fields = ['id', 'blood_type', 'bmi', 'height', 'weight', 'blood_pressure', 'heart_rate', 'cholesterol_level', 'sugar_level', 'p_user_id_id', 'date']


class DiagnosisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisReport
        fields = '__all__'