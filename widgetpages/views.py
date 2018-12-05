from django.shortcuts import render
from django.http import JsonResponse

from db.models import Org
from django.views.generic import View, TemplateView
from django.urls import reverse_lazy

from widgetpages import queries
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

# Удаление неуникальных элементов из списка
def unique(obj: iter):
    args = []
    for a in obj:
        if a not in args:
            args.append(a)
            yield a

class OrgMixin(View):
    org = None
    org_id = None

    def init_dynamic_org(self):
        user = self.request.user
        org_id = None
        org = None

        # Сначала получаем информацию об организации из запроса GET или POST
        if self.request.method == 'GET':
            org_id = self.request.GET.get('org_id','0')
        if self.request.method == 'POST':
            org_id = self.request.POST.get('org_id','0')

        if org_id:
            try:
                org_id = int(org_id)
                org = Org.objects.get(id=org_id)
            except:
                org_id = None
                org = None

        # Если пользователь администратор пытаемся получить текущую организацию из сессии
        if not org:
            if (user.is_superuser or user.is_staff):
                try:
                    org_id = int(self.request.session['org'])
                    org = Org.objects.get(id=org_id)
                except:
                    org = None
                    org_id = None

        # Если текущая организация еще неизвестна, то получаем его по привязке к пользователю
        if not org:
            try:
                org = Org.objects.filter(users=self.request.user)[0]
                org_id = org.id
            except:
                org = None
                org_id = None

        self.org_id = org_id
        self.org = org

        return org_id

    def dispatch(self, request, *args, **kwargs):
        self.init_dynamic_org()
        return super().dispatch(request, *args, **kwargs)

class HomeView(OrgMixin, TemplateView):
    template_name = 'ta_hello.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = self.org
        return context

