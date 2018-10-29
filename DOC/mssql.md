USE [CursorTest]
GO

-- Создаем индекс для связи с таблицей InnR (Международные непатентованные наименования). 
-- Предполагаю, что InnR - это как раз международное непатентованое название,
-- а InnNx его код
-- DB Cursor: 3:30
-- DB Local: 10:35
CREATE NONCLUSTERED INDEX [idxInnNx] ON [dbo].[ComplexRpt_CACHE]
(
	[InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создаем индекс для связи с таблицей TradeNmR (Торговые наименования). 
-- Предполагаю, что TradeNmR - это как раз международное непатентованое название,
-- а TradeNxR его код
-- DB Cursor: 3:57
-- DB Local: 10:34
CREATE NONCLUSTERED INDEX [idxTradeNx] ON [dbo].[ComplexRpt_CACHE]
(
	[TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создаем таблицу InnR
-- (затронуто строк: 3193)
-- DB Cursor: 3:36
select distinct InnNx, REPLACE(REPLACE(LOWER(InnR),'+ ','+'),' +','+') as InnR into InnR from innR
go

-- Смотрим на дубликаты InnNx
select * from InnR1 
where InnNx in (select innNx from innR1 group by innNx having Count(*)>1)


-- Создаем таблицу TradeNmR
-- (затронуто строк: 8604)
-- DB Cursor: 3:36
select distinct TradeNx, TradeNmR into TradeNmR from ComplexRpt_CACHE
go

-- Создаем таблицу Order_TradeNmR
-- (затронуто строк: 8568)
-- DB Cursor: 3:26
select distinct Order_TradeNmNx, REPLACE(REPLACE(LOWER(Order_TradeNmR),'+ ','+'),' +','+') as Order_TradeNmR into Order_TradeNmR from ComplexRpt_CACHE
go

-- Создаем таблицу Contract_TradeName
-- (затронуто строк: 7555)
-- DB Cursor: 0:52
select distinct TradeName_ID, REPLACE(REPLACE(LOWER(TradeName),'+ ','+'),' +','+') as TradeName into Contract_Tradename from ComplexRpt_CACHE_Contract
go

-- Создаенм доп.поле market_id
alter table ComplexRpt_CACHE add market_id int Null
go

-- Создаем связи с рынками
update ComplexRpt_CACHE set market_id=1 where TradeNx in (10763,4255,6767,11187,23647,38148)
update ComplexRpt_CACHE set market_id=2 where InnNx in (444,665,11833,43123)
update ComplexRpt_CACHE set market_id=3 where InnNx in (415,420,4767,10908,47541,51159,55003)
update ComplexRpt_CACHE set market_id=4 where InnNx in (722,734,1188,4751,54251,55018,47733,1117)
go 


-- Создаем индекс для связи с таблицей Market. 
-- DB Cursor: 4:39
CREATE NONCLUSTERED INDEX [idxMarket] ON [dbo].[ComplexRpt_CACHE]
(
	[Market_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создаем таблицу с рынками
create table market(market_id int, market_name varchar(32))
insert into market(market_id,market_name) values(1, 'Тахокомб')
insert into market(market_id,market_name) values(2, 'Дорипрекс')
insert into market(market_id,market_name) values(3, 'Феринжект')
insert into market(market_id,market_name) values(4, 'Фендивия')
go

-- Тест подсчет рынков
select a.market_id, b.market_name, sum(a.TenderPrice)
from ComplexRpt_CACHE a
left join market b on a.market_id=b.market_id
group by a.market_id, b.market_name
having a.market_id is not null