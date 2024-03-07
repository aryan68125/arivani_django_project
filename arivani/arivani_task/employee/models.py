from django.db import models

# Create your models here.
class Employee(models.Model):
    employeeID=models.IntegerField()
    name=models.CharField(max_length=70)
    is_deleted=models.BooleanField(default=0)
    def __str__(self):
        return self.name