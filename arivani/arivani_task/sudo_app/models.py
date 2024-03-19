from django.db import models
from django.contrib.auth.models import User
class RoleList(models.Model):
    roles = models.CharField(max_length=70)

class Employee_profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    employeeID = models.CharField(max_length=10) # userID
    assigned_subordinate = models.ManyToManyField(User, symmetrical=False, related_name='assigned_subordinates', blank=True)
    is_deleted = models.BooleanField(default=False)

# #Model To keep Track of assigned employee to Hr
# class AssignedSubordinateHr(models.Model):
#     employee_id = models.IntegerField()
#     hr_id = models.IntegerField()
# #Model To keep track of assigned subbordinate to Manager
# class AssignSSubordinateToManager(models.Model):
#     manager_id = models.IntegerField()
#     hr_id = models.IntegerField()