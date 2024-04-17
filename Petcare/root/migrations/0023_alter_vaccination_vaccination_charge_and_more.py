# Generated by Django 4.2.5 on 2024-02-28 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0022_vaccination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccination',
            name='vaccination_charge',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='vaccination_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='vaccination_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
