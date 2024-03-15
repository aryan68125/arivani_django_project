from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
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

def createUserPage(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            #register user page should open
            #working should be same as normal user registration process
            data = {
                'is_superuser':1
            }
            return render(request,'sudo_app/register_user.html',data)
        else:
            return redirect("dashboardPage")
    else:
        return redirect("loginUserPage")
