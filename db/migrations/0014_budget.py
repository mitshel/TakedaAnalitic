# Generated by Django 2.1.5 on 2019-05-03 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0013_fo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.CharField(db_column='id', db_index=True, max_length=1, primary_key=True, serialize=False)),
                ('version', models.IntegerField(db_column='version', db_index=True)),
                ('name', models.CharField(db_column='name', max_length=200)),
            ],
            options={
                'db_table': 'db_budgets',
                'managed': False,
            },
        ),
    ]