from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
import random
import json
#import moldes
from auth_user.models import *
from django.contrib.auth.models import User

#resgister , login, logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

#email backend
from django.core.mail import EmailMessage
# Create your views here.
user_saver_data = {}
saved_otp = {}
def registerPage(request):
    if not request.user.is_authenticated:
        return render(request,'auth/resgisterPage.html')
    else:
        return redirect(reverse('home'))
def register(request):
    is_ajax = request.headers.get("X-Requested-With") == 'XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            data = json.load(request)
            user_data = data.get('payload')
            username = user_data['username']
            email = user_data['email']
            password = user_data['password1']
            role = user_data['role']
            user_saver_data.clear()
            user_saver_data.update({
                'username':username,
                'email':email,
                'password':password,
                'role':role,
            })
            otp = random.randint(10000,99999)
            print(f"generated otp : {otp}")
            saved_otp.clear()
            saved_otp.update({
                'otp':otp
            })
            #register your user here and make sure that is_active is set to false
            username = user_saver_data['username']
            email = user_saver_data['email']
            password = user_saver_data['password']
            role = user_saver_data['role']
            user = User.objects.create(
                    username=username,
                    email=email,
            )
            user.set_password(password)
            user.is_active=False
            user.save()
            userDB = User.objects.get(username=username)
            User_profile.objects.create(
                    user=userDB,
                    userRole=role
            )

            #send otp via email here
            # Prepare email
            email_id = user_saver_data['email']
            subject = f"{username} please verify your email"
            message = f"Verify this otp : {otp}"
            recipient_list = [email_id]

            # Create EmailMessage object and attach the Excel file
            email = EmailMessage(subject, message, 'rollex68125@gmail.com', recipient_list)

            # Send the email
            email.send()
            return JsonResponse({'status':200},status=200)
def registerOtpPage(request):
    if not request.user.is_authenticated:
        return render(request,'auth/registerOtp.html')
    else:
        return redirect(reverse('home'))
def registerOtp(request):
    is_ajax=request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            data = json.load(request)
            otp_f = data.get('payload')
            print(f"otp recieved from html : {int(otp_f['otp'])}")
            print(f"saved otp : {saved_otp['otp']}")
            print(f"saved user data:{user_saver_data}")
            if int(otp_f['otp'])==saved_otp['otp']:
                #make user active here
                user = User.objects.get(username=user_saver_data['username'])
                user.is_active=True
                user.save()
                return JsonResponse({'status':200},status=200)
            else:
                return JsonResponse({'status':400},status=400)
def loginPage(request):
    if not request.user.is_authenticated:
        return render(request,'auth/login.html')
    else:
        return redirect(reverse('home'))
def loginUser(request):
    is_ajax=request.headers.get('X-Requested-With')=="XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            data=json.load(request)
            user_login = data.get('payload')
            username_= user_login['username']
            password_= user_login['password']
            print(f"fetched username : {username_}, fetched password:{password_}")
            user  = authenticate(username=username_,password=password_)
            print(f"user from DB : {user}")
            if user:
                auth_login(request,user)
                return JsonResponse({'status':200},status=200)
            else:
                return JsonResponse({'status':404},status=404)
def logoutUser(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            auth_logout(request)
            return JsonResponse({'status':200},status=200)
def forgotPassOtpPage(request,username):
    if not request.user.is_authenticated:
        otp = random.randint(10000,99999)
        #send this otp via email
        saved_otp.clear()
        saved_otp.update({
            'otp':otp
        })
        user_saver_data.clear()
        user_saver_data.update({
            'username':username
        })
        print(user_saver_data)
        print(saved_otp)

        #send otp via email here
        # Prepare email
        user=User.objects.get(username=username)
        email_id = user.email
        subject = f"{username} please verify your email"
        message = f"Verify this otp : {otp}"
        recipient_list = [email_id]

        # Create EmailMessage object and attach the Excel file
        email = EmailMessage(subject, message, 'rollex68125@gmail.com', recipient_list)

        # Send the email
        email.send()
        return render(request,'auth/forgotPassOtp.html')        
    else:
        return redirect(reverse('home'))
def forgotPassOtpVerify(request):
    is_ajax=request.headers.get('X-Requested-With')=='XMLHttpRequest'
    if is_ajax:
        if request.method=='POST':
            data=json.load(request)
            otp_f=data.get('payload')
            otp_front = int(otp_f['otp'])
            otp_s = int(saved_otp['otp'])
            if otp_front == otp_s:
                saved_user = user_saver_data['username']
                user = User.objects.get(username=saved_user)
                if user:
                    return JsonResponse({'status':200},status=200)
                else:
                    return JsonResponse({'status':400},status=400)
            else:
                return JsonResponse({'status':404},status=404)
def changePasswordPage(request):
    if not request.user.is_authenticated:
        return render(request,'auth/ChangePassswordPage.html')
    else:
        return redirect(reverse('home'))
def changePassword(request):
    is_ajax=request.headers.get("X-Requested-With")=="XMLHttpRequest"
    if is_ajax:
        if request.method=='POST':
            data = json.load(request)
            user_passsword = data.get('payload')
            password = user_passsword['password']
            username = user_saver_data['username']
            user = User.objects.get(username=username)
            if user:
                user.set_password(password)
                user.save()
                return JsonResponse({'status':200},status=200)
            else:
                return JsonResponse({'status':404},status=404)
            