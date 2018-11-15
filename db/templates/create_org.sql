
if exists (select 1
            from  sysobjects
           where  id = object_id('org_CACHE_{{org_id}}')
            and   type = 'U')
   drop table org_CACHE_{{org_id}}
go

-- Создание урезанной таблици org_CACHE_nn
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
into org_CACHE_{{org_id}} from ComplexRpt_CACHE a
left join db_marketmnn b1 on a.InnNx=b1.mnn_id
left join db_markettm b2 on a.TradeNx=b2.tm_id
inner join db_market c on ((c.id=b2.market_id) or (c.id=b1.market_id))
where c.org_id={{org_id}}
go

-- Создание Индексов для таблицы test_CACHE_1:
--
alter table org_CACHE_{{org_id}} add id bigint identity not null primary key
go

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_InnNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_TradeNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_CustID] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Cust_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_PlanTYear] ON [dbo].[org_CACHE_{{org_id}}]
(
	[PlanTYear] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO
CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Winner_ID] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Winner_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO