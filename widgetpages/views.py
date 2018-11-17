from django.shortcuts import render
from django.db.models import Count, Sum, F
from django.db.models.functions import Extract
from django.http import JsonResponse

from db.models import Market, StatusT, Org
from db.models import Hs_create
from django.views.generic import View
from django.urls import reverse_lazy

from widgetpages.queries import q_employees, q_markets, q_markets_hs, q_years_hs, q_status, q_status_hs
from db.rawmodel import RawModel

# Filters identification
fempl = 'empl'
fmrkt = 'mrkt'
fyear = 'year'
fcust = 'cust'
fstat = 'stat'
finnr = 'innr'
ftrnr = 'trnr'
fwinr = 'winr'

# Create your views here.
def extra_in_filter(model, field, flt):
    db_table = model if isinstance(model,str) else model._meta.db_table
    if flt:
        if (len(flt['list']) > 0):
            ef = '[{}].{} {}in ({})'. \
                format(db_table, field,
                       'not ' if flt['select'] else '',
                       ','.join([str(e) for e in flt['list']]))
        else:
            ef = '1=1' if flt['select'] else '1>1'
    else:
        ef = '1=1'

    return ef

def Home(request):
    args={}
    return render(request,'ta_hello.html', args)

class FiltersView(View):
    filters_list = [fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust]
    ajax_url = '#'
    template_name = 'ta_competitions.html'
    view_id = 'blank'
    view_name = 'Пустая страница'

    def init_dynamic_org(self):
        org = Org.objects.filter(employee__users=self.request.user)
        org_id = org[0].id if org else 0
        self.Hs = Hs_create('org_CACHE_{}'.format(org_id))
        return org_id

    def filter_empl(self, flt_active=None, org_id=0):
        employee_raw = RawModel(q_employees).filter(username=self.request.user.username)
        if not flt_active:
            employee_enabled = employee_raw.filter(fields='id as iid, name').order_by('name')
        else:
            employee_enabled = employee_raw.filter(fields='id as iid')
        employee_list=list(employee_enabled.open().fetchall())
        employee_enabled.close()
        return [{'name':'Без учета Таргет','iid':0}]+employee_list

    def filter_mrkt(self, flt_active=None, org_id=0):
        if not flt_active:
            market_enabled = RawModel(q_markets).filter(fields="id as iid, name").filter(org_id=org_id).order_by('name')
        else:
            market_enabled = RawModel(q_markets_hs).filter(fields="a.id as iid").filter(org_id=org_id)
            if not (0 in flt_active[fempl]['list']):
                market_enabled = market_enabled.filter(employee_in=extra_in_filter('c', 'employee_id', flt_active[fempl]))
        market_list = list(market_enabled.open().fetchall())
        market_enabled.close()
        return market_list

    def filter_year(self, flt_active=None, org_id=0):
        if not flt_active:
            year_enabled = RawModel(q_years_hs).filter(fields="PlanTYear as iid, PlanTYear as name").filter(org_id=org_id).order_by('PlanTYear')
        else:
            year_enabled = RawModel(q_years_hs).filter(fields="PlanTYear as iid").filter(org_id=org_id)
            if not (0 in flt_active[fempl]['list']):
                year_enabled = year_enabled.filter(employee_in=extra_in_filter('b', 'employee_id', flt_active[fempl]))
        year_list = list(year_enabled.open().fetchall())
        year_enabled.close()
        return year_list

    def filter_stat(self, flt_active=None, org_id=0):
        if not flt_active:
            status_enabled = RawModel(q_status).filter(fields="id as iid, name").order_by('name')
        else:
            status_enabled = RawModel(q_status_hs).filter(fields="a.id as iid").filter(org_id=org_id)
            if not (0 in flt_active[fempl]['list']):
                status_enabled = status_enabled.filter(employee_in=extra_in_filter('c', 'employee_id', flt_active[fempl]))
        status_list = list(status_enabled.open().fetchall())
        status_enabled.close()
        return list(status_list)

    def filter_innr(self, flt_active=None, org_id=0):
        return []

    def filter_trnr(self, flt_active=None, org_id=0):
        return []

    def filter_winr(self, flt_active=None, org_id=0):
        return []

    def filter_cust(self, flt_active=None, org_id=0):
        return []

    def filters(self, flt_active=None, org_id=0):
        filters = []
        for f in self.filters_list:
            if fempl == f :
                filters.append({'id': fempl, 'type': 'btn', 'name': 'Таргет', 'icon':'user', 'expanded': 'false', 'data': self.filter_empl(flt_active, org_id)})
            if fmrkt == f:
                filters.append({'id': fmrkt, 'type': 'btn', 'name': 'Рынок', 'icon':'shopping-cart','data': self.filter_mrkt(flt_active, org_id)})
            if fyear == f:
                filters.append({'id': fyear, 'type': 'btn', 'name': 'Год поставки', 'icon':'calendar', 'data': self.filter_year(flt_active, org_id)})
            if fstat == f:
                filters.append({'id': fstat, 'type': 'btn', 'name': 'Статус торгов', 'icon':'check-square', 'data': self.filter_stat(flt_active, org_id)})
            if finnr == f:
                filters.append({'id': finnr, 'type': 'tbl', 'name': 'МНН', 'icon':'globe', 'data': self.filter_innr(flt_active, org_id)})
            if ftrnr == f:
                filters.append({'id': ftrnr, 'type': 'tbl', 'name': 'Торговое наименование', 'icon':'trademark', 'data': self.filter_trnr(flt_active, org_id)})
            if fwinr == f:
                filters.append({'id': fwinr, 'type': 'tbl', 'name': 'Победитель торгов', 'icon':'handshake', 'data': self.filter_winr(flt_active, org_id)})
            if fcust == f:
                filters.append({'id': fcust, 'type': 'tbl', 'name': 'Грузополучатель', 'icon':'ambulance', 'data': self.filter_cust(flt_active, org_id)})

        return filters

    def get_filter(self,flt,flt_id):
        return next(f for f in flt if f['id'] == flt_id )

    def get_filters_dict(self,flt):
        filters = {}
        for f in self.filters_list:
            filters[f]=self.get_filter(flt,f)
        return filters

    def data(self, flt=None, flt_active=None, org_id=0):
        return {}

    def get(self, request, *args, **kwargs):
        org_id = self.init_dynamic_org()
        filters = self.filters(None, org_id)
        data = self.data(filters, None, org_id)
        return render(request, self.template_name, {'filters': filters,
                                                    'data': data,
                                                    'view': {'id': self.view_id, 'name': self.view_name},
                                                    'ajax_url': self.ajax_url})

    def post(self, request, *args, **kwargs):
        org_id = self.init_dynamic_org()
        if request.is_ajax():
            if request.POST:
                flt_active = {}
                for f in self.filters_list:
                    flt_str = request.POST.get('{}_active'.format(f), '')
                    flt_select = request.POST.get('{}_select'.format(f), '')
                    flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select)}

                filters = self.filters(flt_active, org_id)
                data = self.data(filters, flt_active, org_id)
                response = {'filters': self.get_filters_dict(filters),
                            'data': data,
                            'view': {'id' : self.view_id, 'name': self.view_name},
                            'ajax_url': self.ajax_url}
                return JsonResponse(response)

        return self.get(request)

