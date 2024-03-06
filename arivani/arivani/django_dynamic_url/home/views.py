from django.shortcuts import render,redirect
from django.urls import reverse
from auth_user.models import *
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = request.user
        user_id=user.id
        User_profile_DB = User_profile.objects.get(user=user_id)
        #Student
        #Teacher
        title_ = 'Home'
        data = {
            'title' : title_,
            'user_profile':User_profile_DB
        }
        return render(request,'home/home.html',data)
    else:
        return redirect(reverse('loginPage'))