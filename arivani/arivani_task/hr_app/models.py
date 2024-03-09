from django.db import models
from django.contrib.auth.models import User
# # Create your models here.
class Hr_model(models.Model):
    HrID = models.IntegerField()
    name=models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=0)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name="created_hr",null=True)
    updated_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name="updated_hr",null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="deleted_hr",null=True)
    restored_at = models.DateTimeField(null=True)
    restored_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="restored_hr",null=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.name