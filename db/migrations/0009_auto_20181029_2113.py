# Generated by Django 2.1.2 on 2018-10-29 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_auto_20181023_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lpu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inn', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarketMnn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mnn_id', models.IntegerField()),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Market')),
            ],
        ),
        migrations.CreateModel(
            name='MarketTM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tm_id', models.IntegerField()),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Market')),
            ],
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='hs',
            name='ATC',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='NMC',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='NMS',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='act_paid',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='bidder',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='budget_funds',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_customer_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_dosage_form',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_dosage_packing',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_end_perion',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_full_cost',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_inn_customer',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_inn_shipper',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_interl_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_kpp_shipper',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_link',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_num',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_package_count',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_package_price',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_prod_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_regum',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_shipper_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_status',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_trade_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_unit_cost',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_unit_count',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='c_unit_price',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='consignee',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='consignee_info',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='consignees_n',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='contract_term',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='count',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='delivery_conditions',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='delivery_times',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='delivery_year',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='dosage',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='dosage_form',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='dosage_packing',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='extra_funds',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='federal_area',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='fin_channel',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='goods_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='goods_spec',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='hs_id',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='info_source',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='inn_customer',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='inn_lpu',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='inn_winner',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='interl_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='lot_pos_part',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='lot_start_price',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='lotspec_id',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='market',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='municipal_level',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='order_delivery_region',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='order_finance_source',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='order_n',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='order_region',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='order_stage',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='order_start_price',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='org_type',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='package_avg_price',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='package_count',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='package_price',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='packing',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='product_cost',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='productidnx',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='request_end_date',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='shedule_link',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='tender_create_date',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='tender_holding_date',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='tender_pub_date',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='tender_renew_date',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='trade_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='units',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='volume',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='winner_name',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='winner_protocol_price',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='с_date',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='с_goods_spec',
        ),
        migrations.RemoveField(
            model_name='hs',
            name='с_package_avg_price',
        ),
        migrations.RemoveField(
            model_name='target',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='target',
            name='employee_name',
        ),
        migrations.RemoveField(
            model_name='target',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='target',
            name='inn',
        ),
        migrations.AddField(
            model_name='employee',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='db.Employee'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='market',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Org'),
        ),
        migrations.AddField(
            model_name='lpu',
            name='employee',
            field=models.ManyToManyField(to='db.Employee'),
        ),
        migrations.AddField(
            model_name='employee',
            name='org',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='db.Org'),
            preserve_default=False,
        ),
    ]
