# Generated by Django 4.2.9 on 2024-04-21 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_course_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_obtained', models.IntegerField()),
                ('max_marks', models.IntegerField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.batch')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.branch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subject')),
            ],
        ),
    ]
