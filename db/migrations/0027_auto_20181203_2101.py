# Generated by Django 2.1.2 on 2018-12-03 18:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0026_org_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='employee_user', to=settings.AUTH_USER_MODEL, verbose_name='Логин входа'),
        ),
    ]