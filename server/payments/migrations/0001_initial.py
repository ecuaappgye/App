# Generated by Django 3.2.5 on 2021-07-26 17:51

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Retention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_total', models.FloatField(validators=[django.core.validators.MinValueValidator(0.9), django.core.validators.MaxValueValidator(100)])),
                ('service_supervisor', models.FloatField(validators=[django.core.validators.MinValueValidator(0.9), django.core.validators.MaxValueValidator(100)])),
                ('service_app', models.FloatField(validators=[django.core.validators.MinValueValidator(0.9), django.core.validators.MaxValueValidator(100)])),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
