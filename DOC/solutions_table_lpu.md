## Решения по таблице лечебных учреждений (LPU)

Таблица LPU формируется из таблицы ComplexRpt_CACHE, поля Cust_ID, Org_CustINN, Org_CustNm.
Ключевым полем для организации считаем Cust_ID
- Дубликаты Cust_ID удаляются, оставляем строки с непустым Org_CustINN, Org_CustNm, или выбираем строки с наибольшей длиной

### Скрипт для формирования таблицы LPU
Select DISTINCT Cust_ID, Org_CustINN, Org_CustNm into #lpu_tmp from ComplexRpt_CACHE where Cust_id is not null
go

drop table lpu
go
Create Table Lpu(cust_id int not null, Org_CustINN varchar(12) null, Org_CustNm varchar(2000) null)
go
ALTER TABLE Lpu ADD CONSTRAINT PK_Lpu PRIMARY KEY (cust_id)
go


DECLARE @id int
DECLARE @inn varchar(16)
DECLARE @name varchar(2000)
DECLARE @cid int
DECLARE @cinn varchar(16)
DECLARE @cname varchar(2000)

DECLARE cur CURSOR FOR Select DISTINCT Cust_ID, isnull(Org_CustINN,'') as Org_CustINN, isnull(Org_CustNm,'') as Org_CustNm from #lpu_tmp order by Cust_ID
OPEN cur

FETCH NEXT FROM cur INTO @id, @inn, @name
set @cid = @id
set @cinn = @inn
set @cname = @name

WHILE @@FETCH_STATUS = 0
BEGIN
    if @cid <> @id BEGIN
       insert into LPU(Cust_ID, Org_CustINN, Org_CustNm) VALUES(@cid,@cinn,@cname)
       set @cid = @id
       set @cinn = @inn
       set @cname = @name
    END 
    ELSE BEGIN
       IF LEN(@inn)>LEN(@cinn) BEGIN set @cinn=@inn; set @cname=@name; END
       IF LEN(@inn)=LEN(@cinn) BEGIN 
          IF LEN(@name)>LEN(@cname) BEGIN set @cinn=@inn; set @cname=@name END;
       END
    END
	FETCH NEXT FROM cur INTO @id, @inn, @name
END
CLOSE cur
DEALLOCATE cur
GO

drop table #lpu_tmp
go