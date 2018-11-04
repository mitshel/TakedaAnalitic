----------- 
----------- 1. Устранить в перечне ЛПУ, учреждения содержащие символ одинарной кавычки:
-----------
select * from db_lpu a
left join db_lpu_employee b on a.cust_id=b.lpu_id
where Org_CustNm like '%''%'
