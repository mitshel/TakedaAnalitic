# Доля по рынкам
q_mparts = """
{% autoescape off %}
select CASE WHEN nn.market_id is NULL THEN 'ИТОГО' ELSE mt.name END as name, nn.* from 
(
	select market_id, grouping(market_id) as gr
	{% for y in years %},sum([{{y}}-1]) as [{{y}}-1], isnull(sum([{{y}}-2]),0) as [{{y}}-2], IIF(isnull(sum([{{y}}-1]),0)=0,'-',cast(isnull(cast(sum([{{y}}-2])/sum([{{y}}-1])*100 as int),0) as varchar)+'%') as [{{y}}-3]{% endfor %}
	from
		(
            select market_id, cast(PlanTYear as varchar)+'-1' as PlanTYear, sum({{ market_type_prefix }}summa) as Summa
            from [dbo].[org_CACHE_{{org_id}}] s
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_WinnerOrg w on s.Winner_ID = w.id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            left join db_lpu_employee e on s.cust_id=e.lpu_id
            where PlanTYear is not null 
            {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
            {% if markets %}and s.market_id in ({{markets}}) {% endif %}
            {% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
            {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if winrs_in %}and {{winrs_in}} {% endif %} 
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}                    
            group by market_id, PlanTYear
            
            union all
            select market_id, cast(PlanTYear as varchar)+'-2' as PlanTYear, sum({{ market_type_prefix }}summa) as Summa
            from [dbo].[org_CACHE_{{org_id}}] s
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_WinnerOrg w on s.Winner_ID = w.id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            left join db_lpu_employee e on s.cust_id=e.lpu_id
            where PlanTYear is not null and market_own=1
            {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
            {% if markets %}and s.market_id in ({{markets}}) {% endif %}
            {% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
            {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if winrs_in %}and {{winrs_in}} {% endif %} 
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}             
            group by market_id, PlanTYear          
		) m
		PIVOT
		(
			sum(Summa) for PlanTYear in (
			{% for y in years %}[{{y}}-1], [{{y}}-2]{% if not forloop.last %},{% endif %}{% endfor %})
		) as pvt
	group by
	rollup (market_id)
) nn
left join db_market mt on mt.id=nn.market_id
--order by gr, mt.name
{% endautoescape %}  
"""

q_mparts_count = """
select count(*) from db_market s where s.org_id = {{org_id}}
{% if markets %}and s.id in ({{markets}}) {% endif %}
"""

q_lparts = """
{% autoescape off %}
select CASE WHEN nn.cust_id is NULL THEN 'ИТОГО' ELSE l.Org_CustNm END as name, nn.* from 
(
	select cust_id
	{% for y in years %},isnull([{{y}}-1],0) as [{{y}}-1], isnull([{{y}}-2],0) as [{{y}}-2], IIF(isnull([{{y}}-1],0)=0,'-',cast(isnull(cast([{{y}}-2]/[{{y}}-1]*100 as int),0) as varchar)+'%') as [{{y}}-3]
	{% endfor %}
	from
		(
            select s.cust_id, cast(PlanTYear as varchar)+'-1' as PlanTYear, sum({{ market_type_prefix }}summa) as Summa
            from [dbo].[org_CACHE_{{org_id}}] s
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_WinnerOrg w on s.Winner_ID = w.id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            left join db_lpu_employee e on s.cust_id=e.lpu_id
            where PlanTYear is not null 
            {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
            {% if markets %}and s.market_id in ({{markets}}) {% endif %}
            {% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
            {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if winrs_in %}and {{winrs_in}} {% endif %} 
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}                    
            group by s.cust_id, PlanTYear
            
            union all
            select s.cust_id, cast(PlanTYear as varchar)+'-2' as PlanTYear, sum({{ market_type_prefix }}summa) as Summa
            from [dbo].[org_CACHE_{{org_id}}] s
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_WinnerOrg w on s.Winner_ID = w.id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            left join db_lpu_employee e on s.cust_id=e.lpu_id
            where PlanTYear is not null and market_own=1
            {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
            {% if markets %}and s.market_id in ({{markets}}) {% endif %}
            {% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
            {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if winrs_in %}and {{winrs_in}} {% endif %} 
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}             
            group by s.cust_id, PlanTYear          
		) m
		PIVOT
		(
			sum(Summa) for PlanTYear in (
			{% for y in years %}[{{y}}-1], [{{y}}-2]{% if not forloop.last %},{% endif %}{% endfor %})
		) as pvt
) nn
left join db_lpu l on l.cust_id=nn.cust_id
{% if icontains %}where l.Org_CustNm like '%{{ icontains }}%' {% endif %}
--order by [2018-1] desc, l.Org_CustNm
{% endautoescape %} 
"""

