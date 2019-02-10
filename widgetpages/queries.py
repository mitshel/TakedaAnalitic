#
# For Database Version 0.10
#
fd_budgets_table =  {r'name':  {'title':'Бюджет', 'width':40},
                     r'nm':   {'title': 'Заказчик', 'width': 100},
                     r'cust_id': {'title': 'cust_id', 'width': 0, 'hide':1},
                     r'id':   {'title': 'mnn/tm id', 'width': 0, 'hide':1},
                     r'gr':   {'title': 'Итог', 'width': 5}
}

q_budgets_table = """
{% autoescape off %}
select t.name as name, CASE WHEN nn.cust_id is NULL THEN t.name ELSE l.Org_CustNm END as Nm, nn.*, 
       (0{% for y in years %}+[{{y}}]{% endfor %}) as total
from (
select pvt.cust_id, pvt.budgets_id as id, grouping(pvt.cust_id) as gr
    {% for y in years %},sum( isnull([{{y}}],0) ) as [{{y}}]{% endfor %}
	--,isnull(sum([2015]),0) as [2015], isnull(sum([2016]),0) as [2016], isnull(sum([2017]),0) as [2017], isnull(sum([2018]),0) as [2018], isnull(sum([2019]),0) as [2019]
    from
    (
        select distinct s.cust_id, s.budgets_id, PlanTYear, sum(isnull({{market_type_prefix }}Summa,0)) as Summa
        from [dbo].[org_{{market_type_prefix }}{{ org_id }}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        where PlanTYear is not null
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %}       
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}        
        {% if budgets_in %}and {{budgets_in}} {% endif %}
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}        
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if winrs_in %}and {{winrs_in}} {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %} 
        {% if own_select %}and {{own_select}} {% endif %}              
        {% if icontains %}and l.Org_CustNm like '%{{ icontains }}%' {% endif %}
        group by s.cust_id, s.budgets_id, PlanTYear
    ) m
    PIVOT
    (
    sum(Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
group by
rollup (pvt.budgets_id, pvt.cust_id)
) nn    
left join db_lpu l on nn.cust_id = l.cust_id
left join db_budgets t on nn.id = t.id
where nn.id is not null
--order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, t.name, gr desc, l.Org_CustNm
{% endautoescape %}  
"""

q_budgets_table_count = """
{% autoescape off %}
select COUNT_BIG(*) from
(
	select pvt.budgets_id as id, pvt.cust_id
    from
    ( 
		select distinct s.cust_id, s.budgets_id, s.PlanTYear from [dbo].[org_{{market_type_prefix }}{{ org_id }}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        where  PlanTYear is not null
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}        
        {% if budgets_in %}and {{budgets_in}} {% endif %}
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}        
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if winrs_in %}and {{winrs_in}} {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %} 
        {% if own_select %}and {{own_select}} {% endif %}
        {% if icontains %}and l.Org_CustNm like '%{{ icontains }}%' {% endif %}	
        group by s.cust_id, s.budgets_id, PlanTYear
	) pvt
	group by
	rollup (pvt.budgets_id, pvt.cust_id)
) nn    
where nn.id is not null
{% endautoescape %}  
"""

q_budgets_chart = """
{% autoescape off %}
select a.budgets_id, b.name as budget_name, PlanTYear as iid, ROUND(a.summa/1000,0) as summa from
(select Budgets_ID, PlanTYear, sum( isnull( {{market_type_prefix }}Summa ,0 )) as summa 
from [dbo].[org_{{market_type_prefix }}{{org_id}}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        where  PlanTYear is not null
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}        
        {% if budgets_in %}and {{budgets_in}} {% endif %}
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}        
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if winrs_in %}and {{winrs_in}} {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %} 
        {% if own_select %}and {{own_select}} {% endif %}
group by PlanTYear,  Budgets_ID) a
left join db_Budgets b on a.Budgets_ID=b.id
--order by budgets_id
{{ order_by }}
{% endautoescape %}  
"""

fd_sales_analysis = {r'tenddt': {'title':'Дата аукциона', 'width':10},
                     r'org_custinn': {'title': 'ИНН', 'width': 10},
                     r'org_custnm': {'title': 'Заказчик', 'width': 100},
                     r'order_tradename': {'title': 'ТМ по аукциону', 'width': 15},
                     r'contract_tradename': {'title': 'ТМ по контракту', 'width': 15},
                     r'Order_InnName': {'title': 'МНН по аукциону', 'width': 30},
                     r'Contract_InnName': {'title': 'МНН по контракту', 'width': 30},
                     r'Order_Dosage': {'title': 'Дозировка по аукциону', 'width': 20},
                     r'Contract_Dosage': {'title': 'Дозировка по контракту', 'width': 20},
                     r'Order_Count': {'title': 'Кол-во упаковок аукцион', 'width': 5},
                     r'Contract_Count': {'title': 'Кол-во упаковок контракт', 'width': 5},
                     r'Order_Price': {'title': 'Цена по аукциону', 'width': 8},
                     r'Contract_Price': {'title': 'Цена по контракту', 'width': 8},
                     r'Order_Summa': {'title': 'Сумма по аукциону', 'width': 10},
                     r'Contract_Summa': {'title': 'Сумма по контракту', 'width': 10},
                     r'status_name': {'title': 'Состояние аукциона', 'width': 20},
                     r'SrcInf': {'title': 'URL Аукцион', 'width': 20},
                     r'Contract_URL': {'title': 'URL Контракт', 'width': 20},
                     r'Order_AVG_Summa': {'title': 'Средняя цена по аукциону', 'width': 20, 'hide':1 },
}

