from django.urls import path
from sudo_app.views_employee import *
urlpatterns = [
    path('employee_page',employee_page,name="employee_page"),
]