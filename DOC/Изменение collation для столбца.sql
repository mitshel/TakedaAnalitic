ALTER TABLE dbo.org_CACHE_1 ALTER COLUMN budgets_id
            char(1)COLLATE database_default NULL;
/****** Object:  Index [idx_1_Budgets_ID]    Script Date: 23.12.2018 18:50:12 ******/
CREATE NONCLUSTERED INDEX [idx_1_Budgets_ID] ON [dbo].[org_CACHE_1]
(
	[Budgets_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

