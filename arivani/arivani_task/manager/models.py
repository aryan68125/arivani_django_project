from django.db import models
from django.contrib.auth.models import User
from hr_app.models import *
# Create your models here.
class ManagerModel(models.Model):
    managerID = models.IntegerField()
    name=models.CharField(max_length=50)
    is_deleted=models.BooleanField(default=0)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name="created_manager",null=True)
    updated_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name="updated_manager",null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="deleted_manager",null=True)
    restored_at = models.DateTimeField(null=True)
    restored_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="restored_manager",null=True)
    status = models.BooleanField(default=True)
    hr_under_manager = models.ManyToManyField(Hr_model)
    def __str__(self):
        return self.name