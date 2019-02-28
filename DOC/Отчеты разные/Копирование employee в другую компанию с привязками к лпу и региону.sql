select * from db_org
select * from db_employee where org_id=4
select * from db_lpu_employee 
select * from db_region_employee 


-- Копирование employee с указанным ИД в новую организацию
-- DEMO 15, 16,54,55,56,57,58
declare @user_id int = 55
declare @new_org_id int = 19

declare @scope_name varchar(64)
declare @scope_target bit
declare @new_user_id int

select @scope_name=name,  @scope_target=istarget from db_employee where id=@user_id
insert into db_employee(name, istarget, org_id) values(@scope_name, @scope_target, @new_org_id)
set @new_user_id = @@IDENTITY
insert into db_lpu_employee(employee_id, lpu_id) select @new_user_id, lpu_id from db_lpu_employee where employee_id=@user_id
insert into db_region_employee(employee_id, region_id) select @new_user_id, region_id from db_region_employee where employee_id=@user_id
go
