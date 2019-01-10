-- Заполняем справочник привязок регнионов к сотрудникам
delete from db_region_employee
go

insert into db_region_employee(employee_id, region_id)
select distinct a.id as employee_id, c.regcode as region_id from db_employee a
left join db_lpu_employee b on a.id=b.employee_id
left join db_lpu c on b.lpu_id=c.cust_id
where 
isnull(c.regcode,0) in (select reg_id from db_region)
and c.regcode is not null
go
-- Почему-то в базе данных ЛПУ содержится учрежденеи с кодом региона 90, которого не существует


--select distinct a.regcode, b.regnm from db_lpu a
--left join db_region b on a.regcode=b.reg_id

--select * from db_lpu where regcode = 90