q_lparts_count = """
{% autoescape off %}
select COUNT_BIG(DISTINCT s.cust_id) from [dbo].[org_CACHE_{{org_id}}] s 
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_WinnerOrg w on s.Winner_ID = w.id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            left join db_lpu_employee e on s.cust_id=e.lpu_id
            where PlanTYear is not null 
            {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
            {% if markets %}and s.market_id in ({{markets}}) {% endif %}
            {% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
            {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if winrs_in %}and {{winrs_in}} {% endif %} 
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %} 
            {% if icontains %}and l.Org_CustNm like '%{{ icontains }}%' {% endif %}            
{% endautoescape %}
"""

# Конкурентный анализ
#
q_competitions_lpu = """
{% autoescape off %}
select l.Org_CustINN as ext, l.Org_CustNm as Nm, CASE WHEN tradeNX is NULL THEN 'ИТОГО' ELSE t.name END as name, nn.* from (
select pvt.cust_id as id, pvt.{{ market_type_prefix }}tradeNx as tradeNx, grouping(pvt.{{ market_type_prefix }}tradeNx) as gr
    {% for y in years %},sum([{{y}}]) as [{{y}}]{% endfor %}
    from
    (
        select distinct isnull(s.Lotspec_ID,0) as Lotspec_ID, s.cust_id, isnull({{ market_type_prefix }}tradeNx, -2) as {{ market_type_prefix }}tradeNx, PlanTYear, {{ market_type_prefix }}Summa
        from [dbo].[org_CACHE_{{org_id}}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_WinnerOrg w on s.Winner_ID = w.id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        left join db_lpu_employee e on s.cust_id=e.lpu_id
        --where s.{{ market_type_prefix }}TradeNx > 0
        where 1=1 
        {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
        {% if markets %}and s.market_id in ({{markets}}) {% endif %}
        {% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
        {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if winrs_in %}and {{winrs_in}} {% endif %} 
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if icontains %}and l.Org_CustNm like '%{{ icontains }}%' {% endif %}
    ) m
    PIVOT
    (
    sum({{ market_type_prefix }}Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
group by
rollup (pvt.cust_id, pvt.{{ market_type_prefix }}tradeNx)
) nn    
left join db_lpu l on nn.id = l.cust_id
left join db_TradeNR t on nn.TradeNx = t.id
where nn.id is not null
--order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, l.Org_CustNm, gr, t.name
{% endautoescape %}  
"""

q_competitions_market = """
{% autoescape off %}
select CASE WHEN tradeNX is NULL THEN 'ИТОГО' ELSE t.name END as name, nn.* from (
select pvt.market_id as id, pvt.market_name as Nm, pvt.{{ market_type_prefix }}tradeNx as tradeNx, grouping(pvt.{{ market_type_prefix }}tradeNx) as gr 
    {% for y in years %},sum([{{y}}]) as [{{y}}]{% endfor %}
    from
    (
        select distinct isnull(s.Lotspec_ID,0) as Lotspec_ID, s.market_id, s.market_name, isnull({{ market_type_prefix }}tradeNx, -2) as {{ market_type_prefix }}tradeNx, PlanTYear, {{ market_type_prefix }}Summa from [dbo].[org_CACHE_{{org_id}}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_WinnerOrg w on s.Winner_ID = w.id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        left join db_lpu_employee e on s.cust_id=e.lpu_id
        --where s.{{ market_type_prefix }}TradeNx > 0
        where 1=1 
        {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
        {% if markets %}and s.market_id in ({{markets}}) {% endif %}
        {% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
        {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if winrs_in %}and {{winrs_in}} {% endif %} 
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if icontains %}and s.market_name like '%{{ icontains }}%' {% endif %}
    ) m
    PIVOT
    (
    sum({{ market_type_prefix }}Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
group by
rollup (pvt.market_id, pvt.market_name, pvt.{{ market_type_prefix }}tradeNx)
) nn    
left join db_TradeNR t on nn.TradeNx = t.id
where nn.id is not null and nn.Nm is not Null
--order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, l.Org_CustNm, gr, t.name
{% endautoescape %}  
"""

