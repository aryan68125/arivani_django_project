from django.contrib import admin
from auth_user.models import *
# Register your models here.
@admin.register(AssignedUserRoles)
class RoleModelAdmin(admin.ModelAdmin):
    list_display=('user','user_role')
