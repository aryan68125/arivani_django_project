from django.db import models
from student.models import *
# Create your models here.
class Attendance(models.Model):
    attendance_ID = models.BigAutoField(primary_key=True)
    student_ID = models.OneToOneField(Student, on_delete=models.CASCADE)
    Student_Name = models.CharField(max_length=70)
    date = models.DateField("Date of attendance")
    no_of_days_present = models.IntegerField("Number of Days Present")
    