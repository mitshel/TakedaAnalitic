ft_unknown = -1
ft_none    = 0
ft_integer = 1
ft_numeric = 2
ft_date    = 3
ft_string  = 4
ft_fk      = 5

cache_unknown  = 0
cache_tender   = 1
cache_contract = 2

gr_Tender   = {'name': 'Извещение',  'id': 1}
gr_Spec     = {'name': 'Спецификация',  'id': 2}
gr_Lot      = {'name': 'Лот',  'id': 3}
gr_Winner   = {'name': 'Победитель',  'id': 4}
gr_Contract = {'name': 'Контракт',  'id': 5}
gr_Order    = {'name': 'Заказ',  'id': 6}

fk_mnn      = 'db_innr'
fk_tm       = 'db_tmnr'
fk_status   = 'db_statusT'
fk_region   = 'db_region'
fk_lpu      = 'db_lpu'
fk_fo       = 'db_fo'
fk_budgets  = 'db_budgets'
fk_winner   = 'db_winnerorg'

cache_metadata = [
#    'fname' : {'title' : 'fieldtitle', 'type' : ft_fk, 'fk' : 'foreignkey_ref', 'cache' : cache_tender, 'group' : gr_1},
{ 'name': 'PublDt', 'title' : 'Дата публикации', 'type' : ft_date, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'TendDt', 'title' : 'Дата проведения торгов', 'type' : ft_date, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'NotifNr', 'title' : 'Номер извещения', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 23},
{ 'name': 'FZ_FK', 'title' : 'ФЗ', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 5},
{ 'name': 'SrcInf', 'title' : 'Ссылка на извещение', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 40},
{ 'name': 'TendNm', 'title' : 'Наименование торгов', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 30},
{ 'name': 'TenderPrice', 'title' : 'Начальная (максимальная) цена торгов', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'SmallBusiness', 'title' : 'Торги для МБ', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 5},
{ 'name': 'StatusT_Name', 'title' : 'Статус торгов', 'type' : ft_fk, 'fk' : fk_status, 'fk_field' : 'StatusT_ID', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 15},
{ 'name': 'FormT_Name', 'title' : 'Форма торгов', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 20},
{ 'name': 'FONm', 'title' : 'Федеральный округ проведения торгов', 'type' : ft_fk, 'fk' : fk_fo, 'fk_field' : 'FO_ID', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 20},
{ 'name': 'RegNm', 'title' : 'Регион проведения торгов', 'type' : ft_fk, 'fk' : fk_region, 'fk_field' : 'Reg_ID', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 20},
{ 'name': 'City_Name', 'title' : 'Населенный пункт', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 15},
{ 'name': 'Org_CustINN', 'title' : 'ИНН заказчика торгов', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'Org_CustNm', 'title' : 'Заказчик торгов', 'type' : ft_fk, 'fk' : fk_lpu, 'fk_field' : 'Cust_ID', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 20},
{ 'name': 'Org_SubCustINN', 'title' : 'ИНН уполномоченной организации', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'Org_SubCustNm', 'title' : 'Уполномоченная организация', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'Org_ProviderINN', 'title' : 'ИНН организатора торгов', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'Org_ProviderNm', 'title' : 'Организатор торгов', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'ClaimReglament', 'title' : 'Место подачи заявок', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'ClaimDtBeg', 'title' : 'Дата начала подачи заявок', 'type' : ft_date, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'ClaimDtEnd', 'title' : 'Дата окончания подачи заявок', 'type' : ft_date, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'Budgets_Name', 'title' : 'Тип бюджета', 'type' : ft_fk, 'fk' : fk_budgets, 'fk_field' : 'Budgets_ID', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'TenderDocReglament', 'title' : 'Источник финансирования', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'PaymentReglament', 'title' : 'Порядок оплаты поставок товаров', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'Tender_Lot', 'title' : 'Количество лотов', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'Planned', 'title' : 'Наличие плана-графика', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'PrefRus', 'title' : 'Преимущества для ТС', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'BudgetProg_Name', 'title' : 'Программа финансирования', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'LotNr', 'title' : 'Номер лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'LotStat', 'title' : 'Статус лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'ReasonFailure', 'title' : 'Комментарии к статусу Лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'LotNm', 'title' : 'Наименование лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'SpecCount', 'title' : 'Количество позиций в спецификации', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'LFONm', 'title' : 'Федеральный округ поставки лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'LotRegNm', 'title' : 'Регион поставки лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'PriceStart', 'title' : 'Начальная (максимальная) цена лота', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'ConsigneeNm', 'title' : 'Грузополучатель', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'ConsigneeInfo', 'title' : 'Сведения о грузополучателе', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'PlanTName', 'title' : 'Период поставки', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'PlanTYear', 'title' : 'Год поставки', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'PlanTVal', 'title' : 'Условия поставки', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'SupplyDt', 'title' : 'Срок действия контракта', 'type' : ft_date, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'ContrExpVal', 'title' : 'Примечание к сроку действия контракта', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'ClaimObesp', 'title' : 'Размер обеспечения заявки', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'ContrObesp', 'title' : 'Размер обеспечения контракта', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'MonoMNN', 'title' : 'Монопозиционный (по МНН) лот', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'SupplierGroup_Name', 'title' : 'Группа поставщиков', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'WinnerOrgINN', 'title' : 'ИНН победителя по протоколу', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'WinnerOrg', 'title' : 'Победитель по протоколу', 'type' : ft_fk, 'fk' : fk_winner, 'fk_field': 'Winner_ID', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'WinnerInfo', 'title' : 'Сведения о победителе по протоколу', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'PriceMax', 'title' : 'Цена победителя по протоколу', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'SecondOrgINN', 'title' : 'ИНН второго участника лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'SecondOrgNm', 'title' : 'Второй участник лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'SecordOrgInfo', 'title' : 'Сведения о втором участнике лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'PriceOther', 'title' : 'Цена второго участника лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'ThirdOrgINN', 'title' : 'ИНН третьего участника лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'ThirdOrgNm', 'title' : 'Третий участник лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'ThirdOrgInfo', 'title' : 'Сведения о третьем участнике лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'PriceThird', 'title' : 'Цена третьего участника лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'FourthOrgINN', 'title' : 'ИНН четвертого участника лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'FourthOrgNm', 'title' : 'Четвертый участник лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'FourthOrgInfo', 'title' : 'Сведения о четвертом участнике лота', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'PriceFourth', 'title' : 'Цена четвертого участника лота', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Winner, 'visible' : 1, 'width' : 10},
{ 'name': 'LotSpec_Pos', 'title' : 'Позиция в спецификации', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'Innr', 'title' : 'МНН', 'type' : ft_fk, 'fk' : fk_mnn, 'fk_field':'InnNx', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
#{ 'name': 'InnNx', 'title' : 'МНН ID', 'type' : ft_fk, 'fk' : fk_mnn, 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'TradeNmR', 'title' : 'ТН', 'type' : ft_fk, 'fk' : fk_tm, 'fk_field':'TradeNx','cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
#{ 'name': 'TradeNx', 'title' : 'ТН ID', 'type' : ft_fk, 'fk' : fk_tm, 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'ProdNm', 'title' : 'Наименование позиции в спецификации', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'Form', 'title' : 'Характеристика товара', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'ShortName', 'title' : 'Единица измерения', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'Price', 'title' : 'Начальная цена позиции в спецификации', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'Num', 'title' : 'Количество по позиции в спецификации', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'Summa', 'title' : 'Сумма по позиции в спецификации', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'ATCID', 'title' : 'Классификатор лекарства', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Spec, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractNr', 'title' : 'Реестровый номер контракта', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractURL', 'title' : 'Ссылка на контракт', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractDate', 'title' : 'Дата подписания контракта', 'type' : ft_date, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractPrice', 'title' : 'Цена контракта', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractItemNm', 'title' : 'Наименование позиции контракта', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'IntlName', 'title' : 'МНН контракт', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'TradeName', 'title' : 'ТН контракт', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ItemForma', 'title' : 'Характеристика позиции контракта', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractItemUnit', 'title' : 'Единица измерения по контракту', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractItemPrice', 'title' : 'Цена позиции контракта', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractItemCount', 'title' : 'Количество по позиции контракта', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'ContractItemSum', 'title' : 'Сумма по позиции контракта', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'VendorName', 'title' : 'Производитель/страна позиции контракта', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_InnR', 'title' : 'МНН (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_TradeNmR', 'title' : 'ТН (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Form', 'title' : 'Лекарственная форма полная (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Dosage', 'title' : 'Дозировка (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Package', 'title' : 'Первичная упаковка (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_PrimSize', 'title' : 'Объем (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_BatchSize', 'title' : 'Количество в потребительской упаковке (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Vendor', 'title' : 'Производитель ЛС (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Descr', 'title' : 'Полная характеристика ЛС (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Unit', 'title' : 'Единица измерения (заказ)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Price', 'title' : 'Начальная цена позиции (заказ)', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Count', 'title' : 'Количество по позиции (заказ)', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_Sum', 'title' : 'Сумма по позиции (заказ)', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Order_AVG_Price', 'title' : 'Средняя цена', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Form', 'title' : 'Лекарственная форма (поставка)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Dosage', 'title' : 'Дозировка (поставка)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Volume', 'title' : 'Объем (поставка)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_PrimSize', 'title' : 'Первичная упаковка (поставка)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_BatchSize', 'title' : 'Количество в потребительской упаковке (поставка)', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Vendor', 'title' : 'Производитель ЛС (поставка)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Descr', 'title' : 'Полная характеристика ЛС (поставка)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Unit', 'title' : 'Единица измерения (поставка)', 'type' : ft_string, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Price', 'title' : 'Цена позиции (поставка)', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Count', 'title' : 'Количество по позиции (поставка)', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_Sum', 'title' : 'Сумма по позиции (поставка)', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'Ship_FinalPrice', 'title' : 'Конечная цена лота', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Order, 'visible' : 1, 'width' : 10},
{ 'name': 'PriceDropPercentage', 'title' : 'Изменение цены лота (НМЦ/цена Победителя)', 'type' : ft_numeric, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'Item_ID', 'title' : 'ID Позиции', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'Tender_ID', 'title' : 'ID извещения', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Tender, 'visible' : 1, 'width' : 10},
{ 'name': 'Contract_ID', 'title' : 'ID Контракта', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Contract, 'visible' : 1, 'width' : 10},
{ 'name': 'Lot_ID', 'title' : 'ID лота', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10},
{ 'name': 'LotSpec_ID', 'title' : 'ID спецификации', 'type' : ft_integer, 'fk' : '', 'cache' : cache_tender, 'group' : gr_Lot, 'visible' : 1, 'width' : 10}
]

def get_fieldmeta(name):
    return next(f for f in cache_metadata if f['name'] == name)