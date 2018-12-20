import datetime

from django.shortcuts import render
from django.http import JsonResponse

from db.models import Org
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy

from widgetpages import queries
from db.rawmodel import RawModel
from farmadmin.views import OrgBaseMixin, bOrgUSER, bOrgSESSION, bOrgPOST

# Filters identification
fempl = 'empl'
fempa = 'empa'
fmrkt = 'mrkt'
fyear = 'year'
fcust = 'cust'
fstat = 'stat'
finnr = 'innr'
ftrnr = 'trnr'
fwinr = 'winr'


def extra_in_filter(field, flt):
    if flt:
        if (len(flt['list']) > 0):
            ef = '{} {}in ({})'. \
                format(field,
                       'not ' if flt['select'] else '',
                       ','.join([str(e) for e in flt['list']]))
        else:
            ef = '' if flt['select'] else '1>1'  #1=1
    else:
        ef = '' #1=1

    return ef

def target_in_filter(field, target):
    if target:
        if (len(target) > 0):
            ef = '{} in ({})'.format(field,','.join([str(e['iid']) for e in target]))
        else:
            ef = ''
    else:
        ef = ''

    return ef


# Удаление неуникальных элементов из списка
def unique(obj: iter):
    args = []
    for a in obj:
        if a not in args:
            args.append(a)
            yield a

class OrgMixin(OrgBaseMixin):
    SETUP_METHODS = bOrgPOST | bOrgUSER

class HomeView(OrgMixin, TemplateView):
    template_name = 'ta_hello.html'

