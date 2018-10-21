from django.shortcuts import render
from db.models import Hs, Target
from django.db.models import Count, Sum, Min

# Create your views here.
def Home(request):
    args={}
    return render(request,'ta_main.html', args)

def sales_shedule(request):
    args={}
    market_items = ['Дорипрекс', 'Тахокомб','Фендивия','Феринжект']
    market_items = Hs.objects.values('market').distinct().order_by('market')
    target_items = Target.objects.values('employee').distinct().order_by('employee')
    year_items = Hs.objects.values('delivery_year').distinct().order_by('delivery_year')
    entity_items = Target.objects.exclude(employee__isnull=True).values('inn','entity').distinct().order_by('entity')
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
