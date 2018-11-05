import json
import sys

from django.shortcuts import render
from django.db.models import Count, Sum, Min, F, Q
from django.db.models.functions import Extract
from django.http import HttpResponse, JsonResponse
from django.template.context_processors import csrf

from db.models import Hs, Target, Employee, Lpu, Market
from django.views.generic import View
from django.urls import reverse, reverse_lazy

# Filters identification
fempl = 'empl'
fmrkt = 'mrkt'
fyear = 'year'
fcust = 'cust'

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
    lpu_items = Lpu.objects.exclude(employee__isnull=True).exclude(cust_id=0).values('inn','name','cust_id').distinct().order_by('name')
    year_items = Hs.objects.values('PlanTYear').distinct().order_by('PlanTYear')

    lpu_items_org = Lpu.objects.exclude(employee__isnull=True).exclude(cust_id=0).filter(employee__org=org_id)
    lpu_active = lpu_items_org.values('cust_id')
    hs_active = Hs.objects.filter(cust_id__in=lpu_active)
    market_items = Market.objects.filter(org_id=org_id).values('id','name').order_by('name')
    market_enabled = list(market_items)
    year_items = hs_active.values('PlanTYear').distinct().order_by('PlanTYear')
    year_enabled = list(year_items)
    lpu_list = list(lpu_items.values('inn', 'name', 'cust_id').distinct().order_by('name'))

    print('start pivot')
    pivot1_data = hs_active.values('PlanTYear','market_name').annotate(product_cost_sum=Sum('TenderPrice')/1000000).\
        values('PlanTYear', 'market_name', 'product_cost_sum').order_by('market_name','PlanTYear')
    pivot2_data = hs_active.annotate(mon=Extract('ProcDt', 'month')).values('market_name', 'mon'). \
        annotate(product_cost_sum=Sum('TenderPrice')/1000000, product_count=Count('market_id')). \
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
                pivot1_data = hs_chart.values('market_name','PlanTYear').annotate(product_cost_sum=Sum('TenderPrice')/1000000). \
                    values('market_name', 'PlanTYear',  'product_cost_sum').order_by('market_name', 'PlanTYear')
                pivot2_data = hs_chart.annotate(mon=Extract('ProcDt','month')).values('market_name','mon').\
                    annotate(product_cost_sum=Sum('TenderPrice')/1000000,product_count=Count('market_id')). \
                    values('market_name', 'mon',  'product_cost_sum','product_count').order_by('market_name', 'mon')

                #pivot1_data = []
                #pivot2_data = []
                print("Prepare JSON")
                data = {'market_enabled':list(market_enabled),
                        'year_enabled':list(year_enabled),
                        'year_active': list(year_chart),
                        'lpu_enabled':list(lpu_enabled.values('cust_id').distinct()),
                        'pivot1': list(pivot1_data),
                        'pivot2': list(pivot2_data)
                        }
                print("Return DATA")
                return JsonResponse(data)

    return render(request,'ta_home.html', {})


def competitions(request):
    filters_enable = [fempl,fmrkt,fyear,fcust]
    args={}
    args.update(csrf(request))
    org_id = 1
    employee_items = Employee.objects.filter(org_id=org_id).values('name', iid=F('id')).order_by('name')
    market_items = Market.objects.filter(org_id=org_id).values('name', iid=F('id')).order_by('name')
    year_items = Hs.objects.extra(select = {'iid':'PlanTYear','name':'PlanTYear'}).values('name','iid').distinct().order_by('name')
    lpu_items = Lpu.objects.exclude(employee__isnull=True).exclude(cust_id=0).values('name',iid=F('cust_id'),ext=F('inn')).distinct().order_by('name')

    filters = []
    if fempl in filters_enable:
        filters.append({'id': fempl, 'type': 'btn', 'name': 'Таргет', 'expanded':'true', 'data': employee_items})
    if fmrkt in filters_enable:
        filters.append({'id': fmrkt, 'type': 'btn', 'name': 'Рынок', 'data': market_items})
    if fyear in filters_enable:
        filters.append({'id': fyear, 'type': 'btn', 'name': 'Год поставки', 'data': year_items})
    if fcust in filters_enable:
        filters.append({'id': fcust, 'type': 'tbl', 'name': 'Грузополучатель', 'data': lpu_items})

    args['filters'] = filters
    args['action_url'] = '#'

    return render(request,'ta_competitions.html', args)

def competitions_ajax(request):
    pass

