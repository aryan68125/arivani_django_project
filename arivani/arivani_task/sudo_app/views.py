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

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            data = {
                'is_superuser':1
            }
            return render(request,'sudo_app/sudo_dashboard.html',data)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("loginUserPage")

# CREATE USERS, VERIFY EMAIL AND ASSIGN THEM ROLES ADMIN APP STARTS
def createUserPage(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            #register user page should open
            #working should be same as normal user registration process
            roles = RoleList.objects.all()
            data = {
                'is_superuser':1,
                'roles':roles
            }
            return render(request,'sudo_app/register_user.html',data)
        else:
            return redirect("dashboardPage")
    else:
        return redirect("loginUserPage")
otp_save = {}
user_save = {}
def registerUser(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
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
                                    Employee_profile.objects.create(
                                        user = user,
                                        employeeID = str(user.id) + role_db.roles,
                                        is_deleted = False
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
def registerVerifyOtpPage(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            title='Verify Otp'
            data={
                'title':title
            }
            return render(request,'auth_user/register_verify_otp.html',data)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("dashboardPage")
def resendOtp(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
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

def verifyOtpRegisterUser(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    data = json.load(request)
                    otp_data = data.get('payload')
                    if int(otp_data['otp']) == int(otp_save['otp']):
                        try:
                            user = User.objects.get(username = user_save['username'])
                            user.is_active = True
                            user.save()
                            return JsonResponse({'status':200},status=200)
                        except User.DoesNotExist:
                            return JsonResponse({'status':404,'error':'User does not exist'},status=404)
                    else:
                        return JsonResponse({'status':500,'error':"otp din't match"},status=500)
                else:
                    return JsonResponse({'status':400,'error':'bad request'},status=400)
        else:
            redirect("loginUserPage")
    else:
        return redirect("dashboardPage")
# CREATE USERS, VERIFY EMAIL AND ASSIGN THEM ROLES ADMIN APP ENDS

# UPDATE / RECYCLE BIN / DELETE USER ACCOUNTS
#get user account page
def employee_user_list_Page(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            data = {
                'is_superuser':1,
            }
            return render(request,'sudo_app/employee_user.html',data)
        else:
            return redirect("loginUserPage")
    else:
        return redirect("loginUserPage")
#get users of user role
def get_user_accounts_data(request):
    is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                user = User.objects.get(id=logged_in_user)
                if user.is_superuser:
                    user_list = list(User.objects.all().values())
                    user_employee_list = []
                    for user in user_list:
                        admin = 1
                        if user['id'] != admin:
                            user_role_list = {}
                            get_user_role = AssignedUserRoles.objects.get(user=user['id'])
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
                    return JsonResponse({'status':500,'error':'user not authorized'},status=500)
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad Request'},status=400)
#change users Status
def change_user_status(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser == True:
            is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    data = json.load(request)
                    f_data = data.get('payload')
                    user_pk = f_data['user_id']
                    user = User.objects.get(id=user_pk)
                    if user.is_active == True:
                        user.is_active = False
                        user.save()
                    else :
                        user.is_active = True
                        user.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return JsonResponse({'status':500,'error':'you are not authorized to access this link'},status=500)
    else:
        return redirect("loginUserPage")
# delete user (send user to recycle bin)
def delete_user_accounts(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
            if is_ajax:
                data = json.load(request)
                f_data = data.get('payload')
                user_id_f = f_data['user_id']
                user_instance = User.objects.get(id=user_id_f)
                user_profile_instance = Employee_profile.objects.get(user=user_instance)
                user_profile_instance.is_deleted = True
                user_profile_instance.save()
                return JsonResponse({'status':200},status=200)
        else:
            return JsonResponse({'status':500,'error':'You dont have authority to use this link'},status=500)
    else:
        return redirect("loginUserPage")
# get all deleted users
def get_all_deleted_users(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
            if is_ajax:
                users = list(User.objects.all().values())
                user_list = []
                for user in users:
                    admin = 1
                    if user['id'] != admin:
                        user_role_list = {}
                        get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                        role_list = RoleList.objects.get(id=get_user_role.user_role)
                        employee_profile_id = Employee_profile.objects.get(user=user['id'])
                        if employee_profile_id.is_deleted == True: 
                            user_role_list['user_role'] = get_user_role.user_role #role id
                            user_role_list['user_role_name'] = role_list.roles #role name
                            user_role_list['employeeID'] = employee_profile_id.employeeID
                            user_role_list['is_deleted'] = employee_profile_id.is_deleted
                            user_role_list['user'] = user
                            user_list.append(user_role_list)
                data = {
                            'user_list':user_list,
                       }
            return JsonResponse({'status':200,'user_list':user_list},status=200)
        else:
            return JsonResponse({'status':500,'error':'You dont have authority to use this link'},status=500)
    else:
        return redirect("loginUserPage")
# get all deleted users counts
def get_deleted_users_counts(request):
    is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            if request.user.is_authenticated:
                logged_in_user = request.user.id
                user = User.objects.get(id=logged_in_user)
                if user.is_superuser == True:           
                    user_instance = list(User.objects.all().values())
                    user_list = 0
                    is_deleted_user = 0
                    for user in user_instance:
                        admin = 1
                        if user['id'] != admin:
                            get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                            role_list = RoleList.objects.get(id=get_user_role.user_role)
                            employee_profile_id = Employee_profile.objects.get(user=user['id'])
                            if employee_profile_id.is_deleted == True: 
                                is_deleted_user +=1
                                user_list = is_deleted_user
                    data = {
                        user_list:user_list
                    }
                    return JsonResponse({'status':200,'user_list':user_list},status=200)
                else:
                    return JsonResponse({'status':500,'error':'You dont have authority to use this link'},status=500)
            else:
                return redirect("loginUserPage")
        else:
            return JsonResponse({'status':400,'error':'Bad Request'},status=400)
def restore_user(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
            if is_ajax:
                data = json.load(request)
                f_data = data.get('payload')
                user_instance = User.objects.get(id=f_data['user_id'])
                user_profile_instance = Employee_profile.objects.get(user=user_instance)
                user_profile_instance.is_deleted = False
                user_profile_instance.save()
                return JsonResponse({'status':200},status=200)
        else:
            return JsonResponse({'status':400,'error':'You dont have authority to use this link'},status=400)
    else:
        return redirect("loginUserPage")
def get_all_roles_list(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id = logged_in_user)
        if user.is_superuser:
            is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    roles_list = list(RoleList.objects.all().values())
                    return JsonResponse({'status':200,'context':roles_list},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad request'},status=400)
        else:
            return JsonResponse({'status':400,'error':'You dont have authority to use this link'},status=400)
    else:
        return redirect("loginUserPage")
def get_role_from_front_deleted_users(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    data = json.load(request)
                    f_data = data.get('payload')
                    role_id = f_data['selected_role']
                    if int(role_id) == -1:
                        # print("get all users")
                        users = list(User.objects.all().values())
                        user_list = []
                        for user in users:
                            admin = 1
                            if user['id'] != admin:
                                user_role_list = {}
                                get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                                role_list = RoleList.objects.get(id=get_user_role.user_role)
                                employee_profile_id = Employee_profile.objects.get(user=user['id'])
                                if employee_profile_id.is_deleted == True: 
                                    user_role_list['user_role'] = get_user_role.user_role #role id
                                    user_role_list['user_role_name'] = role_list.roles #role name
                                    user_role_list['employeeID'] = employee_profile_id.employeeID
                                    user_role_list['is_deleted'] = employee_profile_id.is_deleted
                                    user_role_list['user'] = user
                                    user_list.append(user_role_list)
                        data = {
                                    'user_list':user_list,
                               }
                        return JsonResponse({'status':200,'context':data},status=200)
                    else:
                        # print(f"get all users from role {role_id}")
                        users = list(User.objects.all().values())
                        user_list = []
                        for user in users:
                            admin = 1
                            if user['id'] != admin:
                                user_role_list = {}
                                get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                                if int(get_user_role.user_role) == int(role_id):
                                    role_list = RoleList.objects.get(id=get_user_role.user_role)
                                    employee_profile_id = Employee_profile.objects.get(user=user['id'])
                                    if employee_profile_id.is_deleted == True: 
                                        user_role_list['user_role'] = get_user_role.user_role #role id
                                        user_role_list['user_role_name'] = role_list.roles #role name
                                        user_role_list['employeeID'] = employee_profile_id.employeeID
                                        user_role_list['is_deleted'] = employee_profile_id.is_deleted
                                        user_role_list['user'] = user
                                        user_list.append(user_role_list)
                        data = {
                                    'user_list':user_list,
                               }
                        return JsonResponse({'status':200,'context':data},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return JsonResponse({'status':500,'error':'You dont have authority to use this link'},status=500)
    else:
        return redirect("loginUserPage")
def get_role_from_front_users(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
            if is_ajax:
                if request.method=='POST':
                    data = json.load(request)
                    f_data = data.get('payload')
                    role_id = f_data['selected_role']
                    if int(role_id) == -1:
                        print("get all users")
                        users = list(User.objects.all().values())
                        user_list = []
                        for user in users:
                            admin = 1
                            if user['id'] != admin:
                                user_role_list = {}
                                get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                                role_list = RoleList.objects.get(id=get_user_role.user_role)
                                employee_profile_id = Employee_profile.objects.get(user=user['id'])
                                if employee_profile_id.is_deleted == False: 
                                    user_role_list['user_role'] = get_user_role.user_role #role id
                                    user_role_list['user_role_name'] = role_list.roles #role name
                                    user_role_list['employeeID'] = employee_profile_id.employeeID
                                    user_role_list['is_deleted'] = employee_profile_id.is_deleted
                                    user_role_list['user'] = user
                                    user_list.append(user_role_list)
                        data = {
                                    'user_list':user_list,
                               }
                        return JsonResponse({'status':200,'context':data},status=200)
                    else:
                        print(f"get all users from role {role_id}")
                        users = list(User.objects.all().values())
                        user_list = []
                        for user in users:
                            admin = 1
                            if user['id'] != admin:
                                user_role_list = {}
                                get_user_role = AssignedUserRoles.objects.get(user=user['id'])
                                if int(get_user_role.user_role) == int(role_id):
                                    role_list = RoleList.objects.get(id=get_user_role.user_role)
                                    employee_profile_id = Employee_profile.objects.get(user=user['id'])
                                    if employee_profile_id.is_deleted == False: 
                                        user_role_list['user_role'] = get_user_role.user_role #role id
                                        user_role_list['user_role_name'] = role_list.roles #role name
                                        user_role_list['employeeID'] = employee_profile_id.employeeID
                                        user_role_list['is_deleted'] = employee_profile_id.is_deleted
                                        user_role_list['user'] = user
                                        user_list.append(user_role_list)
                        data = {
                                    'user_list':user_list,
                               }
                        return JsonResponse({'status':200,'context':data},status=200)
                else:
                    return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return JsonResponse({'status':500,'error':'You dont have authority to use this link'},status=500)
    else:
        return redirect("loginUserPage")
def update_user_details(request):
    is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
    if is_ajax:
        if request.user.is_authenticated:
            logged_in_user = request.user.id
            user = User.objects.get(id=logged_in_user)
            if request.method=='POST':
                if user.is_superuser:
                    data = json.load(request)
                    f_data = data.get('payload')
                    print(f_data)
                    user_id = f_data['user_id']
                    user_role_id = f_data['userrole_id']
                    username = f_data['username']
                    first_name = f_data['first_name']
                    last_name = f_data['last_name']
                    email = f_data['email']
                    selected_role = f_data['select_user_role_input_box']
                    #assign values to the user in DB
                    user = User.objects.get(id=user_id)
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.save()
                    #assigning user role
                    assigned_user_role = AssignedUserRoles.objects.get(user=user)
                    assigned_user_role.user_role = selected_role
                    assigned_user_role.save()
                    #get all roles
                    role_list = RoleList.objects.get(id=selected_role)
                    role_name = role_list.roles
                    #Regenerate userID (employeeID, hrID, managerID)
                    user_profile = Employee_profile.objects.get(user=user)
                    user_profile.employeeID = str(user.id) + role_name
                    user_profile.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':401, 'error':'You dont have authority to use this link'},status=401)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
        else:
            return redirect("loginUserPage")
# UPDATE / RECYCLE BIN / DELETE USER ACCOUNTS