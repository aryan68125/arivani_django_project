from dataclasses import fields
from xml.dom import ValidationErr
from rest_framework import serializers
from auth_jwt.models import CustomUser

#reset password related stuff
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import EmailMessage
'''This serilaizer is responsible for registering the user'''
class RegisterCustomUserSerializers(serializers.ModelSerializer):
    #This will make sure that password 2 input field is of type password 
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = CustomUser
        fields=['id','email','name','password','password2','tc'] 
        '''
        fields=['id','email','name','password','password2','tc','is_active'] 
        If you define the fields to something like this in django 4 then it will give you error
        AssertionError: ("Creating a ModelSerializer without either the 'fields' attribute or the 'exclude' attribute has
          been deprecated since 3.3.0, and is now disallowed. Add an explicit fields = '__all__' to the CustomUserSerializers 
          serializer.",)
        '''
        #This is to tell django that the password field is write only
        extra_kwargs={
            'password':{'write_only':True}
        }
    # validating if password is same or not
    #this method will be called when we write .is_validate() function in our views
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password does not match")
        else:
          return attrs
    # here we have to create a method to create a user in our customUserModel 
    # Normally we don't have to do something like this but in this case we have to do it because we are using a custom model
    # here validated_data is coming from front end
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    class Meta:
        fields = ['otp']
    def validate(self, attrs):
        otp_f = attrs.get('otp')
        otp_saved = int(self.context.get('otp'))
        email= self.context.get('email')
        if otp_f == otp_saved:
            print(f"otp_f : {otp_f} , saved otp : {otp_saved}")
            try:
               user_local = CustomUser.objects.get(email=email)
               user_local.is_active = True
               user_local.save()
               return attrs
            except CustomUser.DoesNotExist:
                 raise serializers.ValidationErr("User does not exist")
        else:
                raise serializers.ValidationErr("otp din't match")
    
'''This serializer is responsible for user login'''
class LoginCustomUserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        model = CustomUser
        fields = ['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','name']
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=50, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields=['password','passsword2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password!=password2:
            raise serializers.ValidationErr("Password and Confirm password do not match")
        else:
            user.set_password(password)
            user.save()
            return attrs
        
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email = attrs.get('email')
        user = CustomUser.objects.get(email=email)
        if user:
            uid= urlsafe_base64_encode(force_bytes(user.id))
            print(f"encoded uid : {uid}")
            token = PasswordResetTokenGenerator().make_token(user)
            print(f"password reset token : {token}")
            link = f'http://127.0.0.1:8000/reset_password/{uid}/{token}/'
            print(f"generated link : {link}")
            #send email code 
            # send email with a messege otp
            subject = f"{email} please verify your email"
            messege = f"verify email {link}"
            recipient_list = [email]
            EMAIL_HOST_USER = settings.EMAIL_HOST_USER
            email = EmailMessage(subject,messege,EMAIL_HOST_USER,recipient_list)
            email.send()
            return attrs
        else:
            raise serializers.ValidationErr('you are not a registered user')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=50, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields=['password','passsword2']
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password!=password2:
                raise serializers.ValidationErr("Password and Confirm password do not match")
            else:
                id = smart_str(urlsafe_base64_decode(uid))
                user = CustomUser.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user,token):
                    raise serializers.ValidationError("token not valid")
                else:
                    user.set_password(password)
                    user.save()
                return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr('Token is not valid')
