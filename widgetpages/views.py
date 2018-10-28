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
    #market_items = ['Дорипрекс', 'Тахокомб','Фендивия','Феринжект']
    #market_items = Hs.objects.values('market').distinct().order_by('market')
    target_items = Employee.objects.order_by('name')
    entity_items = Target.objects.exclude(employee__isnull=True).values('inn','entity','id').distinct().order_by('entity')
    year_items = Hs.objects.values('delivery_year').distinct().order_by('delivery_year')

    lpu_items = Target.objects.exclude(employee__isnull=True)
    inn_active = lpu_items.values('inn')
    hs_active = Hs.objects.filter(inn_lpu__in=inn_active)
    market_items = hs_active.values('market').distinct().order_by('market')
    market_enabled = list(market_items)
    year_items = hs_active.values('delivery_year').distinct().order_by('delivery_year')
    year_enabled = list(year_items)
    lpu_list = list(lpu_items.values('inn', 'entity', 'id').distinct().order_by('entity'))


    pivot_data = Hs.objects.values('delivery_year','market').annotate(product_cost_sum=Sum('product_cost')).\
        values('delivery_year', 'market', 'product_cost_sum').order_by('market','delivery_year')

    #pivot = []
    #for market in market_items:
    #    pivot.append({'name':market['market'],'data':data})

    args['pivot'] = pivot_data
    args['year_min'] = hs_active.aggregate(delivery_year_min=Min('delivery_year'))['delivery_year_min']
    args['market'] = market_items
    args['target'] = target_items
    args['year'] = year_items
    args['entity'] = entity_items
    print(args)

    return render(request,'ta_sales.html', args)

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

                entity_active = request.POST.get('entity_active','')
                entity_active = [int(e) for e in entity_active.split(',')] if entity_active else []

                year_active = request.POST.get('year_active','')
                year_active = [int(e) for e in year_active.split(',')] if year_active else []

                market_active = request.POST.get('market_active','')
                market_active = [e for e in market_active.split(',')] if market_active else []

                lpu_items = Target.objects.filter(employee__in=empl_active)
                inn_active = lpu_items.filter(inn__in=entity_active).values('inn')
                hs_active = Hs.objects.filter(inn_lpu__in=inn_active, delivery_year__in=year_active, market__in=market_active)
                market_items = hs_active.values('market').distinct().order_by('market')
                market_enabled = list(market_items)
                year_items = hs_active.values('delivery_year').distinct().order_by('delivery_year')
                year_enabled = list(year_items)
                lpu_list = list(lpu_items.values('inn','entity','id').distinct().order_by('entity'))
                print(entity_active)
                print(market_enabled)
                print(year_enabled)
                print(lpu_list)

                pivot_data = hs_active.values('market','delivery_year').annotate(
                    product_cost_sum=Sum('product_cost')). \
                    values('market','delivery_year', 'product_cost_sum').order_by('market', 'delivery_year')

                data = {'entity_len':len(lpu_list), 'status':1, 'market_active':market_enabled, 'year_active':year_enabled,'lpu':lpu_list, 'pivot':list(pivot_data)}
                print(data)

                return JsonResponse(data)

    return render(request,'ta_home.html', {})