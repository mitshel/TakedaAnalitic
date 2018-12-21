import json

from django.http import JsonResponse
from django.views.generic import View, TemplateView

from widgetpages import queries
from widgetpages.ajaxdatatabe import AjaxRawDatatableView

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

# Удаление неуникальных элементов из списка
def unique(obj: iter):
    args = []
    for a in obj:
        if a not in args:
            args.append(a)
            yield a

class OrgMixin(OrgBaseMixin):
    SETUP_METHODS = bOrgPOST | bOrgUSER

class TargetsMixin(View):

    def fempa_selected(self, flt_active, fname):
        return flt_active[fname]['select'] if flt_active else 0

    def targets_in_filter(self, targets):
        return {'list':[e['iid'] for e in targets], 'select': 0}

    def get_initial_targets(self):
        initial_employee = RawModel(queries.q_employees).filter(fields = 'id as iid, name', username=self.request.user.username).order_by('name')
        initial_targets=list(initial_employee.open().fetchall())
        initial_employee.close()
        return initial_targets

class FiltersView(OrgMixin, TargetsMixin, TemplateView):
    template_name = 'ta_competitions.html'
    filters_list = [fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust]
    ajax_url = '#'
    ajax_datatable_url = '#'
    view_id = 'blank'
    view_name = 'Пустая страница'
    select_market_type = 0

    def filter_empl(self, flt_active=None, org_id=0, targets = []):
        if not flt_active:
            employee_list = targets
        else:
            employee_list = [{'iid':t['iid']} for t in targets]

        return {'id': fempl,
                'type': 'btn',
                'name': 'Таргет',
                'icon':'user',
                'expanded': 'false',
                'data': employee_list}

    def filter_mrkt(self, flt_active=None, org_id=0, targets = []):
        market_list_active = []
        if not flt_active:
            # Показываем все доступные рынки для сотрудника организации
            market_enabled = RawModel(queries.q_markets).filter(fields="id as iid, name",org_id=org_id).order_by('name')
            # Но активными будут выглядеть только рынки, доступные сотруднику (через ЛПУ)
            market_active = RawModel(queries.q_markets_hs_empl).filter(fields="a.id as iid",org_id=org_id, \
                                                                       employee_in=extra_in_filter('e.employee_id', self.targets_in_filter(targets)))
            market_list_active = [e['iid'] for e in market_active.open().fetchall()]
            market_active.close()
        else:
            # Показываем все доступные рынки
            market_enabled = RawModel(queries.q_markets_hs).filter(fields="a.id as iid",org_id=org_id)
            #  Если отключена кнопка "Без учета Target" то фильтруем по выбранным сотрудникам
            if not self.fempa_selected(flt_active, fempa):
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
            year_active = RawModel(queries.q_years_hs_empl).filter(fields="PlanTYear as iid",org_id=org_id, \
                                                                   employee_in=extra_in_filter('e.employee_id', self.targets_in_filter(targets)))
            year_list_active = [e['iid'] for e in year_active.open().fetchall()]
            year_active.close()
        else:
            # Показываем все доступные Годы
            year_enabled = RawModel(queries.q_years_hs).filter(fields="PlanTYear as iid",org_id=org_id)
            #  Если отключена кнопка "Без учета Target" то фильтруем по выбранным сотрудникам
            if not self.fempa_selected(flt_active, fempa):
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
            if not self.fempa_selected(flt_active, fempa):
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
        context['ajax_datatable_url'] = self.ajax_datatable_url
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
                # filters = self.filters(None, org_id, targets)
                filters = self.filters(flt_active, org_id, targets)
                data = self.data(filters, flt_active, org_id, targets)
                response = {'filters': self.get_filters_dict(filters),
                            'data': data,
                            'org_id': org_id,
                            'view': {'id' : self.view_id, 'name': self.view_name, 'select_market_type': self.select_market_type},
                            'ajax_url': self.ajax_url,
                            'ajax_datatable_url': self.ajax_datatable_url}
                return JsonResponse(response)

        #return self.get(request)
        return super().post(request, *args, **kwargs)


class BaseDatatableYearView(OrgMixin, TargetsMixin, AjaxRawDatatableView):
    order_columns = ['name']
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]
    org_id = 1
    datatable_query = None
    datatable_count_query = None
    empty_datatable_query = 'select null as name'

    def get_initial_queryset(self):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        self.view_id = self.request.POST.get('view_id', 'BaseDatatableYearView')
        flt = json.loads(filters_ajax_request)
        org_id = self.init_dynamic_org()
        flt_active = {}
        if flt:
            market_type = flt.get('market_type','1')
            for f in self.filters_list:
                flt_str = flt.get('{}_active'.format(f), '')
                flt_select = flt.get('{}_select'.format(f), '')
                flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select if flt_select else 0)}
                flt_active[fempa] = {'list': [], 'select': int(flt.get('empl_all', '0'))}
        else:
            market_type = '1'
            targets = self.get_initial_targets()
            flt_active[fempl] = self.targets_in_filter(targets)
            flt_active[fempa] = {'list': [], 'select': 0}
            years_active = RawModel(queries.q_years_hs_empl).filter(fields="PlanTYear as iid",org_id=org_id, \
                                                                   employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))
            flt_active[fyear] = {'list':[e['iid'] for e in years_active.open().fetchall()], 'select':0}
            years_active.close()

        market_type_prefix = 'Order_' if market_type == '1' else 'Contract_'

        if flt_active[fyear]['list']:
            rawmodel = RawModel(self.datatable_query, self.datatable_count_query)
            rawmodel = rawmodel.filter(years=flt_active[fyear]['list'],
                           markets=','.join([str(e) for e in flt_active[fmrkt]['list']] if flt_active else ''),
                           status=','.join([str(e) for e in flt_active[fstat]['list']] if flt_active else ''),
                           employees=','.join([str(e) for e in flt_active[fempl]['list']] if not self.fempa_selected(flt_active, fempa) else ''),
                           lpus_in=extra_in_filter('l.Cust_ID',flt_active[fcust] if flt_active else ''),
                           winrs_in=extra_in_filter('w.id', flt_active[fwinr] if flt_active else ''),
                           innrs_in = extra_in_filter('s.{}InnNx'.format(market_type_prefix), flt_active[finnr] if flt_active else ''),
                           trnrs_in = extra_in_filter('s.{}TradeNx'.format(market_type_prefix), flt_active[ftrnr] if flt_active else ''),
                           market_type_prefix = market_type_prefix,
                           org_id = org_id)
        else:
            rawmodel = RawModel(self.empty_datatable_query)

        return rawmodel

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = ''
        return context
