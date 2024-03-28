from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from auth_user.models import *
# Create your views here.
def dashboardPage(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.id != 1:
            assigned_user_role = AssignedUserRoles.objects.get(user=user)
            user_role = assigned_user_role.user_role
            if user.is_superuser:
                data={
                    'is_superuser':1,
                    'user_role':user_role,
                }
                print(data)
                return render(request,'dashboard/dashboard.html',data)
            else:  
                if int(user_role) == 1: 
                    return redirect('employee_dashboard')
                elif int(user_role) == 2:
                    return redirect("hr_dashboard")
                elif int(user_role) == 3:
                    return redirect("manager_dashboard")
                else:
                    data={
                        'user_role':user_role,
                    }
                    return render(request,'dashboard/dashboard.html',data)
        else:
            data={
                    'is_superuser':1
                }
            print(data)
            return render(request,'dashboard/dashboard.html',data)