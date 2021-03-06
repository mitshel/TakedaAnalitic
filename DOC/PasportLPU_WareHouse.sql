IF OBJECT_ID('dbo.org_DATA', 'U') IS NOT NULL
   drop table org_DATA
go

CREATE TABLE [dbo].[org_DATA](
  [id] bigint identity not null,
	[cust_id] [int] not null,
	[PlanTYear] [int] not null,
	[Order_Summa] [decimal](38, 2) not null,
	[Contract_Summa] [decimal](38, 2) not null
) ON [PRIMARY]
GO

delete from [dbo].[org_DATA]
go

--insert into [dbo].[org_DATA]([cust_id],[PlanTYear],[summa])
--select cust_id, isnull(year([DTExecuteEnd]),0) as [PlanTYear],sum(isnull(isnull([Ship_Sum],[ItemSum]),0)) as summa
--from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]
--group by cust_id, year([DTExecuteEnd])
--go

--
--  ВАРИАНТ 1
--
insert into [dbo].[org_DATA]([cust_id],[PlanTYear],[Order_Summa],[Contract_Summa])
select isnull(isnull(c1.cust_id,s.cust_id),0) as cust_id, isnull(s.PlanTYear,0) as PlanTYear,
sum(isnull(s.Order_Sum,0)) as Order_Summa,
sum(isnull(isnull(c1.[Ship_Sum],c1.[ItemSum]),0)) as Contract_Summa
from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE] s
--LEFT JOIN [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract] c (nolock)
--	ON c.Lot_ID = s.Lot_ID
--	   and c.Contract_ID > 0
--	   and c.Lotspec_ID IS NULL
LEFT JOIN [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract] c1 (nolock)
	ON c1.LotSpec_ID = s.LotSpec_ID
	   and c1.Contract_ID > 0
	   and isnull(c1.LotSpec_ID,0) > 0
where (s.Reg_ID < 100) and (s.StatusT_ID=4)--AND (s.ProdType_ID = 'L')
group by isnull(isnull(c1.cust_id,s.cust_id),0), isnull(s.PlanTYear,0)
having sum(isnull(isnull(c1.[Ship_Sum],c1.[ItemSum]),0))>0
go
-- 31644 записи 5:41 ,Без первого Join 2:39
-- 33170 Без проверки ProdType 1:57
-- 33164 с s.StatusT_ID=4 5:57   Production 35752 - 42:50


--
--  ВАРИАНТ 2
--
delete from [dbo].[org_DATA]
insert into [dbo].[org_DATA]([cust_id],[PlanTYear],[Order_Summa],[Contract_Summa])
select isnull(cust_id,0) as cust_id, isnull(PlanTYear,0) as PlanTYear, SUM(Order_Summa) as Order_Summa, SUM(Contract_Summa) as Contract_Summa
from (
		select s.cust_id, s.PlanTYear, sum(isnull(s.Order_Sum,0)) as Order_Summa, 0 as Contract_Summa
		from ( select distinct Tender_ID, cust_id, PlanTYear, Order_Sum from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE] where (Reg_ID < 100) and (StatusT_ID=4) ) s
		group by s.cust_id, s.PlanTYear
		having sum(isnull(s.Order_Sum,0))>0
		UNION
		select c1.cust_id, PlanTYear, 0 as Order_Summa, sum(isnull(isnull(c1.[Ship_Sum],c1.[ItemSum]),0)) as Contract_Summa
		from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE] s
		LEFT JOIN [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract] c1 (nolock)
			ON c1.LotSpec_ID = s.LotSpec_ID
			   and c1.Contract_ID > 0
			   and isnull(c1.LotSpec_ID,0) > 0
		where (s.Reg_ID < 100) and (s.StatusT_ID=4)
		group by c1.cust_id, PlanTYear
		having sum(isnull(isnull(c1.[Ship_Sum],c1.[ItemSum]),0))>0
     ) subquery
group by isnull(cust_id,0), isnull(PlanTYear,0)
go
-- 41618 - Devel: 10:29 - Production: 45525 - 1:09:17
-- 41618 - Devel: 10:53 - Production: 45525 - 1:13:20

CREATE NONCLUSTERED INDEX [idx_org_DATA_cust_id] ON [dbo].[org_DATA]
(
	[cust_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go

CREATE NONCLUSTERED INDEX [idx_org_DATA_year] ON [dbo].[org_DATA]
(
	[PlanTYear] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go


IF OBJECT_ID('dbo.org_ATC', 'U') IS NOT NULL
   drop table org_ATC
go

CREATE TABLE [dbo].[org_ATC](
  [id] bigint identity not null,
	[cust_id] [int] not null,
	[year] [int] not null,
	[ATCID] varchar(7) not null,
	[ATCID_L1] varchar(1) not null,
	[ATCID_L2] varchar(2) not null,
	[ATCID_L3] varchar(1) not null,
	[ATCID_L4] varchar(1) not null,
	[ATCID_L5] varchar(2) not null,
	[Summa] [decimal](38, 2) not null
) ON [PRIMARY]
GO

delete from [dbo].[org_ATC]
go

insert into [dbo].[org_ATC]([cust_id],[year],[ATCID], [ATCID_L1], [ATCID_L2], [ATCID_L3], [ATCID_L4], [ATCID_L5],[summa])
select cust_id, isnull(year([DTExecuteEnd]),0) as [year],
isnull(ATCID,''),
SUBSTRING(isnull(ATCID,''),1,1) as [ATCID_L1],
SUBSTRING(isnull(ATCID,''),2,2) as [ATCID_L2],
SUBSTRING(isnull(ATCID,''),4,1) as [ATCID_L3],
SUBSTRING(isnull(ATCID,''),5,1) as [ATCID_L4],
SUBSTRING(isnull(ATCID,''),6,2) as [ATCID_L5],
sum(isnull(isnull([Ship_Sum],[ItemSum]),0)) as summa

from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]
group by cust_id, year([DTExecuteEnd]),ATCID,
SUBSTRING(isnull(ATCID,''),1,1),
SUBSTRING(isnull(ATCID,''),2,2),
SUBSTRING(isnull(ATCID,''),4,1),
SUBSTRING(isnull(ATCID,''),5,1),
SUBSTRING(isnull(ATCID,''),6,2)
go

CREATE NONCLUSTERED INDEX [idx_org_ATC_cust_id] ON [dbo].[org_ATC]
(
	[cust_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go

CREATE NONCLUSTERED INDEX [idx_org_ATC_year] ON [dbo].[org_ATC]
(
	[year] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go

CREATE NONCLUSTERED INDEX [idx_org_ATC_ATCID] ON [dbo].[org_ATC]
(
	[ATCID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go

CREATE NONCLUSTERED INDEX [idx_org_ATC_ATCID_LEV] ON [dbo].[org_ATC]
(
	[ATCID_L1] ASC,
	[ATCID_L2] ASC,
	[ATCID_L3] ASC,
	[ATCID_L4] ASC,
	[ATCID_L5] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
go


