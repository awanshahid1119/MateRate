from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteList(admin.ModelAdmin):
    search_fields = ('user', 'title', 'timestamp')
    list_display = ['user', 'title', 'content', 'timestamp', 'educator_feedback', 'resources']