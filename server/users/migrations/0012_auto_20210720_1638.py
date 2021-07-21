# Generated by Django 3.2.5 on 2021-07-20 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_baseuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección de domicilio'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='cdi',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Cédula de identidad'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='email',
            field=models.EmailField(max_length=30, unique=True, verbose_name='Correo electrónico'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='first_name',
            field=models.CharField(max_length=20, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='last_name',
            field=models.CharField(max_length=20, verbose_name='Apellidos'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Número telefónico'),
        ),
    ]
