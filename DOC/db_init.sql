--
-- Создание и наполнение таблицы годов db_years
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_years')
            and   type = 'U')
   drop table [dbo].[db_years]
go


CREATE TABLE [dbo].[db_years] (
	[PlanTYear] [int] NOT NULL
PRIMARY KEY CLUSTERED
(
	[PlanTYear] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

insert into [dbo].[db_years](PlanTYear) values(2010)
insert into [dbo].[db_years](PlanTYear) values(2011)
insert into [dbo].[db_years](PlanTYear) values(2012)
insert into [dbo].[db_years](PlanTYear) values(2013)
insert into [dbo].[db_years](PlanTYear) values(2014)
insert into [dbo].[db_years](PlanTYear) values(2015)
insert into [dbo].[db_years](PlanTYear) values(2016)
insert into [dbo].[db_years](PlanTYear) values(2017)
insert into [dbo].[db_years](PlanTYear) values(2018)
insert into [dbo].[db_years](PlanTYear) values(2019)
insert into [dbo].[db_years](PlanTYear) values(2020)
insert into [dbo].[db_years](PlanTYear) values(2021)
insert into [dbo].[db_years](PlanTYear) values(2022)
insert into [dbo].[db_years](PlanTYear) values(2023)
insert into [dbo].[db_years](PlanTYear) values(2024)
insert into [dbo].[db_years](PlanTYear) values(2025)
insert into [dbo].[db_years](PlanTYear) values(2026)
insert into [dbo].[db_years](PlanTYear) values(2027)
insert into [dbo].[db_years](PlanTYear) values(2028)
insert into [dbo].[db_years](PlanTYear) values(2029)
insert into [dbo].[db_years](PlanTYear) values(2030)
go

--
-- Создание и наполнение таблицы статусов db_statusT
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_statusT')
            and   type = 'U')
   drop table dbo.db_statusT
go

CREATE TABLE [dbo].[db_statusT](
	[id] [int] NOT NULL,
	[name] [varchar](200) NULL,
	[nameENG] [varchar](200) NULL
  PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

insert into db_statusT
select id, name, nameEng
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[StatusT]
go

--
-- Создание и наполнение таблицы организаций db_allOrg
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_allOrg')
            and   type = 'U')
   drop table dbo.db_allOrg
go

CREATE TABLE [dbo].[db_allOrg](
	[cust_id] [int] NOT NULL,
	[Org_CustINN] [varchar](16) NULL,
	[Org_CustNm] [varchar](512) NULL,
	[shortname] [varchar](512) NULL,
	[addr1] [varchar](512) NULL,
	[addr2] [varchar](512) NULL,
	[regcode] [int] NOT NULL,
 CONSTRAINT [PK_allOrg] PRIMARY KEY CLUSTERED
(
	[cust_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [idx_db_org_Org_CustNm] ON [dbo].[db_allOrg]
(
	[Org_CustNm] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go

-- Добавляем новые организации
--
insert into db_allOrg
select DISTINCT Org_ID as cust_id, INN as Org_CustINN, OrgNm as Org_CustNm, OrgNmS as shortname, Addr1, Addr2, isnull(regcode,0) as regcode
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[org] a
where not exists (select 1 from db_allOrg b where b.cust_id=a.org_id)
go
-- (затронуто строк: 19172)
-- 28.03.2019 (затронуто строк: 4889)


--
-- Создание и наполнение таблицы статусов db_Budgets
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_Budgets')
            and   type = 'U')
   drop table dbo.db_Budgets
go

CREATE TABLE [dbo].[db_Budgets](
	[id] char(1) NOT NULL,
	[version] int NOT NULL,
	[name] [varchar](200) NULL,
	[nameENG] [varchar](200) NULL
  PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


insert into db_Budgets
select a.id, a.version, b.name, b.nameEng from
(select id, max(version) as version
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[Budgets]
group by id) a
left join [VM1-12\CURSORMAIN].[Cursor].[dbo].[Budgets] b on a.id=b.id and a.version=b.version

go

--
-- Создание и наполнение таблицы Федеральныз округов db_FO
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_fo')
            and   type = 'U')
   drop table dbo.db_fo
go

CREATE TABLE [dbo].[db_fo](
	[id] [int]  NOT NULL,
	[name] [varchar](150) NOT NULL,
 CONSTRAINT [PK_FO] PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Обновляем ФО по ID
update t1
	set t1.name = t2.FO_Nm
	from db_fo t1
	inner join [VM1-12\CURSORMAIN].[Cursor].[dbo].[FO] as t2 on t1.id=t2.FO_ID
go

-- Добавляем новые ФО
--
insert into db_fo
select DISTINCT FO_ID as id, FO_Nm as name
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[FO] a
where not exists (select 1 from db_fo b where b.id=a.FO_ID)
go
-- (затронуто строк: 23)


--
-- Создание и наполнение таблицы МНН db_innr
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_innr')
            and   type = 'U')
   drop table dbo.db_innr
go

CREATE TABLE [dbo].[db_innr](
	[id] [int] NOT NULL,
	[name] [varchar](300) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Обновляем наименования по ID
update t1
	set t1.name = t2.InnR
	from db_innR t1
	inner join [VM1-12\CURSORMAIN].[Cursor].[dbo].[regMNN] as t2 on t1.id=t2.innNx
go

-- Добавляем новые МНН, но только те, которые есть в кэше
insert into db_innR
select DISTINCT innNx as id, InnR as name
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[regMNN]
where (innNx in (select Order_InnNx from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE])
or innNx in (select IntlName_ID from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]))
and innNX not in (select id from  db_innR)
go
-- (затронуто строк: 2731)
-- 28.03.2019 (затронуто строк: 46)

--
-- Создание и наполнение таблицы ТМ db_tradenr
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_tradenr')
            and   type = 'U')
   drop table dbo.db_tradenr
go

CREATE TABLE [dbo].[db_tradeNR](
	[id] [int] NOT NULL,
	[name] [varchar](254) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Обновляем наименования по ID
update t1
	set t1.name = t2.TradeNmR
	from db_tradeNR t1
	inner join [VM1-12\CURSORMAIN].[Cursor].[dbo].[regTradenm] as t2 on t1.id=t2.TradeNmNx
go

-- Добавляем новые ТМ, но только те, которые есть в кэше
insert into db_tradeNR
select DISTINCT TradeNmNx as id, TradeNmR as name
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[regTradenm]
where (TradeNmNx in (select Order_TradeNmNx from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE])
or TradeNmNx in (select TradeName_ID from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]))
and TradeNmNx not in (select id from  db_tradeNR)
go

-- (затронуто строк: 8911)
-- 28.03.2019 (затронуто строк: 250)


--
-- Создание и наполнение таблицы ЛПУ db_lpu
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_lpu')
            and   type = 'U')
   drop table dbo.db_lpu
