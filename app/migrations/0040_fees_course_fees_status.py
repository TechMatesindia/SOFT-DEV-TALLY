# Generated by Django 4.2.9 on 2024-04-24 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_alter_fees_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='fees',
            name='course',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='app.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fees',
            name='status',
            field=models.CharField(default='null', max_length=20),
            preserve_default=False,
        ),
    ]
