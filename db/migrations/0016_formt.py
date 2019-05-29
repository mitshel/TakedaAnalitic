# Generated by Django 2.1.5 on 2019-05-03 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0015_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormT',
            fields=[
                ('id', models.IntegerField(db_column='id', db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=50)),
            ],
            options={
                'db_table': 'db_formt',
                'managed': False,
            },
        ),
    ]