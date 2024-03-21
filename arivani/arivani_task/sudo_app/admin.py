from django.contrib import admin
from sudo_app.models import *

@admin.register(RoleList)
class RoleListModelAdmin(admin.ModelAdmin):
    list_display = ('roles','id')
@admin.register(Employee_profile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display=('employeeID','user','subordinate_list','created_by','is_deleted')
    def subordinate_list(self,objects):
        return [object.username for object in objects.assigned_subordinate.all()]


# @admin.register(AssignedSubordinateHr)
# class AssignedSubordinateHrAdmin(admin.ModelAdmin):
#     list_display=('id','employee_id','hr_id')
# @admin.register(AssignSSubordinateToManager)
# class AssignSSubordinateToManagerAdmin(admin.ModelAdmin):
#     list_display = ('id','manager_id','hr_id')