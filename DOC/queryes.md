-- РЫНОК
--
-- Выборка сумм по рынкам, годам и привязанным организациям
select c.name as market, PlanTYear, sum(TenderPrice) from ComplexRpt_CACHE a
inner join lpu d on a.cust_id=d.cust_id 
inner join db_lpu_employee e on d.cust_id=e.lpu_id
left join db_marketmnn b1 on a.InnNx=b1.mnn_id
left join db_markettm b2 on a.TradeNx=b2.tm_id
inner join db_market c on ((c.id=b2.market_id) or (c.id=b1.market_id)) and (c.org_id=1)
where e.employee_id=14 or e.employee_id in (select id from db_employee where parent_id=14)
group by c.name, PlanTYear

-- Количество аукционов по дате выставления
--
-- Выборка сумм по рынкам, годам и привязанным организациям
select c.name as market, PlanTYear, sum(TenderPrice) from ComplexRpt_CACHE a
inner join lpu d on a.cust_id=d.cust_id 
inner join db_lpu_employee e on d.cust_id=e.lpu_id
left join db_marketmnn b1 on a.InnNx=b1.mnn_id
left join db_markettm b2 on a.TradeNx=b2.tm_id
inner join db_market c on ((c.id=b2.market_id) or (c.id=b1.market_id)) and (c.org_id=1)
where e.employee_id=14 or e.employee_id in (select id from db_employee where parent_id=14)
group by c.name, PlanTYear
