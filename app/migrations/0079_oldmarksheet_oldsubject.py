# Generated by Django 4.2.9 on 2024-05-08 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0078_rename_location_branch_address_branch_pincode_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldMarksheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_code', models.CharField(max_length=100)),
                ('student_name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('mother_name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('mobile_number', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('branch_address', models.TextField()),
                ('branch_state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=6)),
                ('enrollment_no', models.CharField(max_length=100)),
                ('session', models.CharField(max_length=100)),
                ('registration_date', models.DateField()),
                ('course_category', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OldSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100)),
                ('theory_marks', models.IntegerField()),
                ('theory_max_marks', models.IntegerField()),
                ('practical_marks', models.IntegerField()),
                ('practical_max_marks', models.IntegerField()),
                ('total_obtained_marks', models.IntegerField()),
                ('total_max_marks', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.oldmarksheet')),
            ],
        ),
    ]
