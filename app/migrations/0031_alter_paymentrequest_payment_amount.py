# Generated by Django 4.2.9 on 2024-04-22 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_remove_paymentrequest_is_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
