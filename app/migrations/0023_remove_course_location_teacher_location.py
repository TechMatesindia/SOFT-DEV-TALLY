# Generated by Django 4.2.9 on 2024-04-21 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_course_location_teacher_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='location',
        ),
        migrations.AddField(
            model_name='teacher',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
