from django.contrib import admin
from sudo_app.models import *

@admin.register(RoleList)
class RoleListModelAdmin(admin.ModelAdmin):
    list_display = ('roles','id')
@admin.register(Employee_profile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display=('employeeID','user','is_deleted')