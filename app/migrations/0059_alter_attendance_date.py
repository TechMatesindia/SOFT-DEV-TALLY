# Generated by Django 4.2.9 on 2024-04-29 09:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_rename_branch_id_attendance_batch_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.date.today, unique=True),
        ),
    ]
