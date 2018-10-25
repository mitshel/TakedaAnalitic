import json

from django.shortcuts import render
from django.db.models import Count, Sum, Min
from django.http import HttpResponse, JsonResponse
from django.template.context_processors import csrf

from db.models import Hs, Target, Employee

# Create your views here.
def Home(request):
    args={}
    return render(request,'ta_main.html', args)

def sales_shedule(request):
    args={}
    args.update(csrf(request))
    market_items = ['Дорипрекс', 'Тахокомб','Фендивия','Феринжект']
    market_items = Hs.objects.values('market').distinct().order_by('market')
    # target_items = Target.objects.values('employee_name').distinct().order_by('employee_name')
    target_items = Employee.objects.order_by('name')
    entity_items = Target.objects.exclude(employee__isnull=True).values('inn','entity','id').distinct().order_by('entity')
    year_items = Hs.objects.values('delivery_year').distinct().order_by('delivery_year')
    pivot = []

    for market in market_items:
        data = Hs.objects.filter(market=market['market']).values('delivery_year').annotate(product_cost_sum=Sum('product_cost')).values('delivery_year','product_cost_sum')
        pivot.append({'name':market['market'],'data':data})

    args['pivot'] = pivot
    args['year_min'] = Hs.objects.aggregate(delivery_year_min=Min('delivery_year'))['delivery_year_min']
    args['market'] = market_items
    args['target'] = target_items
    args['year'] = year_items
    args['entity'] = entity_items

    return render(request,'ta_salesshedule.html', args)

def filters_update(request):
    data = {}
    return data

def filters_employee(request):
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST:
                #print(">>>>",request.POST)
                empl_active = request.POST.get('empl_active','')
                empl_active = [int(e) for e in empl_active.split(',')]  if empl_active else []

                lpu_items = Target.objects.filter(employee__in=empl_active)
                inn_active = lpu_items.values('inn')
                hs_active = Hs.objects.filter(inn_lpu__in=inn_active)
                market_items = hs_active.values('market').distinct().order_by('market')
                market_enabled = list(market_items)
                year_items = hs_active.values('delivery_year').distinct().order_by('delivery_year')
                year_enabled = list(year_items)
                lpu_list = list(lpu_items.values('inn','entity','id').distinct().order_by('entity'))
                print(market_enabled)
                print(year_enabled)
                print(lpu_list)
                data = {'status':1, 'market_active':market_enabled, 'year_active':year_enabled,'lpu':lpu_list}
                print(data)

                # response = HttpResponse()
                # response['Content-Type'] = "text/javascript"
                # response.write(data)
                # return response
                return JsonResponse(data)

    return render(request,'ta_home.html', {})