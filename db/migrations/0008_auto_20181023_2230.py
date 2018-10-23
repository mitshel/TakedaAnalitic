# Generated by Django 2.1.2 on 2018-10-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_auto_20181021_1348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='target',
            name='employee_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.RemoveField(
            model_name='target',
            name='employee',
        ),
        migrations.AddField(
            model_name='target',
            name='employee',
            field=models.ManyToManyField(to='db.Employee'),
        ),
    ]
