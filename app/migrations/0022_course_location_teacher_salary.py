# Generated by Django 4.2.9 on 2024-04-21 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_teacher_password_alter_teacher_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='salary',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
