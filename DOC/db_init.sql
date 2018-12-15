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
) ON [PRIMARY]
GO

insert into db_statusT
select id, name, nameEng
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[StatusT]
go

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
	[regcode] [int] NULL,
 CONSTRAINT [PK_Lpu] PRIMARY KEY CLUSTERED
(
	[cust_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Обновляем Таблицу Организаций
update t1
	set t1.Org_CustINN = t2.INN,
	    t1.Org_CustNm = t2.OrgNm,
		t1.shortname = t2.OrgNmS,
		t1.addr1 = t2.addr1,
		t1.addr2 = t2.addr2,
		t1.regcode = t2.regcode
	from db_lpu t1
	inner join [VM1-12\CURSORMAIN].[Cursor].[dbo].[org] as t2 on t1.cust_id=t2.Org_ID
go

-- Добавляем новые ЛПУ, но только те, которые есть в кэше
--
insert into db_lpu
select DISTINCT Org_ID as cust_id, INN as Org_CustINN, OrgNm as Org_CustNm, OrgNmS as shortname, Addr1, Addr2, regcode
from [VM1-12\CURSORMAIN].[Cursor].[dbo].[org]
where (Org_ID in (select cust_id from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE])
or Org_ID in (select cust_id from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]))
and Org_ID not in (select cust_id from  db_lpu)
go
-- (затронуто строк: 19172)

-- Добавляем новые ЛПУ, которые есть в кэше, но нет даже в спрвочнике ORG
--
insert into db_lpu(cust_id,Org_CustNm)
select DISTINCT cust_id, cast(cust_id as varchar)+' #expected in Org from Contract' as Org_CustNm
from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE]
where cust_id not in (select cust_id from  db_lpu)
go

-- Добавляем новые ЛПУ, которые есть в контрактах, но нет даже в спрвочнике ORG
--
insert into db_lpu(cust_id,Org_CustNm)
select DISTINCT cust_id, cast(cust_id as varchar)+' #expected in Org from Contract' as Org_CustNm
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



--dbo.regFO
--dbo.Org
--dbo.Regions_LK

