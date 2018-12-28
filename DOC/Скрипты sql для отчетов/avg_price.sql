select pvt.market_id as id, pvt.market_name as Nm, pvt.Contract_tradeNx as tradeNx
    ,[1906],[2014],[2015],[2016],[2017],[2018],[2019],[2020],[2021],[2022],[2023],[2024],[2025]
    from
    (
        select distinct s.market_id, s.market_name, isnull(Contract_tradeNx, -2) as Contract_tradeNx, PlanTYear, 
        avg(Contract_Summa) as Contract_AVG
        from [dbo].[org_CACHE_1] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_WinnerOrg w on s.Winner_ID = w.id
        left join db_TradeNR t on s.Contract_TradeNx = t.id
        left join db_lpu_employee e on s.cust_id=e.lpu_id
        --where s.Contract_TradeNx > 0
        where 1=1 
        and s.PlanTYear in (1906,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025) 
        and s.market_id in (14,11,3,10,4,2,1,17) 
        and s.StatusT_ID in (7,4,5,6,2) 
         and e.employee_id in (5,6,7,8,9,10,11,12,13)     
     	group by s.market_id, s.market_name, isnull(Contract_tradeNx, -2), PlanTYear
    ) m
    PIVOT
    (
    avg(Contract_AVG)
    for PlanTYear in ([1906],[2014],[2015],[2016],[2017],[2018],[2019],[2020],[2021],[2022],[2023],[2024],[2025])
    ) as pvt
left join db_TradeNR t on pvt.Contract_TradeNx = t.id
where pvt.market_id is not null and pvt.market_name is not Null
order by pvt.market_name