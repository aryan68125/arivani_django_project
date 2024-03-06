from django.db import models

# # Create your models here.
class Hr_model(models.Model):
    HrID = models.IntegerField()
    name=models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.name