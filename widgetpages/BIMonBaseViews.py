import json

from django.http import JsonResponse
from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect, render_to_response

from widgetpages import queries
from widgetpages.ajaxdatatabe import AjaxRawDatatableView

from db.rawmodel import RawModel
from db.models import SYNC_STATUS_CHOICES, DB_READY, DB_RECREATE, DB_ERROR, DB_OFFLINE, DB_UPDATE
from farmadmin.views import OrgBaseMixin, bOrgUSER, bOrgSESSION, bOrgPOST

# Filters identification
fempl = 'empl'
fmrkt = 'mrkt'
fyear = 'year'
fcust = 'cust'
fstat = 'stat'
finnr = 'innr'
ftrnr = 'trnr'
fwinr = 'winr'
fbudg = 'budg'
fdosg = 'dosg'
fform = 'form'


fempa = 'empa'
fserv = 'serv'

def prepare_serach(s):
    return s.replace("'","")

def extra_in_filter(field, flt):
    if flt:
        if (len(flt['list']) > 0):
            ef = '{} {}in ({})'. \
                format(field,
                       'not ' if flt['select'] else '',
                       ','.join([e for e in flt['list']]))
        else:
            ef = '' if flt['select'] else '1>1'  #1=1
    else:
        ef = '' #1=1

    return ef

def extra_in_strfilter(field, flt):
    if flt:
        if (len(flt['list']) > 0):
            ef = '{} {}in ({})'. \
                format(field,
                       'not ' if flt['select'] else '',
                       ','.join(["'{}'".format(e) for e in flt['list']]))
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

class FiltersMixin(View):
    default_market_type = 2 # Контракт
    default_own = 1         # Свой рынок
    default_prod_type = 2   # ТМ

    def fempa_selected(self, flt_active, fname):
        return flt_active[fname]['select'] if flt_active else 0

    def targets_in_filter(self, targets):
        return {'list':[e['iid'] for e in targets], 'select': 0}

    def get_initial_targets(self):
        initial_employee = RawModel(queries.q_employees).filter(fields = 'id as iid, name', username=self.request.user.username).order_by('name')
        initial_targets=list(initial_employee.open().fetchall())
        initial_employee.close()
        return initial_targets

    # Получает информацию о состоянии фильтров через ajax, или конструирует фильтры по умолчанию
    def filters_active(self, org_id, targets):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        flt = json.loads(filters_ajax_request) if filters_ajax_request else {}
        flt_active = {}
        if flt:
            print(flt)
            print(self.filters_list)
            for f in self.filters_list:
                flt_str = flt.get('{}_active'.format(f), '')
                flt_select = flt.get('{}_select'.format(f), '')
                flt_active[f] = {'list':[e for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select if flt_select else 0)}
                flt_active[fempa] = {'list': [], 'select': int(flt.get('empl_all', '0'))}
                flt_active[fserv] = {'market': int(flt.get('market_type',str(self.default_market_type))), \
                                     'own': int(flt.get('own_type', str(self.default_own))), \
                                     'prod': int(flt.get('prod_type',str(self.default_prod_type)))}
        else:
            flt_active[fempl] = self.targets_in_filter(targets)
            flt_active[fempa] = {'list': [], 'select': 0}
            flt_active[fserv] = {'market': 1, 'own': 1, 'prod': 2}

        return flt_active

    def apply_filters(self, qs, flt_active, org_id, targets):
        market_type_prefix = 'Order_' if flt_active[fserv]['market'] == 1 else 'Contract_'
        own_select = 'market_own=1' if flt_active[fserv]['own'] == 1 else ('market_own=0' if flt_active[fserv]['own'] == 2 else '')
        product_type = 'InnNx' if flt_active[fserv]['prod'] == 1 else 'TradeNx'

        if self.fempa_selected(flt_active, fempa):
            disabled_targets = [e['iid'] for e in targets if str(e['iid']) not in flt_active[fempl]['list']]
            #flt_targets = '(e.employee_id  not in ({}) or e.employee_id is null) '.format(','.join([str(e) for e in disabled_targets])) if disabled_targets else ''
            flt_targets = '(e.employee_id  not in ({})) '.format(','.join([str(e) for e in disabled_targets])) if disabled_targets else ''
        else:
            enabled_targets = [str(e) for e in flt_active[fempl]['list']]
            flt_targets = 'e.employee_id in ({})'.format(','.join(enabled_targets) if enabled_targets else '-1')

        qs = qs.filter(years=flt_active[fyear]['list'] if flt_active.get(fyear) else '',
                       markets=','.join([str(e) for e in flt_active[fmrkt]['list']] if flt_active.get(fmrkt) else ''),
                       status=','.join([str(e) for e in flt_active[fstat]['list']] if flt_active.get(fstat) else ''),
                       targets = flt_targets,
                       product_type = product_type,
                       employees=','.join([str(e) for e in flt_active[fempl]['list']]) if not self.fempa_selected(flt_active, fempa) else '',
                       budgets_in=extra_in_strfilter('s.budgets_ID',flt_active.get(fbudg,'')),
                       lpus_in=extra_in_filter('l.Cust_ID',flt_active.get(fcust,'')),
                       winrs_in=extra_in_filter('w.id', flt_active.get(fwinr,'')),
                       innrs_in = extra_in_filter('s.{}InnNx'.format(market_type_prefix), flt_active.get(finnr,'')),
                       trnrs_in = extra_in_filter('s.{}TradeNx'.format(market_type_prefix), flt_active.get(ftrnr,'')),
                       dosage_in=extra_in_filter('s.Contract_Dosage_id', flt_active.get(fdosg, '')),
                       form_in=extra_in_filter('s.Contract_Form_id', flt_active.get(fform, '')),
                       market_type_prefix = market_type_prefix, own_select = own_select, org_id = org_id)
        return qs


