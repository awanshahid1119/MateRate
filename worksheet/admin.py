from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Solution)

@admin.register(Worksheet)
class WorksheetList(admin.ModelAdmin):
    search_fields = ('name', 'description', 'classroom', 'standard')
    list_display = ['name', 'description', 'standard', 'instructions', 'created']

