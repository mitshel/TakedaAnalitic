create table #avg_test(data numeric)

insert into #avg_test(data) values(2)
insert into #avg_test(data) values(2)
insert into #avg_test(data) values(4)
insert into #avg_test(data) values(4)
insert into #avg_test(data) values(null)

select * from #avg_test

select avg(data) from #avg_test

drop table #avg_test