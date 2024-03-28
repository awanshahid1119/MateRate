from django.contrib import admin
from .models import Student, Classroom, RegistrationDate

ADDITIONAL_FIELDS = ()

OPTIONAL_FIELDS = ()



admin.site.register([Classroom, RegistrationDate])

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('user', 'name', 'standard', 'email', 'premium_user')
    list_display = ['user', 'name', 'standard', 'premium_user',
                    'email', 'contact_no', 'guardian_name', 'school_name']