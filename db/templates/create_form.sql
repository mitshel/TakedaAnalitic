
--
-- НОРМАЛИЗАЦИЯ ЛЕКАРСТВЕННЫХ ФОРМ
--

CREATE TABLE [dbo].[org_FORM_{{org_id}}](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[name] [varchar](256) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

insert into [dbo].[org_FORM_{{org_id}}](name) select distinct isnull(RTRIM(LTRIM(Contract_Form)),'') from org_Contract_{{org_id}}
alter table org_Contract_{{org_id}} add Contract_Form_id bigint

update u
set u.Contract_Form_id=t.id
from org_CACHE_{{org_id}} u
left join org_FORM_{{org_id}} t on isnull(RTRIM(LTRIM(u.Contract_Form)),'') = t.name

update org_FORM_{{org_id}} set name=' НЕТ ДАННЫХ' where name = ''

CREATE NONCLUSTERED INDEX [idx_{{org_id}}_Contract_Form_id] ON [dbo].[org_Contract_{{org_id}}]
(
	[Contract_Form_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)


update db_org set sync_status=0, db_version='{{ db_version }}', last_sync_dt = GETDATE() where id={{ org_id }}

