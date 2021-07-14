# Generated by Django 3.2.5 on 2021-07-14 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('body_html', models.CharField(max_length=250)),
                ('body_text', models.CharField(max_length=250)),
                ('date_sent', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Correo electrónico',
                'verbose_name_plural': 'Emails',
                'ordering': ['-date_sent'],
            },
        ),
    ]