class FiltersView(OrgMixin, TemplateView):
    template_name = 'ta_competitions.html'
    filters_list = [fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust]
    ajax_url = '#'
    view_id = 'blank'
    view_name = 'Пустая страница'
    select_market_type = 0

    # def zero_in(self, flt_active, fname):
    #     return ((flt_active[fname]['select'] == 1) and not (0 in flt_active[fname]['list'])) or \
    #            ((flt_active[fname]['select'] == 0) and (0 in flt_active[fname]['list']))

    def zero_in(self, flt_active, fname):
        return flt_active[fname]['select'] if flt_active else 0
        # return (flt_active[fname]['select'] == 1)

    def get_initial_targets(self):
        initial_employee = RawModel(queries.q_employees).filter(fields = 'id as iid, name', username=self.request.user.username).order_by('name')
        initial_targets=list(initial_employee.open().fetchall())
        initial_employee.close()
        return initial_targets

    def filter_empl(self, flt_active=None, org_id=0, targets = []):
        # employee_raw = RawModel(queries.q_employees).filter(username=self.request.user.username)
        if not flt_active:
            # employee_enabled = employee_raw.filter(fields='id as iid, name').order_by('name')
            employee_list = targets
        else:
            # employee_enabled = employee_raw.filter(fields='id as iid')
            employee_list = [{'iid':t['iid']} for t in targets]

        # employee_list=list(employee_enabled.open().fetchall())
        # employee_enabled.close()
        return {'id': fempl,
                'type': 'btn',
                'name': 'Таргет',
                'icon':'user',
                'expanded': 'false',
                'data': employee_list}
                # 'data': [{'name':'Без учета Таргет','iid':0}]+employee_list}

    def filter_mrkt(self, flt_active=None, org_id=0, targets = []):
        market_list_active = []
        if not flt_active:
            # Показываем все доступные рынки для сотрудника организации
            market_enabled = RawModel(queries.q_markets).filter(fields="id as iid, name",org_id=org_id).order_by('name')
            # Но активными будут выглядеть только рынки, доступные сотруднику (через ЛПУ)
            market_active = RawModel(queries.q_markets_hs_empl).filter(fields="a.id as iid",org_id=org_id, employee_in=target_in_filter('e.employee_id', targets))
            market_list_active = [e['iid'] for e in market_active.open().fetchall()]
            market_active.close()
        else:
            # Показываем все доступные рынки
            market_enabled = RawModel(queries.q_markets_hs).filter(fields="a.id as iid",org_id=org_id)
            #  Если отключена кнопка "Без учета Target" то фильтруем по выбранным сотрудникам
            if not self.zero_in(flt_active, fempa):
                market_enabled = market_enabled.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))

        market_list = list(market_enabled.open().fetchall())
        market_enabled.close()
        return {'id': fmrkt,
                'type': 'btn',
                'name': 'Рынок',
                'icon':'shopping-cart',
                'data': market_list,
                'data0': market_list_active}

    def filter_year(self, flt_active=None, org_id=0, targets = []):
        year_list_active = []
        if not flt_active:
            # Показываем все доступные Годы для сотрудника организации
            year_enabled = RawModel(queries.q_years_hs).filter(fields="PlanTYear as iid, PlanTYear as name",org_id=org_id).order_by('PlanTYear')
            # Но активными будут выглядеть только Годы, доступные сотруднику (через ЛПУ)
            year_active = RawModel(queries.q_years_hs_empl).filter(fields="PlanTYear as iid",org_id=org_id, employee_in=target_in_filter('e.employee_id', targets))
            year_list_active = [e['iid'] for e in year_active.open().fetchall()]
            year_active.close()
        else:
            # Показываем все доступные Годы
            year_enabled = RawModel(queries.q_years_hs).filter(fields="PlanTYear as iid",org_id=org_id)
            #  Если отключена кнопка "Без учета Target" то фильтруем по выбранным сотрудникам
            if not self.zero_in(flt_active, fempa):
                year_enabled = year_enabled.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))

        year_list = list(year_enabled.open().fetchall())
        year_enabled.close()
        return {'id': fyear,
                'type': 'btn',
                'name': 'Год поставки',
                'icon':'calendar',
                'data': year_list,
                'data0': year_list_active}

    def filter_stat(self, flt_active=None, org_id=0, targets = []):
        if not flt_active:
            status_enabled = RawModel(queries.q_status).filter(fields="id as iid, name").order_by('name')
        else:
            status_enabled = RawModel(queries.q_status_hs).filter(fields="a.id as iid").filter(org_id=org_id)
            if not self.zero_in(flt_active, fempa):
                status_enabled = status_enabled.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))
        status_list = list(status_enabled.open().fetchall())
        status_enabled.close()
        return {'id': fstat,
                'type': 'btn',
                'name': 'Статус торгов',
                'icon':'check-square',
                'data': status_list}

    def filter_innr(self, flt_active=None, org_id=0, targets = []):
        return {'id': finnr,
                'type': 'ajx',
                'name': 'МНН',
                'icon':'globe',
                'data': []}

    def filter_trnr(self, flt_active=None, org_id=0, targets = []):
        return {'id': ftrnr,
                'type': 'ajx',
                'name': 'Торговое наименование',
                'icon':'trademark',
                'data': []}

    def filter_winr(self, flt_active=None, org_id=0, targets = []):
        return {'id': fwinr,
                'type': 'ajx',
                'name': 'Победитель торгов',
                'icon':'handshake',
                'data': []}

    def filter_cust(self, flt_active=None, org_id=0, targets = []):
        return {'id': fcust,
                'type': 'ajx',
                'name': 'Грузополучатель',
                'icon':'ambulance',
                'data': []}

    def filters(self, flt_active=None, org_id=0, targets=[]):
        filters = []
        filter_empl = self.filter_empl(flt_active, org_id)
        for f in self.filters_list:
            if fempl == f:
                filters.append(self.filter_empl(flt_active, org_id, targets))
            if fmrkt == f:
                filters.append(self.filter_mrkt(flt_active, org_id, targets))
            if fyear == f:
                filters.append(self.filter_year(flt_active, org_id, targets))
            if fstat == f:
                filters.append(self.filter_stat(flt_active, org_id, targets))
            if finnr == f:
                filters.append(self.filter_innr(flt_active, org_id, targets))
            if ftrnr == f:
                filters.append(self.filter_trnr(flt_active, org_id, targets))
            if fwinr == f:
                filters.append(self.filter_winr(flt_active, org_id, targets))
            if fcust == f:
                filters.append(self.filter_cust(flt_active, org_id, targets))

        return filters

    def get_filter(self,flt,flt_id):
        return next(f for f in flt if f['id'] == flt_id )

    def get_filters_dict(self,flt):
        filters = {}
        for f in self.filters_list:
            filters[f]=self.get_filter(flt,f)
        return filters

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org_id = self.init_dynamic_org()
        targets = self.get_initial_targets()
        filters = self.filters(None, org_id, targets)
        data = self.data(filters, None, org_id, targets)

        context['filters'] = filters
        context['data'] = data
        context['org_id'] = org_id
        context['view'] = {'id': self.view_id, 'name': self.view_name, 'select_market_type': self.select_market_type}
        context['ajax_url'] = self.ajax_url
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST:
                org_id = self.init_dynamic_org()
                flt_active = {}
                for f in self.filters_list:
                    flt_str = request.POST.get('{}_active'.format(f), '')
                    flt_select = request.POST.get('{}_select'.format(f), '')
                    flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select)}
                flt_active[fempa] = {'list':[], 'select': int(request.POST.get('empl_all', '0'))}

                targets = self.get_initial_targets()
                filters = self.filters(None, org_id, targets)
                # filters = self.filters(flt_active, org_id)
                data = self.data(filters, flt_active, org_id)
                response = {'filters': self.get_filters_dict(filters),
                            'data': data,
                            'org_id': org_id,
                            'view': {'id' : self.view_id, 'name': self.view_name, 'select_market_type': self.select_market_type},
                            'ajax_url': self.ajax_url}
                return JsonResponse(response)

        #return self.get(request)
        return super().post(request, *args, **kwargs)

