# Generated by Django 4.2.9 on 2024-04-26 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_student_studentsession'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='batch',
            field=models.ManyToManyField(to='app.batch'),
        ),
    ]
