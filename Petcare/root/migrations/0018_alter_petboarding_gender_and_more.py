# Generated by Django 4.2.5 on 2024-02-17 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0017_alter_petboarding_appointment_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petboarding',
            name='gender',
            field=models.CharField(max_length=7),
        ),
        migrations.AlterField(
            model_name='petboarding',
            name='postal_code',
            field=models.CharField(max_length=6),
        ),
    ]