from django.contrib import admin
from dashboard.models import *
# Register your models here.
@admin.register(Hr_model)
class Hr_modelAdmin(admin.ModelAdmin):
    list_display = ('HrID','name','is_deleted')