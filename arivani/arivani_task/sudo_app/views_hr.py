from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from sudo_app.models import *
from auth_user.models import *

from django.contrib.auth.models  import User

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.db import IntegrityError
import json
import random
from django.urls import reverse

#custom user password validation related import
import re

from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#Email related import
from django.conf import settings
#email backend
from django.core.mail import EmailMessage

#django messeges related imports
from django.contrib import messages

def hr_page(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            data = {
                'is_superuser':1
            }
            return render(request,'sudo_app/hr_page.html',data)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("loginUserPage")

# GET ALL DATA STARTS
#get all employees
def get_all_employees(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            if user.is_superuser:
                if request.method=='POST':
                    user_list = list(User.objects.all().values())
                    user_employee_list = []
                    for user in user_list:
                        admin = 1
                        if user['id'] != admin:
                            user_role_list = {}
                            get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                            if get_user_role.user_role == '1':
                                role_list = RoleList.objects.get(id=get_user_role.user_role)
                                employee_profile_id = Employee_profile.objects.get(user=user['id']) 
                                user_role_list['user_role'] = get_user_role.user_role #role id
                                user_role_list['user_role_name'] = role_list.roles #role name
                                user_role_list['employeeID'] = employee_profile_id.employeeID
                                user_role_list['is_deleted'] = employee_profile_id.is_deleted
                                user_role_list['user'] = user
                                user_employee_list.append(user_role_list)
                    data = {
                        'user_employee_list':user_employee_list,
                    }
                    return JsonResponse({'status':200,'user_list':user_employee_list},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
            else:
                return Jsonresponse({'status':401,'error':'You are not Authorize to access this link'},status=401)
        else:
            return redirect("loginUserPage")
#get all hr's
def get_all_hr(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            if user.is_superuser:
                if request.method=='POST':
                    user_list = list(User.objects.all().values())
                    user_employee_list = []
                    for user in user_list:
                        admin = 1
                        if user['id'] != admin:
                            user_role_list = {}
                            get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                            if get_user_role.user_role == '2':
                                role_list = RoleList.objects.get(id=get_user_role.user_role)
                                employee_profile_id = Employee_profile.objects.get(user=user['id']) 
                                user_role_list['user_role'] = get_user_role.user_role #role id
                                user_role_list['user_role_name'] = role_list.roles #role name
                                user_role_list['employeeID'] = employee_profile_id.employeeID
                                user_role_list['is_deleted'] = employee_profile_id.is_deleted
                                user_role_list['user'] = user
                                user_employee_list.append(user_role_list)
                    data = {
                        'user_employee_list':user_employee_list,
                    }
                    return JsonResponse({'status':200,'user_list':user_employee_list},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
            else:
                return Jsonresponse({'status':401,'error':'You are not Authorize to access this link'},status=401)
        else:
            return redirect("loginUserPage")
# GET ALL DATA ENDS

# ASSIGN SUBORDINATES TO THE USER (HR) STARTS
def assign_subordinates(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            user = User.objects.get(id = logged_in_user)
            if user.is_superuser:
                if request.method=='POST':
                    data = json.load(request)
                    f_data = data.get('payload')
                    employee_id_list = f_data['saved_selected_employee']
                    hr_id_list = f_data['saved_selected_Hr']
                    hr_id = hr_id_list[0]
                    print(f"employeeID  = {employee_id_list} hr_id : {hr_id}")

                    # user whoes role is hr
                    user_hr = User.objects.get(id=hr_id) 
                    user_profile_hr = Employee_profile.objects.get(user=user_hr)
                    

                    user_profile_hr.assigned_subordinate.clear()  
                    # Add selected Hr_model instances to the manager
                    for employee_id in employee_id_list:
                        #user whoes role is employee
                        user_employee = User.objects.get(id=employee_id)
                        user_profile_employee = Employee_profile.objects.get(user=user_employee)
                        user_profile_hr.assigned_subordinate.add(user_employee)
                    user_profile_hr.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
            else:
                return redirect("loginUserPage")
        else:
            return redirect("loginUserPage")
# ASSIGN SUBORDINATES TO THE USER (HR) ENDS