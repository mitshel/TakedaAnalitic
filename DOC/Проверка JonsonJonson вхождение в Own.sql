select c1.*, m1.id, m1.name, b1.own, m2.id, m2.name, b2.own, b2.market_id
from (
select null as intlName_id, 1802 as innNx, NULL as TradeName_ID, 17241 as TradeNx
) c1
left join db_market_innrs b1 on isNull(c1.IntlName_ID,c1.InnNx)=b1.innr_id
left join db_market m1 on ((m1.id=b1.market_id) and m1.org_id=9)
left join db_market_tmnrs b2 on isNull(c1.TradeName_ID,c1.TradeNx)=b2.tradenr_id
left join db_market m2 on ((m2.id=b2.market_id) and m2.org_id=9)
where (m1.id is not null or m2.id is not null)


select * from db_tradeNr where name like 'Маб%'
-- Стелара% = 34519
-- 17241	Мабтера

select * from db_InNr where name like 'Ритуксим%'
-- Устекин% = 52610
-- 1802	Ритуксимаб

select * from db_market where id=18

-- сравнение own
select IIF(    IIF(m1.id is null,0,isnull(b1.own,0))>0
    or  IIF(m2.id is null,0,isnull(b2.own,0))>0, 1,0) as real_own,
	c1.market_own,
	i1.name as MNNname, i2.name as TNname, c1.*
	from org_cache_9 c1
left join db_market_innrs b1 on isNull(c1.Contract_innNx,c1.Order_innNx)=b1.innr_id
left join db_innr i1 on b1.innr_id=i1.id
left join db_market m1 on ((m1.id=b1.market_id) and m1.org_id=9)
left join db_market_tmnrs b2 on isNull(c1.Contract_TradeNx,c1.Order_TradeNx)=b2.tradenr_id
left join db_tradenr i2 on b2.tradenr_id=i2.id
left join db_market m2 on ((m2.id=b2.market_id) and m2.org_id=9)
where
IIF(    IIF(m1.id is null,0,isnull(b1.own,0))>0
    or  IIF(m2.id is null,0,isnull(b2.own,0))>0, 1,0) <> c1.market_own

select count(*) from org_cache_9

-- update own
update  c1
set c1.market_own = IIF(    IIF(m1.id is null,0,isnull(b1.own,0))>0
    or  IIF(m2.id is null,0,isnull(b2.own,0))>0, 1,0)
from org_cache_9 c1
left join db_market_innrs b1 on isNull(c1.Contract_innNx,c1.Order_innNx)=b1.innr_id
left join db_market m1 on ((m1.id=b1.market_id) and m1.org_id=9)
left join db_market_tmnrs b2 on isNull(c1.Contract_TradeNx,c1.Order_TradeNx)=b2.tradenr_id
left join db_market m2 on ((m2.id=b2.market_id) and m2.org_id=9)
where
IIF(    IIF(m1.id is null,0,isnull(b1.own,0))>0
    or  IIF(m2.id is null,0,isnull(b2.own,0))>0, 1,0) <> c1.market_own
go

