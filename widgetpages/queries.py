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
        from [dbo].[org_CACHE_{{ org_id }}] s
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
		select distinct s.cust_id, s.budgets_id, s.PlanTYear from [dbo].[org_CACHE_{{ org_id }}] s
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
from [dbo].[org_CACHE_{{org_id}}] s
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

q_sales_analysis = """
{% autoescape off %}
select CAST(TendDt as date) as TendDt, l.Org_CustINN, l.Org_CustNm, t1.name as Order_TradeName, t2.name as Contract_TradeName, 
       i1.name as Order_InnName, i2.name as Contract_InnName,
       Order_Dosage, Contract_Dosage,
       -- isnull(Order_Dosage,'')+IIF(Order_BatchSize is Null,'',' №'+CAST(Order_BatchSize as varchar)) as Order_Dosage,
       -- isnull(Contract_Dosage,'')+IIF(Contract_Volume is Null, '', ' '+Contract_volume)+IIF(Contract_BatchSize is Null,'',' №'+CAST(Contract_BatchSize as varchar)) as Contract_Dosage, 
       Order_Count, Contract_Count, Order_Price, Contract_Price, Order_Summa, 
       Order_AVG_Price*Order_Count as Order_AVG_Summa, Contract_Summa,  u.name as status_name, SrcInf, Contract_URL
from [dbo].[org_CACHE_{{org_id}}] s
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
from [dbo].[org_CACHE_{{org_id}}] s
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
            from [dbo].[org_CACHE_{{org_id}}] s
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
            from [dbo].[org_CACHE_{{org_id}}] s
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
            from [dbo].[org_CACHE_{{org_id}}] s
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
            from [dbo].[org_CACHE_{{org_id}}] s
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
select COUNT_BIG(DISTINCT s.cust_id) from [dbo].[org_CACHE_{{org_id}}] s 
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
q_competitions_lpu = """
{% autoescape off %}
select l.Org_CustINN as ext, l.Org_CustNm as Nm, CASE WHEN tradeNX is NULL THEN 'ИТОГО' ELSE t.name END as name, nn.* from (
select pvt.cust_id as id, pvt.{{ market_type_prefix }}{{ product_type }} as tradeNx, grouping(pvt.{{ market_type_prefix }}{{ product_type }}) as gr
    {% for y in years %},sum([{{y}}]) as [{{y}}]{% endfor %}
    from
    (
        select distinct s.cust_id, isnull({{ market_type_prefix }}{{ product_type }}, -2) as {{ market_type_prefix }}{{ product_type }}, PlanTYear, 
        sum(isnull({{ market_type_prefix }}Summa,0)) as {{ market_type_prefix }}Summa
        from [dbo].[org_CACHE_{{org_id}}] s with (nolock)
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
        {% if lpus_in %}and {{lpus_in}} {% endif %}    
        {% if innrs_in %}and {{innrs_in}} {% endif %}
        {% if trnrs_in %}and {{trnrs_in}} {% endif %}
        {% if winrs_in %}and {{winrs_in}} {% endif %}
        {% if lpus_in %}and {{lpus_in}} {% endif %} 
        {% if own_select %}and {{own_select}} {% endif %}                                    
        {% if icontains %}and l.Org_CustNm like '%{{ icontains }}%' {% endif %}
        group by s.cust_id, isnull({{ market_type_prefix }}{{ product_type }}, -2), PlanTYear
    ) m
    PIVOT
    (
    sum({{ market_type_prefix }}Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
group by
rollup (pvt.cust_id, pvt.{{ market_type_prefix }}{{ product_type }})
) nn    
left join db_lpu l on nn.id = l.cust_id
left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on nn.TradeNx = t.id
where nn.id is not null
--order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, l.Org_CustNm, gr, t.name
{{ order_by }}
{% endautoescape %}  
"""

q_competitions_market = """
{% autoescape off %}
select CASE WHEN tradeNX is NULL THEN 'ИТОГО' ELSE t.name END as name, nn.* from (
select pvt.market_id as id, pvt.market_name as Nm, pvt.{{ market_type_prefix }}{{ product_type }} as tradeNx, grouping(pvt.{{ market_type_prefix }}{{ product_type }}) as gr 
    {% for y in years %},sum([{{y}}]) as [{{y}}]{% endfor %}
    from
    (
        select distinct s.market_id, s.market_name, isnull({{ market_type_prefix }}{{ product_type }}, -2) as {{ market_type_prefix }}{{ product_type }}, PlanTYear, 
        sum(isnull({{ market_type_prefix }}Summa,0)) as {{ market_type_prefix }}Summa
        from [dbo].[org_CACHE_{{org_id}}] s
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
     	group by s.market_id, s.market_name, isnull({{ market_type_prefix }}{{ product_type }}, -2), PlanTYear
    ) m
    PIVOT
    (
    sum({{ market_type_prefix }}Summa)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
group by
rollup (pvt.market_id, pvt.market_name, pvt.{{ market_type_prefix }}{{ product_type }})
) nn    
left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on nn.TradeNx = t.id
where nn.id is not null and nn.Nm is not Null
--order by sum([2018]) over (PARTITION BY nn.id, nn.gr) desc, l.Org_CustNm, gr, t.name
{{ order_by }}
{% endautoescape %}  
"""

q_avg_price = """
{% autoescape off %}
select pvt.market_id as id, pvt.market_name as Nm, pvt.{{ market_type_prefix }}{{ product_type }} as tradeNx, isnull(t.name,'') as name, 0 as gr 
    {% for y in years %},[{{y}}]{% endfor %}
    from
    (
        select distinct s.market_id, s.market_name, isnull({{ market_type_prefix }}{{ product_type }}, -2) as {{ market_type_prefix }}{{ product_type }}, PlanTYear, 
        avg({{ market_type_prefix }}Price) as {{ market_type_prefix }}AVG
        from [dbo].[org_CACHE_{{org_id}}] s
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
     	group by s.market_id, s.market_name, isnull({{ market_type_prefix }}{{ product_type }}, -2), PlanTYear
    ) m
    PIVOT
    (
    AVG({{ market_type_prefix }}AVG)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on pvt.{{ market_type_prefix }}{{ product_type }} = t.id
where pvt.market_id is not null and pvt.market_name is not Null and isnull(t.name,'')<>''
--order by pvt.market_name
{{ order_by }}
{% endautoescape %}  
"""

q_packages = """
{% autoescape off %}
select pvt.market_id as id, pvt.market_name as Nm, pvt.{{ market_type_prefix }}{{ product_type }} as tradeNx, isnull(t.name,'') as name, 0 as gr 
    {% for y in years %},[{{y}}]{% endfor %}
    from
    (
        select distinct s.market_id, s.market_name, isnull({{ market_type_prefix }}{{ product_type }}, -2) as {{ market_type_prefix }}{{ product_type }}, PlanTYear, 
        sum(isnull({{ market_type_prefix }}Count,0)) as {{ market_type_prefix }}Count
        from [dbo].[org_CACHE_{{org_id}}] s
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
     	group by s.market_id, s.market_name, isnull({{ market_type_prefix }}{{ product_type }}, -2), PlanTYear
    ) m
    PIVOT
    (
    SUM({{ market_type_prefix }}Count)
    for PlanTYear in ({% for y in years %}[{{y}}]{% if not forloop.last %},{% endif %}{% endfor %})
    ) as pvt
left join {% if product_type == 'TradeNx' %}db_TradeNR{% else %}db_InNr{% endif %} t on pvt.{{ market_type_prefix }}{{ product_type }} = t.id
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
and exists ( select 1 from org_CACHE_{{ org_id }} s
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

q_years_hs = """
{% autoescape off %}
select {{ fields }} from db_years a
where exists ( select 1 from org_CACHE_{{ org_id }} s
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

# Использование условия "and s.cust_id is Not Null" увеличивает задержку с ~1 до ~7 секунд
q_years_hs0 = """
{% autoescape off %}
select distinct {{ fields }} from org_CACHE_{{ org_id }} s
--{% if targets %}left join db_lpu_employee e on s.cust_id=e.lpu_id {% endif %}
where s.PlanTYear is not Null -- and s.cust_id is Not Null
{% if targets %} and exists (select 1 from db_lpu_employee e where e.lpu_id=s.cust_id and {{targets}} ) {% endif %}
{% if own_select %}and {{own_select}} {% endif %}
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
        ( select top 1 1 from org_CACHE_{{ org_id }} s
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
        ( select top 1 1 from org_CACHE_{{ org_id }} s
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
        ( select top 1 1 from org_CACHE_{{ org_id }} s
          {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
          where s.Contract_Dosage_id=a.id
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
        ( select top 1 1 from org_CACHE_{{ org_id }} s
          {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}        
          where s.Contract_Form_id=a.id
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
      ( select top 1 1 from org_CACHE_{{ org_id }} s 
        {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
        where a.id=s.Order_innNx 
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
      ( select top 1 1 from org_CACHE_{{ org_id }} s 
        {% if no_target %}left join db_lpu l on s.cust_id=l.cust_id{% endif %}
        where a.id=s.Order_tradeNx 
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
  ( select top 1 1 from org_CACHE_{{ org_id }} s 
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
  ( select top 1 1 from org_CACHE_{{ org_id }} s 
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
select b.name as market_name, PlanTYear as iid, Sum(isnull(Order_Summa,0))/1000000 as product_cost_sum
from org_CACHE_{{ org_id }} s
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
select b.name as market_name, month(ProcDt) as mon, Sum(isnull(Order_Summa,0))/1000000 as product_cost_sum, count(*) as product_count
from org_CACHE_{{ org_id }} s
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
select {{ fields }} from db_years a
where exists ( select 1 from org_DATA s
               where s.[year]=a.PlanTYear 
               {% if lpus_in %}and {{lpus_in}} {% endif %} 
             )
{{ order_by }}
{% endautoescape %}
"""

q_lpu_passport = """
{% autoescape off %}
select DISTINCT {{ fields }} from db_lpu l
where exists (select 1 from org_DATA s where s.cust_id=l.cust_id)
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

q_passport_winners_table = """
{% autoescape off %}
select * from db_WinnersOrg
{{ order_by }}
{% endautoescape %}
"""