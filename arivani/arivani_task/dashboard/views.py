from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
def dashboardPage(request):
    if request.user.is_authenticated:
        logged_in_user = request.user.id
        user = User.objects.get(id=logged_in_user)
        if user.is_superuser:
            data={
                'is_superuser':1,
            }
            return render(request,'dashboard/dashboard.html',data)
        else:   
            return render(request,'dashboard/dashboard.html')