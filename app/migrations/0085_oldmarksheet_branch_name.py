# Generated by Django 4.2.9 on 2024-05-10 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0084_alter_oldmarksheet_enrollment_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldmarksheet',
            name='branch_name',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
    ]
