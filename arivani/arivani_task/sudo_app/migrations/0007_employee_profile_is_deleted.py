# Generated by Django 4.2.8 on 2024-03-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudo_app', '0006_rename_employeeid_employee_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_profile',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