class SalessheduleView(FiltersView):
    filters_list = [fempl, fmrkt, fyear, fcust]
    template_name = 'ta_salesshedule.html'
    ajax_url = reverse_lazy('widgetpages:salesshedule')
    view_id = 'salesshedule'
    view_name = 'График продаж'

    def data(self, flt=None, flt_active=None, org_id=0):
        pivot_data = {}
        if flt:
            hs_active = self.Hs.objects.exclude(cust_id=0).exclude(PlanTYear__isnull=True)
            if flt_active:
                if not (0 in flt_active[fempl]['list']):
                    # Если не выбрано 'Без учета Таргет' то фильтруем по сотрудникам
                    hs_active = hs_active.filter(cust_id__employee__in=flt_active[fempl]['list'])

                hs_active = hs_active.filter(PlanTYear__in=flt_active[fyear]['list'], \
                                             market_id__in=flt_active[fmrkt]['list']).\
                                             extra(where=[extra_in_filter(self.Hs,'Cust_ID',flt_active[fcust])])

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
    view_name = 'Конкурентный анализ (тыс.руб.)'

    def data(self, flt=None, flt_active=None, org_id=0):
        data = {}
        if not flt_active:
            years_active = list(self.Hs.objects.exclude(PlanTYear__isnull=True).\
                values('PlanTYear').distinct().order_by('PlanTYear').\
                values_list('PlanTYear', flat=True))
        else:
            years_active = flt_active[fyear]['list']

        data['year'] = years_active

        return data