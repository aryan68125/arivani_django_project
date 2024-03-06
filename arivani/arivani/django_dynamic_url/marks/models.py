from email.policy import default
from django.db import models
from student.models import *
# Create your models here.
class Marks(models.Model):
    marks_ID = models.BigAutoField("marks ID",primary_key=True)
    Student_ID = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='marks')
    Student_name = models.CharField("Student's Name",max_length=70,default="student")
    Maths = models.FloatField()
    Physics = models.FloatField()
    Chemistry = models.FloatField()
    Computer = models.FloatField()
    English = models.FloatField()
    Hindi = models.FloatField()
    Total_marks_obtained = models.FloatField("Total marks obtained")
    Percentage = models.FloatField()
    pass_fail = models.BooleanField("Pass status")
    date_created = models.DateTimeField(auto_now_add=True,null=True) 
    date_updated = models.DateTimeField(auto_now_add=True,null=True) 
class MarksSettings(models.Model):
    marks_settings_ID = models.IntegerField("Marks settings ID",default=1)
    passing_percentage = models.FloatField("Passing Percentage",default = 40)
    passing_marks_per_subject = models.FloatField("Passing marks per subject",default=40)
    Total_marks_per_subject = models.FloatField("Total per subject",default=100)
    date_created = models.DateTimeField(auto_now_add=True,null=True) 
    date_updated = models.DateTimeField(auto_now_add=True,null=True)