# Generated by Django 2.1.5 on 2019-05-03 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0012_filters_xls_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='FO',
            fields=[
                ('id', models.IntegerField(db_column='id', db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='name', max_length=150)),
            ],
            options={
                'db_table': 'db_fo',
                'managed': False,
            },
        ),
    ]
