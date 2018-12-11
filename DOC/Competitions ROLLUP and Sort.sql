select l.Org_CustINN as ext, l.Org_CustNm as Nm, CASE WHEN tradeNX is NULL THEN 'хрнцн' ELSE t.name END as name, nn.* from (
select pvt.cust_id as id, pvt.Order_tradeNx as tradeNx, grouping(pvt.Order_tradeNx) as gr,
    sum([2014]) as [2014] ,sum([2015]) as [2015],sum([2016]) as [2016],sum([2017]) as [2017],sum([2018]) as [2018],sum([2019]) as [2019],sum([2020]) as [2020],sum([2021]) as [2021],sum([2022]) as [2022],
	sum([2023]) as [2023],sum([2024]) as [2024],sum([2025]) as [2025]
    from
    (
        select s.cust_id, isnull(Order_tradeNx,-2) as Order_tradeNx, PlanTYear, Summa from [dbo].[org_CACHE_1] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_WinnerOrg w on s.Winner_ID = w.id
        left join db_TradeNR t on s.Order_TradeNx = t.id
        left join db_lpu_employee e on s.cust_id=e.lpu_id
        --where s.Order_TradeNx > 0
        where 1=1 
        and s.PlanTYear in (2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025) 
        and s.market_id in (3,4,2,1) 
        and s.StatusT_ID in (7,4,5,6,2)     
    ) m
    PIVOT
    (
    sum(Summa)
    for PlanTYear in ([2014],[2015],[2016],[2017],[2018],[2019],[2020],[2021],[2022],[2023],[2024],[2025])
    ) as pvt
group by
rollup (pvt.cust_id, pvt.Order_tradeNx)
) nn
left join db_lpu l on nn.id = l.cust_id
left join db_TradeNR t on nn.TradeNx = t.id
where nn.id is not null
order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, l.Org_CustNm, gr, t.name