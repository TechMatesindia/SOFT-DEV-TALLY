# Generated by Django 5.0.6 on 2024-05-27 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0107_yearlyadmitcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='YearlyAdmitCard',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