class FiltersView(OrgMixin, FiltersMixin, TemplateView):
    template_name = 'ta_competitions.html'
    filters_list = [fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust]
    ajax_filters_url = '#'
    ajax_datatable_url = '#'
    view_id = 'blank'
    view_name = 'Пустая страница'
    select_market_type = 0
    select_own = 0
    select_prod_type = 0

    def filter_empl(self, flt_active=None, org_id=0, targets = []):
        employee_list = targets

        return {'id': fempl,
                'type': 'btn',
                'name': 'Таргет',
                'icon':'user',
                'expanded': 'false',
                'data': employee_list}

    def filter_mrkt(self, flt_active=None, org_id=0, targets = []):
        market_list_active = []
        if not flt_active.get(fmrkt):
            # Показываем все доступные рынки для сотрудника организации
            market_enabled = RawModel(queries.q_markets).filter(fields="id as iid, name",org_id=org_id).order_by('name')
            # Но активными будут выглядеть только рынки, доступные сотруднику (через ЛПУ)
            market_active = self.apply_filters(RawModel(queries.q_markets_hs).filter(fields="a.id as iid"), flt_active, org_id, targets)
            market_list_active = [e['iid'] for e in market_active.open().fetchall()]
            market_active.close()
        else:
            # Показываем все доступные рынки
            market_enabled = self.apply_filters(RawModel(queries.q_markets_hs).filter(fields="a.id as iid"), flt_active, org_id, targets)

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
        if not flt_active.get(fyear):
            # Показываем все доступные Годы для сотрудника организации
            year_enabled = RawModel(queries.q_years_hs).filter(fields="PlanTYear as iid, PlanTYear as name",org_id=org_id).order_by('PlanTYear')
            # Но активными будут выглядеть только Годы, доступные сотруднику (через ЛПУ)
            year_active = self.apply_filters(RawModel(queries.q_years_hs).filter(fields="PlanTYear as iid"), flt_active, org_id, targets)
            year_list_active = [e['iid'] for e in year_active.open().fetchall()]
            year_active.close()
        else:
            # Показываем все доступные Годы
            year_enabled = self.apply_filters(RawModel(queries.q_years_hs).filter(fields="PlanTYear as iid"), flt_active, org_id, targets)

        year_list = list(year_enabled.open().fetchall())
        year_enabled.close()
        return {'id': fyear,
                'type': 'btn',
                'name': 'Год поставки',
                'icon':'calendar',
                'data': year_list,
                'data0': year_list_active}

    def filter_stat(self, flt_active=None, org_id=0, targets = []):
        fields =  "a.id as iid, name" if flt_active.get(fstat) else "a.id as iid, name"
        status_enabled = RawModel(queries.q_status).filter(fields=fields).order_by('name')
        # status_enabled  = self.apply_filters(RawModel(queries.q_status_hs),flt_active, org_id, targets).filter(fields=fields).order_by('name')

        status_list = list(status_enabled.open().fetchall())
        status_enabled.close()
        return {'id': fstat,
                'type': 'btn',
                'name': 'Статус торгов',
                'icon':'check-square',
                'data': status_list}

    def filter_budg(self, flt_active=None, org_id=0, targets = []):
        fields =  "a.id as iid, name" if flt_active.get(fbudg) else "a.id as iid, name"
        budgets_enabled = RawModel(queries.q_budgets).filter(fields=fields).order_by('name')
        # budgets_enabled = self.apply_filters(RawModel(queries.q_budgets_hs),flt_active, org_id, targets).filter(fields=fields ).order_by('name')

        budgets_list = list(budgets_enabled.open().fetchall())
        budgets_enabled.close()
        return {'id': fbudg,
                'type': 'tbl',
                'name': 'Бюджет',
                'icon':'ruble-sign',
                'data': budgets_list}


    def filter_dosg(self, flt_active=None, org_id=0, targets = []):
        return {'id': fdosg,
                'type': 'ajx',
                'name': 'Фасовка',
                'icon': 'th',
                'data': []}

    def filter_form(self, flt_active=None, org_id=0, targets = []):
        return {'id': fform,
                'type': 'ajx',
                'name': 'Лекарственные формы',
                'icon': 'medkit',
                'data': []}

    def filter_innr(self, flt_active=None, org_id=0, targets = []):
        return {'id': finnr,
                'type': 'ajx',
                'name': 'МНН',
                'icon': 'globe',
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
        for f in self.filters_list:
            if fempl == f:
                filters.append(self.filter_empl(flt_active, org_id, targets))
            if fmrkt == f:
                filters.append(self.filter_mrkt(flt_active, org_id, targets))
            if fyear == f:
                filters.append(self.filter_year(flt_active, org_id, targets))
            if fstat == f:
                filters.append(self.filter_stat(flt_active, org_id, targets))
            if fbudg == f:
                filters.append(self.filter_budg(flt_active, org_id, targets))
            if finnr == f:
                filters.append(self.filter_innr(flt_active, org_id, targets))
            if ftrnr == f:
                filters.append(self.filter_trnr(flt_active, org_id, targets))
            if fwinr == f:
                filters.append(self.filter_winr(flt_active, org_id, targets))
            if fcust == f:
                filters.append(self.filter_cust(flt_active, org_id, targets))
            if fdosg == f:
                filters.append(self.filter_dosg(flt_active, org_id, targets))
            if fform == f:
                filters.append(self.filter_form(flt_active, org_id, targets))

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
        if self.org.sync_status > 1:
            self.template_name = 'ta_dbstatus.html'
            context['dbstatus'] = self.org.sync_status
            context['dbinfo'] = dict(SYNC_STATUS_CHOICES).get(self.org.sync_status)
            return context

        targets = self.get_initial_targets()
        flt_active = self.filters_active(org_id, targets)
        filters = self.filters(flt_active, org_id, targets)
        data = self.data(filters, flt_active, org_id, targets)

        context['filters'] = filters
        context['data'] = data
        context['org_id'] = org_id
        context['view'] = {'id': self.view_id, 'name': self.view_name,
                           'select_market_type': self.select_market_type, 'select_own': self.select_own,  'select_prod_type': self.select_prod_type,
                           'default_market_type' : self.default_market_type, 'default_own':  self.default_own, 'default_prod_type' : self.default_prod_type }
        context['ajax_filters_url'] = self.ajax_filters_url
        context['ajax_datatable_url'] = self.ajax_datatable_url
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST:
                org_id = self.init_dynamic_org()
                targets = self.get_initial_targets()
                flt_active = self.filters_active(org_id, targets)
                filters = self.filters(flt_active, org_id, targets)
                data = self.data(filters, flt_active, org_id, targets)
                response = {'filters': self.get_filters_dict(filters),
                            'data': data,
                            'org_id': org_id,
                            'view': {'id' : self.view_id, 'name': self.view_name },
                            'ajax_filters_url': self.ajax_filters_url,
                            'ajax_datatable_url': self.ajax_datatable_url}
                return JsonResponse(response)

        return super().post(request, *args, **kwargs)


class BaseDatatableYearView(OrgMixin, FiltersMixin, AjaxRawDatatableView):
    order_columns = ['name']
    filters_list = [fempl, fmrkt, fyear, fstat, fdosg, fform, finnr, ftrnr, fwinr, fcust]
    org_id = 1
    orderable = 1
    datatable_query = None
    datatable_count_query = None
    empty_datatable_query = 'select null as name '

    def get_initial_queryset(self):
        self.view_id = self.request.POST.get('view_id', 'BaseDatatableYearView')
        org_id = self.init_dynamic_org()
        targets = self.get_initial_targets()
        flt_active = self.filters_active(org_id, targets)

        if not flt_active.get(fyear):
            years_active = RawModel(queries.q_years_hs_empl).filter(fields="PlanTYear as iid",org_id=org_id, \
                                                                   employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))
            flt_active[fyear] = {'list':[e['iid'] for e in years_active.open().fetchall()], 'select':0}
            years_active.close()

        if flt_active[fyear]['list']:
            rawmodel = RawModel(self.datatable_query, self.datatable_count_query)
        else:
            rawmodel = RawModel(self.empty_datatable_query)

        rawmodel = self.apply_filters(rawmodel, flt_active, org_id, targets)
        return rawmodel

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(icontains=prepare_serach(search))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = ''
        return context
