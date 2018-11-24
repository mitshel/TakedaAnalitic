# Конкурентный анализ
#
q_competitions_lpu = """
{% autoescape off %}
select pvt.cust_id as id, l.Org_CustINN as ext, l.Org_CustNm as Nm, pvt.{{ market_type_prefix }}tradeNx as tradeNx, t.name 
    {% for y in years %},[{{y}}]{% endfor %}
    from
    (
        select s.cust_id, {{ market_type_prefix }}tradeNx, PlanTYear, Summa from [dbo].[org_CACHE_{{org_id}}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_WinnerOrg w on s.Winner_ID = w.id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        left join db_lpu_employee e on s.cust_id=e.lpu_id
        where s.{{ market_type_prefix }}TradeNx > 0
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
    sum(Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
    left join db_lpu l on pvt.cust_id = l.cust_id
    left join db_TradeNR t on pvt.{{ market_type_prefix }}TradeNx = t.id
{% endautoescape %}  
"""

q_competitions_market = """
{% autoescape off %}
select pvt.market_id as id, pvt.market_name as Nm, pvt.{{ market_type_prefix }}tradeNx as tradeNx, t.name 
    {% for y in years %},[{{y}}]{% endfor %}
    from
    (
        select s.market_id, s.market_name, {{ market_type_prefix }}tradeNx, PlanTYear, Summa from [dbo].[org_CACHE_{{org_id}}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_WinnerOrg w on s.Winner_ID = w.id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        left join db_lpu_employee e on s.cust_id=e.lpu_id
        where s.{{ market_type_prefix }}TradeNx > 0
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
    sum(Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
    left join db_TradeNR t on pvt.{{ market_type_prefix }}TradeNx = t.id
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
inner join org_CACHE_{{ org_id }} b on a.id=b.innNx and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% if market_in %}inner join db_market_innrs m on a.id=m.innr_id and {{ market_in }} {% endif %}
{% endautoescape %} 
"""

q_tradenr_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_tradenr a
inner join org_CACHE_{{ org_id }} b on a.id=b.tradeNx and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% if market_in %}inner join db_market_tmnrs m on a.id=m.tradenr_id and {{ market_in }} {% endif %}
{% endautoescape %} 
"""

q_winner_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_winnerorg a
inner join org_CACHE_{{ org_id }} b on a.id=b.winner_id and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% endautoescape %} 
"""

q_lpu_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_lpu a
inner join org_CACHE_{{ org_id }} b on a.cust_id=b.cust_id and b.cust_id<>0
{% if employee_in %}inner join db_lpu_employee e on b.cust_id=e.lpu_id and {{ employee_in }} {% endif %}
{% endautoescape %} 
"""

q_sales_year = """
{% autoescape off %}
select b.name as market_name, PlanTYear as iid, Sum(Summa)/1000000 as product_cost_sum
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
select b.name as market_name, month(ProcDt) as mon, Sum(Summa)/1000000 as product_cost_sum, count(*) as product_count
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