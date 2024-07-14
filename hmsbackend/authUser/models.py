from django.contrib.auth.models import User
from django.db import models

class HHMSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=10)
    l_name = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    district = models.CharField(max_length=10)
    division = models.CharField(max_length=10)
    date_of_birth = models.DateTimeField()
    TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    user_status = models.CharField(max_length=10, blank=True, null=True)

class HHMSUserDoctor(models.Model):
    doc_id = models.OneToOneField(HHMSUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=15)
    years_of_experience = models.IntegerField()
    daily_hours = models.IntegerField()
    room_number = models.IntegerField()

class HHMSUserDoctorSpecialization(models.Model):
    doc_id = models.OneToOneField(HHMSUserDoctor, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=10)

class HHMSUserPatient(models.Model):
    pat_id = models.OneToOneField(HHMSUser, on_delete=models.CASCADE)
    