class FiltersView(View):
    filters_list = [fempl,fmrkt,fyear,fcust]
    ajax_url = '#'
    template_name = 'ta_competitions.html'
    view_id = 'blank'
    view_name = 'Пустая страница'
    org_id = 1

    def filters(self, flt_active=None):
        if not flt_active:
            employee_enabled = Employee.objects.filter(org_id=self.org_id).values('name', iid=F('id')).order_by('name')
            market_enabled = Market.objects.filter(org_id=self.org_id).values('name', iid=F('id')).order_by('name')
            year_enabled = Hs.objects.exclude(PlanTYear__isnull=True).extra(select={'iid': 'PlanTYear', 'name': 'PlanTYear'}).\
                values('name','iid').distinct().order_by('name')
            lpu_enabled = Lpu.objects.exclude(cust_id=0).filter(employee__org=self.org_id).\
                values('name', iid=F('cust_id'),ext=F('inn')).distinct().order_by('name')
        else:
            employee_enabled = Employee.objects.filter(org_id=self.org_id).values(iid=F('id'))
            lpu_enabled = Lpu.objects.filter(employee__in=flt_active[fempl]).exclude(cust_id=0).values(iid=F('cust_id'))
            #if notarget_flag: hs_enabled = Hs.objects.all() else: hs_enabled = Hs.objects.filter(cust_id__in=lpu_enabled)
            hs_enabled = Hs.objects.exclude(cust_id=0).filter(cust_id__employee__in=flt_active[fempl])
            year_enabled = hs_enabled.values('PlanTYear').distinct().values(iid=F('PlanTYear'))
            market_enabled = hs_enabled.values('market_id').annotate(id=F('market_id')).distinct().values(iid=F('market_id'))

        filters = []
        if fempl in self.filters_list:
            filters.append({'id': fempl, 'type': 'btn', 'name': 'Таргет', 'expanded': 'true', 'data': list(employee_enabled)})
        if fmrkt in self.filters_list:
            filters.append({'id': fmrkt, 'type': 'btn', 'name': 'Рынок', 'data': list(market_enabled)})
        if fyear in self.filters_list:
            filters.append({'id': fyear, 'type': 'btn', 'name': 'Год поставки', 'data': list(year_enabled)})
        if fcust in self.filters_list:
            filters.append({'id': fcust, 'type': 'tbl', 'name': 'Грузополучатель', 'data': list(lpu_enabled)})

        return filters

    def get_filter(self,flt,flt_id):
        return next(f for f in flt if f['id'] == flt_id )

    def get_filters_dict(self,flt):
        filters = {}
        for f in self.filters_list:
            filters[f]=self.get_filter(flt,f)
        return filters

    def data(self, flt=None, flt_active=None):
        return {}

    def get(self, request, *args, **kwargs):
        filters = self.filters()
        data = self.data(filters)
        return render(request, self.template_name, {'filters': filters,
                                                    'data': data,
                                                    'view': {'id': self.view_id, 'name': self.view_name},
                                                    'ajax_url': self.ajax_url})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST:
                flt_active = {}
                for f in self.filters_list:
                    flt_str = request.POST.get('{}_active'.format(f), '')
                    flt_active[f] = [int(e) for e in flt_str.split(',')] if flt_str else []

                #print('------ From FrontEnd -----')
                #print(flt_active)
                #print(len(flt_active[fcust]))

                filters = self.filters(flt_active)
                data = self.data(filters, flt_active)
                response = {'filters': self.get_filters_dict(filters),
                            'data': data,
                            'view': {'id' : self.view_id, 'name': self.view_name},
                            'ajax_url': self.ajax_url}
                return JsonResponse(response)

        return self.get(request)

class SalessheduleView(FiltersView):
    template_name = 'ta_salesshedule.html'
    ajax_url = reverse_lazy('widgetpages:salesshedule')
    view_id = 'salesshedule'
    view_name = 'График продаж'

    def data(self, flt=None, flt_active=None):
        pivot_data = {}
        if flt:
            hs_active = Hs.objects.exclude(cust_id=0)
            if flt_active:
                hs_active = hs_active.filter(cust_id__employee__in=flt_active[fempl], \
                                             cust_id__in=flt_active[fcust], \
                                             PlanTYear__in=flt_active[fyear], \
                                             market_id__in=flt_active[fmrkt])
            else:
                hs_active = hs_active.filter(cust_id__employee__org_id=self.org_id)

            pivot_data['year'] = list(hs_active.values(iid=F('PlanTYear')).distinct().order_by('iid'))
            pivot_data['pivot1'] = list(hs_active.values('market_name',iid=F('PlanTYear')).annotate(
                product_cost_sum=Sum('TenderPrice') / 1000000). \
                values('iid', 'market_name', 'product_cost_sum').order_by('market_name', 'iid'))
            pivot_data['pivot2'] = list(hs_active.annotate(mon=Extract('ProcDt', 'month')).values('market_name', 'mon'). \
                annotate(product_cost_sum=Sum('TenderPrice') / 1000000, product_count=Count('market_id')). \
                values('market_name', 'mon', 'product_cost_sum', 'product_count').order_by('market_name', 'mon'))

        return pivot_data

class CompetitionsView(FiltersView):
    template_name = 'ta_competitions.html'
    ajax_url = reverse_lazy('widgetpages:competitions')
    view_id = 'competitions'
    view_name = 'Конкурентный анализ'