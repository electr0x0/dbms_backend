# appointment/admin.py

from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'ap_date', 'ap_start_time', 'ap_end_time', 'ap_type', 'google_meet_link')
    search_fields = ('doctor__doc_id__username', 'patient__p_user_id__username', 'ap_type')
    list_filter = ('ap_date', 'ap_type', 'doctor__department')

admin.site.register(Appointment, AppointmentAdmin)
