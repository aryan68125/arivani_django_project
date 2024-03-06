from django.urls import path
from marks.views import *
urlpatterns = [
    path('',marks,name="marks"),
    path('read_student_data',read_student_data,name="read_student_data"),
    path('insert_marks_data',insert_marks_data,name="insert_marks_data"),
    path('marks_settings',marks_settings,name="marks_settings"),
    path('read_marks_data',read_marks_data,name="read_marks_data"),
    path('recalculate_pass_fail',recalculate_pass_fail,name="recalculate_pass_fail"),
    path('update_marks_data',update_marks_data,name="update_marks_data"),
    path('delete_marks_data',delete_marks_data,name="delete_marks_data"),
]
