from django.contrib import admin

from attendence.models import *

# Register your models here.
@admin.register(Attendance)
class attendance_admin(admin.ModelAdmin):
    list_display=('attendance_ID','student_ID','Student_Name','date','no_of_days_present')