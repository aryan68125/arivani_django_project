from django.contrib import admin
from employee.models import *
# Register your models here.
@admin.register(Employee)
class EmployeeModel(admin.ModelAdmin):
    list_display=('id','employeeID','name','is_deleted','status',
    'created_by','updated_by','created_at','updated_at','deleted_by','deleted_at','restored_at','restored_by')
    list_display_links = ('name',)