class SalessheduleView(FiltersView):
    filters_list = [fempl, fmrkt, fyear, fcust]
    template_name = 'ta_salesshedule.html'
    ajax_url = reverse_lazy('widgetpages:salesshedule')
    view_id = 'salesshedule'
    view_name = 'График продаж'

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        pivot_data = {}
        if flt:
            hsy_active = RawModel(queries.q_sales_year).filter(org_id=org_id).order_by('1', '2')
            hsm_active = RawModel(queries.q_sales_month).filter(org_id=org_id).order_by('1', '2')
            if flt_active:
                if not self.zero_in(flt_active, fempa):
                    # Если не выбрано 'Без учета Таргет' то фильтруем по сотрудникам
                    hsy_active = hsy_active.filter( employee_in=extra_in_filter('e.employee_id', flt_active[fempl]) )
                    hsm_active = hsm_active.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))

                hsy_active = hsy_active.filter(years_in=extra_in_filter('PlanTYear',flt_active[fyear]), \
                                               markets_in=extra_in_filter('market_id',flt_active[fmrkt]), \
                                               lpus_in = extra_in_filter('Cust_ID',flt_active[fcust]))
                hsm_active = hsm_active.filter(years_in=extra_in_filter('PlanTYear',flt_active[fyear]), \
                                               markets_in=extra_in_filter('market_id',flt_active[fmrkt]), \
                                               lpus_in = extra_in_filter('Cust_ID',flt_active[fcust]))

            pivot_data['pivot1'] = list (hsy_active.open().fetchall())
            pivot_data['pivot2'] = list (hsm_active.open().fetchall())
            pivot_data['year'] = list( unique([e['iid'] for e in pivot_data['pivot1']]) )
            pivot_data['year'].sort()

            hsy_active.close()
            hsm_active.close()
        return pivot_data


class CompetitionsView(FiltersView):
    template_name = 'ta_competitions.html'
    ajax_url = reverse_lazy('widgetpages:competitions')
    view_id = 'competitions'
    view_name = 'Конкурентный анализ(тыс.руб.)'
    select_market_type = 1

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        data = {}

        if not flt_active:
            years_active = [y['iid'] for y in self.get_filter(flt, fyear)['data']]
        else:
            years_active = flt_active[fyear]['list']

        current_year = datetime.datetime.now().year
        try:
            sort_col = years_active.index(current_year)+3
            sort_dir = 'desc'
        except:
            sort_col = 2
            sort_dir = 'asc'

        data['year'] = years_active
        data['sort_col'] = sort_col
        data['sort_dir'] = sort_dir
        return data

class CompetitionsLpuView(CompetitionsView):
    ajax_url = reverse_lazy('widgetpages:competitions_lpu')
    view_id = 'competitions_lpu'
    view_name = 'Конкурентный анализ по ЛПУ (тыс.руб.)'

class CompetitionsMarketView(CompetitionsView):
    ajax_url = reverse_lazy('widgetpages:competitions_market')
    view_id = 'competitions_market'
    view_name = 'Конкурентный анализ по рынкам (тыс.руб.)'

class PartsView(CompetitionsView):
    template_name = 'ta_parts.html'
    ajax_url = reverse_lazy('widgetpages:parts')
    view_id = 'parts'
    view_name = 'Доля (тыс.руб.)'

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        data = {}

        if not flt_active:
            years_active = [y['iid'] for y in self.get_filter(flt, fyear)['data']]
        else:
            years_active = flt_active[fyear]['list']

        current_year = datetime.datetime.now().year
        try:
            sort_col = years_active.index(current_year)*3+1
            sort_dir = 'desc'
        except:
            sort_col = 1
            sort_dir = 'asc'

        data['year'] = years_active
        data['sort_col'] = sort_col
        data['sort_dir'] = sort_dir
        return data