q_sales_analysis = """
{% autoescape off %}
select CAST(TendDt as date) as TendDt, l.Org_CustINN, l.Org_CustNm, 
        i1.name as Order_InnName, t1.name as Order_TradeName,  Order_Dosage, Order_Count, Order_Price, Order_Summa, 
        Order_AVG_Price*Order_Count as Order_AVG_Summa,
        i2.name as Contract_InnName, t2.name as Contract_TradeName, Contract_Dosage, Contract_Count, Contract_Price, Contract_Summa,       
        u.name as status_name, SrcInf, Contract_URL
from [dbo].[org_Contract_{{org_id}}] s
left join db_lpu l on s.cust_id = l.cust_id
left join db_TradeNR t1 on s.Order_TradeNx = t1.id
left join db_TradeNR t2 on s.Contract_TradeNx = t2.id
left join db_inNR i1 on s.Order_InnNx = i1.id
left join db_inNR i2 on s.Contract_InnNx = i2.id
left join db_statusT u on s.StatusT_ID=u.id
where 1=1 
{% if no_target %} 
    and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
    {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
{% else %}
    {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
{% endif %}
{% if years_in %}and {{years_in}} {% endif %}
{% if markets_in %}and {{markets_in}} {% endif %}
{% if status_in %}and {{status_in}} {% endif %}        
{% if budgets_in %}and {{budgets_in}} {% endif %}
{% if dosage_in %}and {{dosage_in}} {% endif %}
{% if form_in %}and {{form_in}} {% endif %}        
{% if lpus_in %}and {{lpus_in}} {% endif %}    
{% if innrs_in %}and {{innrs_in}} {% endif %}
{% if trnrs_in %}and {{trnrs_in}} {% endif %}
{% if winrs_in %}and {{winrs_in}} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %} 
{% if own_select %}and {{own_select}} {% endif %}
{% if icontains %}and (l.Org_CustNm like '%{{ icontains }}%' or l.Org_CustINN like '%{{ icontains }}%'){% endif %}
{{ order_by }}
{% endautoescape %}  
"""

q_sales_analysis_count = """
{% autoescape off %}
select COUNT_BIG(*)
from [dbo].[org_Contract_{{org_id}}] s
left join db_lpu l on s.cust_id = l.cust_id
left join db_TradeNR t1 on s.Order_TradeNx = t1.id
left join db_TradeNR t2 on s.Contract_TradeNx = t2.id
left join db_inNR i1 on s.Order_InnNx = i1.id
left join db_inNR i2 on s.Contract_InnNx = i2.id
left join db_statusT u on s.StatusT_ID=u.id
where 1=1 
{% if no_target %} 
    and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
    {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
{% else %}
    {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
{% endif %}
{% if years_in %}and {{years_in}} {% endif %}
{% if markets_in %}and {{markets_in}} {% endif %}
{% if status_in %}and {{status_in}} {% endif %}        
{% if budgets_in %}and {{budgets_in}} {% endif %}
{% if dosage_in %}and {{dosage_in}} {% endif %}
{% if form_in %}and {{form_in}} {% endif %}        
{% if lpus_in %}and {{lpus_in}} {% endif %}    
{% if innrs_in %}and {{innrs_in}} {% endif %}
{% if trnrs_in %}and {{trnrs_in}} {% endif %}
{% if winrs_in %}and {{winrs_in}} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %} 
{% if own_select %}and {{own_select}} {% endif %}
{% if icontains %}and (l.Org_CustNm like '%{{ icontains }}%' or l.Org_CustINN like '%{{ icontains }}%'){% endif %}
{{ order_by }}
{% endautoescape %}  
"""


# Доля по рынкам
q_mparts = """
{% autoescape off %}
select CASE WHEN nn.market_id is NULL THEN 'ИТОГО' ELSE mt.name END as name, nn.* from 
(
	select market_id, grouping(market_id) as gr
	{% for y in years %},sum([{{y}}-1]) as [{{y}}-1], isnull(sum([{{y}}-2]),0) as [{{y}}-2], IIF(isnull(sum([{{y}}-1]),0)=0,'-',cast(isnull(cast(sum([{{y}}-2])/sum([{{y}}-1])*100 as int),0) as varchar)+'%') as [{{y}}-3]{% endfor %}
	from
		(
            select market_id, cast(PlanTYear as varchar)+'-1' as PlanTYear, sum(isnull({{ market_type_prefix }}summa,0)) as Summa
            from [dbo].[org_{{market_type_prefix }}{{org_id}}] s
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            where PlanTYear is not null 
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
            {% if years_in %}and {{years_in}} {% endif %}
            {% if markets_in %}and {{markets_in}} {% endif %}
            {% if status_in %}and {{status_in}} {% endif %}        
            {% if budgets_in %}and {{budgets_in}} {% endif %}
            {% if dosage_in %}and {{dosage_in}} {% endif %}
            {% if form_in %}and {{form_in}} {% endif %}        
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}
            {% if winrs_in %}and {{winrs_in}} {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %} 
            group by market_id, PlanTYear
            
            union all
            select market_id, cast(PlanTYear as varchar)+'-2' as PlanTYear, sum(isnull({{ market_type_prefix }}summa,0)) as Summa
            from [dbo].[org_{{market_type_prefix }}{{org_id}}] s
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            where PlanTYear is not null and market_own=1
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
            {% if years_in %}and {{years_in}} {% endif %}
            {% if markets_in %}and {{markets_in}} {% endif %}
            {% if status_in %}and {{status_in}} {% endif %}        
            {% if budgets_in %}and {{budgets_in}} {% endif %}
            {% if dosage_in %}and {{dosage_in}} {% endif %}
            {% if form_in %}and {{form_in}} {% endif %}        
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}
            {% if winrs_in %}and {{winrs_in}} {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %} 
            group by market_id, PlanTYear          
		) m
		PIVOT
		(
			sum(Summa) for PlanTYear in (
			{% for y in years %}[{{y}}-1], [{{y}}-2]{% if not forloop.last %},{% endif %}{% endfor %})
		) as pvt
	group by
	rollup (market_id)
) nn
left join db_market mt on mt.id=nn.market_id
--order by gr, mt.name
{{ order_by }}
{% endautoescape %}  
"""