go

CREATE TABLE [dbo].[db_lpu](
	[cust_id] [int] NOT NULL,
	[Org_CustINN] [varchar](16) NULL,
	[Org_CustNm] [varchar](512) NULL,
	[shortname] [varchar](512) NULL,
	[addr1] [varchar](512) NULL,
	[addr2] [varchar](512) NULL,
	[regcode] [int] NOT NULL,
 CONSTRAINT [PK_Lpu] PRIMARY KEY CLUSTERED
(
	[cust_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

CREATE NONCLUSTERED INDEX [idx_db_lpu_regcode] ON [dbo].[db_lpu]
(
	[regcode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go

CREATE NONCLUSTERED INDEX [idx_db_lpu_Org_CustNm] ON [dbo].[db_lpu]
(
	[Org_CustNm] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go

-- Обновляем Таблицу Организаций
update t1
	set t1.Org_CustINN = t2.INN,
	    t1.Org_CustNm = t2.OrgNm,
		t1.shortname = t2.OrgNmS,
		t1.addr1 = t2.addr1,
		t1.addr2 = t2.addr2,
		t1.regcode = isnull(t2.regcode,0)
	from db_lpu t1
	inner join [VM1-12\CURSORMAIN].[Cursor].[dbo].[org] as t2 on t1.cust_id=t2.Org_ID
go

-- Добавляем новые ЛПУ, но только те, которые есть в кэше
--
insert into db_lpu
select DISTINCT Org_ID as cust_id, INN as Org_CustINN, OrgNm as Org_CustNm, OrgNmS as shortname, Addr1, Addr2, isnull(regcode,0) as regcode
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[org]
where (Org_ID in (select cust_id from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE])
or Org_ID in (select cust_id from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]))
and Org_ID not in (select cust_id from  db_lpu)
go
-- (затронуто строк: 19172)
-- 28.03.2019 (затронуто строк: 1688)


-- Добавляем новые ЛПУ, которые есть в кэше, но нет даже в спрвочнике ORG
--
insert into db_lpu(cust_id,Org_CustNm, regcode)
select DISTINCT cust_id, cast(cust_id as varchar)+' #expected in Org from Tender' as Org_CustNm, 0 as regcode
from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE]
where cust_id not in (select cust_id from  db_lpu)
go

-- Добавляем новые ЛПУ, которые есть в контрактах, но нет даже в спрвочнике ORG
--
insert into db_lpu(cust_id,Org_CustNm, regcode)
select DISTINCT cust_id, cast(cust_id as varchar)+' #expected in Org from Contract' as Org_CustNm, 0 as regcode
from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]
where cust_id not in (select cust_id from  db_lpu)
go


--
-- Создание и наполнение таблицы Победителей торгов db_WinnerOrg
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_WinnerOrg')
            and   type = 'U')
   drop table dbo.db_WinnerOrg
go

CREATE TABLE [dbo].[db_WinnerOrg](
	[id] [int] NOT NULL,
	[inn] [varchar](16) NULL,
	[name] [varchar](512) NULL,
	[shortname] [varchar](512) NULL,
	[addr1] [varchar](512) NULL,
	[addr2] [varchar](512) NULL,
	[regcode] [int] NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


-- Обновляем Таблицу Победителей
update t1
	set t1.inn = t2.INN,
	    t1.name = t2.OrgNm,
		t1.shortname = t2.OrgNmS,
		t1.addr1 = t2.addr1,
		t1.addr2 = t2.addr2,
		t1.regcode = t2.regcode
	from db_WinnerOrg t1
	inner join [VM1-12\CURSORMAIN].[Cursor].[dbo].[org] as t2 on t1.id=t2.Org_ID
go

-- Добавляем новых Победителей, но только те, которые есть в кэше
--
insert into db_WinnerOrg
select DISTINCT Org_ID as cust_id, INN as inn, OrgNm as name, OrgNmS as shortname, Addr1, Addr2, regcode
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[org]
where (Org_ID in (select Winner_ID from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE])
or Org_ID in (select Winner_ID from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]))
and Org_ID not in (select id from  db_WinnerOrg)
go

-- (затронуто строк: 14063)
-- 28.03.2019 (затронуто строк: 268)


--
-- Создание и наполнение таблицы Регионов db_region
--
if exists (select 1
            from  sysobjects
           where  id = object_id('dbo.db_region')
            and   type = 'U')
   drop table dbo.db_region
go

CREATE TABLE [dbo].[db_region](
	[Reg_ID] [int] NOT NULL,
	[RegNm] [varchar](50) NOT NULL,
	[RegNmEn] [varchar](50) NULL,
	[FO_ID] [int] NULL,
	[RegCode] [int] NULL,
	[Cond] [char](1) NULL,
 CONSTRAINT [PK_Region] PRIMARY KEY CLUSTERED
(
	[Reg_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

insert into [dbo].[db_region]([Reg_ID],[RegNm],[RegNmEn],[FO_ID],[RegCode],[Cond])
select [Reg_ID],[RegNm],[RegNmEn],[FO_ID],[RegCode],[Cond]
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[Region]
where isnull([Cond],'W')<>'A'
go

update db_lpu set regcode=isnull(regcode,0)
go


--dbo.regFO
--dbo.Org
--dbo.Regions_LK

