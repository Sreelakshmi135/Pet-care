# Generated by Django 4.2.5 on 2023-10-02 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0003_alter_userdetails_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('experience', models.IntegerField()),
                ('qualification', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phonenumber', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='UserDetails',
        ),
    ]
