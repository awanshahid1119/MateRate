# Generated by Django 4.2.6 on 2023-10-21 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ongoing_register_date', models.DateField()),
                ('upcoming_regsiter_date', models.DateField()),
            ],
        ),
    ]