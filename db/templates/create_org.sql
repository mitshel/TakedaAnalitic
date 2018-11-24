if exists (select 1
            from  sysobjects
           where  id = object_id('org_CACHE_{{org_id}}')
            and   type = 'U')
   drop table org_CACHE_{{org_id}}

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
a.Order_InnNx,
a.TradeNx,
a.Order_TradeNmNx as Order_TradeNx,
a.Order_Price,
a.Order_Count,
a.Order_Sum,
a.Summa,
a.Ship_FinalPrice,
a.Winner_Id,
c.name as market_name,
c.id as market_id
into org_CACHE_{{org_id}} from ComplexRpt_CACHE a
left join db_market_innrs b1 on a.InnNx=b1.innr_id
left join db_market_tmnrs b2 on a.TradeNx=b2.tradenr_id
inner join db_market c on ((c.id=b2.market_id) or (c.id=b1.market_id))
where c.org_id={{org_id}}

alter table org_CACHE_{{org_id}} add id bigint identity not null primary key

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_InnNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Order_InnNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Order_InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Order_TradeNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Order_TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_TradeNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[TradeNx] ASC
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
