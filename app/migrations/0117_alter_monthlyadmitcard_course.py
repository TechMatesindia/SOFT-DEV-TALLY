# Generated by Django 5.0.6 on 2024-05-29 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0116_alter_yearlyadmitcard_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyadmitcard',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.course'),
        ),
    ]
