# Generated by Django 3.2.5 on 2021-07-20 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_documenttype_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDocumentTypeRol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('document_type_rol_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.documenttyperol')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
