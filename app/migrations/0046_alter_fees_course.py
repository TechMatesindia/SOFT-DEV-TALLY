# Generated by Django 4.2.9 on 2024-04-25 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_alter_fees_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.course'),
        ),
    ]
