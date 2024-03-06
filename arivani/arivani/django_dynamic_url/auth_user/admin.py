from django.contrib import admin
from auth_user.models import *

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# Register your models here.
# the old code
# @admin.register(User_profile)
# class User_profileAdmin(admin.ModelAdmin):
#     list_display = ('user','userRole',) 

#using inline method to combine User table contents and User_profile contents table in the admin panel
class USerProfileInline(admin.StackedInline):
    model = User_profile
    can_delete = False
class AccountUserAdmin(AuthUserAdmin):
    inlines = [USerProfileInline]

#inorder to get this working we first need to unregister User model from the admin panel
# and then we need to register the AccountUserAdmin model back in the admin panel
admin.site.unregister(User)
admin.site.register(User,AccountUserAdmin)