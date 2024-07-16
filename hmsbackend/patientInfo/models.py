from django.db import models




class PatientHealthRecord(models.Model):
    blood_type = models.CharField(max_length=3)
    bmi = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()
    blood_pressure = models.CharField(max_length=7)
    heart_rate = models.IntegerField()
    cholesterol_level = models.FloatField()
    sugar_level = models.FloatField()
    p_user_id = models.ForeignKey('authUser.HHMSUser', on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return f"Record {self.id} for User {self.p_user_id}"
