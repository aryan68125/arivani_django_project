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

from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.

def registerUserPage(request):
    if not request.user.is_authenticated:
        title="Register Page"
        data={
            'title':title
        }
        return render(request,'auth_user/register_page.html')
    else:
        return redirect("dashboard_home")
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
                    username = user_data['username']
                    email = user_data['email']
                    password1 = user_data['password1']
                    password2 = user_data['password2']
                    if password1 == password2:
                            user = User.objects.create(
                                username = username,
                                email = email,
                            )
                            user.set_password(password1)
                            user.is_active=False
                            user.save()

                            # generate a random otp
                            user_save.clear()
                            user_save['email'] = email
                            user_save['username'] = username
                            otp_save.clear()
                            otp_save['otp'] = random.randint(1000,9999)
                            print(f"otp_save : {otp_save}")
                            #send otp via email
                            '''.... your code to send email here ....'''
                            # Prepare email
                            # email_addr = email
                            # subject = f"{username} please verify your otp"
                            # message = "Your otp"
                            # recipient_list = [email_addr]
                
                
                            # # Create EmailMessage object and attach the Excel file
                            # email = EmailMessage(subject, message, 'rollex68125@gmail.com', recipient_list)
                            # email.attach_file(excel_file_path)
                
                
                            # # Send the email
                            # email.send()

                            return JsonResponse({'status':200},status=200)
                    else:
                        return JsonResponse({'status':500,'error':"Password don't match"})
                except IntegrityError as e:
                    return JsonResponse({'status':500,'error':'username taken'},status=500)
            else:
                return JsonResponse({'status':400,'error':'bad request'},status=400)
    else:
        return redirect("dashboard_home")

def registerVerifyOtpPage(request):
    if not request.user.is_authenticated:
        title='Verify Otp'
        data={
            'title':title
        }
        return render(request,'auth_user/register_verify_otp.html',data)
    else:
        return redirect("dashboard_home")

def resendOtp(request):
    if not request.user.is_authenticated:
        is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
        if is_ajax:
            if request.method=='POST':
                otp_save.clear()
                otp_save['otp'] = random.randint(1000,9999)
                print(otp_save)
                #send otp via email
                return JsonResponse({'status':200},status=200)
            else:
                return JsonResponse({'status':400,'error':'Bad Request'},status=400)
    else:
        return redirect("dashboard_home")
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
        return redirect("dashboard_home")

def loginUserPage(request):
    if not request.user.is_authenticated:
        title="Login Page"
        data={
            'title':title
        }
        return render(request,'auth_user/loginUser.html',data)
    else:
        return redirect("dashboard_home")

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
                    login_user(request,user)
                    return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':404,'error':'Bad User credentials'},status=404)
            else:
                return JsonResponse({'status':400,'error':'Bad request'},status=400)
    return redirect("dashboard_home")

def forgotPasswordPageUsername(request):
    if not request.user.is_authenticated:
        return render(request,"auth_user/forgotPasswordPage.html")
    else:
        return redirect("dashboard_home")
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
                    return JsonResponse({'status':200},status=200)
                except User.DoesNotExist:
                    return JsonResponse({'status':404,'error':'User not found'},status=404)
            else:
                return JsonResponse({'status':400,'error':'Bad request'},status=400)

    else:
        return redirect("dashboard_home")
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
def resetPasswordPage(request):
    if not request.user.is_authenticated:
        return render(request,"auth_user/resetPasswordPage.html")
    else:
        return redirect("dashboard_home")
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
        return redirect("dashboard_home")
def logoutUser(request):
    if request.user.is_authenticated:
        logout_user(request)
        return redirect("loginUserPage")
    else:
        return redirect("loginUserPage")