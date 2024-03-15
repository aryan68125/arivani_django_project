from django.urls import path
from sudo_app.views import *
urlpatterns = [
    path('',dashboard,name="dashboard_admin"),
    path('createUserPage/',createUserPage,name="createUserPage"),
]
