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

class Worksheet(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True)
    classroom = models.ManyToManyField(Classroom, blank=True)
    standard = models.PositiveSmallIntegerField(
        choices=STUDENT_STD, null=True, blank=True)
    instructions = RichTextUploadingField(max_length=10000, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    educator_feedback = models.TextField(null=True, blank=True)
    resources = models.TextField(null=True, blank=True)
    isDraft = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='worksheet_images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Worksheets"

    def __str__(self):
        return self.name
    
    def intro_details(self):
        details = {
            'id': self.id,
            'name': self.name,
            'description': [self.description],
            'instructions': self.instructions,
            'assignment_type': self.assignment_type,
            'num_of_questions': self.question_set.count(),

        }
        return details
    
class Question(models.Model):
    worksheet = models.ForeignKey(Worksheet, on_delete=models.CASCADE)
    name = models.CharField(max_length=31, null=True, blank=True)
    q_no = models.PositiveIntegerField(verbose_name="Question no.")
    question = RichTextField()
    difficulty = models.SmallIntegerField(
        choices=Q_DIFFICULTY, null=True, default=0)
    # type = models.PositiveIntegerField(choices=Q_TYPE, null=True, default=1)
    # marks = models.FloatField(null=True, default=1)
    # penalty = models.FloatField(null=True, default=0)
    explanation = RichTextField(null=True, blank=True)
    # hint = RichTextField(blank=True, null=True)
    answer = models.TextField(null=True, blank=True)

    def Meta(self):
        verbose_name = "Question"
        unique_together = ('q_no', 'quiz')
        ordering = ('q_no',)

    def __str__(self):
        return str(self.name)

class Solution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.CharField(max_length=4)
    final_answer = models.TextField(null=True, blank=True) 
    solution_steps = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Submission(models.Model):
    """
    Student's response in a assignment
    """
    student = models.ForeignKey(Student, null=True,
                                on_delete=models.SET_NULL,  related_name='student_submission')
    worksheet = models.ForeignKey(
        Worksheet, null=True, on_delete=models.CASCADE)
    submitted = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __unicode__(self):
        return str(self.worksheet.id)+':'+self.student.user.username

    def __str__(self):
        return str(self.worksheet.id)+':'+self.student.user.username
    

class Response_model(models.Model):

    student_id = models.ForeignKey(
        Student, related_name="user_response", null=True, on_delete=models.SET_NULL)
    worksheet_id = models.ForeignKey(
        Worksheet, verbose_name="Assignment ID", null=True, on_delete=models.CASCADE)
    total_attempts = models.PositiveIntegerField(
        default=0, verbose_name="total_attempts")
    responses = models.ManyToManyField(Solution, verbose_name="Responses")
    custom_answers = JSONField(verbose_name="Custom Answers", null=True, blank=True,
                               help_text="""
            This is a JSON field to store custom answers entered by the student wherever custom input is possible. <br />
            Use the <i>Question ID</i> as key and <i>answer marked</i> as the value pair. <br />
            Whenever such a question is encountered, the value in option text (opt_text) will get replaced by the value in answer marked. 
            """)
    time_stats = JSONField(verbose_name="Time spent in each question", null=True, blank=True,
                           help_text="""
            This is a JSON Field to store time spent in each question by the student. <br />
            """)
    response_behaviour = JSONField(verbose_name="Track the behaviour of student in each question", null=True, blank=True, help_text="""

        This is a json field to store the boolean value of explaination and hint in each question by the student
    """)
    marks_obtained = models.FloatField(
        null=True, default=0, verbose_name="Marks obtained", help_text="""
            total marks_obtained of student for current submission.
        """)

    # rank = models.PositiveIntegerField(
    #     null=True, default=0, blank=True, verbose_name="Rank in the Assignment")

    # highest_marks_obtained = models.FloatField(null=True, default=0, verbose_name="Highest marks obtained",
                                            #    help_text="""highest marks of student in current assignment in all the attempts so far. """)

    performance = models.SmallIntegerField(
        choices=PERFORMANCE,
        null=True,
        blank=True,
        default=1,
        verbose_name="Performance of the Student",
        help_text="""
            The overall performance of the student in the quiz. <br />
            <b>0</b> Needs improvement <br />
            <b>1</b> Good <br />
            <b>2</b> Excellent <br />
            """
    )

    def __unicode__(self):
        return str(self.worksheet_id.id)+':'+self.student_id.user.username

    def __str__(self):
        return str(self.worksheet_id.id)+':'+self.student_id.user.username

