# Generated by Django 4.2.9 on 2024-05-03 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0073_rename_father_name_student_mother_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='upload_sign',
            field=models.ImageField(blank=True, null=True, upload_to='signatures/'),
        ),
    ]