q_mparts_count = """
{% autoescape off %}
select count(*) from db_market s where s.org_id = {{org_id}}
{% if markets_in %}and {{markets_cnt_in}} {% endif %}
{% endautoescape %} 
"""

fd_lparts =  {r'name':   {'title': 'Заказчик', 'width': 100},
              r'cust_id': {'title': 'cust_id', 'width': 0, 'hide':1},
              r'(20\d.)-1':   {'title': '\g<1> весь рынок', 'width': 10 },
              r'(20\d.)-2':   {'title': '\g<1> свой рынок', 'width': 10 },
              r'(20\d.)-3':   {'title': '\g<1> %', 'width': 8 }
}

q_lparts = """
{% autoescape off %}
select CASE WHEN nn.cust_id is NULL THEN 'ИТОГО' ELSE l.Org_CustNm END as name, nn.* from 
(
	select cust_id
	{% for y in years %},isnull([{{y}}-1],0) as [{{y}}-1], isnull([{{y}}-2],0) as [{{y}}-2], IIF(isnull([{{y}}-1],0)=0,'-',cast(isnull(cast([{{y}}-2]/[{{y}}-1]*100 as int),0) as varchar)+'%') as [{{y}}-3]
	{% endfor %}
	from
		(
            select s.cust_id, cast(PlanTYear as varchar)+'-1' as PlanTYear, sum(isnull({{ market_type_prefix }}summa,0)) as Summa
            from [dbo].[org_{{market_type_prefix }}{{org_id}}] s
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            where PlanTYear is not null 
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
            {% if years_in %}and {{years_in}} {% endif %}
            {% if markets_in %}and {{markets_in}} {% endif %}
            {% if status_in %}and {{status_in}} {% endif %}        
            {% if budgets_in %}and {{budgets_in}} {% endif %}
            {% if dosage_in %}and {{dosage_in}} {% endif %}
            {% if form_in %}and {{form_in}} {% endif %}        
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}
            {% if winrs_in %}and {{winrs_in}} {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %} 
            group by s.cust_id, PlanTYear
            
            union all
            select s.cust_id, cast(PlanTYear as varchar)+'-2' as PlanTYear, sum(isnull({{ market_type_prefix }}summa,0)) as Summa
            from [dbo].[org_{{market_type_prefix }}{{org_id}}] s
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            where PlanTYear is not null and market_own=1
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
            {% if years_in %}and {{years_in}} {% endif %}
            {% if markets_in %}and {{markets_in}} {% endif %}
            {% if status_in %}and {{status_in}} {% endif %}        
            {% if budgets_in %}and {{budgets_in}} {% endif %}
            {% if dosage_in %}and {{dosage_in}} {% endif %}
            {% if form_in %}and {{form_in}} {% endif %}        
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}
            {% if winrs_in %}and {{winrs_in}} {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %} 
            group by s.cust_id, PlanTYear          
		) m
		PIVOT
		(
			sum(Summa) for PlanTYear in (
			{% for y in years %}[{{y}}-1], [{{y}}-2]{% if not forloop.last %},{% endif %}{% endfor %})
		) as pvt
) nn
left join db_lpu l on l.cust_id=nn.cust_id
{% if icontains %}where l.Org_CustNm like '%{{ icontains }}%' {% endif %}
--order by [2018-1] desc, l.Org_CustNm
{{ order_by }}
{% endautoescape %} 
"""

q_lparts_count = """
{% autoescape off %}
select COUNT_BIG(DISTINCT s.cust_id) from [dbo].[org_{{market_type_prefix }}{{org_id}}] s 
            left join db_lpu l on s.cust_id = l.cust_id
            left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
            where PlanTYear is not null 
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
            {% if years_in %}and {{years_in}} {% endif %}
            {% if markets_in %}and {{markets_in}} {% endif %}
            {% if status_in %}and {{status_in}} {% endif %}        
            {% if budgets_in %}and {{budgets_in}} {% endif %}
            {% if dosage_in %}and {{dosage_in}} {% endif %}
            {% if form_in %}and {{form_in}} {% endif %}        
            {% if lpus_in %}and {{lpus_in}} {% endif %}    
            {% if innrs_in %}and {{innrs_in}} {% endif %}
            {% if trnrs_in %}and {{trnrs_in}} {% endif %}
            {% if winrs_in %}and {{winrs_in}} {% endif %}
            {% if lpus_in %}and {{lpus_in}} {% endif %} 
            {% if icontains %}and l.Org_CustNm like '%{{ icontains }}%' {% endif %}            
{% endautoescape %}
"""

# Конкурентный анализ
#
fd_competitions_lpu =  {r'ext':  {'title':'ИНН', 'width':10},
                        r'nm':   {'title': 'Заказчик', 'width': 100},
                        r'name': {'title': 'МНН/ТМ', 'width': 30},
                        r'dosage_name': {'title': 'Дозировка+Фасовка', 'width': 30},
                        r'id':   {'title': 'mnn/tm id', 'width': 0, 'hide':1},
                        r'tradenx': {'title': 'mnn/tm id', 'width': 0, 'hide':1},
                        r'gr':   {'title': 'Группа', 'width': 0, 'hide':1}
}

