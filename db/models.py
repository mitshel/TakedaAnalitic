import datetime
from django.db import models
from django.contrib.auth.models import User

class Org(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True, verbose_name='Организация')
    sync_time = models.CharField(verbose_name='Время синхронизации', max_length=5, null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
         return  self.name

class Employee(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Организация')
    parent = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True, db_index=True, verbose_name='Руководитель')
    name = models.CharField(max_length=64, null=True, blank=True,verbose_name='Краткое имя')
    users = models.ManyToManyField(User, verbose_name='Логин входа', blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
         return self.name

class InNR(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=300, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'db_inNR'

    def __str__(self):
         return  self.name

class TradeNR(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=256, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'db_tradeNR'

    def __str__(self):
         return  self.name

class Market(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
         return  self.name

class MarketMnn(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    mnn_id = models.ForeignKey(InNR, null=False, blank=False, db_index=True, on_delete=models.CASCADE)

class MarketTM(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    tm_id = models.ForeignKey(TradeNR, null=False, blank=False, db_index=True, on_delete=models.CASCADE)

class Lpu(models.Model):
    cust_id = models.IntegerField(db_column='Cust_ID', primary_key=True, db_index=True, null=False, blank=False)
    inn = models.CharField(db_column='Org_CustINN', max_length=12, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='Org_CustNm', max_length=2000, null=False, blank=False)
    employee = models.ManyToManyField(Employee)

    class Meta:
        managed = False
        db_table = 'db_lpu'

    def __str__(self):
         return  self.name

class StatusT(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=40, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'db_statusT'

class WinnerOrg(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=200, null=False, blank=False)
    inn = models.CharField(db_column='inn', max_length=12, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'db_WinnerOrg'

class Target(models.Model):
    pass

# class Hs(models.Model):
#     Tender_ID = models.IntegerField(db_column='Tender_ID', null=False)
#     ProcDt = models.DateTimeField(db_column='ProcDt', null=False)
#     TenderPrice = models.FloatField(db_column='TenderPrice', null=True)
#     StatusT_ID = models.IntegerField(db_column='StatusT_ID', null=False)
#     FormT_ID = models.IntegerField(db_column='FormT_ID', null=False)
#     cust_id = models.ForeignKey(Lpu, db_column='Cust_ID', db_index=True, null=True, on_delete=models.SET_NULL)
#     ClaimDtBeg = models.DateTimeField(db_column='ClaimDtBeg', null=True)
#     TendSYSDATE = models.DateTimeField(db_column='TendSYSDATE', null=False)
#     Lot_ID = models.IntegerField(db_column='Lot_ID', null=False)
#     PlanTYear = models.IntegerField(db_column='PlanTYear', null=True, db_index=True)
#     #InnNx = models.IntegerField(db_column='InnNx', null=True, db_index=True)
#     #TradeNx = models.IntegerField(db_column='TradeNx', null=True)
#     InnNx = models.ForeignKey(InNR, db_column='InnNx', null=True, db_index=True, on_delete=models.SET_NULL)
#     TradeNx = models.ForeignKey(TradeNR, db_column='TradeNx', null=True, db_index=True, on_delete=models.SET_NULL)
#     Order_Price = models.FloatField(db_column='Order_Price', null=True)
#     Order_Count = models.IntegerField(db_column='Order_Count', null=True)
#     Order_Sum = models.FloatField(db_column='Order_Sum', null=True)
#     Ship_FinalPrice = models.FloatField(db_column='Ship_FinalPrice', null=True)
#     Winner_ID = models.ForeignKey(WinnerOrg, db_column='Winner_ID', null=True, db_index=True, on_delete=models.SET_NULL)
#
#     market_name = models.CharField(max_length=32, db_column='market_name', null=True)
#     market_id = models.IntegerField(db_column='market_id', db_index=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'Test_CACHE_2'
        

def Hs_create(table_name):
    hs_model = type('Hs', (models.Model,), {
        '__module__': 'widgetpages.models',
        'Tender_ID' : models.IntegerField(db_column='Tender_ID', null=False),
        'ProcDt' : models.DateTimeField(db_column='ProcDt', null=False),
        'TenderPrice' : models.FloatField(db_column='TenderPrice', null=True),
        'StatusT_ID' : models.IntegerField(db_column='StatusT_ID', null=False),
        'FormT_ID' : models.IntegerField(db_column='FormT_ID', null=False),
        'cust_id' : models.ForeignKey(Lpu, db_column='Cust_ID', db_index=True, null=True, on_delete=models.SET_NULL),
        'ClaimDtBeg' : models.DateTimeField(db_column='ClaimDtBeg', null=True),
        'TendSYSDATE' : models.DateTimeField(db_column='TendSYSDATE', null=False),
        'Lot_ID' : models.IntegerField(db_column='Lot_ID', null=False),
        'PlanTYear' : models.IntegerField(db_column='PlanTYear', null=True, db_index=True),
        'InnNx' : models.ForeignKey(InNR, db_column='InnNx', null=True, db_index=True, on_delete=models.SET_NULL),
        'TradeNx' : models.ForeignKey(TradeNR, db_column='TradeNx', null=True, db_index=True, on_delete=models.SET_NULL),
        'Order_Price' : models.FloatField(db_column='Order_Price', null=True),
        'Order_Count' : models.IntegerField(db_column='Order_Count', null=True),
        'Order_Sum' : models.FloatField(db_column='Order_Sum', null=True),
        'Ship_FinalPrice' : models.FloatField(db_column='Ship_FinalPrice', null=True),
        'Winner_ID' : models.ForeignKey(WinnerOrg, db_column='Winner_ID', null=True, db_index=True, on_delete=models.SET_NULL),
    
        'market_name' : models.CharField(max_length=32, db_column='market_name', null=True),
        'market_id' : models.IntegerField(db_column='market_id', db_index=True, null=True)
    })

    hs_model._meta.managed  = False
    hs_model._meta.db_table = table_name

    return hs_model


