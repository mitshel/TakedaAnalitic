import json

from django.http import JsonResponse
from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy

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

# select_market_type, default_market_type,  select_own, default_own,           select_prod_type, default_prod_type
# 0|1                 1-Аукц|2-Контр        0|1         1-свой|2-чужой|3-все   0|1               1-МНН|2-ТМ
selHide = 0
selShow = 1
selMrktTender   = 1
selMrktContract = 2
selOwnYes = 1
selOwnNo = 2
selOwnAll = 3
selProdMNN = 1
selProdTM = 2

serv_defaults = [selHide,selMrktContract,   selHide,selOwnYes,   selHide,selProdTM]

filters_all = [fempl, fmrkt, fyear, fstat, fbudg, fform, fdosg, finnr, ftrnr, fwinr, fcust]

views_prop = {
    'salesshedule'          : { 'filters' : filters_all,            'props': [selHide,selMrktTender,     selShow,selOwnAll,   selHide,selProdTM] },
    'budgets'               : { 'filters' : filters_all,            'props': [selShow,selMrktContract,   selShow,selOwnYes,   selHide,selProdTM] },
    'competitions_lpu'      : { 'filters' : filters_all,            'props': [selShow,selMrktContract,   selShow,selOwnYes,   selShow,selProdTM] },
    'competitions_market'   : { 'filters' : filters_all,            'props': [selShow,selMrktContract,   selShow,selOwnYes,   selShow,selProdTM] },
    'avg_price'             : { 'filters' : filters_all,            'props': [selShow,selMrktContract,   selShow,selOwnYes,   selShow,selProdTM] },
    'packages'              : { 'filters' : filters_all,            'props': [selHide,selMrktContract,   selShow,selOwnYes,   selShow,selProdTM] },
    'parts'                 : { 'filters' : filters_all,            'props': [selShow,selMrktContract,   selHide,selOwnAll,   selHide,selProdTM] },
    'sales_analysis'        : { 'filters' : filters_all,            'props': [selShow,selMrktContract,   selShow,selOwnYes,   selShow,selProdTM] },
    'passport'              : { 'filters' : [fempl,fcust,fyear],    'props': [selShow,selMrktContract,   selHide,selOwnYes,   selHide,selProdTM] },
}

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