q_competitions_lpu = """
{% autoescape off %}
select l.Org_CustINN as ext, l.Org_CustNm as Nm, 
{% if sku_select %}ds.name as dosage_name,{% endif %}
CASE WHEN tradeNX is NULL THEN 'ИТОГО' ELSE t.name END as name, nn.* from (
select pvt.cust_id as id, pvt.{{ market_type_prefix }}{{ product_type }} as tradeNx, 
    {% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %}
     grouping(pvt.{{ market_type_prefix }}{{ product_type }}) as gr
    {% for y in years %},sum([{{y}}]) as [{{y}}]{% endfor %}
    from
    (
        select distinct s.cust_id, 
        {% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %} 
        isnull({{ market_type_prefix }}{{ product_type }}, -2) as {{ market_type_prefix }}{{ product_type }}, PlanTYear, 
        sum(isnull({{ market_type_prefix }}Summa,0)) as {{ market_type_prefix }}Summa
        from [dbo].[org_{{ market_type_prefix }}{{org_id}}] s with (nolock)
        left join db_lpu l on s.cust_id = l.cust_id
        left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on s.{{ market_type_prefix }}{{ product_type }} = t.id
        where 1=1 
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}        
        {% if budgets_in %}and {{budgets_in}} {% endif %}
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}           
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if winrs_in %}and {{winrs_in}} {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %} 
        {% if own_select %}and {{own_select}} {% endif %}                                    
        {% if icontains %}and l.Org_CustNm like '%{{ icontains }}%' {% endif %}
        group by s.cust_id,
                 {% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %} 
                 isnull({{ market_type_prefix }}{{ product_type }}, -2), PlanTYear
        having sum(isnull({{ market_type_prefix }}Summa,0))>0
    ) m
    PIVOT
    (
    sum({{ market_type_prefix }}Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
group by
rollup (pvt.cust_id, pvt.{{ market_type_prefix }}{{ product_type }} {% if sku_select %},{{ market_type_prefix }}Dosage_id{% endif %})
{% if sku_select %}having grouping(pvt.{{ market_type_prefix }}Dosage_id)=0 or grouping(pvt.{{ market_type_prefix }}{{ product_type }})<>0 {% endif %}
) nn    
left join db_lpu l on nn.id = l.cust_id
left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on nn.TradeNx = t.id
{% if sku_select %}left join org_DOSAGE_{{ org_id }} ds on nn.{{ market_type_prefix }}Dosage_id = ds.id{% endif %}
where nn.id is not null
--order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, l.Org_CustNm, gr, t.name
{{ order_by }}
{% endautoescape %}  
"""

fd_competitions_market =  {r'ext':  {'title':'ИНН', 'width':10},
                        r'nm':   {'title': 'Рынок', 'width': 20},
                        r'name': {'title': 'МНН/ТМ', 'width': 30},
                        r'dosage_name': {'title': 'Дозировка+Фасовка', 'width': 30},
                        r'id':   {'title': 'mnn/tm id', 'width': 0, 'hide':1},
                        r'tradenx': {'title': 'mnn/tm id', 'width': 0, 'hide':1},
                        r'gr':   {'title': 'Группа', 'width': 0, 'hide':1}
}

q_competitions_market = """
{% autoescape off %}
select nn.id, nn.Nm, nn.tradeNx, 
{% if sku_select %}ds.name as dosage_name,{% endif %}
CASE WHEN tradeNX is NULL THEN 'ИТОГО' ELSE t.name END as name, nn.gr 
{% for y in years %},nn.[{{y}}]{% endfor %} from (
select pvt.market_id as id, pvt.market_name as Nm, 
    pvt.{{ market_type_prefix }}{{ product_type }} as tradeNx, 
    {% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %}
    grouping(pvt.{{ market_type_prefix }}{{ product_type }}) as gr 
    {% for y in years %},sum([{{y}}]) as [{{y}}]{% endfor %}
    from
    (
        select distinct s.market_id, s.market_name, 
        {% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %} 
        isnull({{ market_type_prefix }}{{ product_type }}, -2) as {{ market_type_prefix }}{{ product_type }}, PlanTYear, 
        sum(isnull({{ market_type_prefix }}Summa,0)) as {{ market_type_prefix }}Summa
        from [dbo].[org_{{ market_type_prefix }}{{org_id}}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on s.{{ market_type_prefix }}{{ product_type }} = t.id
        --where s.{{ market_type_prefix }}TradeNx > 0
        where 1=1 
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %} 
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}        
        {% if budgets_in %}and {{budgets_in}} {% endif %}
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}        
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if winrs_in %}and {{winrs_in}} {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %} 
        {% if own_select %}and {{own_select}} {% endif %}                                    
        {% if icontains %}and s.market_name like '%{{ icontains }}%' {% endif %}
     	group by s.market_id, s.market_name, 
     	         {% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %} 
     	         isnull({{ market_type_prefix }}{{ product_type }}, -2), PlanTYear
     	having sum(isnull({{ market_type_prefix }}Summa,0))>0
    ) m
    PIVOT
    (
    sum({{ market_type_prefix }}Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
group by
rollup (pvt.market_id, pvt.market_name, pvt.{{ market_type_prefix }}{{ product_type }} {% if sku_select %},{{ market_type_prefix }}Dosage_id{% endif %})
{% if sku_select %}having grouping(pvt.{{ market_type_prefix }}Dosage_id)=0 or grouping(pvt.{{ market_type_prefix }}{{ product_type }})<>0 {% endif %}
) nn    
left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on nn.TradeNx = t.id
{% if sku_select %}left join org_DOSAGE_{{ org_id }} ds on nn.{{ market_type_prefix }}Dosage_id = ds.id{% endif %}
where nn.id is not null and nn.Nm is not Null
--order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, l.Org_CustNm, gr, t.name
{{ order_by }}
{% endautoescape %}  
"""

