----------- 
----------- 1. Устранить в перечне ЛПУ, учреждения содержащие символ одинарной кавычки:
-----------
select * from db_lpu a
left join db_lpu_employee b on a.cust_id=b.lpu_id
where Org_CustNm like '%''%'


    {% for e in data.pivot %}
        { {% for k,v in e.items %}'{{ k }}':'{{ v }}'{% if not forloop.last %},{% endif %}{% if not forloop.last %},{% endif %}{% endfor %} }{% if not forloop.last %},{% endif %}
    {% endfor %}
    
    {% for row in data.pivot %}
        { {%for key in row|get_dict %}{% if  key != "_state" and key != "id" and key != "tradeNx" %}{% with d=row|get_dict  %}{{ key }}:'{%  if d|get_val:key  %}{{ d|get_val:key }}{% endif %}'{% endwith %}{% if not forloop.last %},{% endif %}{% endif %}{% endfor %} }{% if not forloop.last %},{% endif %}
    {% endfor %}
    
    // WORKING!!!
    {% for row in data.pivot %}
        { 'Org_CustINN':'{{ row.Org_CustINN }}', 'Org_CustNm':'{{ row.Org_CustNm }}', 'name':'{{ row.name }}'{% for y in data.year %},{% with d=row|get_dict  %}'{{ y }}':'{%  if d|get_val:y  %}{{ d|get_val:y|floatformat:2 }}{% endif %}'{% endwith %}{% endfor %} }{% if not forloop.last %},{% endif %}
    {% endfor %}        
    
    
    def to_list(self, qs):
        mlist = list()
        for row in qs:
            d = {}
            for f in qs.columns:
                d[f] = getattr(row, f)
            mlist.append(d)
        return mlist