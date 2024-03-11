from django.contrib import admin
from hr_app.models import *
# Register your models here.
@admin.register(Hr_model)
class Hr_modelAdmin(admin.ModelAdmin):
    list_display = ('HrID','name','is_deleted','status',
    'created_by','updated_by','created_at','updated_at','deleted_by','deleted_at','restored_at',
    'restored_by')
    list_display_links = ('name',)