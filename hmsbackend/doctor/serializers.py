from rest_framework import serializers

class DoctorDetailSerializer(serializers.Serializer):
    doc_id_id = serializers.IntegerField()
    doctor_name = serializers.CharField()
    department = serializers.CharField()
    years_of_experience = serializers.IntegerField()
    daily_hours = serializers.CharField()
    room_number = serializers.CharField()
    specialization = serializers.CharField()
