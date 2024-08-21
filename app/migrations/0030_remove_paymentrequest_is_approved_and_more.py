# Generated by Django 4.2.9 on 2024-04-21 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_paymentrequest_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentrequest',
            name='is_approved',
        ),
        migrations.RemoveField(
            model_name='paymentrequest',
            name='user',
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='name',
            field=models.CharField(default='user', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentrequest',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='email',
            field=models.EmailField(default='user@gmail.com', max_length=254),
            preserve_default=False,
        ),
    ]
