from django.db import models
from django.contrib.auth.models import User

#django signals related imports
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone
# Create your models here.
class Employee(models.Model):
    employeeID=models.IntegerField()
    name=models.CharField(max_length=70)
    is_deleted=models.BooleanField(default=0)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name="created_employee",null=True)
    updated_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name="updated_employee",null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="deleted_employee",null=True)
    restored_at = models.DateTimeField(null=True)
    restored_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="restored_employee",null=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.name
#signal that will update the updated_at field when user updates a record in Employee model
# @receiver(pre_save, sender=Employee)
# def update_employee_updated_at(sender, instance, **kwargs):
#     instance.updated_at = timezone.now()
