# Generated by Django 4.2.8 on 2024-03-11 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='managermodel',
            old_name='ManagerID',
            new_name='managerID',
        ),
    ]
