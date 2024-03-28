from django.db import models
from django.contrib.auth.models import User
from .constants import *
from django.utils import timezone
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from jsonfield import JSONField
from student.models import *
from student.constants import *


class Note(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    educator_feedback = models.TextField(null=True, blank=True)
    resources = models.TextField(null=True, blank=True)

    # educator feedback, list of resources

    def __unicode__(self):
        return f"{self.title}, {self.timestamp}"

    def __str__(self):
        return f"{self.title}, {self.timestamp}"