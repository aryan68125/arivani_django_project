# Generated by Django 4.2.8 on 2024-03-16 06:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sudo_app', '0005_alter_employeeid_employeeid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmployeeID',
            new_name='Employee_profile',
        ),
    ]
