from django.shortcuts import render,redirect
from employee.models import *
from django.urls import reverse
from django.utils import timezone
import json
from django.http import JsonResponse
#custom user password validation related import
import re
from django.contrib.auth.models import User
from auth_user.models import *
from sudo_app.models import *

# HR DASHBOARD RELATED FUNCTIONS STARTS
def employee_dashboard(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        username = user.username
        date_joined = user.date_joined.date()

        name = first_name + " " + last_name
        assigned_user_role = AssignedUserRoles.objects.get(user=user)
        user_role = assigned_user_role.user_role
        role_list = RoleList.objects.get(id=user_role)
        role_name = role_list.roles
        user_profile = Employee_profile.objects.get(user=user)
        user_profile_id = user_profile.employeeID
        if user.is_superuser:
            data = {
                'is_superuser':1,
                'role_name':role_name,
                'name':name,
            }
            return render(request,'hr_app/hr_app_home2.html',data)
        else:
            data = {
                'user_role':user_role,
                'role_name':role_name,
                'name':name,
                'username':username,
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'user_profile_id':user_profile_id,
                'date_joined':date_joined,
            }
            return render(request,'Employee/employee_dashboard.html',data)
    else:
        return redirect("loginUserPage")
# HR DASHBOARD RELATED FUNCTIONS ENDS

# EMPLOYEE PROFILE UPDATE RELATED FUNCTIONS STARTS
def employeePage(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        username = user.username

        name = first_name + " " + last_name
        assigned_user_role = AssignedUserRoles.objects.get(user=user)
        user_role = assigned_user_role.user_role
        role_list = RoleList.objects.get(id=user_role)
        role_name = role_list.roles
        user_profile = Employee_profile.objects.get(user=user)
        user_profile_id = user_profile.employeeID
        if user.is_superuser:
            data = {
                'is_superuser':1,
                'role_name':role_name,
                'name':name,
            }
            return render(request,'hr_app/hr_app_home2.html',data)
        else:
            data = {
                'user_role':user_role,
                'role_name':role_name,
                'name':name,
                'username':username,
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'user_profile_id':user_profile_id,
            }
            return render(request, 'Employee/employee_profile_page.html', data)
    else:
        return redirect("loginUserPage")

def employee_app_update_employee_profile(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            currently_logged_in_user = User.objects.get(id=logged_in_user)
            user_profile = AssignedUserRoles.objects.get(user=currently_logged_in_user)
            user_role = int(user_profile.user_role)
            if user_role==1:
                if request.method=='POST':
                    data = json.load(request)
                    f_data = data.get('payload')
                    userID = f_data['employeeID']
                    user_pk = int(re.search(r'\d+', userID).group())
                    username = f_data['username']
                    first_name = f_data['first_name']
                    last_name = f_data['last_name']
                    email = f_data['email']
                    try:
                        user = User.objects.get(email=email,username=username)
                        return JsonResponse({'status':500,'error':'username or email is taken'},status=500)
                    except User.DoesNotExist:
                        currently_logged_in_user.username=username
                        currently_logged_in_user.first_name=first_name
                        currently_logged_in_user.last_name=last_name
                        currently_logged_in_user.email=email
                        currently_logged_in_user.save()
                        return JsonResponse({'status':200},status=200)
                    except IntegrityError as e:
                        return JsonResponse({'status':500,'error':e},status=500)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status==400)
            else:
                return redirect("loginUserPage")
        else:
            return redirect("loginUserPage")
# EMPLOYEE PROFILE UPDATE RELATED FUNCTIONS ENDS