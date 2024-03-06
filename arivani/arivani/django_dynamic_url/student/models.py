from ctypes import BigEndianStructure
from random import choice
from django.db import models

# Create your models here.
class Student(models.Model):
    student_ID = models.BigAutoField(primary_key=True,blank=True)
    Student_Name = models.CharField("Student's name",max_length = 70,blank=True)
    Father_Name = models.CharField("Father's Name",max_length = 70,blank=True)
    roll_no = models.IntegerField(blank=True)
    mobile = models.BigIntegerField(blank=True)
    email = models.EmailField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True) 
    date_updated = models.DateTimeField(auto_now_add=True,null=True)
    