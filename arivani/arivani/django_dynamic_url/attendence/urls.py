from django.urls import path
from attendence.views import *
urlpatterns = [
    path('',attendance,name='attendance'),
    path('get_student_data',get_student_data,name='get_student_data'),
    path('insert_attendance',insert_attendance,name='insert_attendance'),
    path('Read_attendance',Read_attendance,name='Read_attendance'),
    path('update_attendance',update_attendance,name='update_attendance'),
    path('delete_attendance',delete_attendance,name='delete_attendance'),
]
