# Generated by Django 4.2.8 on 2024-03-19 14:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sudo_app', '0012_delete_assignedsubordinatehr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_profile',
            name='assigned_subordinate',
            field=models.ManyToManyField(blank=True, related_name='assigned_subordinates', to=settings.AUTH_USER_MODEL),
        ),
    ]