fd_avg_price =  {r'id': {'title':'Дата аукциона', 'width':0, 'hide':1},
                 r'nm': {'title': 'Рынок', 'width': 30},
                 r'tradenx': {'title': 'mnn/tm id', 'width': 0, 'hide':1},
                 r'name': {'title': 'МНН/ТМ по аукциону', 'width': 30},
                 r'dosage_name': {'title': 'Дозировка+Фасовка', 'width': 30},
                 r'gr': {'title': 'Группа', 'width': 0, 'hide':1}
}

q_avg_price = """
{% autoescape off %}
select pvt.market_id as id, pvt.market_name as Nm, 
    {% if sku_select %}ds.name as dosage_name,{% endif %} 
    pvt.{{ market_type_prefix }}{{ product_type }} as tradeNx, isnull(t.name,'') as name, 0 as gr 
    {% for y in years %},[{{y}}]{% endfor %}
    from
    (
        select distinct s.market_id, s.market_name, 
        {% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %} 
        isnull({{ market_type_prefix }}{{ product_type }}, -2) as {{ market_type_prefix }}{{ product_type }}, PlanTYear, 
        avg({{ market_type_prefix }}Price) as {{ market_type_prefix }}AVG
        from [dbo].[org_{{ market_type_prefix }}{{org_id}}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        where 1=1 
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}        
        {% if budgets_in %}and {{budgets_in}} {% endif %}
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}        
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if winrs_in %}and {{winrs_in}} {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %} 
        {% if own_select %}and {{own_select}} {% endif %}                                     
        {% if icontains %}and s.market_name like '%{{ icontains }}%' {% endif %}
     	group by s.market_id, s.market_name,{% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %} isnull({{ market_type_prefix }}{{ product_type }}, -2), PlanTYear
    ) m
    PIVOT
    (
    AVG({{ market_type_prefix }}AVG)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on pvt.{{ market_type_prefix }}{{ product_type }} = t.id
{% if sku_select %}left join org_DOSAGE_{{ org_id }} ds on pvt.{{ market_type_prefix }}Dosage_id = ds.id{% endif %}
where pvt.market_id is not null and pvt.market_name is not Null and isnull(t.name,'')<>''
--order by pvt.market_name
{{ order_by }}
{% endautoescape %}  
"""

fd_packages =  {r'id': {'title':'id', 'width':0, 'hide':1},
                 r'nm': {'title': 'Рынок', 'width': 30},
                 r'tradenx': {'title': 'mnn/tm id', 'width': 0, 'hide':1},
                 r'name': {'title': 'МНН/ТМ по аукциону', 'width': 30},
                 r'dosage_name': {'title': 'Дозировка+Фасовка', 'width': 30},
                 r'gr': {'title': 'Группа', 'width': 0, 'hide':1}
}

q_packages = """
{% autoescape off %}
select pvt.market_id as id, pvt.market_name as Nm, 
    {% if sku_select %}ds.name as dosage_name,{% endif %} 
    pvt.{{ market_type_prefix }}{{ product_type }} as tradeNx, isnull(t.name,'') as name, 0 as gr 
    {% for y in years %},[{{y}}]{% endfor %}
    from
    (
        select distinct s.market_id, s.market_name, 
        {% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %} 
        isnull({{ market_type_prefix }}{{ product_type }}, -2) as {{ market_type_prefix }}{{ product_type }}, PlanTYear, 
        sum(isnull({{ market_type_prefix }}Count,0)) as {{ market_type_prefix }}Count
        from [dbo].[org_{{ market_type_prefix }}{{org_id}}] s
        left join db_lpu l on s.cust_id = l.cust_id
        left join db_TradeNR t on s.{{ market_type_prefix }}TradeNx = t.id
        where 1=1 
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}        
        {% if budgets_in %}and {{budgets_in}} {% endif %}
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}        
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if winrs_in %}and {{winrs_in}} {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %} 
        {% if own_select %}and {{own_select}} {% endif %}                                   
        {% if icontains %}and s.market_name like '%{{ icontains }}%' {% endif %}
     	group by s.market_id, s.market_name,{% if sku_select %}{{ market_type_prefix }}Dosage_id,{% endif %} isnull({{ market_type_prefix }}{{ product_type }}, -2), PlanTYear
    ) m
    PIVOT
    (
    SUM({{ market_type_prefix }}Count)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on pvt.{{ market_type_prefix }}{{ product_type }} = t.id
{% if sku_select %}left join org_DOSAGE_{{ org_id }} ds on pvt.{{ market_type_prefix }}Dosage_id = ds.id{% endif %}
where pvt.market_id is not null and pvt.market_name is not Null and isnull(t.name,'')<>''
--order by pvt.market_name
{{ order_by }}
{% endautoescape %}  
"""

q_employees = """
{% autoescape off %}
with tree as 
(
select a.id, a.name, a.parent_id, a.org_id, a.istarget 
from db_employee a
left join db_employee_users a2 on a.id=a2.employee_id
left join auth_user a3 on a2.user_id=a3.id
where a3.username = '{{username}}'
union all
select a.id, a.name, a.parent_id, a.org_id, a.istarget
from db_employee a 
inner join tree t on t.id = a.parent_id and a.org_id=t.org_id
)
select distinct {{ fields }} from tree 
where istarget=1 
{{ order_by }}
{% endautoescape %} 
"""


# Использование q_markets_hs вместо q_markets дает задержку около 1-2 секунд
q_markets = """
{% autoescape off %}
select distinct {{ fields }} from db_market a where a.org_id = {{ org_id }}
{{ order_by }}
{% endautoescape %} 
"""

