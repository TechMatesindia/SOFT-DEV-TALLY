# Generated by Django 4.2.9 on 2024-04-24 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_marksheetrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.student'),
        ),
    ]
