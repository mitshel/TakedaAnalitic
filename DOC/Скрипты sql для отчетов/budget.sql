select t.name as name, CASE WHEN nn.cust_id is NULL THEN t.name ELSE l.Org_CustNm END as nm, isnull(l.Org_CustINN, '') as ext, nn.*, 
       (0 + [2015] + [2016] + [2017] + [2018] + [2019]) as Total
from (
select pvt.cust_id, pvt.budgets_id as id, grouping(pvt.cust_id) as gr
    --{% for y in years %},sum([{{y}}]) as [{{y}}]{% endfor %}
	,isnull(sum([2015]),0) as [2015], isnull(sum([2016]),0) as [2016], isnull(sum([2017]),0) as [2017], isnull(sum([2018]),0) as [2018], sum([2019]) as [2019]
    from
    (
        select distinct s.cust_id, s.budgets_id, PlanTYear, isnull(Order_Summa,0) as Summa
        from [dbo].[org_CACHE_1] s
        --left join db_lpu l on s.cust_id = l.cust_id
        --left join db_WinnerOrg w on s.Winner_ID = w.id
        --left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        --left join db_lpu_employee e on s.cust_id=e.lpu_id      
        --where 1=1 
        --{% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
        --{% if markets %}and s.market_id in ({{markets}}) {% endif %}
        --{% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
        --{% if targets %} and {{targets}} {% endif %}
        --{% if lpus_in %}and {{lpus_in}} {% endif %}    
        --{% if winrs_in %}and {{winrs_in}} {% endif %} 
        --{% if innrs_in %}and {{innrs_in}} {% endif %}
        --{% if trnrs_in %}and {{trnrs_in}} {% endif %}
        --{% if icontains %}and l.Org_CustNm like '%{{ icontains }}%' {% endif %}
		--group by s.cust_id, s.budgets_id, PlanTYear
    ) m
    PIVOT
    (
    sum(Summa)
	for PlanTYear in ([2015],[2016],[2017],[2018],[2019])
    --for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
group by
rollup (pvt.budgets_id, pvt.cust_id)
) nn    
left join db_lpu l on nn.cust_id = l.cust_id
left join db_budgets t on nn.id = t.id
where nn.id is not null
order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, t.name, gr desc, l.Org_CustNm