q_markets_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_market a 
where a.org_id = {{ org_id }}
and exists ( select 1 from org_{{ market_type_prefix }}{{ org_id }} s
               {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
               where s.market_id=a.id
                {% if no_target %} 
                    and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                    {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
                {% else %}
                    {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
                {% endif %}
               {% if own_select %}and {{own_select}} {% endif %}
)
{{ order_by }}
{% endautoescape %} 
"""

# Использование условия "and s.cust_id is Not Null" увеличивает задержку с ~1 до ~7 секунд
q_years_hs = """
{% autoescape off %}
select {{ fields }} from db_years a
where exists ( select 1 from org_{{ market_type_prefix }}{{ org_id }} s
               {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
               where s.PlanTYear=a.PlanTYear
                {% if no_target %} 
                    and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                    {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
                {% else %}
                    {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
                {% endif %}
               {% if own_select %}and {{own_select}} {% endif %}
)
{{ order_by }}
{% endautoescape %}  
 """

q_status = """
{% autoescape off %}
select distinct {{fields}} from db_statusT a where a.id>0
{{ order_by }}
{% endautoescape %} 
"""

q_status_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_statusT a
where exists
        ( select top 1 1 from org_{{ market_type_prefix }}{{ org_id }} s
          {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
          where a.id=s.statusT_ID
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}   
        {% if own_select %}and {{own_select}} {% endif %}              
        )
{{ order_by }}
{% endautoescape %} 
"""

q_budgets = """
{% autoescape off %}
select distinct {{fields}} from db_budgets a
{{ order_by }}
{% endautoescape %} 
"""

q_budgets_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_budgets a
where exists
        ( select top 1 1 from org_{{ market_type_prefix }}{{ org_id }} s
          {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
          where a.id=s.budgets_ID
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}    
        {% if own_select %}and {{own_select}} {% endif %}                     
        )
{{ order_by }}
{% endautoescape %} 
"""

q_dosage = """
{% autoescape off %}
select distinct {{fields}} from org_DOSAGE_{{ org_id }} a
{{ order_by }}
{% endautoescape %} 
"""

q_dosage_hs = """
{% autoescape off %}
select distinct {{ fields }} from org_DOSAGE_{{ org_id }} a
where exists
        ( select top 1 1 from org_{{ market_type_prefix }}{{ org_id }} s
          {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
          where s.{{ market_type_prefix }}Dosage_id=a.id
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
          {% if years_in %}and {{years_in}} {% endif %}
          {% if markets_in %}and {{markets_in}} {% endif %}
          {% if status_in %}and {{status_in}} {% endif %}
          {% if budgets_in %}and {{budgets_in}} {% endif %}     
          {% if form_in %}and {{form_in}} {% endif %}    
          {% if own_select %}and {{own_select}} {% endif %}           
          {% if name__icontains %} and a.name like '%{{ name__icontains }}%'{% endif %}  
        )                              
{{ order_by }}
{% endautoescape %} 
"""

q_form_hs = """
{% autoescape off %}
select distinct {{ fields }} from org_FORM_{{ org_id }} a
where exists
        ( select top 1 1 from org_{{ market_type_prefix }}{{ org_id }} s
          {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}        
          where s.{{ market_type_prefix }}Form_id=a.id
            {% if no_target %} 
                and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
                {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
            {% else %}
                {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
            {% endif %}
          {% if years_in %}and {{years_in}} {% endif %}
          {% if markets_in %}and {{markets_in}} {% endif %}
          {% if status_in %}and {{status_in}} {% endif %}       
          {% if budgets_in %}and {{budgets_in}} {% endif %}      
          {% if own_select %}and {{own_select}} {% endif %}    
          {% if name__icontains %} and a.name like '%{{ name__icontains }}%'{% endif %} 
        )                                       
{{ order_by }}
{% endautoescape %} 
"""

q_innr_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_innr a
where exists
      ( select top 1 1 from org_{{ market_type_prefix }}{{ org_id }} s 
        {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
        where a.id=s.{{ market_type_prefix }}innNx 
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}  
        {% if budgets_in %}and {{budgets_in}} {% endif %}       
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}       
        {% if own_select %}and {{own_select}} {% endif %}   
        {% if name__icontains %} and name like '%{{ name__icontains }}%'{% endif %}
      )  
{{ order_by }}
{% endautoescape %} 
"""

q_tradenr_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_tradenr a
where exists
      ( select top 1 1 from org_{{ market_type_prefix }}{{ org_id }} s 
        {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
        where a.id=s.{{ market_type_prefix }}tradeNx 
        {% if no_target %} 
            and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
            {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
        {% else %}
            {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
        {% endif %}
        {% if years_in %}and {{years_in}} {% endif %}
        {% if markets_in %}and {{markets_in}} {% endif %}
        {% if status_in %}and {{status_in}} {% endif %}    
        {% if budgets_in %}and {{budgets_in}} {% endif %}     
        {% if dosage_in %}and {{dosage_in}} {% endif %}
        {% if form_in %}and {{form_in}} {% endif %}        
        {% if own_select %}and {{own_select}} {% endif %}                
        {% if name__icontains %} and name like '%{{ name__icontains }}%'{% endif %}
      )
{{ order_by }}
{% endautoescape %} 
"""

q_winner_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_winnerorg a
where exists 
  ( select top 1 1 from org_{{ market_type_prefix }}{{ org_id }} s 
    {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
    where a.id=s.winner_id
    {% if no_target %} 
        and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
        {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
    {% else %}
        {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
    {% endif %}
    {% if years_in %}and {{years_in}} {% endif %}
    {% if markets_in %}and {{markets_in}} {% endif %}
    {% if status_in %}and {{status_in}} {% endif %}    
    {% if budgets_in %}and {{budgets_in}} {% endif %}     
    {% if innrs_in %}and {{innrs_in}} {% endif %}
    {% if trnrs_in %}and {{trnrs_in}} {% endif %}
    {% if dosage_in %}and {{dosage_in}} {% endif %}
    {% if form_in %}and {{form_in}} {% endif %}       
    {% if own_select %}and {{own_select}} {% endif %} 
    {% if name__icontains %} and name like '%{{ name__icontains }}%'{% endif %}
  )
{{ order_by }}
{% endautoescape %} 
"""

q_lpu_hs = """
{% autoescape off %}
select distinct {{ fields }} from db_lpu a
where exists 
  ( select top 1 1 from org_{{ market_type_prefix }}{{ org_id }} s 
    where a.cust_id=s.cust_id
    {% if no_target %} 
        and exists (select top 1 1 from db_region_employee r where r.region_id=a.regcode and r.employee_id in ({{all_targets}}) ) 
        {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
    {% else %}
        {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
    {% endif %}
    {% if years_in %}and {{years_in}} --years_in{% endif %}
    {% if markets_in %}and {{markets_in}} --markets_in{% endif %}
    {% if status_in %}and {{status_in}} --status_in{% endif %}
    {% if budgets_in %}and {{budgets_in}} --budgets_in{% endif %}         
    {% if innrs_in %}and {{innrs_in}} --innrs_in{% endif %}
    {% if trnrs_in %}and {{trnrs_in}} --trnrs_in{% endif %}
    {% if dosage_in %}and {{dosage_in}} --dosage_in{% endif %}
    {% if form_in %}and {{form_in}} --form_in{% endif %}    
    {% if winrs_in %}and {{winrs_in}} --winrs_in{% endif %}
    {% if own_select %}and {{own_select}} {% endif %} 
    {% if name__icontains %} and ( a.Org_CustNm like '%{{ name__icontains }}%' or a.Org_CustInn like '%{{ name__icontains }}%' ) {% endif %}
  )
{{ order_by }}
{% endautoescape %} 
"""

q_sales_year = """
{% autoescape off %}
select b.name as market_name, PlanTYear as iid, Sum(isnull({{ market_type_prefix }}Summa,0))/1000000 as product_cost_sum
from org_{{ market_type_prefix }}{{ org_id }} s
left join db_lpu l on s.cust_id = l.cust_id
left join db_market b on s.market_id=b.id --and org_id={{ org_id }}
where s.PlanTYear is not NULL --and s.cust_id<>0
{% if no_target %} 
    and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
    {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
{% else %}
    {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
{% endif %}
{% if years_in %}and {{years_in}} {% endif %}
{% if markets_in %}and {{markets_in}} {% endif %}
{% if status_in %}and {{status_in}} {% endif %}        
{% if budgets_in %}and {{budgets_in}} {% endif %}
{% if dosage_in %}and {{dosage_in}} {% endif %}
{% if form_in %}and {{form_in}} {% endif %}        
{% if lpus_in %}and {{lpus_in}} {% endif %}    
{% if innrs_in %}and {{innrs_in}} {% endif %}
{% if trnrs_in %}and {{trnrs_in}} {% endif %}
{% if winrs_in %}and {{winrs_in}} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %}  
{% if own_select %}and {{own_select}} {% endif %}       
group by b.name, PlanTYear
{{ order_by }}
{% endautoescape %} 
"""

q_sales_month = """
{% autoescape off %}
select b.name as market_name, month(ProcDt) as mon, Sum(isnull({{ market_type_prefix }}Summa,0))/1000000 as product_cost_sum, count(*) as product_count
from org_{{ market_type_prefix }}{{ org_id }} s
left join db_lpu l on s.cust_id = l.cust_id
left join db_market b on s.market_id=b.id --and org_id={{ org_id }}
where s.PlanTYear is not NULL --and s.cust_id<>0
{% if no_target %} 
    and exists (select top 1 1 from db_region_employee r where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
    {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
{% else %}
    {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e where e.lpu_id=s.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
{% endif %}
{% if years_in %}and {{years_in}} {% endif %}
{% if markets_in %}and {{markets_in}} {% endif %}
{% if status_in %}and {{status_in}} {% endif %}        
{% if budgets_in %}and {{budgets_in}} {% endif %}
{% if dosage_in %}and {{dosage_in}} {% endif %}
{% if form_in %}and {{form_in}} {% endif %}        
{% if lpus_in %}and {{lpus_in}} {% endif %}    
{% if innrs_in %}and {{innrs_in}} {% endif %}
{% if trnrs_in %}and {{trnrs_in}} {% endif %}
{% if winrs_in %}and {{winrs_in}} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %}      
{% if own_select %}and {{own_select}} {% endif %}   
group by b.name, month(ProcDt)
{{ order_by }}
{% endautoescape %} 
"""

q_years_passport0 = """
{% autoescape off %}
select DISTINCT {{ fields }} from org_DATA s
where 1=1 
{% if lpus_in %}and {{lpus_in}} {% endif %} 
{{ order_by }}
{% endautoescape %}
"""

q_years_passport = """
{% autoescape off %}
select {{ fields }} from db_years a (nolock)
where exists ( select 1 from org_DATA s (nolock)
               where s.PlanTYear=a.PlanTYear           
               {% if lpus_in %}and {{lpus_in}} {% endif %} 
               {% if market_type_prefix %}and s.{{ market_type_prefix }}summa>0 {% endif %}     
             )
{{ order_by }}
{% endautoescape %}
"""

q_lpu_passport = """
{% autoescape off %}
select DISTINCT {{ fields }} from db_lpu l (nolock)
where exists (select 1 from org_DATA s (nolock) where s.cust_id=l.cust_id)
    {% if no_target %} 
        and exists (select top 1 1 from db_region_employee r (nolock) where r.region_id=l.regcode and r.employee_id in ({{all_targets}}) ) 
        {% if disabled_targets %} and not exists (select top 1 1 from db_lpu_employee e (nolock) where e.lpu_id=l.cust_id and e.employee_id in ({{disabled_targets}}) ) {% endif %}
    {% else %}
        {% if enabled_targets %} and exists (select top 1 1 from db_lpu_employee e (nolock) where e.lpu_id=l.cust_id and e.employee_id in ({{enabled_targets}}) ) {% endif %}
    {% endif %}
{% if name__icontains %} and ( l.Org_CustNm like '%{{ name__icontains }}%' or l.Org_CustInn like '%{{ name__icontains }}%' ) {% endif %}
{{ order_by }}
{% endautoescape %}
"""

q_lpu_passport0 = """
{% autoescape off %}
select {{ fields }} from db_years a
where exists ( 
where s.PlanTYear=a.PlanTYear
select 1 from db_lpu l
                where exists (select 1 from org_DATA s where s.cust_id=l.cust_id)
                {% if name__icontains %} and ( l.Org_CustNm like '%{{ name__icontains }}%' or l.Org_CustInn like '%{{ name__icontains }}%' ) {% endif %}
             )   
{{ order_by }}
{% endautoescape %}
"""

q_passport_chart_years = """
{% autoescape off %}
select [PlanTYear] as [year], isnull(s.[{{ market_type_prefix }}summa],0)/1000 as [summa] from org_DATA s
where isnull(s.[{{ market_type_prefix }}summa],0)>0
{% if years_in %}and {{years_in}} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %}
{{ order_by }}
{% endautoescape %}
"""

q_passport_chart_markets = """
{% autoescape off %}
select market_id, market_name, CAST(sum(isnull(s.[{{ market_type_prefix }}Summa],0))/1000 as INT) as summa 
from org_{{ market_type_prefix }}{{ org_id }} s
where StatusT_ID=4
{% if years_in %}and {{years_in}} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %}
group by market_id, market_name
having sum(isnull(s.{{ market_type_prefix }}Summa,0)) > 0
--order by market_name
{{ order_by }}
{% endautoescape %}
"""

q_passport_winners_table0 = """
{% autoescape off %}
select IIF(grouping(s.WinnerOrg)=1,'ИТОГО',isnull(s.WinnerOrg,' НЕТ ДАННЫХ')) as name, s.WinnerOrgInn as inn, grouping(s.WinnerOrg) as gr,
sum(isnull(isnull(s.[Ship_Sum],s.[ItemSum]),0)) as summa
from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract] s (nolock)
where exists (select 1 from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE] c where s.LotSpec_ID=c.LotSpec_ID and (c.Reg_ID < 100) AND (c.ProdType_ID = 'L'))
where 1=1
{% if years %}and isnull(year([DTExecuteEnd]),0) in ({% for y in years %}{{y}}{% if not forloop.last %},{% endif %}{%endfor%}) {% endif %}
--{% if years_in %}and {{years_in}} {% endif %}
{% if lpus_in %}and {{lpus_in}} {% endif %}
{% if icontains %}and (w.Org_CustNm like '%{{ icontains }}%' or w.Org_CustINN like '%{{ icontains }}%'){% endif %}
group by 
rollup (WinnerOrg, WinnerOrgInn)
having (grouping(WinnerOrgInn)=0 or grouping(WinnerOrg)=1)
--order by grouping(WinnerOrg) desc, [name] asc
{{ order_by }}
{% endautoescape %}
"""

fd_passport_winners_table =  {r'name': {'title':'Победитель торгов', 'width':100},
                             r'inn': {'title': 'ИНН', 'width': 10},
                             r'summa': {'title': 'Сумма, руб', 'width': 15},
                             r'gr': {'title': 'Группа', 'width': 0, 'hide':1}
}

q_passport_winners_table = """
{% autoescape off %}
select IIF(grouping(w.Org_CustNm)=1,'ИТОГО',isnull(w.Org_CustNm,' НЕТ ДАННЫХ')) as name, w.Org_CustInn as inn, grouping(w.Org_CustNm) as gr,
{% if market_type_prefix == 'Contract_' %}
   sum(isnull(isnull(c1.[Ship_Sum],c1.[ItemSum]),0)) as summa
   from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE] s (nolock)
   LEFT JOIN [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE_Contract] c1 (nolock)
	    ON c1.LotSpec_ID = s.LotSpec_ID and c1.Contract_ID > 0  and isnull(c1.LotSpec_ID,0) > 0
{% else %}
   sum(isnull(s.Order_Sum,0)) as summa
   from (select DISTINCT Tender_ID, cust_id, PlanTYear, Winner_Id, Reg_ID, StatusT_ID, Order_Sum from [Cursor_rpt_LK].[dbo].[ComplexRpt_CACHE] (nolock)) s
{% endif %}   
left join db_allOrg w on s.Winner_Id=w.cust_id
where (s.Reg_ID < 100) and (s.StatusT_ID=4) --AND (s.ProdType_ID = 'L')
{% if years_in %}and {{years_in}} {% endif %}
{% if market_type_prefix == 'Contract_' %}
    {% if lpus_contract_in %}and {{lpus_contract_in}}{% endif %}  
{% else %}
   {% if lpus_in %}and {{lpus_in}}{% endif %} 
{% endif %}      
{% if icontains %}and (w.Org_CustNm like '%{{ icontains }}%' or w.Org_CustINN like '%{{ icontains }}%'){% endif %}
group by 
rollup (w.Org_CustNm, w.Org_CustInn)
having (grouping(w.Org_CustInn)=0 or grouping(w.Org_CustNm)=1)
--order by grouping(w.Org_CustNm) desc, [name] asc
{{ order_by }}
{% endautoescape %}
"""