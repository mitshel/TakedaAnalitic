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

class FiltersView(View):
    filters_list = [fempl,fmrkt,fyear,fcust]
    ajax_url = '#'
    template_name = 'ta_competitions.html'
    view_id = 'blank'
    view_name = 'Пустая страница'
    org_id = 1

    def filter_empl(self, flt_active=None):
        if not flt_active:
            employee_enabled = Employee.objects.filter(org_id=self.org_id).values('name', iid=F('id')).order_by('name')
        else:
            employee_enabled = Employee.objects.filter(org_id=self.org_id).values(iid=F('id'))
        return [{'name':'Без учета Таргет','iid':0}]+list(employee_enabled)

    def filter_mrkt(self, flt_active=None):
        if not flt_active:
            market_enabled = Market.objects.filter(org_id=self.org_id).values('name', iid=F('id')).order_by('name')
        else:
            hs_enabled = Hs.objects.exclude(cust_id=0)
            if not (0 in flt_active[fempl]):
                hs_enabled = hs_enabled.filter(cust_id__employee__in=flt_active[fempl])
            market_enabled = hs_enabled.values('market_id').annotate(id=F('market_id')).distinct().values(iid=F('market_id'))
        return list(market_enabled)

    def filter_year(self, flt_active=None):
        if not flt_active:
            year_enabled = Hs.objects.exclude(PlanTYear__isnull=True).\
                extra(select={'iid': 'PlanTYear', 'name': 'PlanTYear'}). \
                values('name', 'iid').distinct().order_by('name')
        else:
            hs_enabled = Hs.objects.exclude(cust_id=0)
            if not (0 in flt_active[fempl]):
                hs_enabled = hs_enabled.filter(cust_id__employee__in=flt_active[fempl])
            year_enabled = hs_enabled.values('PlanTYear').distinct().values(iid=F('PlanTYear'))
        return list(year_enabled)

    def filter_cust(self, flt_active=None):
        if not flt_active:
            lpu_enabled = Lpu.objects.exclude(cust_id=0).filter(employee__org=self.org_id). \
                values('name', iid=F('cust_id'), ext=F('inn')).distinct().order_by('name')
        else:
            lpu_enabled = Lpu.objects.filter(employee__in=flt_active[fempl]).exclude(cust_id=0).values(iid=F('cust_id'))
        return list(lpu_enabled)

    def filters(self, flt_active=None):
        filters = []
        for f in self.filters_list:
            if fempl == f :
                filters.append({'id': fempl, 'type': 'btn', 'name': 'Таргет', 'expanded': 'true', 'data': self.filter_empl(flt_active)})
            if fmrkt == f:
                filters.append({'id': fmrkt, 'type': 'btn', 'name': 'Рынок', 'data': self.filter_mrkt(flt_active)})
            if fyear == f:
                filters.append({'id': fyear, 'type': 'btn', 'name': 'Год поставки', 'data': self.filter_year(flt_active)})
            if fcust == f:
                filters.append({'id': fcust, 'type': 'tbl', 'name': 'Грузополучатель', 'data': self.filter_cust(flt_active)})

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
            hs_active = Hs.objects.exclude(cust_id=0).exclude(PlanTYear__isnull=True)
            if flt_active:
                if (0 in flt_active[fempl]):
                    # Если выбрано 'Без учета Таргет' то не фильтруем ни сотрудников ни ЛПУ
                    hs_active = hs_active.filter(PlanTYear__in=flt_active[fyear], \
                                                 market_id__in=flt_active[fmrkt])
                else:
                    hs_active = hs_active.filter(cust_id__employee__in=flt_active[fempl], \
                                                 cust_id__in=flt_active[fcust], \
                                                 PlanTYear__in=flt_active[fyear], \
                                                 market_id__in=flt_active[fmrkt])

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