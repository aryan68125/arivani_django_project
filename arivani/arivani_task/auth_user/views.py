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

def registerUserPage(request):
    if not request.user.is_authenticated:
        title="Register Page"
        data={
            'title':title
        }
        return render(request,'auth_user/register_page.html')
    else:
        return redirect("dashboardPage")
otp_save = {}
user_save = {}
def registerUser(request):
    if not request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
        if is_ajax:
            if request.method=='POST':
                try:
                    data = json.load(request)
                    user_data = data.get('payload')
                    print(user_data)
                    username = user_data['username']
                    email = user_data['email']
                    first_name = user_data['first_name']
                    last_name=user_data['last_name']
                    password1 = user_data['password1']
                    password2 = user_data['password2']
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
        return redirect("dashboardPage")

def registerVerifyOtpPage(request):
    if not request.user.is_authenticated:
        title='Verify Otp'
        data={
            'title':title
        }
        return render(request,'auth_user/register_verify_otp.html',data)
    else:
        return redirect("dashboardPage")

def resendOtp(request):
    if not request.user.is_authenticated:
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
        return redirect("dashboardPage")
def verifyOtpRegisterUser(request):
    if not request.user.is_authenticated:
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
        return redirect("dashboardPage")

def loginUserPage(request):
    if not request.user.is_authenticated:
        title="Login Page"
        data={
            'title':title
        }
        return render(request,'auth_user/loginUser.html',data)
    else:
        return redirect("dashboardPage")

def loginUser(request):
    if not request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
        if is_ajax:
            if request.method=='POST':
                data = json.load(request)
                login_data = data.get('payload')
                username = login_data['username']
                password = login_data['password']
                user = authenticate(username=username,password=password)
                if user:
                    if user.is_superuser == True:
                        login_user(request,user)
                        return JsonResponse({'status':200,'is_superuser':1},status=200)
                    else:
                        login_user(request,user)
                        return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':404,'error':'Bad User credentials'},status=404)
            else:
                return JsonResponse({'status':400,'error':'Bad request'},status=400)
    return redirect("dashboardPage")

def forgotPasswordPageUsername(request):
    if not request.user.is_authenticated:
        return render(request,"auth_user/forgotPasswordPage.html")
    else:
        return redirect("dashboardPage")
def sendVerificationUrl(request):
    if not request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
        if is_ajax:
            if request.method=='POST':
                data = json.load(request)
                user_data = data.get('payload')
                try:
                    user = User.objects.get(username = user_data['username'])
                    uid= urlsafe_base64_encode(force_bytes(user.id))
                    print(f"encoded uid : {uid}")
                    token = PasswordResetTokenGenerator().make_token(user)
                    print(f"password reset token : {token}")
                    link = f'http://127.0.0.1:8000/reset_password/{uid}/{token}/'
                    print(f"generated link : {link}")

                    #send otp via email here
                    # Prepare email
                    lint_to_send = link
                    email_id = user.email
                    username = user.username
                    subject = f"{username} please reset your password"
                    message = f"Reset PAssword by clicking this link : {lint_to_send}"
                    recipient_list = [email_id]

                    # Create EmailMessage object and attach the Excel file
                    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)

                    # Send the email
                    email.send()
                    
                    return JsonResponse({'status':200},status=200)
                except User.DoesNotExist:
                    return JsonResponse({'status':404,'error':'User not found'},status=404)
            else:
                return JsonResponse({'status':400,'error':'Bad request'},status=400)

    else:
        return redirect("dashboardPage")
uid_save = {}
token_save = {}
def resetPassword(request,uid,token):
    if not request.user.is_authenticated:
        uid_save.clear()
        uid_save['uid'] = uid
        token_save.clear()
        token_save['token'] = token
        print(f"uid_saved : {uid_save['uid']}, token_saved : {token_save['token']}")
        return redirect("resetPasswordPage")
    else:
        return redirect("dashboardPage")
def resetPasswordPage(request):
    if not request.user.is_authenticated:
        return render(request,"auth_user/resetPasswordPage.html")
    else:
        return redirect("dashboardPage")
def resetPassword_pass(request):
    if not request.user.is_authenticated:
        is_ajax=request.headers.get("X-Requested-With")=='XMLHttpRequest'
        if is_ajax:
            if request.method=='POST':
                data = json.load(request)
                user_data = data.get('payload')
                print(f"pass1 : {user_data['password1']}, pass2 : {user_data['password2']}")
                if user_data['password1'] == user_data['password2']:
                    id = smart_str(urlsafe_base64_decode(uid_save['uid']))
                    user = User.objects.get(id=id)
                    if not PasswordResetTokenGenerator().check_token(user,token_save['token']):
                        return JsonResponse({'status':500,'error':'token mismatch'},status=500)
                    else:
                        user.set_password(user_data['password1'])
                        user.save()
                    return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':500,'error':"password don't match"},status=500)
            else:
                return JsonResponse({'status':400,'error':'badrequest'},status=400)
    else:
        return redirect("dashboardPage")
def logoutUser(request):
    if request.user.is_authenticated:
        logout_user(request)
        return redirect("loginUserPage")
    else:
        return redirect("loginUserPage")


# This function should be accesible after the user is logged in starts
def ChangePasswordPage(request):
    if request.user.is_authenticated:
        return render(request,'auth_user/changeUserPass.html')
    else:
        return redirect("loginUserPage")

def ChangePassword(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            username = request.user.username
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            print(f"password1 : {password1} , password2 : {password2}")
            if password1 and password2:
                if password1 == password2:
                    # messages.error(request, 'Passwords matched')
                    if is_valid_password(password1):
                        # messages.success(request, 'Password is valid')
                        logged_in_user = request.user.id
                        try:
                            user = User.objects.get(id=logged_in_user)
                            user.set_password(password1)
                            user.save()

                            #after the password is changed log the user back in 
                            login_user_data = authenticate(username=username,password=password1)
                            if login_user:
                                login_user(request,login_user_data)
                                return redirect(reverse("dashboardPage"))
                            else:
                                return JsonResponse({'status':404,'error':'Bad User credentials'},status=404)
                            return redirect(reverse("ChangePasswordPage"))
                        except User.DoesNotExist:
                            messages.success(request, 'User does not exist')
                            return render(request,'auth_user/changeUserPass.html')
                    else:
                        messages.error(request, 'Password must be a combination of numbers, letters and @ symbol')
                        messages.error(request, 'Password must be of length >= 6')
                    return render(request,'auth_user/changeUserPass.html')
                else:
                    messages.success(request, 'Password do not match')
                    return render(request,'auth_user/changeUserPass.html')
            else:
                messages.success(request, 'Password must not be empty')
                return render(request,'auth_user/changeUserPass.html')
    else:
        return redirect("loginUserPage")
# This function should be accesible after the user is logged in ends