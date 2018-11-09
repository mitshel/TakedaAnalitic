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
        
 // WORKING!!!   
 var competitions_data = [
    {% for row in data.pivot %}
        { {% for k,v in row.items %}'{{ k }}':'{% if k|slice:"0:2" == "20" %}{{ v|floatformat:2 }}{% else %}{{ v }}{% endif %}'{% if not forloop.last %},{% endif %}{% endfor %} }{% if not forloop.last %},{% endif %}
    {% endfor %}
]     
    
    
    def to_list(self, qs):
        mlist = list()
        for row in qs:
            d = {}
            for f in qs.columns:
                d[f] = getattr(row, f)
            mlist.append(d)
        return mlist
        
        <thead>
            <tr>
                <th>ИНН</th>
                <th width="50%">ЛПУ</th>
                <th>Торговая марка</th>
                <th>2018</th>
                <!--{ % for y in data.year %}<th>{ { y }}</th>{ % endfor %}-->
            </tr>
        </thead>
                     endRender: function ( rows, group ) {
                        return group;  +' ('+rows.count()+')';
                    },
                           
                    //endRender: function ( rows, group ) {
                    //    {% for y in data.year %}
                    //    var sum{{ y }} = rows
                    //        .data()
                    //        .pluck('{{ y }}')
                    //        .reduce( function (a, b) {
                    //            return a + b.replace(/[^\d]/g, '')*1;
                    //        }, 0) / 100;
                    //    {% endfor %}

                    //    return $('<tr/>')
                    //        .append( '<td colspan="2">'+group+' ИТОГ:</td>' )
                    //        {% for y in data.year %}
                    //        .append( '<td>'+sum{{ y }}.toFixed(2)+'</td>' ){% endfor %};
                    //},                
                    
                    endRender: function ( rows, group ) {
                        {% for y in data.year %}
                        var sum{{ y }} = rows
                            .data()
                            .pluck('{{ y }}')
                            .reduce( function (a, b) {
                                return a + b.replace(/[^\d]/g, '')*1;
                            }, 0) / 100;
                        {% endfor %}

                        return $('<tr/>')
                            .append( '<td colspan="2">'+group+' ИТОГ:</td>' )
                            {% for y in data.year %}
                            .append( '<td>'+sum{{ y }}.toFixed(2)+'</td>' ){% endfor %};
                    },      
                    
                    
                    endRender: function ( rows, group ) {
                        {% for y in data.year %}
                        var sum{{ forloop.counter0|add:3 }} = rows
                            .data()
                            .pluck({{ forloop.counter0|add:3 }})
                            .reduce( function (a, b) {
                                return a + b.replace(/[^\d]/g, '')*1;
                            }, 0) / 100000;
                        {% endfor %}

                        return $('<tr/>')
                            .append( '<td colspan="2">'+group+' ИТОГ:</td>' )
                            {% for y in data.year %}
                            .append( '<td>'+sum{{ forloop.counter0|add:3 }}.toFixed(2)+'</td>' ){% endfor %};
                    },      
                    
                    for (i = 3; i <= $('#ta_competitions_table thead th').length; i++) {                    