-- Создаем индекс для связи с таблицей InnR (Международные непатентованные наименования). 
-- Предполагаю, что InnR - это как раз международное непатентованое название,
-- а InnNx его код
-- DB Cursor: 3:30
-- DB Local (2Core, 8Gb RAM): 10:35
-- DB Local (4Core, 16Gb RAM): 10:28
-- DB Local (4Core, 16Gb RAM, AHCI+ VMWARE 6.7u1): 4:43
CREATE NONCLUSTERED INDEX [idxInnNx] ON [dbo].[test_CACHE_1]
(
	[InnNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создаем индекс для связи с таблицей TradeNmR (Торговые наименования). 
-- Предполагаю, что TradeNmR - это как раз международное непатентованое название,
-- а TradeNxR его код
-- DB Cursor: 3:57
-- DB Local: 10:34
CREATE NONCLUSTERED INDEX [idxTradeNx] ON [dbo].[test_CACHE_1]
(
	[TradeNx] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создаем индекс по полю Cust_ID для связи с таблицей LPU (Учреждения-заказчики). 
-- DB Cursor: 
-- DB Local: 04:37
CREATE NONCLUSTERED INDEX [idxCustID] ON [dbo].[test_CACHE_1]
(
	[Cust_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создаем индекс по полю PlanTYear. 
-- DB Cursor: 
-- DB Local: 04:41
CREATE NONCLUSTERED INDEX [idxPlanTYear] ON [dbo].[test_CACHE_1]
(
	[PlanTYear] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

-- Создаем индекс для связи с таблицей Market. 
-- DB Cursor: 4:39
CREATE NONCLUSTERED INDEX [idxMarket] ON [dbo].[test_CACHE_1]
(
	[Market_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

ALTER TABLE [dbo].[db_lpu] ADD PRIMARY KEY CLUSTERED 
(
	[cust_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO

ALTER TABLE [dbo].[db_lpu_employee] ADD PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO
CREATE NONCLUSTERED INDEX [idx_lpu_employee_lpu_id] ON [dbo].[db_lpu_employee]
(
	[lpu_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO
CREATE NONCLUSTERED INDEX [idx_lpu_employee_employee_id] ON [dbo].[db_lpu_employee]
(
	[employee_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
GO