# Generated by Django 2.1.2 on 2019-01-09 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_auto_20181226_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='db_version',
            field=models.CharField(blank=True, default='0.00', max_length=5, null=True, verbose_name='Версия БД'),
        ),
    ]
