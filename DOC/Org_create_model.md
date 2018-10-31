-- Создание отдельной таблицы с выбранными рынками для организации с ID=1
-- LocalDB execute Time: 03:57

drop table test_CACHE_1
go


-- Создание урезанной таблици test_CACHE_1
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
c.name as market_name, 
c.id as market_id
into test_CACHE_1 from ComplexRpt_CACHE a
left join db_marketmnn b1 on a.InnNx=b1.mnn_id
left join db_markettm b2 on a.TradeNx=b2.tm_id
inner join db_market c on ((c.id=b2.market_id) or (c.id=b1.market_id)) 
where c.org_id=1
--inner join lpu d on a.cust_id=d.cust_id 
--inner join db_lpu_employee e on d.cust_id=e.lpu_id
--inner join db_employee e1 on e1.id=e.employee_id and e1.org_id=1
go

-- Создание полной таблици test_CACHE_1f
--
select 
a.*,
c.name as market_name, 
c.id as market_id
into test_CACHE_1f from ComplexRpt_CACHE a
left join db_marketmnn b1 on a.InnNx=b1.mnn_id
left join db_markettm b2 on a.TradeNx=b2.tm_id
inner join db_market c on ((c.id=b2.market_id) or (c.id=b1.market_id)) 
where c.org_id=1
--inner join lpu d on a.cust_id=d.cust_id 
--inner join db_lpu_employee e on d.cust_id=e.lpu_id
--inner join db_employee e1 on e1.id=e.employee_id and e1.org_id=1
go

-- Создание Индексов для таблицы test_CACHE_1:
--

CREATE NONCLUSTERED INDEX [idx_1_InnNx] ON [dbo].[test_CACHE_1]
(
	[InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_1_TradeNx] ON [dbo].[test_CACHE_1]
(
	[TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_1_CustID] ON [dbo].[test_CACHE_1]
(
	[Cust_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

CREATE NONCLUSTERED INDEX [idx_1_PlanTYear] ON [dbo].[test_CACHE_1]
(
	[PlanTYear] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO


-- Создание полной таблицы dod для организации 1
--
--
drop table test_CACHE_1f_dod
go
select * into test_CACHE_1f_dod from complexRpt_CACHE_dod  where id_dod in
(select DISTINCT dod_id from test_CACHE_1f)
go 

-- Создание полной таблицы Contract для организации 1
--
--
drop table test_CACHE_1f_contract
go
select * into test_CACHE_1f_contract from ComplexRpt_CACHE_Contract 
where lot_id in (select DISTINCT lot_id from test_CACHE_1f)
or Lotspec_ID in (select DISTINCT Lotspec_ID from test_CACHE_1f)
go 
