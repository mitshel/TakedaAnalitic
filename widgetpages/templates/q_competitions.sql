select l.Org_CustINN, l.Org_CustNm, pvt.cust_id, pvt.tradeNx, t.name, {{years}}
    from
    (
    select cust_id, tradeNx, PlanTYear, TenderPrice from [dbo].[test_CACHE_1]
    ) m
    PIVOT
    (
    sum(TenderPrice)
    for PlanTYear in ({{years}})
    ) as pvt
    left join db_lpu l on pvt.cust_id = l.cust_id
    left join db_TradeNR t on pvt.TradeNx = t.id
    left join db_lpu_employee e on pvt.cust_id=e.lpu_id
    where
    {% if years %}PlanYear in ({{years}}) {% endif %}
    {% if markets %}and market_id in ({{markets}}) {% endif %}
    {% if employees %}and e.employee_id in ({{employees}}) {% endif %}
    {% if lpus_in %}and {{lpus_in}} {% endif %}
    order by pvt.cust_id, pvt.tradeNx