class FiltersMixin():
    view_id = 'blank'
    filters_list = filters_all
    default_market_type = 2 # Контракт
    default_own = 1         # Свой рынок
    default_prod_type = 2   # ТМ

    def print_defaults(self):
        print('market_type={}, own={},product_type={}'.format(self.default_market_type,self.default_own,self.default_prod_type))

    def init_view_properties(self):
        vprop = views_prop.get(self.view_id,None)
        if vprop:
            self.filters_list = vprop.get('filters')
            serv_props = vprop.get('props', serv_defaults)
            self.select_market_type = serv_props[0]
            self.default_market_type = serv_props[1]
            self.select_own = serv_props[2]
            self.default_own = serv_props[3]
            self.select_prod_type = serv_props[4]
            self.default_prod_type = serv_props[5]
        else:
            self.filters_list = filters_all
            self.select_market_type = serv_defaults[0]
            self.default_market_type = serv_defaults[1]
            self.select_own = serv_defaults[2]
            self.default_own = serv_defaults[3]
            self.select_prod_type = serv_defaults[4]
            self.default_prod_type = serv_defaults[5]

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
        if flt:
            # Удаляем значение view_id, т.к. далее логикой предусмотрено проверка на пустое flt
            self.view_id=flt.pop('view_id', self.view_id)
        self.init_view_properties()

        flt_active = {}
        if flt:
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
            flt_active[fserv] = {'market': self.default_market_type, 'own': self.default_own, 'prod': self.default_prod_type}

        return flt_active

    def apply_filters_default(self, qs):
        market_type_prefix = 'Contract_'
        qs = qs.filter(market_type_prefix = market_type_prefix)
        return qs

    def apply_filters(self, qs, flt_active, org_id, targets):
        market_type_prefix = 'Order_' if flt_active[fserv]['market'] == 1 else 'Contract_'
        own_select = 'market_own=1' if flt_active[fserv]['own'] == 1 else ('market_own=0' if flt_active[fserv]['own'] == 2 else '')
        product_type = 'InnNx' if flt_active[fserv]['prod'] == 1 else 'TradeNx'

        if fempl in self.filters_list:
            no_target = 1 if self.fempa_selected(flt_active, fempa) else None
            all_targets = ','.join([str(e['iid']) for e in targets])
            enabled_targets = [str(e) for e in flt_active[fempl]['list']] if flt_active[fempl]['list'] else ['-1',]
            disabled_targets = [str(e['iid']) for e in targets if str(e['iid']) not in flt_active[fempl]['list']]
            enabled_targets = ','.join([e for e in enabled_targets])
            disabled_targets = ','.join([e for e in disabled_targets])
        else:
            no_target = None
            disabled_targets = None
            enabled_targets = None
            all_targets = None

        qs = qs.filter(years=(flt_active[fyear]['list'] if flt_active.get(fyear) else '') if fyear in self.filters_list else None,
           all_targets = all_targets,
           enabled_targets=enabled_targets,
           disabled_targets=disabled_targets,
           no_target = no_target,
           markets_cnt_in=extra_in_strfilter('s.id', flt_active.get(fmrkt, '')) if fmrkt in self.filters_list else None, #Нужно подумать как избавится от этого
           years_in=extra_in_strfilter('s.PlanTYear', flt_active.get(fyear, '')) if fyear in self.filters_list else None,
           markets_in=extra_in_strfilter('s.market_id',flt_active.get(fmrkt,'')) if fmrkt in self.filters_list else None,
           status_in=extra_in_strfilter('s.StatusT_ID', flt_active.get(fstat, '')) if fstat in self.filters_list else None,
           budgets_in=extra_in_strfilter('s.budgets_ID',flt_active.get(fbudg,'')) if fbudg in self.filters_list else None,
           lpus_in=extra_in_filter('s.Cust_ID',flt_active.get(fcust,'')) if fcust in self.filters_list else None,
           winrs_in=extra_in_filter('s.Winner_ID', flt_active.get(fwinr,'')) if fwinr in self.filters_list else None,
           innrs_in=extra_in_filter('s.{}InnNx'.format(market_type_prefix), flt_active.get(finnr,'')) if finnr in self.filters_list else None,
           trnrs_in=extra_in_filter('s.{}TradeNx'.format(market_type_prefix), flt_active.get(ftrnr,'')) if ftrnr in self.filters_list else None,
           dosage_in=extra_in_filter('s.{}Dosage_id'.format(market_type_prefix), flt_active.get(fdosg, '')) if fdosg in self.filters_list else None,
           form_in=extra_in_filter('s.{}Form_id'.format(market_type_prefix), flt_active.get(fform, '')) if fform in self.filters_list else None,
           market_type_prefix = market_type_prefix, own_select = own_select, product_type = product_type, org_id = org_id)
        return qs


