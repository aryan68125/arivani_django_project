from django.contrib import admin
from employee.models import *
# Register your models here.
@admin.register(Employee)
class EmployeeModel(admin.ModelAdmin):
    list_display=('id','employeeID','name','is_deleted')