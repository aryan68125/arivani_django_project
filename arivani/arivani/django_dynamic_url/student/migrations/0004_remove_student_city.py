# Generated by Django 4.2.8 on 2024-02-01 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='city',
        ),
    ]
