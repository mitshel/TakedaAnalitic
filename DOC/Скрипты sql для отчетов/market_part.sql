select CASE WHEN nn.market_id is NULL THEN 'хрнцн' ELSE mt.name END as name, nn.* from 
(
	select market_id, grouping(market_id) as gr,
	sum([2015-1]) as [2015-1], isnull(sum([2015-2]),0) as [2015-2], IIF(sum([2015-1]) is null,'-',cast(isnull(cast(sum([2015-2])/sum([2015-1])*100 as int),0) as varchar)+'%') as [2015-3], 
	sum([2016-1]) as [2016-1], isnull(sum([2016-2]),0) as [2016-2], IIF(sum([2015-1]) is null,'-',cast(isnull(cast(sum([2016-2])/sum([2016-1])*100 as int),0) as varchar)+'%') as [2016-3], 
	sum([2017-1]) as [2017-1], isnull(sum([2017-2]),0) as [2017-2], IIF(sum([2015-1]) is null,'-',cast(isnull(cast(sum([2017-2])/sum([2017-1])*100 as int),0) as varchar)+'%') as [2017-3], 
	sum([2018-1]) as [2018-1], isnull(sum([2018-2]),0) as [2018-2], IIF(sum([2015-1]) is null,'-',cast(isnull(cast(sum([2018-2])/sum([2018-1])*100 as int),0) as varchar)+'%') as [2018-3], 
	sum([2019-1]) as [2019-1], isnull(sum([2019-2]),0) as [2019-2], IIF(sum([2015-1]) is null,'-',cast(isnull(cast(sum([2019-2])/sum([2019-1])*100 as int),0) as varchar)+'%') as [2019-3]
	from
		(
			select market_id, cast(PlanTYear as varchar)+'-1' as PlanTYear, sum(Order_summa) as Summa
			from org_cache_1
			where PlanTYear is not null
			group by market_id, PlanTYear
			union all
			select market_id, cast(PlanTYear as varchar)+'-2' as PlanTYear, sum(Order_summa) as Summa
			from org_cache_1
			where PlanTYear is not null and market_own=1
			group by market_id, PlanTYear
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
	group by
	rollup (market_id)
) nn
left join db_market mt on mt.id=nn.market_id
order by gr, mt.name
