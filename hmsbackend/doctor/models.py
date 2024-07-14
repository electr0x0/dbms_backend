from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DoctorDetails(models.Model):
    doc_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    doctor_name = models.CharField(max_length=50, default="John Doe")
    department = models.CharField(max_length=15)
    years_of_experience = models.IntegerField()
    daily_hours = models.IntegerField()
    room_number = models.IntegerField()

    def __str__(self):
        return f"Doctor {self.doc_id} - {self.department}"

class DoctorSpecialization(models.Model):
    CARDIOLOGY = 'Cardiology'
    NEUROLOGY = 'Neurology'
    PEDIATRICS = 'Pediatrics'
    GENERAL_SURGERY = 'General Surgery'
    ORTHOPEDICS = 'Orthopedics'

    SPECIALIZATION_CHOICES = [
        (CARDIOLOGY, 'Cardiology'),
        (NEUROLOGY, 'Neurology'),
        (PEDIATRICS, 'Pediatrics'),
        (GENERAL_SURGERY, 'General Surgery'),
        (ORTHOPEDICS, 'Orthopedics'),
    ]

    doc_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=15, choices=SPECIALIZATION_CHOICES)

    def __str__(self):
        return f"Doctor {self.doc_id} - Specialization {self.specialization}"
