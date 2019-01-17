IF OBJECT_ID('dbo.org_DATA', 'U') IS NOT NULL
   drop table org_DATA
go

CREATE TABLE [dbo].[org_DATA](
  [id] bigint identity not null,
	[cust_id] [int] not null,
	[PlanTYear] [int] not null,
	[Summa] [decimal](38, 2) not null
) ON [PRIMARY]
GO

delete from [dbo].[org_DATA]
go

insert into [dbo].[org_DATA]([cust_id],[PlanTYear],[summa])
select cust_id, isnull(year([DTExecuteEnd]),0) as [PlanTYear],sum(isnull(isnull([Ship_Sum],[ItemSum]),0)) as summa
from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract]
group by cust_id, year([DTExecuteEnd])
go

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


