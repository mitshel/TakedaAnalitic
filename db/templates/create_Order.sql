select DISTINCT
Tender_ID,
ProcDt,
TendDt,
StatusT_ID,
FormT_ID,
Budgets_ID,
cust_id,
TendSYSDATE,
T_UPDDATE,
Lot_ID,
Lotspec_ID,
PlanTYear,
Order_InnNx,
Order_TradeNx,
Order_Price,
Order_Count,
Order_Summa,
Winner_Id,
market_name,
market_id,
market_own,
Order_Dosage_id,
Order_Form_id
into org_Order_{{org_id}} from org_Contract_{{org_id}} (nolock)

alter table org_Order_{{org_id}} add id bigint identity not null primary key

CREATE NONCLUSTERED INDEX [idxo_{{org_id}}_market_id] ON [dbo].[org_Order_{{org_id}}]
(
	[market_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idxo_{{org_id}}_market_own] ON [dbo].[org_Order_{{org_id}}]
(
	[market_own] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idxo_{{org_id}}_Order_InnNx] ON [dbo].[org_Order_{{org_id}}]
(
	[Order_InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


CREATE NONCLUSTERED INDEX [idxo_{{org_id}}_Order_TradeNx] ON [dbo].[org_Order_{{org_id}}]
(
	[Order_TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idxo_{{org_id}}_CustID] ON [dbo].[org_Order_{{org_id}}]
(
	[Cust_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idxo_{{org_id}}_PlanTYear] ON [dbo].[org_Order_{{org_id}}]
(
	[PlanTYear] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idxo_{{org_id}}_Winner_ID] ON [dbo].[org_Order_{{org_id}}]
(
	[Winner_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idxo_{{org_id}}_Budgets_ID] ON [dbo].[org_Order_{{org_id}}]
(
	[Budgets_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idxo_{{orgt_id}}_Order_Dosage_id] ON [dbo].[org_Order_{{org_id}}]
(
	[Order_Dosage_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)

CREATE NONCLUSTERED INDEX [idxo_{{orgt_id}}_Order_Form_id] ON [dbo].[org_Order_{{org_id}}]
(
	[Order_Form_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


update db_org set sync_status=0, db_version='{{ db_version }}', last_sync_dt = GETUTCDATE() where id={{ org_id }}

