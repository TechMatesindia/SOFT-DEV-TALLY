# Generated by Django 4.2.9 on 2024-04-21 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_remove_course_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='branch',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='app.branch'),
            preserve_default=False,
        ),
    ]
