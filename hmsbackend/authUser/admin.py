from django.contrib import admin
from .models import HHMSUser, HHMSUserDoctor, HHMSUserDoctorSpecialization, HHMSUserPatient

admin.site.register(HHMSUser)
admin.site.register(HHMSUserDoctor)
admin.site.register(HHMSUserDoctorSpecialization)
admin.site.register(HHMSUserPatient)

