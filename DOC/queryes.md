-- Создание UnManaged таблиц ДО MIGRATIONS
select * into BIMonitor..test_CACHE_1 from CursorTest..test_CACHE_1
select * into BIMonitor..db_lpu from CursorTest..db_lpu
select * into BIMonitor..db_lpu_employee from CursorTest..db_lpu_employee

-- Наполнение Managed таблиц после MIGRATIONS
set IDENTITY_INSERT db_org ON
insert into BIMonitor..db_org(id,name) select * from CursorTest..db_org
set IDENTITY_INSERT db_org OFF 
go
set IDENTITY_INSERT db_employee ON
insert into BIMonitor..db_employee(id,name,parent_id,org_id) select * from CursorTest..db_employee
set IDENTITY_INSERT db_employee OFF 
go
set IDENTITY_INSERT db_market ON
insert into BIMonitor..db_market(id,name,org_id) select * from CursorTest..db_market
set IDENTITY_INSERT db_market OFF 
go
set IDENTITY_INSERT db_marketmnn ON
insert into BIMonitor..db_marketmnn(id,mnn_id, market_id) select * from CursorTest..db_marketmnn
set IDENTITY_INSERT db_marketmnn OFF 
go
set IDENTITY_INSERT db_markettm ON
insert into BIMonitor..db_markettm(id,tm_id,market_id) select * from CursorTest..db_markettm
set IDENTITY_INSERT db_markettm OFF 
go


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


-- Конкурентный анализ
--
select l.Org_CustINN, l.Org_CustNm, pvt.cust_id, pvt.tradeNx, t.name, [2015], [2016], [2017], [2018], [2019], [2020], [2021], [2022]
from
(
select cust_id, tradeNx, PlanTYear, TenderPrice from [dbo].[test_CACHE_1]
) m
PIVOT
(
sum(TenderPrice)
for PlanTYear in ([2015],[2016],[2017],[2018],[2019],[2020],[2021],[2022])
) as pvt
left join db_lpu l on pvt.cust_id = l.cust_id
left join db_TradeNR t on pvt.TradeNx = t.id
order by pvt.cust_id, pvt.tradeNx

select * from db_lpu 