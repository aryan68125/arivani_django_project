from django.contrib import admin
from auth_jwt.models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ['email','name','tc','is_active','is_admin', "password"]

# Define an admin class for your custom user model
class UserModelAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ['id','email','name','tc','is_active','is_admin','created_at','updated_at']
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ['name','tc']}),
        ("Permissions", {"fields": ["is_admin",'is_active']}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    #this will generate the form in the admin panel to create new users
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ['email','name','tc','is_active','is_admin', "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email",'id']
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(CustomUser, UserModelAdmin)