if exists (select 1
            from  sysobjects
           where  id = object_id('org_CACHE_{{org_id}}')
            and   type = 'U')
   drop table org_CACHE_{{org_id}}

select
t.Tender_ID,
t.ProcDt,
t.TendDt,
t.TenderPrice,
t.SrcInf,
t.StatusT_ID,
t.FormT_ID,
t.Budgets_ID COLLATE database_default as Budgets_ID,
isnull(c1.cust_id, t.cust_id) as cust_id,
t.TendSYSDATE,
t.T_UPDDATE,
t.Lot_ID,
t.Lotspec_ID,
t.PlanTYear,
t.InnNx as Order_InnNx,
t.TradeNx as Order_TradeNx,
t.Order_Price as Order_Price,
t.Order_Count as Order_Count,
t.Order_Sum as Order_Summa,
t.Order_AVG_Price,
t.Winner_Id,
--t.Unit_Id as Order_Unit_ID,
--t.Order_Unit,
--c1.Ship_Unit as Contract_Unit,
isnull( ctm.market_name, isnull(cmnn.market_name, isnull(otm.market_name,omnn.market_name ) ) ) as market_name,
isnull( ctm.market_id, isnull(cmnn.market_id, isnull(otm.market_id, omnn.market_id ) ) ) as market_id,
IIF(
(ctm.own is null) and (cmnn.own is null),
-- Если в контрактах везде NULL то определяем OWN по аукционам
IIF( IIF(otm.own is null,0,isnull(otm.own,0))>0 or IIF(omnn.own is null,0,isnull(omnn.own,0))>0,1,0),
-- Иначе определяем OWN по контрактам
IIF( IIF(ctm.own is null,0,isnull(ctm.own,0))>0 or IIF(cmnn.own is null,0,isnull(cmnn.own,0))>0,1,0)
) as market_own,

c1.IntlName_ID as Contract_InnNx,
c1.TradeName_ID as Contract_TradeNx,
ISNULL(c1.Url,c.Url) as Contract_URL,
isnull(c1.[Ship_Price],c1.[ItemPrice]) as Contract_Price,
isnull(CAST(c1.[Ship_Count] as bigint),c1.[ItemCount]) as Contract_Count,
isnull(c1.[Ship_Sum],c1.[ItemSum]) as Contract_Summa,

--t.Order_Dosage,
--t.Order_BatchSize,
-- c1.Ship_Dosage as Contract_Dosage,
-- c1.Ship_Volume as Contract_Volume,
-- c1.Ship_BatchSize as Contract_BatchSize
isnull(t.Order_Dosage,'')+IIF(t.Order_BatchSize is Null,'',' №'+CAST(t.Order_BatchSize as varchar)) COLLATE database_default as Order_Dosage,
isnull(c1.Ship_Dosage,'')+IIF(c1.Ship_Volume is Null, '', ' '+c1.Ship_Volume)+IIF(c1.Ship_BatchSize is Null,'',' №'+CAST(c1.Ship_BatchSize as varchar)) COLLATE database_default as Contract_Dosage,
c1.Ship_form COLLATE database_default as Contract_Form

into org_CACHE_{{org_id}} from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE] t

LEFT JOIN [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract] c (nolock)
	ON c.Lot_ID = t.Lot_ID
	   and c.Contract_ID > 0
	   and c.Lotspec_ID IS NULL
LEFT JOIN [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract] c1 (nolock)
	ON c1.LotSpec_ID = t.LotSpec_ID
	   and c1.Contract_ID > 0
	   and isnull(c1.LotSpec_ID,0) > 0

--Markets
left join (select ji.innr_id, ji.market_id, ji.own, jm.name as market_name
           from db_market_innrs ji
		   left join db_market jm on ji.market_id=jm.id where jm.org_id={{ org_id }}) cmnn on c1.IntlName_ID=cmnn.innr_id
left join (select ji.innr_id, ji.market_id, ji.own, jm.name as market_name
           from db_market_innrs ji
		   left join db_market jm on ji.market_id=jm.id where jm.org_id={{ org_id }}) omnn on t.InnNx=omnn.innr_id
left join (select ji.tradenr_id, ji.market_id, ji.own, jm.name as market_name
           from db_market_tmnrs ji
		   left join db_market jm on ji.market_id=jm.id where jm.org_id={{ org_id }}) ctm on c1.TradeName_ID=ctm.tradenr_id
left join (select ji.tradenr_id, ji.market_id, ji.own, jm.name as market_name
           from db_market_tmnrs ji
		   left join db_market jm on ji.market_id=jm.id where jm.org_id={{ org_id }}) otm on t.TradeNx=otm.tradenr_id


where (t.Reg_ID < 100) AND (t.ProdType_ID = 'L') and (cmnn.market_id is not null or omnn.market_id is not null or ctm.market_id is not null or otm.market_id is not null)

alter table org_CACHE_{{org_id}} add id bigint identity not null primary key

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_market_id] ON [dbo].[org_CACHE_{{org_id}}]
(
	[market_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_market_own] ON [dbo].[org_CACHE_{{org_id}}]
(
	[market_own] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Order_InnNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Order_InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Order_TradeNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Order_TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_InnNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Contract_InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_TradeNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Contract_TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_CustID] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Cust_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_PlanTYear] ON [dbo].[org_CACHE_{{org_id}}]
(
	[PlanTYear] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Winner_ID] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Winner_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Budgets_ID] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Budgets_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_Dosage] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Contract_Dosage] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_Form] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Contract_Form] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


--
-- Нормализуем БД
--

--
-- НОРМАЛИЗАЦИЯ ДОЗИРОВОК
--

if exists (select 1
            from  sysobjects
           where  id = object_id('org_DOSAGE_{{org_id}}')
            and   type = 'U')
   drop table org_DOSAGE_{{org_id}}

CREATE TABLE [dbo].[org_DOSAGE_{{org_id}}](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[name] [varchar](128) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

insert into [dbo].[org_DOSAGE_{{org_id}}](name) select distinct isnull(RTRIM(LTRIM(Contract_Dosage)),'') from org_CACHE_{{org_id}}
alter table org_CACHE_{{org_id}} add Contract_Dosage_id bigint

update u
set u.Contract_Dosage_id=t.id
from org_CACHE_{{org_id}} u
left join org_DOSAGE_{{org_id}} t on isnull(RTRIM(LTRIM(u.Contract_Dosage)),'') = t.name

update org_DOSAGE_{{org_id}} set name=' НЕТ ДАННЫХ' where name = ''

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_Dosage_id] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Contract_Dosage_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


--
-- НОРМАЛИЗАЦИЯ ЛЕКАРСТВЕННЫХ ФОРМ
--

if exists (select 1
            from  sysobjects
           where  id = object_id('org_FORM_{{org_id}}')
            and   type = 'U')
   drop table org_FORM_{{org_id}}

CREATE TABLE [dbo].[org_FORM_{{org_id}}](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[name] [varchar](256) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

insert into [dbo].[org_FORM_{{org_id}}](name) select distinct isnull(RTRIM(LTRIM(Contract_Form)),'') from org_CACHE_{{org_id}}
alter table org_CACHE_{{org_id}} add Contract_Form_id bigint

update u
set u.Contract_Form_id=t.id
from org_CACHE_{{org_id}} u
left join org_FORM_{{org_id}} t on isnull(RTRIM(LTRIM(u.Contract_Form)),'') = t.name

update org_FORM_{{org_id}} set name=' НЕТ ДАННЫХ' where name = ''

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_Form_id] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Contract_Form_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


update db_org set sync_status=0 where id={{ org_id }}