q_employees = """
{% autoescape off %}
with tree as 
(
select a1.id, a1.name, a1.parent_id, a1.org_id, a1.istarget 
from db_employee a1
left join db_employee_users a2 on a1.id=a2.employee_id
left join auth_user a3 on a2.user_id=a3.id
where a3.username = '{{username}}'
--where a1.org_id = '{{org_id}}' 
union all
select a.id, a.name, a.parent_id, a.org_id, a.istarget from db_employee a 
inner join tree t on t.id = a.parent_id and a.org_id=t.org_id
)
select distinct {{ fields }} from tree 
where istarget=1 
{% endautoescape %} 
"""

q_markets = """
{% autoescape off %}
select {{fields}} from db_market a where org_id={{org_id}} 
{% endautoescape %} 
"""

q_markets_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_market a
inner join org_CACHE_{{ org_id }} b on a.id=b.market_id and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% if org_id %}where a.org_id = {{ org_id }} {% endif %}
{% endautoescape %} 
"""

q_years_hs = """
{% autoescape off %}
select distinct {{ fields }} from org_CACHE_{{ org_id }} a
{% if employee_in %}inner join db_lpu_employee e on a.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
where a.PlanTYear is not Null and a.cust_id is Not Null
{% endautoescape %} 
"""

q_status = """
{% autoescape off %}
select distinct {{fields}} from db_statusT a 
{% endautoescape %} 
"""

q_status_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_statusT a
inner join org_CACHE_{{ org_id }} b on a.id=b.statusT_ID and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% endautoescape %} 
"""

q_innr_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_innr a
inner join org_CACHE_{{ org_id }} b on a.id=b.Order_innNx and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% if market_in %}inner join db_market_innrs m on a.id=m.innr_id and {{ market_in }} {% endif %}
{% if name__icontains %} where name like '%{{ name__icontains }}%'{% endif %}
{% endautoescape %} 
"""

q_tradenr_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_tradenr a
inner join org_CACHE_{{ org_id }} b on a.id=b.Order_tradeNx and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% if market_in %}inner join db_market_tmnrs m on a.id=m.tradenr_id and {{ market_in }} {% endif %}
{% if name__icontains %} where name like '%{{ name__icontains }}%'{% endif %}
{% endautoescape %} 
"""

q_winner_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_winnerorg a
inner join org_CACHE_{{ org_id }} b on a.id=b.winner_id and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% if name__icontains %} where name like '%{{ name__icontains }}%'{% endif %}
{% endautoescape %} 
"""

q_lpu_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_lpu a
inner join org_CACHE_{{ org_id }} b on a.cust_id=b.cust_id and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% if name__icontains %} where a.Org_CustNm like '%{{ name__icontains }}%'{% endif %}
{% endautoescape %} 
"""

q_sales_year = """
{% autoescape off %}
select b.name as market_name, PlanTYear as iid, Sum(Order_Summa)/1000000 as product_cost_sum
from org_CACHE_{{ org_id }} a
left join db_market b on a.market_id=b.id and org_id={{ org_id }}
{% if employee_in %}inner join db_lpu_employee e on a.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
where PlanTYear is not NULL and a.cust_id<>0
{% if years_in %}and {{ years_in }} {% endif %}
{% if markets_in %}and {{ markets_in }} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %}  
group by b.name, PlanTYear
{% endautoescape %} 
"""

q_sales_month = """
{% autoescape off %}
select b.name as market_name, month(ProcDt) as mon, Sum(Order_Summa)/1000000 as product_cost_sum, count(*) as product_count
from org_CACHE_{{ org_id }} a
left join db_market b on a.market_id=b.id and org_id={{ org_id }}
{% if employee_in %}inner join db_lpu_employee e on a.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
where PlanTYear is not NULL and a.cust_id<>0
{% if years_in %}and {{ years_in }} {% endif %}
{% if markets_in %}and {{ markets_in }} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %}    
group by b.name, month(ProcDt)
{% endautoescape %} 
"""