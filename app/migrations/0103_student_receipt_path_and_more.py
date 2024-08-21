# Generated by Django 5.0.6 on 2024-05-26 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0102_oldmarksheet_pdf_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='receipt_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='oldmarksheet',
            name='profile_picture',
            field=models.ImageField(default='default_profile_picture.jpg', upload_to='old_profile_pictures/'),
        ),
    ]
