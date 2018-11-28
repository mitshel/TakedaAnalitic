# Generated by Django 2.1.2 on 2018-11-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0020_delete_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='sync_flag',
            field=models.BooleanField(blank=True, default=False, verbose_name='Запустить формирования БД'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='lpu',
            field=models.ManyToManyField(blank=True, related_name='lpus', to='db.Lpu', verbose_name='Грузополучатели'),
        ),
    ]