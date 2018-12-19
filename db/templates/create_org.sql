if exists (select 1
            from  sysobjects
           where  id = object_id('org_CACHE_{{org_id}}')
            and   type = 'U')
   drop table org_CACHE_{{org_id}}

select
t.Tender_ID,
t.ProcDt,
t.TenderPrice,
t.StatusT_ID,
t.FormT_ID,
isnull(c1.cust_id, t.cust_id) as cust_id,
t.ClaimDtBeg,
t.TendSYSDATE,
t.Lot_ID,
t.Lotspec_ID,
t.PlanTYear,
t.InnNx as Order_InnNx,
--t.Order_InnNx,
t.TradeNx as Order_TradeNx,
--t.Order_TradeNmNx as Order_TradeNx,
t.Order_Price as Order_Price,
t.Order_Count as Order_Count,
t.Order_Sum as Order_Summa,
--t.Summa,
--t.Ship_FinalPrice,
t.Winner_Id,
isnull(m1.name, m2.name) as market_name,
isnull(m1.id, m2.id) as market_id,
--IIF(m1.id is not null, b1.own, b2.own) as market_own,
IIF(isnull(b1.own,0)>0 or isnull(b2.own,0)>0,1,0) as market_own,
c1.IntlName_ID as Contract_InnNx,
c1.TradeName_ID as Contract_TradeNx,
--ISNULL(c1.RegNumber,c.RegNumber) as ContractNr,
--ISNULL(c1.SignedDate,c.SignedDate) as ContractDate,
--ISNULL(c1.Url,c.Url) as ContractURL,
ISNULL(c1.Price,c.Price) as Contract_Price,
c1.ItemName as ContractItemNm,
--c1.ItemForma as ItemForma,
c1.ItemUnit as ContractItemUnit,
c1.ItemPrice as ContractItemPrice,
c1.ItemCount as ContractItemCount,

isnull(c1.[Ship_Sum],c1.[ItemSum]) as Contract_Summa,
isnull(CAST(c1.[Ship_Count] as bigint),c1.[ItemCount]) as Contract_Count

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
left join db_market_innrs b1 on isNull(c1.IntlName_ID,t.InnNx)=b1.innr_id
left join db_market m1 on ((m1.id=b1.market_id) and m1.org_id={{org_id}})

left join db_market_tmnrs b2 on isNull(c1.TradeName_ID,t.TradeNx)=b2.tradenr_id
left join db_market m2 on ((m2.id=b2.market_id) and m2.org_id={{org_id}})

where (t.Reg_ID < 100) AND (t.ProdType_ID = 'L') and (m1.id is not null or m2.id is not null)

alter table org_CACHE_{{org_id}} add id bigint identity not null primary key

--CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Order_InnNx] ON [dbo].[org_CACHE_{{org_id}}]
--(
--	[InnNx] ASC
--)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

--CREATE NONCLUSTERED INDEX [idx_{{org_id}}_TradeNx] ON [dbo].[org_CACHE_{{org_id}}]
--(
--	[TradeNx] ASC
--)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
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
