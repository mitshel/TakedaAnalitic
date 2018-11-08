# Конкурентный анализ
#
q_competitions = """
select l.Org_CustINN, l.Org_CustNm, pvt.cust_id, pvt.tradeNx, t.name, 
    {% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %}
    from
    (
        select s.cust_id, tradeNx, PlanTYear, TenderPrice from [dbo].[test_CACHE_1] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_TradeNR t on s.TradeNx = t.id
        left join db_lpu_employee e on s.cust_id=e.lpu_id
        where 1=1 
        {% if years %}and s.PlanTYear in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{% endfor %}) {% endif %}
        {% if markets %}and s.market_id in ({{markets}}) {% endif %}
        {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
    ) m
    PIVOT
    (
    sum(TenderPrice)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
    left join db_lpu l on pvt.cust_id = l.cust_id
    left join db_TradeNR t on pvt.TradeNx = t.id
    order by pvt.cust_id, pvt.tradeNx
"""