# Generated by Django 5.0.6 on 2024-05-28 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0113_remove_marksheetrequest_marks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oldmarksheet',
            old_name='pdf_url',
            new_name='certificate_pdf_url',
        ),
        migrations.AddField(
            model_name='oldmarksheet',
            name='marksheet_pdf_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
