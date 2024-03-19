"""
URL configuration for arivani_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('auth_user.urls')),
    path('hr_app/',include('hr_app.urls')),
    path('employee/',include('employee.urls')),
    path('manager/',include('manager.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('sudo_admin/',include('sudo_app.urls')),
    path('sudo_admin/hr/',include('sudo_app.urls_hr')),
    path('sudo_admin/manager/',include('sudo_app.urls_manager')),
]
