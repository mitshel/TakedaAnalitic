select c1.*, m1.name, b1.own, m2.name, b2.own
from (
select 1 as intlName_id, 1802 as innNx, NULL as TradeName_ID, 17241 as TradeNx
) c1
left join db_market_innrs b1 on isNull(c1.IntlName_ID,c1.InnNx)=b1.innr_id
left join db_market m1 on ((m1.id=b1.market_id) and m1.org_id=9)
left join db_market_tmnrs b2 on isNull(c1.TradeName_ID,c1.TradeNx)=b2.tradenr_id
left join db_market m2 on ((m2.id=b2.market_id) and m2.org_id=9)
where (m1.id is not null or m2.id is not null)


select * from db_tradeNr where name like '���%'
-- �������% = 34519
-- 17241	�������

select * from db_InNr where name like '��������%'
-- �������% = 52610
-- 1802	����������