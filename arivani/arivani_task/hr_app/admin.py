from django.contrib import admin
from hr_app.models import *
# Register your models here.
@admin.register(Hr_model)
class Hr_modelAdmin(admin.ModelAdmin):
    def employees_under_hr_list(self,objects):
        return [object.name for object in objects.employees_under_hr.all()]
    list_display = ('HrID','name','is_deleted','status','employees_under_hr_list',
    'created_by','updated_by','created_at','updated_at','deleted_by','deleted_at','restored_at',
    'restored_by')
    list_display_links = ('name',)