from django.db import models
from patientInfo.models import PatientHealthRecord
from doctor.models import DoctorDetails
from django.utils import timezone

class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE, related_name='appointments')
    title = models.CharField(max_length=255, default='Check-up')  
    description = models.TextField(default='Appointment details')  
    patient = models.ForeignKey(PatientHealthRecord, on_delete=models.CASCADE, related_name='appointments', to_field='p_user_id')
    ap_date = models.DateField()
    ap_start_time = models.TimeField()
    ap_end_time = models.TimeField()
    ap_type = models.CharField(max_length=10, choices=[('online', 'Online'), ('physical', 'Physical')])
    google_meet_link = models.CharField(max_length=255,blank=True, default='www.youtube.com')
    room_number = models.CharField(max_length=50, blank=True, null=True)
    completed = models.BooleanField(default=False)
    missed = models.BooleanField(default=False, editable=False)  # New field

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['doctor', 'patient', 'ap_date', 'ap_start_time'], name='unique_appointment')
        ]

    def __str__(self):
        return f"Appointment with Doctor {self.doctor.doc_id.username} and Patient {self.patient.p_user_id.username} on {self.ap_date} from {self.ap_start_time} to {self.ap_end_time}"

    def save(self, *args, **kwargs):
        # Determine if the appointment is missed
        if not self.completed and self.ap_date < timezone.now().date():
            self.missed = True
        else:
            self.missed = False
        super(Appointment, self).save(*args, **kwargs)
