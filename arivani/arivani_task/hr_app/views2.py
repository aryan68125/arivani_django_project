from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from hr_app.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from employee.models import *

#make employee json serializable in function "employees_under_hr_list"
from django.core.serializers import serialize
from auth_user.models import *

def dashboard_home(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        assigned_user_role = AssignedUserRoles.objects.get(user=user)
        user_role = assigned_user_role.user_role
        if user.is_superuser:
            data = {
                'is_superuser':1,
            }
            return render(request,'hr_app/hr_app_home2.html',data)
        else:
            data = {
                'user_role':user_role
            }
            return render(request,'hr_app/hr_app_home2.html',data)
    else:
        return redirect("loginUserPage")