class FiltersView(OrgMixin, View):
    filters_list = [fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust]
    ajax_url = '#'
    template_name = 'ta_competitions.html'
    view_id = 'blank'
    view_name = 'Пустая страница'
    select_market_type = 0

    # def init_dynamic_org(self):
    #     org = Org.objects.filter(users=self.request.user)
    #     org_id = org[0].id if org else 0
    #     return org_id

    def zero_in(self, flt_active, fname):
        return ((flt_active[fname]['select'] == 1) and not (0 in flt_active[fname]['list'])) or \
               ((flt_active[fname]['select'] == 0) and (0 in flt_active[fname]['list']))

    def filter_empl(self, flt_active=None, org_id=0):
        employee_raw = RawModel(queries.q_employees).filter(org_id=org_id)
        if not flt_active:
            employee_enabled = employee_raw.filter(fields='id as iid, name').order_by('name')
        else:
            employee_enabled = employee_raw.filter(fields='id as iid')
        employee_list=list(employee_enabled.open().fetchall())
        employee_enabled.close()
        return {'id': fempl,
                'type': 'btn',
                'name': 'Таргет',
                'icon':'user',
                'expanded': 'false',
                'data': [{'name':'Без учета Таргет','iid':0}]+employee_list}

    def filter_mrkt(self, flt_active=None, org_id=0):
        if not flt_active:
            market_enabled = RawModel(queries.q_markets).filter(fields="id as iid, name").filter(org_id=org_id).order_by('name')
        else:
            market_enabled = RawModel(queries.q_markets_hs).filter(fields="a.id as iid").filter(org_id=org_id)
            if not self.zero_in(flt_active, fempl):
                market_enabled = market_enabled.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))
        market_list = list(market_enabled.open().fetchall())
        market_enabled.close()
        return {'id': fmrkt,
                'type': 'btn',
                'name': 'Рынок',
                'icon':'shopping-cart',
                'data': market_list}

    def filter_year(self, flt_active=None, org_id=0):
        if not flt_active:
            year_enabled = RawModel(queries.q_years_hs).filter(fields="PlanTYear as iid, PlanTYear as name").filter(org_id=org_id).order_by('PlanTYear')
        else:
            year_enabled = RawModel(queries.q_years_hs).filter(fields="PlanTYear as iid").filter(org_id=org_id)
            if not self.zero_in(flt_active, fempl):
                year_enabled = year_enabled.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))
        year_list = list(year_enabled.open().fetchall())
        year_enabled.close()
        return {'id': fyear,
                'type': 'btn',
                'name': 'Год поставки',
                'icon':'calendar',
                'data': year_list}

    def filter_stat(self, flt_active=None, org_id=0):
        if not flt_active:
            status_enabled = RawModel(queries.q_status).filter(fields="id as iid, name").order_by('name')
        else:
            status_enabled = RawModel(queries.q_status_hs).filter(fields="a.id as iid").filter(org_id=org_id)
            if not self.zero_in(flt_active, fempl):
                status_enabled = status_enabled.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))
        status_list = list(status_enabled.open().fetchall())
        status_enabled.close()
        return {'id': fstat,
                'type': 'btn',
                'name': 'Статус торгов',
                'icon':'check-square',
                'data': status_list}

    def filter_innr(self, flt_active=None, org_id=0):
        return {'id': finnr,
                'type': 'ajx',
                'name': 'МНН',
                'icon':'globe',
                'data': []}

    def filter_trnr(self, flt_active=None, org_id=0):
        return {'id': ftrnr,
                'type': 'ajx',
                'name': 'Торговое наименование',
                'icon':'trademark',
                'data': []}

    def filter_winr(self, flt_active=None, org_id=0):
        return {'id': fwinr,
                'type': 'ajx',
                'name': 'Победитель торгов',
                'icon':'handshake',
                'data': []}

    def filter_cust(self, flt_active=None, org_id=0):
        return {'id': fcust,
                'type': 'ajx',
                'name': 'Грузополучатель',
                'icon':'ambulance',
                'data': []}

    def filters(self, flt_active=None, org_id=0):
        filters = []
        for f in self.filters_list:
            if fempl == f:
                filters.append(self.filter_empl(flt_active, org_id))
            if fmrkt == f:
                filters.append(self.filter_mrkt(flt_active, org_id))
            if fyear == f:
                filters.append(self.filter_year(flt_active, org_id))
            if fstat == f:
                filters.append(self.filter_stat(flt_active, org_id))
            if finnr == f:
                filters.append(self.filter_innr(flt_active, org_id))
            if ftrnr == f:
                filters.append(self.filter_trnr(flt_active, org_id))
            if fwinr == f:
                filters.append(self.filter_winr(flt_active, org_id))
            if fcust == f:
                filters.append(self.filter_cust(flt_active, org_id))

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
                                                    'org_id': org_id,
                                                    'view': {'id': self.view_id, 'name': self.view_name, 'select_market_type': self.select_market_type},
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
                            'org_id': org_id,
                            'view': {'id' : self.view_id, 'name': self.view_name, 'select_market_type': self.select_market_type},
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
            hsy_active = RawModel(queries.q_sales_year).filter(org_id=org_id).order_by('1', '2')
            hsm_active = RawModel(queries.q_sales_month).filter(org_id=org_id).order_by('1', '2')
            if flt_active:
                if not self.zero_in(flt_active, fempl):
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
            hsy_active.close()
            hsm_active.close()
        return pivot_data


class CompetitionsView(FiltersView):
    template_name = 'ta_competitions.html'
    ajax_url = reverse_lazy('widgetpages:competitions')
    view_id = 'competitions'
    view_name = 'Конкурентный анализ(тыс.руб.)'
    select_market_type = 1

    def data(self, flt=None, flt_active=None, org_id=0):
        data = {}
        if not flt_active:
            years_active = [y['iid'] for y in self.get_filter(flt, fyear)['data']]
        else:
            years_active = flt_active[fyear]['list']

        data['year'] = years_active
        return data

class CompetitionsLpuView(CompetitionsView):
    ajax_url = reverse_lazy('widgetpages:competitions_lpu')
    view_id = 'competitions_lpu'
    view_name = 'Конкурентный анализ по ЛПУ (тыс.руб.)'

class CompetitionsMarketView(CompetitionsView):
    ajax_url = reverse_lazy('widgetpages:competitions_market')
    view_id = 'competitions_market'
    view_name = 'Конкурентный анализ по рынкам (тыс.руб.)'


