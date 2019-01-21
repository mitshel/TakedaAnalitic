--
-- НОРМАЛИЗАЦИЯ ДОЗИРОВОК
--

CREATE TABLE [dbo].[org_DOSAGE_{{org_id}}](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[name] [varchar](128) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

insert into [dbo].[org_DOSAGE_{{org_id}}](name) select distinct isnull(RTRIM(LTRIM(Contract_Dosage)),'') from org_Contract_{{org_id}}
alter table org_Contract_{{org_id}} add Contract_Dosage_id bigint

update u
set u.Contract_Dosage_id=t.id
from org_Contract_{{org_id}} u
left join org_DOSAGE_{{org_id}} t on isnull(RTRIM(LTRIM(u.Contract_Dosage)),'') = t.name

update org_DOSAGE_{{org_id}} set name=' НЕТ ДАННЫХ' where name = ''

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_Dosage_id] ON [dbo].[org_Contract_{{org_id}}]
(
	[Contract_Dosage_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
