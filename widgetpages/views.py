import json

from django.shortcuts import render
from django.db.models import Count, Sum, Min, F, Q
from django.db.models.functions import Extract
from django.http import HttpResponse, JsonResponse
from django.template.context_processors import csrf

from db.models import Hs, Target, Employee, Lpu, Market

# Create your views here.
def Home(request):
    args={}
    return render(request,'ta_main.html', args)

def sales_shedule(request):
    args={}
    args.update(csrf(request))
    org_id = 1
    print('start sales shedule')
    employee_items = Employee.objects.filter(org_id=org_id).order_by('name')
    lpu_items = Lpu.objects.exclude(employee__isnull=True).values('inn','name','cust_id').distinct().order_by('name')
    year_items = Hs.objects.values('PlanTYear').distinct().order_by('PlanTYear')

    lpu_items_org = Lpu.objects.exclude(employee__isnull=True).filter(employee__org=org_id)
    lpu_active = lpu_items_org.values('cust_id')
    hs_active = Hs.objects.filter(cust_id__in=lpu_active)
    market_items = Market.objects.filter(org_id=org_id).values('id','name').order_by('name')
    market_enabled = list(market_items)
    year_items = hs_active.values('PlanTYear').distinct().order_by('PlanTYear')
    year_enabled = list(year_items)
    lpu_list = list(lpu_items.values('inn', 'name', 'cust_id').distinct().order_by('name'))

    print('start pivot')
    pivot1_data = hs_active.values('PlanTYear','market_name').annotate(product_cost_sum=Sum('TenderPrice')).\
        values('PlanTYear', 'market_name', 'product_cost_sum').order_by('market_name','PlanTYear')
    pivot2_data = hs_active.annotate(mon=Extract('ProcDt', 'month')).values('market_name', 'mon'). \
        annotate(product_cost_sum=Sum('TenderPrice'), product_count=Count('market_id')). \
        values('market_name', 'mon', 'product_cost_sum','product_count').order_by('market_name', 'mon')

    #pivot = []
    #for market in market_items:
    #    pivot.append({'name':market['market'],'data':data})

    args['pivot1'] = pivot1_data
    args['pivot2'] = pivot2_data
    args['year_min'] = hs_active.aggregate(PlanTYear_min=Min('PlanTYear'))['PlanTYear_min']
    args['market'] = market_items
    args['employee'] = employee_items
    args['year'] = year_items
    args['lpu'] = lpu_items
    print(args)

    return render(request,'ta_sales.html', args)

def filters_update(request):
    data = {}
    return data

def filters_employee(request):
    org_id = 1
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST:
                #print(">>>>",request.POST)
                empl_active = request.POST.get('empl_active','')
                empl_active = [int(e) for e in empl_active.split(',')]  if empl_active else []

                market_active = request.POST.get('market_active','')
                market_active = [int(e) for e in market_active.split(',')] if market_active else []

                year_active = request.POST.get('year_active','')
                year_active = [int(e) for e in year_active.split(',')] if year_active else []

                lpu_active = request.POST.get('lpu_active','')
                lpu_active = [int(e) for e in lpu_active.split(',')] if lpu_active else []

                print('------ From FrontEnd -----')
                print(empl_active)
                print(market_active)
                print(year_active)
                print(lpu_active)

                notarget_flag = (0 in empl_active)

                # Enabled - Доступны (видны на фильтре) те ЛПУ к которым привязаны выбранные в фильтре сотрудники
                lpu_enabled = Lpu.objects.filter(employee__in=empl_active).exclude(cust_id=0)
                if notarget_flag:
                    hs_enabled = Hs.objects.all()
                else:
                    hs_enabled = Hs.objects.filter(cust_id__in=lpu_enabled)
                year_enabled = hs_enabled.values('PlanTYear').distinct().order_by('PlanTYear')
                market_enabled = hs_enabled.values('market_id').annotate(id=F('market_id')).distinct().values('id')

                print("Prepare chart data")
                # Chart - данные, иcпользующиеся для вывода графиков
                year_chart = year_enabled.filter(PlanTYear__in=year_active)
                if notarget_flag:
                    hs_chart = hs_enabled.filter(PlanTYear__in=year_active, market_id__in=market_active)
                else:
                    hs_chart = hs_enabled.filter(cust_id__in=lpu_active, PlanTYear__in=year_active, market_id__in=market_active)

                print("Prepare pivot data")
                pivot1_data = hs_chart.values('market_name','PlanTYear').annotate(product_cost_sum=Sum('TenderPrice')). \
                    values('market_name', 'PlanTYear',  'product_cost_sum').order_by('market_name', 'PlanTYear')
                pivot2_data = hs_chart.annotate(mon=Extract('ProcDt','month')).values('market_name','mon').\
                    annotate(product_cost_sum=Sum('TenderPrice'),product_count=Count('market_id')). \
                    values('market_name', 'mon',  'product_cost_sum','product_count').order_by('market_name', 'mon')

                #pivot1_data = []
                #pivot2_data = []
                print("Prepare JSON")
                data = {'market_enabled':list(market_enabled),
                        'year_enabled':list(year_enabled),
                        'year_active': list(year_chart),
                        'lpu_enabled':list(lpu_enabled.values('inn', 'name', 'cust_id').distinct().order_by('name')),
                        'pivot1': list(pivot1_data),
                        'pivot2': list(pivot2_data)
                        }
                print("Return DATA")
                print(data)
                return JsonResponse(data)

    return render(request,'ta_home.html', {})
