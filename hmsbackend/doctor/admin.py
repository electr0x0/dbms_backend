from django.contrib import admin
from .models import DoctorDetails, DoctorSpecialization

class DoctorDetailsAdmin(admin.ModelAdmin):
    list_display = ('doc_id', 'department', 'years_of_experience', 'daily_hours', 'room_number')
    search_fields = ('doc_id__username', 'department')
    list_filter = ('department',)

class DoctorSpecializationAdmin(admin.ModelAdmin):
    list_display = ('doc_id', 'specialization')
    search_fields = ('doc_id__username', 'specialization')
    list_filter = ('specialization',)

admin.site.register(DoctorDetails, DoctorDetailsAdmin)
admin.site.register(DoctorSpecialization, DoctorSpecializationAdmin)
