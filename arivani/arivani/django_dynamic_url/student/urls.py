from django.urls import path
from student.views import *
urlpatterns = [
    path('',student,name="student"),
    path('insert_student_data',insert_student_data,name='insert_student_data'),
    path('read_student_data',read_student_data,name='read_student_data'),
    path('update_student_data',update_student_data,name='update_student_data'),
    path('delete_student_data',delete_student_data,name='delete_student_data'),
    path('open_student_detail_page',student_details,name='open_student_detail_page'),
    path('student_details/<int:ID>',student_details_page,name='student_details'),
    path('send_email',send_email,name='send_email'),
]
