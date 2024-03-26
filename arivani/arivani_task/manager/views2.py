from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
# from hr_app.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from employee.models import *

#make employee json serializable in function "employees_under_hr_list"
from django.core.serializers import serialize
from auth_user.models import *
from sudo_app.models import *
from django.db import IntegrityError

#custom user password validation related import
import re

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user
from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.db import IntegrityError
import json
import random

#Email related import
from django.conf import settings
#email backend
from django.core.mail import EmailMessage

#django messeges related imports
from django.contrib import messages

# Custom password validation for change password
def is_valid_password(password):
    # Check if password has minimum 6 characters
    if len(password) < 6:
        return False
    
    # Check if password contains at least one letter, one number, and one "@" character
    if not re.search(r'[a-zA-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[@]', password):
        return False
    
    # If all conditions are met, return True
    return True
# Custom password validation for change password

#MANAGER PROFILE PAGE RELATED FUNCTIONS STARTS
def manager_home(request):
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
            return render(request,'manager/manager_profile_page.html',data)
    else:
        return redirect("loginUserPage")
def manager_app_update_manager_profile(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            currently_logged_in_user = User.objects.get(id=logged_in_user)
            user_profile = AssignedUserRoles.objects.get(user=currently_logged_in_user)
            user_role = int(user_profile.user_role)
            if user_role==3:
                if request.method=='POST':
                    data = json.load(request)
                    f_data = data.get('payload')
                    userID = f_data['hrID']
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
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
            else:
                return redirect("loginUserPage")
        else:
            return redirect("loginUserPage")
#MANAGER PROFILE PAGE RELATED FUNCTIONS ENDS

# ADD HR RELATED FUNCTIONS STARTS
def manager_add_hr_Page(request):
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

        role_list_dropdown = list(RoleList.objects.all().filter(id=2).values())
        if user.is_superuser:
            data = {
                'is_superuser':1,
                'role_name':role_name,
                'name':name,
            }
            return render(request,'manager/manager_add_hr_page.html',data)
        else:
            data = {
                'user_role':user_role,
                'role_name':role_name,
                'name':name,
                'roles':role_list_dropdown,
            }
            return render(request,'manager/manager_add_hr_page.html',data)
    else:
        return redirect("loginUserPage")
# CREATE USERS, VERIFY EMAIL AND RE-SEND-OTP STARTS
otp_save = {}
user_save = {}
def register_hr_manager(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        user_profile = AssignedUserRoles.objects.get(user=user)
        user_role = int(user_profile.user_role)
        if user_role == 3:
            is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    try:
                        data = json.load(request)
                        user_data = data.get('payload')
                        username = user_data['username']
                        email = user_data['email']
                        first_name = user_data['first_name']
                        last_name=user_data['last_name']
                        password1 = user_data['password1']
                        password2 = user_data['password2']
                        selected_role = user_data['role_select']
                        try:
                            is_email_taken = User.objects.get(email=email)
                            taken_email = is_email_taken.email
                            return JsonResponse({'status':500,'error':f'Email "{taken_email}" is already taken'},status=500)
                        except User.DoesNotExist:
                            if password1 == password2:
                                if is_valid_password(password1):
                                    #employee users created
                                    user = User.objects.create(
                                        username = username,
                                        email = email,
                                        first_name=first_name,
                                        last_name=last_name
                                    )
                                    user.set_password(password1)
                                    user.is_active=False
                                    user.save()
                                    # currently logged in hr
                                    user_hr = User.objects.get(id=logged_in_user)
                                    #save the employees in assigned_subordinate under currently logged in user 
                                    user_hr_profile = Employee_profile.objects.get(user=user_hr)
                                    user_hr_profile.assigned_subordinate.add(user)

                                    #save the role in Db related to this particular user that we just registered
                                    role_db = RoleList.objects.get(id=selected_role)
                                    AssignedUserRoles.objects.create(
                                        user=user,
                                        user_role = role_db.id
                                    )

                                    #generate IDs based on roles employeeID, hrID, managerID
                                    #set user's is_deleted to false by default
                                    current_logged_in_user_instance = User.objects.get(id=logged_in_user)
                                    Employee_profile.objects.create(
                                        user = user,
                                        employeeID = str(user.id) + role_db.roles,
                                        is_deleted = False,
                                        created_by = current_logged_in_user_instance,
                                    )

                                    # save user email and username for later use
                                    user_save.clear()
                                    user_save['email'] = email
                                    user_save['username'] = username
                                    # generate a random otp and save it for later use
                                    otp_save.clear()
                                    otp_save['otp'] = random.randint(1000,9999)
                                    print(f"otp_save : {otp_save}")
                                    
                                    #send otp via email here
                                    # Prepare email
                                    otp = otp_save['otp']
                                    email_id = user_save['email']
                                    username = user_save['username']
                                    subject = f"{username} please verify your email"
                                    message = f"Verify this otp : {otp}"
                                    recipient_list = [email_id]
    
                                    # Create EmailMessage object and attach the Excel file
                                    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    
                                # Send the email
                                    email.send()
        
                                    return JsonResponse({'status':200},status=200) 
                                else:
                                    return JsonResponse({'status':500,'error':"Password must be a combination of letters, numbers and '@' also it should have characters greater than 5"})
                            else:
                                return JsonResponse({'status':500,'error':"Password don't match"})
                    except IntegrityError as e:
                        return JsonResponse({'status':500,'error':'username taken'},status=500)
                else:
                    return JsonResponse({'status':400,'error':'bad request'},status=400)
        else:
            return JsonResponse({'status':404,'error':'You are not authorized to access this url'},status=404)
    else:
        return redirect("dashboardPage")
def registerVerifyOtpPage_manager(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        user_profile = AssignedUserRoles.objects.get(user=user)
        user_role = int(user_profile.user_role)
        if user_role == 3:
            title='Verify Otp'
            data={
                'title':title
            }
            return render(request,'manager/manager_verifyOtpRegister.html',data)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("dashboardPage")
def resendOtp_manager(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        user_profile = AssignedUserRoles.objects.get(user=user)
        user_role = int(user_profile.user_role)
        if user_role == 3:
            is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
            if is_ajax:
                if request.method=='POST':
                    otp_save.clear()
                    otp_save['otp'] = random.randint(1000,9999)
                    print(otp_save)
    
                    #send otp via email here
                    # Prepare email
                    otp = otp_save['otp']
                    email_id = user_save['email']
                    username = user_save['username']
                    subject = f"{username} please verify your email"
                    message = f"Verify this otp : {otp}"
                    recipient_list = [email_id]
    
                    # Create EmailMessage object and attach the Excel file
                    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    
                    # Send the email
                    email.send()
                    
                    return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            redirect("loginUserPage")
    else:
        return redirect("dashboardPage")

def verifyOtpRegisterUser_manager(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        user_profile = AssignedUserRoles.objects.get(user=user)
        user_role = int(user_profile.user_role)
        if user_role == 3:
            is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    data = json.load(request)
                    otp_data = data.get('payload')
                    if int(otp_data['otp']) == int(otp_save['otp']):
                        try:
                            user = User.objects.get(username = user_save['username'])
                            print(user)
                            user.is_active = True
                            user.save()
                            return JsonResponse({'status':200},status=200)
                        except User.DoesNotExist:
                            return JsonResponse({'status':404,'error':'User does not exist'},status=404)
                    else:
                        return JsonResponse({'status':500,'error':"otp didn't match"},status=500)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("dashboardPage")

# CREATE USERS, VERIFY EMAIL AND RE-SEND-OTP ENDS
# ADD HR RELATED FUNCTIONS ENDS

# MANAGER UPDATE HR RELATED FUNTIONS STARTS
def manager_app_update_hr_Page(request):
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

        role_list_dropdown = list(RoleList.objects.all().filter(id=1).values())
        if user.is_superuser:
            data = {
                'is_superuser':1,
                'role_name':role_name,
                'name':name,
            }
            return render(request,'hr_app/hr_add_employee.html',data)
        else:
            data = {
                'user_role':user_role,
                'role_name':role_name,
                'name':name,
                'roles':role_list_dropdown,
            }
            return render(request,'manager/manager_update_hr.html',data)
    else:
        return redirect("loginUserPage")
#send all hr to be able to display in in the front-end
def manager_app_update_get_all_hr(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            if request.method=='POST':
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id=logged_in_user)
                user_profile = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(user_profile.user_role)
                if user_role == 3: # if manager
                    users = list(User.objects.all().values())
                    employee_list = []
                    for user in users:
                        if user['id'] != 1:
                            user_role_assigned = AssignedUserRoles.objects.get(user = user['id'])
                            user_role = int(user_role_assigned.user_role)
                            user_data = {}
                            if user_role == 2: # hr list
                                user_profile = Employee_profile.objects.get(user=user['id'])
                                role_list = RoleList.objects.get(id=user_role)
                                user_role_name = role_list.roles
                                user_data['user']=user
                                user_data['userID'] = user_profile.employeeID
                                user_data['is_deleted'] = user_profile.is_deleted
                                user_data['created_by'] = user_profile.created_by.username
                                user_data['user_role_name'] = user_role_name
                                user_data['user_role_id'] = user_role
                                #get all subbordinates assigned to the manager
                                subordinates = list(user_profile.assigned_subordinate.all().values())
                                user_data['subordinates'] = subordinates
                                if user_profile.created_by == currently_logged_in_user and user_profile.is_deleted == False:
                                    employee_list.append(user_data) # hr list
                    # hr list dictionary                
                    data = {
                        'employee_list':employee_list
                    }
                    return JsonResponse({'status':200,'context':data},status=200)
                else:
                    return JsonResponse({'status':401,'error':'Only Users with the role of hr can access this api'},status=401)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
# set hr is_active status
def manager_app_set_hr_is_active(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            if request.method=='POST':
                logged_in_user = request.user.id
                current_logged_in_user = User.objects.get(id = logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=current_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_pk']
                    user = User.objects.get(id=user_pk)
                    if user.is_active == True:
                        user.is_active = False
                    else:
                        user.is_active = True
                    user.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return Jsonresponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
# soft delete hr 
def manager_app_soft_delete_hr(request):
    is_ajax = request.headers.get('X-Requested-With')=="XMLHttpRequest"
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            current_logged_in_user = User.objects.get(id = logged_in_user)
            ass_user_role = AssignedUserRoles.objects.get(user=current_logged_in_user)
            user_role = int(ass_user_role.user_role)
            if request.method == 'POST':
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_pk']
                    user = User.objects.get(id=user_pk)
                    user.is_active = False
                    user.save()
                    user_profile = Employee_profile.objects.get(user=user)
                    user_profile.is_deleted = True
                    user_profile.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return Jsonresponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
# Get all deleted userd from recycle bin
def manager_app_gel_all_deleted_users(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            if request.method=='POST':
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id = logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                        users = list(User.objects.all().values())
                        employee_list = []
                        for user in users:
                            if user['id'] != 1:
                                user_role_assigned = AssignedUserRoles.objects.get(user = user['id'])
                                user_role = int(user_role_assigned.user_role)
                                user_data = {}
                                if user_role == 2:
                                    user_profile = Employee_profile.objects.get(user=user['id'])
                                    role_list = RoleList.objects.get(id=user_role)
                                    user_role_name = role_list.roles
                                    user_data['user']=user
                                    user_data['userID'] = user_profile.employeeID
                                    user_data['is_deleted'] = user_profile.is_deleted
                                    user_data['created_by'] = user_profile.created_by.username
                                    user_data['user_role_name'] = user_role_name
                                    user_data['user_role_id'] = user_role
                                    #get all subbordinates assigned to the manager
                                    subordinates = list(user_profile.assigned_subordinate.all().values())
                                    user_data['subordinates'] = subordinates
                                    if user_profile.created_by == currently_logged_in_user and user_profile.is_deleted == True:
                                        employee_list.append(user_data)
                        data = {
                            'employee_list':employee_list
                        }
                        return JsonResponse({'status':200,'context':data},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return Jsonresponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return rediretct("loginUserPage")
#restore user from recycle bin
def manager_app_restore_user(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id = logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_id']
                    user = User.objects.get(id=user_pk)
                    user.is_active = True
                    user.save()
                    user_profile = Employee_profile.objects.get(user = user)
                    if user_profile.is_deleted == True:
                        user_profile.is_deleted = False
                    user_profile.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad Request'},status=400)

# gat all the users counts who are in the recycle bin
def manager_app_get_all_deleted_user_count(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id=logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    deleted_users_count = Employee_profile.objects.filter(is_deleted=True).count()
                    data = {
                        'deleted_users_count':deleted_users_count
                    }
                    return JsonResponse({'status':200,'context':data},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad Request'},status=400)
#update hr function 
def manager_app_update_hr_record(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id = logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_pk']
                    user_role_id = f_data['user_role_id']
                    username = f_data['username']
                    first_name = f_data['first_name']
                    last_name = f_data['last_name']
                    email = f_data['email']
                    user = User.objects.get(id=user_pk)
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad Request'},status=400)
#perpanently delete hr
def manager_app_delete_user_permanently(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id=logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_id']
                    #delete employee from many to many relation from under this logged in hr
                    user_hr_profile = Employee_profile.objects.get(user=currently_logged_in_user)
                    #delete employee permanently
                    user = User.objects.get(id=user_pk)
                    #remove the user to eleted from many tomany relation before deleting
                    user_hr_profile.assigned_subordinate.remove(user) 
                    user.delete()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad request'},status=400)
# MANAGER UPDATE HR RELATED FUNTIONS ENDS

#ADD EMPLOYEE OPERATIONS STARTS
def manager_add_employee_Page(request):
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

        role_list_dropdown = list(RoleList.objects.all().filter(id=1).values())
        if user.is_superuser:
            data = {
                'is_superuser':1,
                'role_name':role_name,
                'name':name,
            }
            return render(request,'manager/manager_add_employee_page.html',data)
        else:
            data = {
                'user_role':user_role,
                'role_name':role_name,
                'name':name,
                'roles':role_list_dropdown,
            }
            return render(request,'manager/manager_add_employee_page.html',data)
    else:
        return redirect("loginUserPage")
# ADD EMPLOYEE
otp_save = {}
user_save = {}
def register_employee_manager(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        user_profile = AssignedUserRoles.objects.get(user=user)
        user_role = int(user_profile.user_role)
        if user_role == 3:
            is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    try:
                        data = json.load(request)
                        user_data = data.get('payload')
                        username = user_data['username']
                        email = user_data['email']
                        first_name = user_data['first_name']
                        last_name=user_data['last_name']
                        password1 = user_data['password1']
                        password2 = user_data['password2']
                        selected_role = user_data['role_select']
                        try:
                            is_email_taken = User.objects.get(email=email)
                            taken_email = is_email_taken.email
                            return JsonResponse({'status':500,'error':f'Email "{taken_email}" is already taken'},status=500)
                        except User.DoesNotExist:
                            if password1 == password2:
                                if is_valid_password(password1):
                                    #employee users created
                                    user = User.objects.create(
                                        username = username,
                                        email = email,
                                        first_name=first_name,
                                        last_name=last_name
                                    )
                                    user.set_password(password1)
                                    user.is_active=False
                                    user.save()
                                   
                                    #save the role in Db related to this particular user that we just registered
                                    role_db = RoleList.objects.get(id=selected_role)
                                    AssignedUserRoles.objects.create(
                                        user=user,
                                        user_role = role_db.id
                                    )

                                    #generate IDs based on roles employeeID, hrID, managerID
                                    #set user's is_deleted to false by default
                                    current_logged_in_user_instance = User.objects.get(id=logged_in_user)
                                    Employee_profile.objects.create(
                                        user = user,
                                        employeeID = str(user.id) + role_db.roles,
                                        is_deleted = False,
                                        created_by = current_logged_in_user_instance,
                                    )

                                    # save user email and username for later use
                                    user_save.clear()
                                    user_save['email'] = email
                                    user_save['username'] = username
                                    # generate a random otp and save it for later use
                                    otp_save.clear()
                                    otp_save['otp'] = random.randint(1000,9999)
                                    print(f"otp_save : {otp_save}")
                                    
                                    #send otp via email here
                                    # Prepare email
                                    otp = otp_save['otp']
                                    email_id = user_save['email']
                                    username = user_save['username']
                                    subject = f"{username} please verify your email"
                                    message = f"Verify this otp : {otp}"
                                    recipient_list = [email_id]
    
                                    # Create EmailMessage object and attach the Excel file
                                    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    
                                # Send the email
                                    email.send()
        
                                    return JsonResponse({'status':200},status=200) 
                                else:
                                    return JsonResponse({'status':500,'error':"Password must be a combination of letters, numbers and '@' also it should have characters greater than 5"})
                            else:
                                return JsonResponse({'status':500,'error':"Password don't match"})
                    except IntegrityError as e:
                        return JsonResponse({'status':500,'error':'username taken'},status=500)
                else:
                    return JsonResponse({'status':400,'error':'bad request'},status=400)
        else:
            return JsonResponse({'status':404,'error':'You are not authorized to access this url'},status=404)
    else:
        return redirect("dashboardPage")
def registerVerifyOtpPage_employee_manager(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        user_profile = AssignedUserRoles.objects.get(user=user)
        user_role = int(user_profile.user_role)
        if user_role == 3:
            title='Verify Otp'
            data={
                'title':title
            }
            return render(request,'manager/manager_verifyOtpRegister.html',data)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("dashboardPage")
def resendOtp_employee_manager(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        user_profile = AssignedUserRoles.objects.get(user=user)
        user_role = int(user_profile.user_role)
        if user_role == 3:
            is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
            if is_ajax:
                if request.method=='POST':
                    otp_save.clear()
                    otp_save['otp'] = random.randint(1000,9999)
                    print(otp_save)
    
                    #send otp via email here
                    # Prepare email
                    otp = otp_save['otp']
                    email_id = user_save['email']
                    username = user_save['username']
                    subject = f"{username} please verify your email"
                    message = f"Verify this otp : {otp}"
                    recipient_list = [email_id]
    
                    # Create EmailMessage object and attach the Excel file
                    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    
                    # Send the email
                    email.send()
                    
                    return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            redirect("loginUserPage")
    else:
        return redirect("dashboardPage")

def verifyOtpRegisterUser_employee_manager(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        user_profile = AssignedUserRoles.objects.get(user=user)
        user_role = int(user_profile.user_role)
        if user_role == 3:
            is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    data = json.load(request)
                    otp_data = data.get('payload')
                    if int(otp_data['otp']) == int(otp_save['otp']):
                        try:
                            user = User.objects.get(username = user_save['username'])
                            print(user)
                            user.is_active = True
                            user.save()
                            return JsonResponse({'status':200},status=200)
                        except User.DoesNotExist:
                            return JsonResponse({'status':404,'error':'User does not exist'},status=404)
                    else:
                        return JsonResponse({'status':500,'error':"otp didn't match"},status=500)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("dashboardPage")
#ADD EMPLOYEE OPERATIONS ENDS

# UPDATE EMPLOYEE CRUD OPERATIONS STARTS
def manager_app_update_employee_Page(request):
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

        role_list_dropdown = list(RoleList.objects.all().filter(id=1).values())
        if user.is_superuser:
            data = {
                'is_superuser':1,
                'role_name':role_name,
                'name':name,
            }
            return render(request,'manager/manager_update_employee.html',data)
        else:
            data = {
                'user_role':user_role,
                'role_name':role_name,
                'name':name,
                'roles':role_list_dropdown,
            }
            return render(request,'manager/manager_update_employee.html',data)
    else:
        return redirect("loginUserPage")
#send all employee to be able to display in in the front-end
def manager_app_update_get_all_employee(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            if request.method=='POST':
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id=logged_in_user)
                user_profile = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(user_profile.user_role)
                if user_role == 3: # if manager
                    users = list(User.objects.all().values())
                    employee_list = []
                    for user in users:
                        if user['id'] != 1:
                            user_role_assigned = AssignedUserRoles.objects.get(user = user['id'])
                            user_role = int(user_role_assigned.user_role)
                            user_data = {}
                            if user_role == 1: # hr list
                                user_profile = Employee_profile.objects.get(user=user['id'])
                                role_list = RoleList.objects.get(id=user_role)
                                user_role_name = role_list.roles
                                user_data['user']=user
                                user_data['userID'] = user_profile.employeeID
                                user_data['is_deleted'] = user_profile.is_deleted
                                user_data['created_by'] = user_profile.created_by.username
                                user_data['user_role_name'] = user_role_name
                                user_data['user_role_id'] = user_role
                                #get all subbordinates assigned to the manager
                                subordinates = list(user_profile.assigned_subordinate.all().values())
                                user_data['subordinates'] = subordinates
                                if user_profile.created_by == currently_logged_in_user and user_profile.is_deleted == False:
                                    employee_list.append(user_data) # hr list
                    # hr list dictionary                
                    data = {
                        'employee_list':employee_list
                    }
                    return JsonResponse({'status':200,'context':data},status=200)
                else:
                    return JsonResponse({'status':401,'error':'Only Users with the role of hr can access this api'},status=401)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
# set employee is_active status
def manager_app_set_employee_is_active(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            if request.method=='POST':
                logged_in_user = request.user.id
                current_logged_in_user = User.objects.get(id = logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=current_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_pk']
                    user = User.objects.get(id=user_pk)
                    if user.is_active == True:
                        user.is_active = False
                    else:
                        user.is_active = True
                    user.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return Jsonresponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
# soft delete employee 
def manager_app_soft_delete_employee(request):
    is_ajax = request.headers.get('X-Requested-With')=="XMLHttpRequest"
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            current_logged_in_user = User.objects.get(id = logged_in_user)
            ass_user_role = AssignedUserRoles.objects.get(user=current_logged_in_user)
            user_role = int(ass_user_role.user_role)
            if request.method == 'POST':
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_pk']
                    user = User.objects.get(id=user_pk)
                    user.is_active = False
                    user.save()
                    user_profile = Employee_profile.objects.get(user=user)
                    user_profile.is_deleted = True
                    user_profile.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return Jsonresponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
# Get all deleted employee from recycle bin
def manager_app_gel_all_deleted_employee(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            if request.method=='POST':
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id = logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                        users = list(User.objects.all().values())
                        employee_list = []
                        for user in users:
                            if user['id'] != 1:
                                user_role_assigned = AssignedUserRoles.objects.get(user = user['id'])
                                user_role = int(user_role_assigned.user_role)
                                user_data = {}
                                if user_role == 1:
                                    user_profile = Employee_profile.objects.get(user=user['id'])
                                    role_list = RoleList.objects.get(id=user_role)
                                    user_role_name = role_list.roles
                                    user_data['user']=user
                                    user_data['userID'] = user_profile.employeeID
                                    user_data['is_deleted'] = user_profile.is_deleted
                                    user_data['created_by'] = user_profile.created_by.username
                                    user_data['user_role_name'] = user_role_name
                                    user_data['user_role_id'] = user_role
                                    #get all subbordinates assigned to the manager
                                    subordinates = list(user_profile.assigned_subordinate.all().values())
                                    user_data['subordinates'] = subordinates
                                    if user_profile.created_by == currently_logged_in_user and user_profile.is_deleted == True:
                                        employee_list.append(user_data)
                        data = {
                            'employee_list':employee_list
                        }
                        return JsonResponse({'status':200,'context':data},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return Jsonresponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return rediretct("loginUserPage")
#restore employee from recycle bin
def manager_app_restore_employee(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id = logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_id']
                    user = User.objects.get(id=user_pk)
                    user.is_active = True
                    user.save()
                    user_profile = Employee_profile.objects.get(user = user)
                    if user_profile.is_deleted == True:
                        user_profile.is_deleted = False
                    user_profile.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad Request'},status=400)

# gat all the employee counts who are in the recycle bin
def manager_app_get_all_deleted_employee_count(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id=logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    deleted_users_count = Employee_profile.objects.filter(is_deleted=True).count()
                    data = {
                        'deleted_users_count':deleted_users_count
                    }
                    return JsonResponse({'status':200,'context':data},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad Request'},status=400)
#update employee function 
def manager_app_update_employee_record(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id = logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_pk']
                    user_role_id = f_data['user_role_id']
                    username = f_data['username']
                    first_name = f_data['first_name']
                    last_name = f_data['last_name']
                    email = f_data['email']
                    user = User.objects.get(id=user_pk)
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad Request'},status=400)
#perpanently delete employee
def manager_app_delete_employee_permanently(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                currently_logged_in_user = User.objects.get(id=logged_in_user)
                ass_user_role = AssignedUserRoles.objects.get(user=currently_logged_in_user)
                user_role = int(ass_user_role.user_role)
                if user_role == 3:
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_id']
                    #delete employee from many to many relation from under this logged in hr
                    user_hr_profile = Employee_profile.objects.get(user=currently_logged_in_user)
                    #delete employee permanently
                    user = User.objects.get(id=user_pk)
                    #remove the user to eleted from many tomany relation before deleting
                    user_hr_profile.assigned_subordinate.remove(user) 
                    user.delete()
                    return JsonResponse({'status':200},status=200)
                else:
                    return redirect("loginUserPage")
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad request'},status=400)
# UPDATE EMPLOYEE CRUD OPERATIONS ENDS

# ASSIGN SUBORDINATES TO THE USER (HR) STARTS
def manager_ass_employee_to_hr_page(request):
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
            return render(request,'manager/manager_ass_employee_hr.html',data)
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
            return render(request,'manager/manager_ass_employee_hr.html',data)
    else:
        return redirect("loginUserPage")

# GET ALL DATA STARTS
#get all employees
def get_all_employees_manager_app(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            currently_logged_in_user = User.objects.get(id=logged_in_user)
            user_profile = AssignedUserRoles.objects.get(user=currently_logged_in_user)
            user_role = int(user_profile.user_role)
            if user_role == 3:
                if request.method=='POST':
                    user_list = list(User.objects.all().values())
                    user_employee_list = []
                    for user in user_list:
                        admin = 1
                        if user['id'] != admin:
                            user_role_list = {}
                            get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                            if get_user_role.user_role == '1':
                                user_profile = Employee_profile.objects.get(user=user['id'])
                                role_list = RoleList.objects.get(id=get_user_role.user_role)
                                employee_profile_id = Employee_profile.objects.get(user=user['id']) 
                                user_role_list['user_role'] = get_user_role.user_role #role id
                                user_role_list['user_role_name'] = role_list.roles #role name
                                user_role_list['employeeID'] = employee_profile_id.employeeID
                                user_role_list['is_deleted'] = employee_profile_id.is_deleted
                                user_role_list['user'] = user
                                if user_profile.created_by == currently_logged_in_user and user_profile.is_deleted == False:
                                    user_employee_list.append(user_role_list)
                    data = {
                        'user_employee_list':user_employee_list,
                    }
                    return JsonResponse({'status':200,'user_list':user_employee_list},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
            else:
                return JsonResponse({'status':401,'error':'You are not Authorize to access this link'},status=401)
        else:
            return redirect("loginUserPage")
#get all hr's
def get_all_hr_manager_app(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            currently_logged_in_user = User.objects.get(id=logged_in_user)
            user_profile = AssignedUserRoles.objects.get(user=currently_logged_in_user)
            user_role = int(user_profile.user_role)
            if user_role == 3:
                if request.method=='POST':
                    user_list = list(User.objects.all().values())
                    user_employee_list = []
                    for user in user_list:
                        admin = 1
                        if user['id'] != admin:
                            user_role_list = {}
                            get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                            if get_user_role.user_role == '2':
                                user_profile = Employee_profile.objects.get(user=user['id'])
                                role_list = RoleList.objects.get(id=get_user_role.user_role)
                                employee_profile_id = Employee_profile.objects.get(user=user['id']) 
                                user_role_list['user_role'] = get_user_role.user_role #role id
                                user_role_list['user_role_name'] = role_list.roles #role name
                                user_role_list['employeeID'] = employee_profile_id.employeeID
                                user_role_list['is_deleted'] = employee_profile_id.is_deleted
                                user_role_list['user'] = user
                                if user_profile.created_by == currently_logged_in_user and user_profile.is_deleted == False:
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

def assign_subordinates_manager_app(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            user_profile = AssignedUserRoles.objects.get(user=user)
            user_role = int(user_profile.user_role)
            if user_role == 3:
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
#get all assign subordinates to hr
def get_all_assigned_subordinates_manager_app(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            currently_logged_in_user = User.objects.get(id=logged_in_user)
            user_profile = AssignedUserRoles.objects.get(user=currently_logged_in_user)
            user_role = int(user_profile.user_role)
            if user_role == 3:
                if request.method=='POST':
                    data = json.load(request)
                    f_data = data.get('payload')
                    hrID = f_data['hrID']
                    hr_pk = int(re.search(r'\d+', hrID).group())
                    # print(f"selected hr id : {hr_pk}")
                    users = User.objects.all().filter(pk=hr_pk).values()
                    user_employee_list = []
                    for user in users:
                        admin = 1
                        if user['id'] != admin:
                            user_role_list = {}
                            get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                            if get_user_role.user_role == '2': # hr
                                user_profile = Employee_profile.objects.get(user=user['id'])
                                role_list = RoleList.objects.get(id=get_user_role.user_role)
                                hr_profile_id = Employee_profile.objects.get(user=user['id']) 
                                user_role_list['user_role'] = get_user_role.user_role #role id
                                user_role_list['user_role_name'] = role_list.roles #role name
                                user_role_list['hrID'] = hr_profile_id.employeeID
                                user_role_list['is_deleted'] = hr_profile_id.is_deleted
                                user_role_list['user'] = user
                                #get all subbordinates assigned to the manager
                                subordinates = list(hr_profile_id.assigned_subordinate.all().values())
                                user_role_list['subordinates'] = subordinates
                                if user_profile.created_by == currently_logged_in_user and user_profile.is_deleted == False:
                                    user_employee_list.append(user_role_list)
                    return JsonResponse({'status':200,'context':user_employee_list},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
            else:
                return redirect("loginUserPage")
        else:
            return redirect("loginUserPage")
# ASSIGN SUBORDINATES TO THE USER (HR) ENDS
