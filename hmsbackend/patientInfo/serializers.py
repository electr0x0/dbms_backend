from rest_framework import serializers
from .models import PatientHealthRecord

class PatientHealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHealthRecord
        fields = '__all__'