class FiltersView(OrgMixin, FiltersMixin, TemplateView):
    template_name = 'ta_competitions.html'
    filter_list = filters_all
    ajax_filters_url = '#'
    ajax_filters_tbl_url = reverse_lazy('widgetpages:jdata')
    ajax_datatable_url = '#'
    view_id = 'blank'
    view_name = 'Пустая страница'

    def filter_empl(self, flt_active=None, org_id=0, targets = []):
        employee_list = targets

        return {'id': fempl,
                'type': 'btn',
                'name': 'Таргет',
                'icon':'user',
                'expanded': 0,
                'data': employee_list}

    def filter_mrkt(self, flt_active=None, org_id=0, targets = []):
        market_list_active = []
        if not flt_active.get(fmrkt):
            # Показываем все доступные рынки для сотрудника организации
            market_enabled = self.apply_filters_default(RawModel(queries.q_markets)).filter(fields="id as iid, name",org_id=org_id).order_by('name')
            # Но активными будут выглядеть только рынки, доступные сотруднику (через ЛПУ)
            # Использование q_markets_hs вместо q_markets дает задержку около 1-2 секунд
            market_active = self.apply_filters(RawModel(queries.q_markets_hs).filter(fields="a.id as iid"), flt_active, org_id, targets)
            market_list_active = [e['iid'] for e in market_active.open().fetchall()]
            market_active.close()
        else:
            # Показываем все доступные рынки
            # Использование q_markets_hs вместо q_markets дает задержку около 1-2 секунд
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
            year_enabled = self.apply_filters_default(RawModel(queries.q_years_hs)).filter(fields="PlanTYear as iid, PlanTYear as name",org_id=org_id).order_by('PlanTYear')
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
        # Запрос по всему кэшу чтобы проверить статусы очень тяжел и занимает от 350 до 900 мс
        # Поэтому пока просто выводим все доступные статусы
        # впоследсвие можно предусмотреть кэширование информации по статусам или предподготовку специальной таблицы
        status_enabled = self.apply_filters_default(RawModel(queries.q_status)).filter(fields="id as iid, name", org_id=org_id).order_by('name')
        #status_list_active = []
        #if not flt_active.get(fstat):
        #    # Показываем все доступные статусы для сотрудника организации
        #    status_enabled = RawModel(queries.q_status).filter(fields="id as iid, name",org_id=org_id).order_by('name')
        #    # Но активными будут выглядеть только рынки, доступные сотруднику (через ЛПУ)
        #    # Использование q_markets_hs вместо q_markets дает задержку около 1-2 секунд
        #    status_active = self.apply_filters(RawModel(queries.q_status_hs).filter(fields="a.id as iid"), flt_active, org_id, targets)
        #    status_list_active = [e['iid'] for e in status_active.open().fetchall()]
        #    status_active.close()
        #else:
        #    # Показываем все доступные рынки
        #    # Использование q_markets_hs вместо q_markets дает задержку около 1-2 секунд
        #    status_enabled = self.apply_filters(RawModel(queries.q_status_hs).filter(fields="a.id as iid"), flt_active, org_id, targets)

        status_list = list(status_enabled.open().fetchall())
        status_enabled.close()
        return {'id': fstat,
                'type': 'btn',
                'name': 'Статус торгов',
                'icon':'check-square',
                'data':  status_list,
                #'data0': status_list_active,
                }

    def filter_budg(self, flt_active=None, org_id=0, targets = []):
        #fields =  "a.id as iid, name" if flt_active.get(fbudg) else "a.id as iid, name"
        #budgets_enabled = RawModel(queries.q_budgets).filter(fields=fields).order_by('name')
        # budgets_enabled = self.apply_filters(RawModel(queries.q_budgets_hs),flt_active, org_id, targets).filter(fields=fields ).order_by('name')

        #budgets_list = list(budgets_enabled.open().fetchall())
        #budgets_enabled.close()

        budgets_list_active = []
        if not flt_active.get(fbudg):
            # Показываем все доступные Бюджеты для сотрудника организации
            budgets_enabled = self.apply_filters_default(RawModel(queries.q_budgets)).filter(fields="id as iid, name",org_id=org_id).order_by('name')
            # Но активными будут выглядеть только Бюджеты, доступные сотруднику (через ЛПУ)
            budgets_active = self.apply_filters(RawModel(queries.q_budgets_hs).filter(fields="a.id as iid"), flt_active, org_id, targets)
            budgets_list_active = [e['iid'] for e in budgets_active.open().fetchall()]
            budgets_active.close()
        else:
            # Показываем все доступные бюджеты
            budgets_enabled = self.apply_filters(RawModel(queries.q_budgets_hs).filter(fields="a.id as iid"), flt_active, org_id, targets)

        budgets_list = list(budgets_enabled.open().fetchall())
        budgets_enabled.close()
        return {'id': fbudg,
                'type': 'tbl',
                'name': 'Бюджет',
                'icon':'ruble-sign',
                'data': budgets_list,
                'data0': budgets_list_active}

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
        context['ajax_filters_tbl_url'] = self.ajax_filters_tbl_url
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
                            #'ajax_filters_url': self.ajax_filters_url,
                            #'ajax_filters_tbl_url': self.ajax_filters_tbl_url,
                            'ajax_datatable_url': self.ajax_datatable_url}
                return JsonResponse(response)

        return super().post(request, *args, **kwargs)


class BaseDatatableYearView(OrgMixin, FiltersMixin, AjaxRawDatatableView):
    order_columns = ['name']
    #filters_list = [fempl, fmrkt, fyear, fstat, fbudg, fdosg, fform, finnr, ftrnr, fwinr, fcust]
    #org_id = 1
    datatable_query = None
    datatable_count_query = None
    empty_datatable_query = 'select null as name'

    def get_initial_queryset(self):
        #self.view_id = self.request.POST.get('view_id', 'BaseDatatableYearView')
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
            self.orderable = 0

        rawmodel = self.apply_filters(rawmodel, flt_active, org_id, targets)
        print(rawmodel.query)
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
