import uuid
from django.contrib.auth.models import User, AbstractUser
from django.db import models

class HHMSUser(AbstractUser):
    first_name = models.CharField(("first name"), max_length=150, blank=True)
    last_name = models.CharField(("last name"), max_length=150, blank=True)
    contact_number = models.CharField(max_length=11)
    
    date_of_birth = models.DateTimeField(null=True, blank=True)
    type = models.CharField(
        max_length=10,
        choices=[
            ("doctor", "Doctor"),
            ("patient", "Patient"),
            ("manager", "Manager")
        ],
    )
    email = models.EmailField(("email address"), null=False, unique=True)
    user_status = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=128, default="defaultpassword")
    
    
    latitude = models.CharField(max_length=255, blank='True')
    longitude = models.CharField(max_length=255, blank='True')
    address = models.CharField(max_length=255, blank='True')
    


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


class Session(models.Model):
    user = models.OneToOneField(HHMSUser, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default='django.utils.timezone.now')