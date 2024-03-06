# Generated by Django 4.2.8 on 2024-01-31 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_date_created_student_date_updated_and_more'),
        ('marks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarksSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_settings_ID', models.IntegerField(default=1, verbose_name='Marks settings ID')),
                ('passing_percentage', models.FloatField(default=40, verbose_name='Passing Percentage')),
                ('passing_marks_per_subject', models.FloatField(default=40, verbose_name='Passing marks per subject')),
                ('Total_marks_per_subject', models.FloatField(default=100, verbose_name='Total per subject')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='marks',
            name='Total_marks_per_subject',
        ),
        migrations.AddField(
            model_name='marks',
            name='Student_name',
            field=models.CharField(default='student', max_length=70, verbose_name="Student's Name"),
        ),
        migrations.AddField(
            model_name='marks',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='marks',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='marks',
            name='Student_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='student.student'),
        ),
        migrations.AlterField(
            model_name='marks',
            name='Total_marks_obtained',
            field=models.FloatField(verbose_name='Total marks obtained'),
        ),
        migrations.AlterField(
            model_name='marks',
            name='marks_ID',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='marks ID'),
        ),
        migrations.AlterField(
            model_name='marks',
            name='pass_fail',
            field=models.BooleanField(verbose_name='Pass status'),
        ),
    ]
