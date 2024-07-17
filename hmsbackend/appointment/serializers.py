# serializers.py

from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        room_number = data.get('room_number', '')
        google_meet_link = data.get('google_meet_link', '')

        if room_number == '' and google_meet_link == '':
            raise serializers.ValidationError("Either 'room_number' or 'google_meet_link' must be provided.")
        
        if room_number != '' and google_meet_link != '':
            raise serializers.ValidationError("Provide either 'room_number' or 'google_meet_link', not both.")
        
        return data