# Generated by Django 5.0.6 on 2024-05-27 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0106_remove_monthlyadmitcard_receipt_path_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearlyAdmitCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=10)),
                ('course_type', models.CharField(max_length=20)),
                ('course', models.CharField(max_length=100)),
                ('exam_date', models.DateField()),
                ('paper1_start_time', models.TimeField()),
                ('paper1_end_time', models.TimeField()),
                ('paper1_total_hours', models.IntegerField()),
                ('paper2_start_time', models.TimeField()),
                ('paper2_end_time', models.TimeField()),
                ('paper2_total_hours', models.IntegerField()),
                ('exam_centre', models.CharField(max_length=255)),
            ],
        ),
    ]
