# Generated by Django 4.2.8 on 2024-03-19 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudo_app', '0010_assignssubordinatetomanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_profile',
            name='assigned_subordinate',
            field=models.ManyToManyField(blank=True, related_name='assigned_subordinates', to='sudo_app.employee_profile'),
        ),
    ]
