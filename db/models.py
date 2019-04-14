from django.db import models
from django.contrib.auth.models import User

DB_VERSION = '0.10'

DB_READY = 0
DB_UPDATE = 1
DB_RECREATE = 2
DB_OFFLINE = 3
DB_ERROR = 4

SYNC_STATUS_CHOICES = (
    (DB_READY, 'БД в работе'),
    (DB_UPDATE, 'БД обновляется'),
    (DB_RECREATE, 'БД формируется'),
    (DB_OFFLINE, 'БД на обслуживании'),
    (DB_ERROR, 'Сбой БД'),
)

class Org(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True, verbose_name='Организация')
    sync_time = models.CharField(verbose_name='Время синхронизации', max_length=5, null=True, blank=True, default='')
    sync_flag = models.BooleanField(default=False, verbose_name='Запустить формирование БД', null=False, blank=True)
    sync_status = models.IntegerField(default=0, verbose_name='Состояние синхронизации', null=False, blank=True, choices = SYNC_STATUS_CHOICES)
    users = models.ManyToManyField(User, verbose_name='Логин входа', blank=True)
    db_version = models.CharField(verbose_name='Версия БД', max_length=5, null=True, blank=True, default='0.00')
    last_sync_dt = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
         return  self.name

class Org_log(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    time = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    description = models.CharField(max_length=128, null=False, blank=False, verbose_name='Сообщение')

    class Meta:
        verbose_name = 'Событие БД'
        verbose_name_plural = 'События БД'

    def __str__(self):
         return  self.description

class Lpu(models.Model):
    cust_id = models.IntegerField(db_column='Cust_ID', primary_key=True, db_index=True, null=False, blank=False)
    inn = models.CharField(db_column='Org_CustINN', max_length=16, db_index=True, null=False, blank=False, verbose_name='ИНН')
    name = models.CharField(db_column='Org_CustNm', max_length=512, db_index=True, null=False, blank=False, verbose_name='Грузополучатель')
    shortname = models.CharField(db_column='shortname', max_length=512, null=True, blank=True, verbose_name='Грузополучатель полное имя')
    addr1 = models.CharField(db_column='addr1', max_length=512, null=True, blank=True, verbose_name='Адрес1')
    addr2 = models.CharField(db_column='addr2', max_length=512, null=True, blank=True, verbose_name='Адрес2')
    regcode = models.ForeignKey('Region', db_column='regcode', null=True, verbose_name='Код региона', on_delete=models.SET_NULL)
    employee = models.ManyToManyField('Employee', related_name='employees', verbose_name='Сотрудник')

    class Meta:
        verbose_name = 'Грузополучатель'
        verbose_name_plural = 'Грузополучатели'
        managed = False
        db_table = 'db_lpu'

    def __str__(self):
         return  self.inn if self.inn else ''+' '+self.name if self.name else ''

class Region(models.Model):
    reg_id = models.IntegerField(db_column='Reg_ID', primary_key=True, db_index=True, null=False, blank=False)
    regnm = models.CharField(db_column='RegNm', max_length=50, db_index=True, null=False, blank=False, verbose_name='Название региона')
    employee = models.ManyToManyField('Employee', related_name='region_employees', verbose_name='Сотрудник')

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        managed = False
        db_table = 'db_region'

    def __str__(self):
         return  self.regnm

class Employee(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Организация')
    parent = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True, db_index=True, verbose_name='Руководитель')
    name = models.CharField(max_length=64, null=True, blank=True,verbose_name='Краткое имя')
    users = models.ManyToManyField(User, related_name='employee_user', verbose_name='Логин входа', blank=True)
    istarget = models.BooleanField(default=True, db_index=True, verbose_name='Таргет')
    lpu = models.ManyToManyField('Lpu', through=Lpu.employee.through, related_name='lpus', blank=True, verbose_name='Грузополучатели') #Lpu.employee.through
    region = models.ManyToManyField('Region', through=Region.employee.through, related_name='employee_regions', blank=True, verbose_name='Регионы')  # Region.employee.through

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
        db_table = 'db_innr'

    def __str__(self):
         return  self.name

class TradeNR(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=254, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'db_tradenr'

    def __str__(self):
         return  self.name

class Market(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, verbose_name='Организация')
    name = models.CharField(max_length=32, null=True, blank=True, verbose_name='Рынок')
    innrs = models.ManyToManyField(InNR, blank=True, through='Market_Innrs', verbose_name='МНН')
    tmnrs = models.ManyToManyField(TradeNR, blank=True, through='Market_Tmnrs', verbose_name='Торговые наименования')

    class Meta:
        verbose_name = 'Рынок'
        verbose_name_plural = 'Рынки'

    def __str__(self):
         return  self.name

class Market_Innrs(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    innr = models.ForeignKey(InNR, on_delete=models.CASCADE)
    own = models.IntegerField(default=0, null=False, blank=False)

class Market_Tmnrs(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    tradenr = models.ForeignKey(TradeNR, on_delete=models.CASCADE)
    own = models.IntegerField(default=0, null=False, blank=False)

class StatusT(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=40, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'db_statusT'

class WinnerOrg(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=512, null=False, blank=False)
    inn = models.CharField(db_column='inn', max_length=16, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'db_WinnerOrg'

class Filters(models.Model):
    user =  models.ForeignKey(User, verbose_name='Логин входа', null=True, blank=True, db_index=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256, null=False, blank=False, db_index=True)
    fields_json = models.TextField(null=False, blank=False)
    filters_json = models.TextField(null=False, blank=False)
    created = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    report_start = models.DateTimeField(null=True)
    report_finish = models.DateTimeField(null=True)
    status = models.IntegerField(null=False, default=0)

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

    def __str__(self):
         return self.name
