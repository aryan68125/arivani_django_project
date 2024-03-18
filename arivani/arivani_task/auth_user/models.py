from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class AssignedUserRoles(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_role = models.CharField(max_length=70) #It stores role's id