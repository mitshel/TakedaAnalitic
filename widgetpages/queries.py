# Конкурентный анализ
#
q_competitions = """
{% autoescape off %}
select pvt.cust_id as id, l.Org_CustINN, l.Org_CustNm, pvt.tradeNx, t.name 
    {% for y in years %},[{{y}}]{% endfor %}
    from
    (
        select s.cust_id, tradeNx, PlanTYear, TenderPrice from [dbo].[test_CACHE_1] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_WinnerOrg w on s.Winner_ID = w.id
        left join db_TradeNR t on s.TradeNx = t.id
        left join db_lpu_employee e on s.cust_id=e.lpu_id
        where s.TradeNx > 0
        {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
        {% if markets %}and s.market_id in ({{markets}}) {% endif %}
        {% if status %}and s.StatusT_ID in ({{status}}) {% endif %}
        {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if winrs_in %}and {{winrs_in}} {% endif %} 
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if lpu__icontains %}and l.Org_CustNm like '%{{ lpu__icontains }}%' {% endif %}
    ) m
    PIVOT
    (
    sum(TenderPrice)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
    left join db_lpu l on pvt.cust_id = l.cust_id
    left join db_TradeNR t on pvt.TradeNx = t.id
{% endautoescape %}  
"""