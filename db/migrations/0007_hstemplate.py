# Generated by Django 2.1.2 on 2018-11-10 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_auto_20181110_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='HsTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tender_ID', models.IntegerField(db_column='Tender_ID')),
                ('ProcDt', models.DateTimeField(db_column='ProcDt')),
                ('TenderPrice', models.FloatField(db_column='TenderPrice', null=True)),
                ('StatusT_ID', models.IntegerField(db_column='StatusT_ID')),
                ('FormT_ID', models.IntegerField(db_column='FormT_ID')),
                ('ClaimDtBeg', models.DateTimeField(db_column='ClaimDtBeg', null=True)),
                ('TendSYSDATE', models.DateTimeField(db_column='TendSYSDATE')),
                ('Lot_ID', models.IntegerField(db_column='Lot_ID')),
                ('PlanTYear', models.IntegerField(db_column='PlanTYear', db_index=True, null=True)),
                ('Order_Price', models.FloatField(db_column='Order_Price', null=True)),
                ('Order_Count', models.IntegerField(db_column='Order_Count', null=True)),
                ('Order_Sum', models.FloatField(db_column='Order_Sum', null=True)),
                ('Ship_FinalPrice', models.FloatField(db_column='Ship_FinalPrice', null=True)),
                ('market_name', models.CharField(db_column='market_name', max_length=32, null=True)),
                ('market_id', models.IntegerField(db_column='market_id', db_index=True, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
    ]