from django.db import models
from django.contrib.auth.models import User
class RoleList(models.Model):
    roles = models.CharField(max_length=70)

class Employee_profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    employeeID = models.CharField(max_length=10)
    is_deleted = models.BooleanField(default=False)
