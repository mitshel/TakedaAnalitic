# Generated by Django 2.1.2 on 2018-11-13 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0011_employee_notarget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='notarget',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Не показывать как Таргет'),
        ),
    ]