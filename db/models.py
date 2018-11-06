from django.db import models

class IdList(models.Model):
    item = models.IntegerField(db_column='Item', null=False, blank=False)
    class Meta:
        managed = False

class Org(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)

class Employee(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, db_index=True)
    name = models.CharField(max_length=64, null=True, blank=True)

class Market(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, null=True, blank=True)

class MarketMnn(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    mnn_id = models.IntegerField(null=False, blank=False, db_index=True)

class MarketTM(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    tm_id = models.IntegerField(null=False, blank=False, db_index=True)

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

class InNR(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=64, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'db_inNR'

class TradeNR(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=64, null=False, blank=False)

    class Meta:
        managed = False
        db_table = 'db_tradeNR'

class WinnerOrg(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True, db_index=True, null=False, blank=False)
    name = models.CharField(db_column='name', max_length=200, null=False, blank=False)
    inn = models.CharField(db_column='inn', max_length=12, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'db_WinnerOrg'

class Target(models.Model):
    pass

class Hs(models.Model):
    Tender_ID = models.IntegerField(db_column='Tender_ID', null=False)
    ProcDt = models.DateTimeField(db_column='ProcDt', null=False)
    TenderPrice = models.FloatField(db_column='TenderPrice', null=True)
    StatusT_ID = models.IntegerField(db_column='StatusT_ID', null=False)
    FormT_ID = models.IntegerField(db_column='FormT_ID', null=False)
    cust_id = models.ForeignKey(Lpu, db_column='Cust_ID', db_index=True, null=True, on_delete=models.SET_NULL)
    ClaimDtBeg = models.DateTimeField(db_column='ClaimDtBeg', null=True)
    TendSYSDATE = models.DateTimeField(db_column='TendSYSDATE', null=False)
    Lot_ID = models.IntegerField(db_column='Lot_ID', null=False)
    PlanTYear = models.IntegerField(db_column='PlanTYear', null=True, db_index=True)
    #InnNx = models.IntegerField(db_column='InnNx', null=True, db_index=True)
    #TradeNx = models.IntegerField(db_column='TradeNx', null=True)
    InnNx = models.ForeignKey(InNR, db_column='InnNx', null=True, db_index=True, on_delete=models.SET_NULL)
    TradeNx = models.ForeignKey(TradeNR, db_column='TradeNx', null=True, db_index=True, on_delete=models.SET_NULL)
    Order_Price = models.FloatField(db_column='Order_Price', null=True)
    Order_Count = models.IntegerField(db_column='Order_Count', null=True)
    Order_Sum = models.FloatField(db_column='Order_Sum', null=True)
    Ship_FinalPrice = models.FloatField(db_column='Ship_FinalPrice', null=True)
    Winner_ID = models.ForeignKey(WinnerOrg, db_column='Winner_ID', null=True, db_index=True, on_delete=models.SET_NULL)

    market_name = models.CharField(max_length=32, db_column='market_name', null=True)
    market_id = models.IntegerField(db_column='market_id', db_index=True, null=True)

    class Meta:
        managed = False
        db_table = 'Test_CACHE_1'

# class Target(models.Model):
#     inn = models.IntegerField(db_index=True, null=False, blank=False)
#     entity = models.CharField(max_length=128, null=False, blank=False)
#     employee_name = models.CharField(max_length=128, null=True, blank=True)
#     employee = models.ManyToManyField(Employee, null=True, blank=True)
#
#     def __str__(self):
#          return  self.entity

# class Hs(models.Model):
#     hs_id = models.PositiveIntegerField()
#     market = models.CharField(max_length=19, null=False, blank=False, db_index=True)  # Рынок
#     tender_pub_date = models.DateTimeField(null=False, blank=False, db_index=True)  # Дата публикации тендера
#     order_n = models.CharField(max_length=31, null=False, blank=False, db_index=True)  # Заказ №
#     order_stage = models.CharField(max_length=30, null=False, blank=False, db_index=True)  # Этап размещения заказа
#     federal_area = models.CharField(max_length=24, null=False, blank=False, db_index=True)  # Федеральный округ
#     fin_channel = models.CharField(max_length=30, null=True, blank=True, db_index=True)  # Канал финансирования
#     order_region = models.CharField(max_length=28, null=False, blank=False, db_index=True)  # Регион размещения заказа
#     customer_name = models.CharField(max_length=259)  # Заказчик
#     municipal_level = models.CharField(max_length=34, null=True, blank=True, db_index=True)  # Муниципальный уровень
#     inn_customer = models.IntegerField()  # Заказчик ИНН
#     org_type = models.CharField(max_length=108, null=True, blank=True, db_index=True)  # Тип организации
#     bidder = models.CharField(max_length=259)  # Организатор торгов
#     request_end_date = models.DateTimeField(null=False, blank=False, db_index=True)  # Окончание подачи заявок
#     tender_holding_date = models.DateTimeField(null=False, blank=False, db_index=True)  # Дата проведения тендера
#     order_finance_source = models.CharField(max_length=71, null=False, blank=False,db_index=True)  # Источник финансирования заказа
#     order_start_price = models.FloatField(null=False, blank=False)  # Начальная цена заказа
#     shedule_link = models.CharField(max_length=170, null=True, blank=True)  # Ссылка на план-график
#     tender_create_date = models.DateTimeField(null=False, blank=False, db_index=True)  # Дата создания тендера
#     tender_renew_date = models.DateTimeField(null=False, blank=False, db_index=True)  # Дата обновления тендера
#     lot_start_price = models.FloatField(null=False, blank=False)  # Начальная цена Лота
#     winner_protocol_price = models.FloatField(null=True, blank=True)  # Цена победителя по протоколу
#     order_delivery_region = models.CharField(max_length=40, null=False, blank=False,db_index=True)  # Регион поставки заказа
#     consignee = models.CharField(max_length=259, )  # Грузополучатель
#     consignee_info = models.CharField(max_length=125, null=False, blank=False)  # Сведения о грузополучателе
#     delivery_conditions = models.CharField(max_length=1010, null=False,blank=False)  # Место, условия и сроки (периоды) поставки товара
#     delivery_times = models.CharField(max_length=29, null=False, blank=False, db_index=True)  # Сроки поставки
#     contract_term = models.DateTimeField(null=True, blank=True, db_index=True)  # Срок действия контракта
#     delivery_year = models.PositiveIntegerField(null=False, blank=False, db_index=True)  # Год поставки
#     winner_name = models.CharField(max_length=124, null=True, blank=True, db_index=True)  # Победитель тендера
#     consignees_n = models.PositiveIntegerField(null=True, blank=True, )  # Количество грузополучателей
#     inn_winner = models.CharField(max_length=28,null=True, blank=True, db_index=True)  # ИНН Победителя
#     trade_name = models.CharField(max_length=50, null=False, blank=False, db_index=True)  # Торговое наименование
#     interl_name = models.CharField(max_length=65, null=False, blank=False,db_index=True)  # Международное непатентованное наименование
#     goods_name = models.CharField(max_length=293, null=True, blank=True,db_index=True)  # Наименование товара (по документации к заказу)
#     goods_spec = models.CharField(max_length=1010, null=True, blank=True)  # Характеристика товара (по документации к заказу)
#     product_type = models.CharField(max_length=58, null=False, blank=False, db_index=True)  # Тип продукции
#     dosage_form = models.CharField(max_length=63, null=True, blank=True, db_index=True)  # Лекарственная форма
#     dosage = models.CharField(max_length=23, null=True, blank=True)  # Дозировка
#     packing = models.PositiveIntegerField(null=True, blank=True)  # Фасовка
#     volume = models.CharField(max_length=25, null=True, blank=True)  # Объем
#     NMC = models.FloatField(null=False, blank=False)  # НМЦ за ед. (руб)
#     ATC = models.CharField(max_length=65, null=True, blank=True)  # АТС
#     dosage_packing = models.CharField(max_length=44, null=True, blank=True)  # Дозировка + Фасовка
#     count = models.PositiveIntegerField(null=False, blank=False)  # Количество ед
#     NMS = models.FloatField(null=False, blank=False)  # НМ сумма за ед. (руб)
#     product_cost = models.FloatField(null=False, blank=False)  # Стоимость продукта
#     package_count = models.PositiveIntegerField(null=False, blank=False)  # Количество упаковок
#     package_price = models.FloatField(null=False, blank=False)  # Цена за упаковку
#     package_avg_price = models.FloatField(null=True, blank=True)  # Средняя цена за упак.
#     info_source = models.CharField(max_length=144, null=True, blank=True)  # Источник информации
#     lot_pos_part = models.FloatField(null=True, blank=True)  # Доля позиции в лоте (руб.)
#     lotspec_id = models.PositiveIntegerField(null=False, blank=False)  # Lotspec_id
#     с_package_avg_price = models.FloatField(null=True, blank=True)  # Средняя цена за упак.(контракт)
#     с_date = models.DateTimeField(null=True, blank=True, db_index=True)  # Дата заключения контракта
#     units = models.CharField(max_length=16, null=True, blank=True, db_index=True)  # Единица измерения
#     с_goods_spec = models.CharField(max_length=1010, null=True, blank=True)  # Характеристика товара (контракт)
#     c_dosage_form = models.CharField(max_length=63, null=True, blank=True)  # Лекарственная форма (контракт)
#     c_dosage_packing = models.CharField(max_length=44, null=True, blank=True)  # Дозировка + Фасовка (контракт)
#     c_end_perion = models.CharField(max_length=23, null=True, blank=True)  # Срок исполнения контракта
#     c_num = models.CharField(max_length=236, null=True, blank=True)  # № Контракта
#     c_unit_price = models.FloatField(null=True, blank=True)  # Цена за ед. по контракту (руб)
#     c_unit_count = models.PositiveIntegerField(null=True, blank=True)  # Количество единиц по контракту
#     c_full_cost = models.FloatField(null=True, blank=True)  # Общая сумма контракта (руб)
#     c_regum = models.CharField(max_length=35, null=True, blank=True)  # № контракта (регистр.)
#     c_link = models.CharField(max_length=107, null=True, blank=True)  # Ссылка на контракт
#     c_unit_cost = models.FloatField(null=True, blank=True)  # Сумма за ед. по контракту (руб)
#     c_shipper_name = models.CharField(max_length=143, null=True, blank=True)  # Наименование поставщика (исполнителя, подрядчика) по контракту
#     c_customer_name = models.CharField(max_length=174, null=True, blank=True)  # Заказчик по контракту
#     c_package_price = models.FloatField(null=True, blank=True)  # Цена за упаковку (контракт)
#     c_package_count = models.PositiveIntegerField(null=True, blank=True)  # Количество упаковок (контракт)
#     c_status = models.CharField(max_length=31, null=True, blank=True, db_index=True)  # Статус контракта
#     c_inn_shipper = models.CharField(max_length=26,null=True, blank=True, db_index=True)  # ИНН поставщика (исполнителя, подрядчика) по контракту
#     c_kpp_shipper = models.CharField(max_length=34, null=True,blank=True)  # КПП Поставщика  (исполнителя, подрядчика) по контракту
#     c_trade_name = models.CharField(max_length=54, null=True, blank=True,db_index=True)  # Торговое наименование (контракт)
#     c_interl_name = models.CharField(max_length=65, null=True, blank=True, db_index=True)  # Международное непатентованное наименование (контракт)
#     act_paid = models.FloatField(null=True, blank=True)  # Фактически оплачено
#     c_inn_customer = models.PositiveIntegerField(null=True, blank=True, db_index=True)  # ИНН заказчика по контракту
#     c_prod_name = models.CharField(max_length=527, null=True, blank=True)  # Наименование товаров (контракт)
#     extra_funds = models.FloatField(null=True, blank=True)  # Внебюджетные средства
#     budget_funds = models.FloatField(null=True, blank=True)  # Бюджетные средства
#     productidnx = models.PositiveIntegerField(null=True, blank=True)  # ProductIdNx
#     inn_lpu = models.PositiveIntegerField(null=True, blank=True, db_index=True)  # ЛПУ ИНН
#
#     def __str__(self):
#          return  self.order_n+' '+self.customer_name

# class Employee(models.Model):
#     fio = models.CharField(max_length=64,db_index=True, null=False, blank=False)
#     targets = models.ManyToManyField(Target, null=False)
