# Generated by Django 5.2.1 on 2025-06-22 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_enrollment_email_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='short_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
