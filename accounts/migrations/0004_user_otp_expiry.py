# Generated by Django 5.1.4 on 2025-01-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_expiry',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
