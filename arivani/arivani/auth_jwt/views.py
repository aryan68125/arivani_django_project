import random
from django.http import JsonResponse
from django.shortcuts import render
from auth_jwt.serializer import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
import random
from django.core.mail import EmailMessage
from django.conf import settings
from auth_jwt.models import CustomUser
from auth_jwt.renderers import UserRenderer
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from rest_framework.permissions import IsAuthenticated
# generate token manually
from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
user={}
otp = {}
class UserRegistrationview(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = RegisterCustomUserSerializers(data=request.data)
        if serializer.is_valid():
            user.clear()
            user.update({'email':request.data['email']})
            print(f"saved user email : {user}")
            otp.clear()
            otp.update({'otp':random.randint(1000,9999)})
            print(f"saved otp:{otp}")
            serializer.save()

            # send email with a messege otp
            subject = f"{user['email']} please verify your email"
            messege = f"verify OTP {str(otp['otp'])}"
            recipient_list = [user['email']]
            EMAIL_HOST_USER = settings.EMAIL_HOST_USER
            email = EmailMessage(subject,messege,EMAIL_HOST_USER,recipient_list)
            email.send()
            return Response({'status':'register user success'},status=201)
        else:
            print(serializer.errors)
            return Response({'status':serializer.errors},status=400)

class VerifyEmail(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request):
        otp_saved = int(otp.get('otp'))
        email_saved = user.get('email')
        try:
            if otp:
                serializer = VerifyEmailSerializer(data=request.data,context={'otp' : otp_saved, 'email' : email_saved})
                if serializer.is_valid():
                    return Response({'status':'Email verification success!!'},status=200)
                else:
                    return Response({'errors',serializer.errors},status=400)
            else:
                return Response({'errors':'no saved otp'},status=500)
        except:
            return Response({'errors':'something went wrong'},status=500)
        
class UserLoginView(APIView):
    def post(self,request):
        serializer = LoginCustomUserSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user_local = authenticate(email=email,password=password)
            if user_local:
                token= get_tokens_for_user(user_local)
                return Response({'status':'Login success','token':token},status=200)
            else:
                return Response({'errors':{'non_field_errors':['email or password is not valid']}},status=404)
        else:
            return Response({'status':serializer.errors},status=500)
        
class USerProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = UserProfileSerializer(request.user)
        return Response({'data':serializer.data},status=200)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            return Response({'status':'password changed success!!'},status=200)
        else:
            return Response({'errors':serializer.errors},status=400)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'status':'Password reset link send to your email'},status=200)
        else:
            return Response({'errors',serializer.errors},status=400)
        
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token):
        serializer = UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid():
            return Response({'status':'Password reset success!!'},status=200)
        else:
            return Response({'errors':serializer.errors},status=400)