# Generated by Django 4.2.8 on 2024-03-19 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sudo_app', '0008_assignedsubordinate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AssignedSubordinate',
            new_name='AssignedSubordinateHr',
        ),
    ]
