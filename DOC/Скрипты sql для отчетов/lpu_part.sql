select CASE WHEN nn.cust_id is NULL THEN 'хрнцн' ELSE l.Org_CustNm END as name, nn.* from 
(
	select cust_id,
	isnull([2015-1],0) as [2015-1], isnull([2015-2],0) as [2015-2], IIF([2015-1]=0,'-',cast(isnull(cast([2015-2]/[2015-1]*100 as int),0) as varchar)+'%') as [2015-3], 
	isnull([2016-1],0) as [2016-1], isnull([2016-2],0) as [2016-2], IIF([2016-1]=0,'-',cast(isnull(cast([2016-2]/[2016-1]*100 as int),0) as varchar)+'%') as [2016-3], 
	isnull([2017-1],0) as [2017-1], isnull([2017-2],0) as [2017-2], IIF([2017-1]=0,'-',cast(isnull(cast([2017-2]/[2017-1]*100 as int),0) as varchar)+'%') as [2017-3], 
	isnull([2018-1],0) as [2018-1], isnull([2018-2],0) as [2018-2], IIF([2018-1]=0,'-',cast(isnull(cast([2018-2]/[2018-1]*100 as int),0) as varchar)+'%') as [2018-3], 
	isnull([2019-1],0) as [2019-1], isnull([2019-2],0) as [2019-2], IIF([2019-1]=0,'-',cast(isnull(cast([2019-2]/[2019-1]*100 as int),0) as varchar)+'%') as [2019-3]
	from
		(
			select cust_id, cast(PlanTYear as varchar)+'-1' as PlanTYear, sum(Order_summa) as Summa
			from org_cache_1
			where PlanTYear is not null
			group by cust_id, PlanTYear
			union all
			select cust_id, cast(PlanTYear as varchar)+'-2' as PlanTYear, sum(Order_summa) as Summa
			from org_cache_1
			where PlanTYear is not null and market_own=1
			group by cust_id, PlanTYear
		) m
		PIVOT
		(
			sum(Summa) for PlanTYear in (
			[2015-1], [2015-2], 
			[2016-1], [2016-2],
			[2017-1], [2017-2], 
			[2018-1], [2018-2], 
			[2019-1], [2019-2])
		) as pvt
) nn
left join db_lpu l on l.cust_id=nn.cust_id
order by [2018-1] desc, l.Org_CustNm