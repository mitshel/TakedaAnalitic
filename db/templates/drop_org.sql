update db_org set sync_status=2 where id={{ org_id }}

IF OBJECT_ID('dbo.org_CACHE_{{org_id}}', 'U') IS NOT NULL
   drop table org_CACHE_{{org_id}}

IF OBJECT_ID('dbo.org_DOSAGE_{{org_id}}}', 'U') IS NOT NULL
   drop table org_DOSAGE_{{org_id}}

IF OBJECT_ID('dbo.org_FORM_{{org_id}}', 'U') IS NOT NULL
   drop table org_FORM_{{org_id}}
