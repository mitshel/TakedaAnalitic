select count(*) from  (
select nn.id from 
(
	select pvt.budgets_id as id, pvt.cust_id
    from
    ( 
		select distinct s.cust_id, s.budgets_id, s.PlanTYear from [dbo].[org_CACHE_1] s
	) pvt	
	group by
	rollup (pvt.budgets_id, pvt.cust_id)
) nn    
where nn.id is not null
) aa
