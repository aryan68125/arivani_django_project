from django.contrib import admin
from student.models import *
# Register your models here.
@admin.register(Student)
class Student_admin(admin.ModelAdmin):
     list_display = ('student_ID', 'date_created','date_updated','Student_Name', 'Father_Name',
                    'roll_no', 'mobile','email'
                    )