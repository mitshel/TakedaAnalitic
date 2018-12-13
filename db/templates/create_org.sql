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
t.cust_id,
t.ClaimDtBeg,
t.TendSYSDATE,
t.Lot_ID,
t.Lotspec_ID,
t.PlanTYear,
t.InnNx,
t.Order_InnNx,
t.TradeNx,
t.Order_TradeNmNx as Order_TradeNx,
t.Order_Price,
t.Order_Count,
t.Order_Sum as Order_Summa,
t.Summa,
t.Ship_FinalPrice,
t.Winner_Id,
isnull(m1.name, m2.name) as market_name,
isnull(m1.id, m2.id) as market_id,
c1.IntlName_ID as Contract_InnNx,
c1.TradeName_ID as Contract_TradeNx,
--ISNULL(c1.RegNumber,c.RegNumber) as ContractNr,
--ISNULL(c1.SignedDate,c.SignedDate) as ContractDate,
--ISNULL(c1.Url,c.Url) as ContractURL,
ISNULL(c1.Price,c.Price) as ContractPrice,
c1.ItemName as ContractItemNm,
--c1.ItemForma as ItemForma,
c1.ItemUnit as ContractItemUnit,
c1.ItemPrice as ContractItemPrice,
c1.ItemCount as ContractItemCount,
c1.ItemSum as Contract_Summa --ContractItemSum

into org_CACHE_{{org_id}} from ComplexRpt_CACHE t

LEFT JOIN dbo.ComplexRpt_CACHE_Contract c (nolock)
	ON c.Lot_ID = t.Lot_ID
	   and c.Contract_ID > 0
	   and c.Lotspec_ID IS NULL
LEFT JOIN dbo.ComplexRpt_CACHE_Contract c1 (nolock)
	ON c1.LotSpec_ID = t.LotSpec_ID
	   and c1.Contract_ID > 0
	   and isnull(c1.LotSpec_ID,0) > 0

left join db_market_innrs b1 on isNull(c1.IntlName_ID,t.InnNx)=b1.innr_id
left join db_market m1 on ((m1.id=b1.market_id) and m1.org_id={{org_id}})

left join db_market_tmnrs b2 on isNull(c1.TradeName_ID,t.TradeNx)=b2.tradenr_id
left join db_market m2 on ((m2.id=b2.market_id) and m1.org_id={{org_id}})

where (t.Reg_ID < 100) AND (t.ProdType_ID = 'L') and (m1.id is not null or m2.id is not null)

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

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_InnNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Contract_InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_TradeNx] ON [dbo].[org_CACHE_{{org_id}}]
(
	[Contract_TradeNx] ASC
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
