# Generated by Django 4.2.9 on 2024-04-29 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0065_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='branchstaticid',
            field=models.CharField(default='null', max_length=20),
            preserve_default=False,
        ),
    ]
