# Generated by Django 2.1.2 on 2018-10-30 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0011_auto_20181030_1223'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='hs',
            table='ComplexRpt_CACHE',
        ),
        migrations.AlterModelTable(
            name='lpu',
            table='lpu',
        ),
    ]
