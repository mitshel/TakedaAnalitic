-- Создание отдельной таблицы с выбранными рынками для организации с ID=1
-- LocalDB execute Time: 03:57

drop table test_CACHE_1
go

-- Создание урезанной таблици test_CACHE_1
--
select 
a.Tender_ID,
a.ProcDt,
a.TenderPrice,
a.StatusT_ID,
a.FormT_ID,
a.cust_id,
a.ClaimDtBeg,
a.TendSYSDATE,
a.Lot_ID,
a.PlanTYear,
a.InnNx,
a.TradeNx,
a.Order_Price,
a.Order_Count,
a.Order_Sum,
a.Ship_FinalPrice,
a.Winner_Id,
c.name as market_name, 
c.id as market_id
into test_CACHE_1 from ComplexRpt_CACHE a
left join db_marketmnn b1 on a.InnNx=b1.mnn_id
left join db_markettm b2 on a.TradeNx=b2.tm_id
inner join db_market c on ((c.id=b2.market_id) or (c.id=b1.market_id)) 
where c.org_id=1
--inner join lpu d on a.cust_id=d.cust_id 
--inner join db_lpu_employee e on d.cust_id=e.lpu_id
--inner join db_employee e1 on e1.id=e.employee_id and e1.org_id=1
go

-- Создание Индексов для таблицы test_CACHE_1:
--
alter table test_CACHE_1 add id bigint identity not null primary key
go

CREATE NONCLUSTERED INDEX [idx_1_InnNx] ON [dbo].[test_CACHE_1]
(
	[InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_1_TradeNx] ON [dbo].[test_CACHE_1]
(
	[TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_1_CustID] ON [dbo].[test_CACHE_1]
(
	[Cust_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_1_PlanTYear] ON [dbo].[test_CACHE_1]
(
	[PlanTYear] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO
CREATE NONCLUSTERED INDEX [idx_1_Winner_ID] ON [dbo].[test_CACHE_1]
(
	[Winner_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создание таблицы со статусами
--
--
drop table db_statusT
go
select distinct StatusT_ID as id, statusT_Name as name into db_statusT from CursorTest..test_CACHE_1f order by statusT_ID
go
alter table db_statusT alter column name varchar(40)
go
ALTER TABLE [dbo].[db_statusT] ADD PRIMARY KEY CLUSTERED 
([id] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создание таблицы с Международными непатентованными наименованиями (International Nopatent Name)
--
--
drop table db_inNR
go
select distinct 
a.innNx as id, 
(select top 1 c.innR from CursorTest..test_CACHE_1f c where c.innNX=a.innNX) as name 
into db_inNR
from CursorTest..ComplexRpt_CACHE a
where a.innNX is not null 
go
select max(len(name)) from db_inNR
alter table db_inNR alter column name varchar(300)
alter table db_inNR alter column id int not null
go
update db_InnR set name=CONCAT('#',CAST(id as VARCHAR(5))) where isnull(name,'')=''
go
ALTER TABLE [dbo].[db_inNR] ADD PRIMARY KEY CLUSTERED 
([id] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO
update db_innr set name = 
LTRIM(REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(name,'\f',''),
'\n',''),
'\r',''),
'\t',''),
'\u0000',''),
'\u0001',''),
'\u001f',''))
go

-- Создание таблицы с Торговыми наименованиями (TradeName)
--
--
drop table db_tradeNR
go
select distinct 
a.TradeNx as id, 
(select top 1 c.TradeNmR from CursorTest..ComplexRpt_CACHE c where c.TradeNX=a.TradeNX) as name 
into db_tradeNR
from CursorTest..ComplexRpt_CACHE a
where a.TradeNX is not null 
go
select max(len(name)) from db_tradeNR
alter table db_tradeNR alter column name varchar(256)
alter table db_tradeNR alter column id int not null
go
update db_tradeNR set name=CONCAT('#',CAST(id as VARCHAR(5))) where isnull(name,'')=''
go
ALTER TABLE [dbo].[db_tradeNR] ADD PRIMARY KEY CLUSTERED 
([id] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO
update db_TradeNr set name = 
LTRIM(REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(
REPLACE(name,'\f',''),
'\n',''),
'\r',''),
'\t',''),
'\u0000',''),
'\u0001',''),
'\u001f',''))
go

-- Создание таблицы с Победителями Торгов (WinnerOrg)
--
--
drop table db_WinnerOrg
go
select distinct 
Winner_ID as id, 
(select top 1 WinnerOrgINN from CursorTest..ComplexRpt_CACHE b where a.Winner_ID=b.Winner_ID) as inn,
(select top 1 WinnerOrg from CursorTest..ComplexRpt_CACHE c where a.Winner_ID=c.Winner_ID) as name
into db_WinnerOrg
from CursorTest..ComplexRpt_CACHE a
where Winner_ID is not null 
order by Winner_ID
go
select max(len(name)),max(len(inn)) from db_WinnerOrg
alter table db_WinnerOrg alter column name varchar(200)
alter table db_WinnerOrg alter column inn varchar(16)
alter table db_WinnerOrg alter column id int not null
go
update db_WinnerOrg set name=REPLACE(REPLACE(name, char(10), ''),char(13),'')
go
update db_WinnerOrg set name=CONCAT('#',CAST(id as VARCHAR(5))) where isnull(name,'')=''
go
ALTER TABLE [dbo].[db_WinnerOrg] ADD PRIMARY KEY CLUSTERED 
([id] ASC) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Перенос ранее вручную созданной таблицы db_marketmnn в db_market_innrs, для возможнсти отображения виджета многие ко многим в админке
insert into db_market_innrs(market_id, innr_id) select market_id, mnn_id_id from db_marketmnn
go
-- Перенос ранее вручную созданной таблицы db_markettm в db_market_tmnrs, для возможнсти отображения виджета многие ко многим в админке
insert into db_market_tmnrs(market_id, tradenr_id) select market_id, tm_id_id from db_markettm
go


-- Создание полной таблици test_CACHE_1f
--
select 
a.*,
c.name as market_name, 
c.id as market_id
into test_CACHE_1f from ComplexRpt_CACHE a
left join db_marketmnn b1 on a.InnNx=b1.mnn_id
left join db_markettm b2 on a.TradeNx=b2.tm_id
inner join db_market c on ((c.id=b2.market_id) or (c.id=b1.market_id)) 
where c.org_id=1
--inner join lpu d on a.cust_id=d.cust_id 
--inner join db_lpu_employee e on d.cust_id=e.lpu_id
--inner join db_employee e1 on e1.id=e.employee_id and e1.org_id=1
go

-- Создание полной таблицы dod для организации 1
--
--
drop table test_CACHE_1f_dod
go
select * into test_CACHE_1f_dod from complexRpt_CACHE_dod  where id_dod in
(select DISTINCT dod_id from test_CACHE_1f)
go 

-- Создание полной таблицы Contract для организации 1
--
--
drop table test_CACHE_1f_contract
go
select * into test_CACHE_1f_contract from ComplexRpt_CACHE_Contract 
where lot_id in (select DISTINCT lot_id from test_CACHE_1f)
or Lotspec_ID in (select DISTINCT Lotspec_ID from test_CACHE_1f)
go 
