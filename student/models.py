from django.db import models
from django.contrib.auth.models import User
from .constants import *
from datetime import datetime
    
class Classroom(models.Model):
    name = models.CharField(max_length=31)
    standard = models.PositiveSmallIntegerField(
        choices=STUDENT_STD, null=True, blank=True)
    division = models.CharField(max_length=3, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ExamSlot = models.ForeignKey(ExamSlot, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    standard = models.PositiveSmallIntegerField(
        choices=STUDENT_STD, null=True, blank=True)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Classroom")
    premium_user = models.PositiveSmallIntegerField(
        choices=PREMIUM, null=False, blank=False)
    email = models.EmailField(max_length=150, blank=True, verbose_name="Email")
    contact_no = models.CharField(
        max_length=20, blank=True, verbose_name="Contact No.")
    guardian_name = models.CharField(
        max_length=40, blank=True, verbose_name="Parent's/Guardian's Name")
    guardian_contact = models.CharField(
        max_length=20, blank=True, verbose_name="Parent's/Guardian's Contact No")
    guardian_address = models.TextField(
        max_length=150, blank=True, verbose_name="Parent's/Guardian's Address")
    school_name = models.TextField(
        max_length=150, blank=True, verbose_name="School Name")
    # olympiad = models.ForeignKey(
    #     Olympiad, on_delete=models.SET_NULL, null=True, verbose_name="olympiad")

    # startTime = models.TimeField(blank=True,)
    # endTime = models.TimeField(blank=True)
    # date = models.DateField(blank=True)
    forget_password_token = models.CharField(max_length=4, blank=True)
    # login_tracker = models.BooleanField(
    #     verbose_name='login tracker', default=False)


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
    
class RegistrationDate(models.Model):
    ongoing_register_date = models.DateField()
    upcoming_regsiter_date = models.DateField()

    def __str__(self):
        return f"{self.upcoming_regsiter_date}"
    
class Chapter(models.Model):
    name = models.CharField(max_length=63)
    standard = models.PositiveSmallIntegerField(choices=STUDENT_STD)

    def __unicode__(self):
        return str(self.standard)+' : '+self.name

    def __str__(self):
        return str(self.standard)+' : '+self.name

    @classmethod
    def getallChapterRelatedToStandard(cls, standard):

        chapters_queryset = cls.objects.filter(standard=standard)
        res_chapters = [{'id': chapter.id, 'name': chapter.name}
                        for chapter in chapters_queryset]

        return res_chapters