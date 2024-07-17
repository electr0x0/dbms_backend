from django.db import models
import os



class PatientHealthRecord(models.Model):
    blood_type = models.CharField(max_length=3)
    bmi = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()
    blood_pressure = models.CharField(max_length=25)
    heart_rate = models.IntegerField()
    cholesterol_level = models.FloatField()
    sugar_level = models.FloatField()
    p_user_id = models.ForeignKey('authUser.HHMSUser', on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    def __str__(self):
        return f"Record {self.id} for User {self.p_user_id}"


class DiagnosisReport(models.Model):
    report_id = models.CharField(max_length=255)
    file = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()

    def __str__(self):
        return self.file

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)