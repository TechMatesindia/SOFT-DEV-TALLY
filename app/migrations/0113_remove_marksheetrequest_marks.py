# Generated by Django 5.0.6 on 2024-05-27 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0112_marksheetrequest_issuedate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marksheetrequest',
            name='marks',
        ),
    ]
