import json

from widgetpages.views import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust
from widgetpages.views import extra_in_filter
from db.rawmodel import RawModel
from widgetpages import queries
from widgetpages.ajaxdatatabe import AjaxRawDatatableView
from widgetpages.views import OrgMixin

class MPartsAjaxTable(OrgMixin, AjaxRawDatatableView):
    order_columns = ['name', ]
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]
    org_id = 1

    def get_initial_queryset(self):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        self.view_id = self.request.POST.get('view_id', 'parts')
        market_type = '1'
        flt = json.loads(filters_ajax_request)
        flt_active = {}
        if flt:
            market_type = flt.get('market_type','1')
            for f in self.filters_list:
                flt_str = flt.get('{}_active'.format(f), '')
                flt_select = flt.get('{}_select'.format(f), '')
                flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select if flt_select else 0)}

        org_id = self.init_dynamic_org()

        if not flt_active:
            years_model = RawModel(queries.q_years_hs).filter(fields="PlanTYear").filter(org_id=org_id).order_by('PlanTYear')
            years_active = [y['PlanTYear'] for y in years_model.open().fetchall()]
            years_model.close()
        else:
            years_active = flt_active[fyear]['list']

        market_type_prefix = 'Order_' if market_type == '1' else 'Contract_'

        if years_active:
            rawmodel = RawModel(queries.q_mparts, queries.q_mparts_count)
            rawmodel = rawmodel.filter(years=years_active,
                           markets=','.join([str(e) for e in flt_active[fmrkt]['list']] if flt_active else ''),
                           status=','.join([str(e) for e in flt_active[fstat]['list']] if flt_active else ''),
                           employees=','.join([str(e) for e in flt_active[fempl]['list']] if flt_active and not (0 in flt_active[fempl]['list']) else ''),
                           lpus_in=extra_in_filter('l.Cust_ID',flt_active[fcust] if flt_active else ''),
                           winrs_in=extra_in_filter('w.id', flt_active[fwinr] if flt_active else ''),
                           innrs_in = extra_in_filter('s.{}InnNx'.format(market_type_prefix), flt_active[finnr] if flt_active else ''),
                           trnrs_in = extra_in_filter('s.{}TradeNx'.format(market_type_prefix), flt_active[ftrnr] if flt_active else ''),
                           market_type_prefix = market_type_prefix,
                           org_id = org_id)
        else:
            rawmodel = RawModel('select null as name')

        return rawmodel

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(icontains=search)
        return qs

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        if sort_col==0:
            qs = qs.order_by('gr', 'mt.name')
        else:
            qs = qs.order_by('gr','[{0}] {1}'.format(self._columns[sort_col], sort_dir))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = ''
        return context


class LPartsAjaxTable(OrgMixin, AjaxRawDatatableView):
    order_columns = ['name', ]
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]
    org_id = 1

    def get_initial_queryset(self):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        self.view_id = self.request.POST.get('view_id', 'parts')
        market_type = '1'
        flt = json.loads(filters_ajax_request)
        flt_active = {}
        if flt:
            market_type = flt.get('market_type','1')
            for f in self.filters_list:
                flt_str = flt.get('{}_active'.format(f), '')
                flt_select = flt.get('{}_select'.format(f), '')
                flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select if flt_select else 0)}

        org_id = self.init_dynamic_org()

        if not flt_active:
            years_model = RawModel(queries.q_years_hs).filter(fields="PlanTYear").filter(org_id=org_id).order_by('PlanTYear')
            years_active = [y['PlanTYear'] for y in years_model.open().fetchall()]
            years_model.close()
        else:
            years_active = flt_active[fyear]['list']

        market_type_prefix = 'Order_' if market_type == '1' else 'Contract_'

        if years_active:
            rawmodel = RawModel(queries.q_lparts, queries.q_lparts_count)
            rawmodel = rawmodel.filter(years=years_active,
                           markets=','.join([str(e) for e in flt_active[fmrkt]['list']] if flt_active else ''),
                           status=','.join([str(e) for e in flt_active[fstat]['list']] if flt_active else ''),
                           employees=','.join([str(e) for e in flt_active[fempl]['list']] if flt_active and not (0 in flt_active[fempl]['list']) else ''),
                           lpus_in=extra_in_filter('l.Cust_ID',flt_active[fcust] if flt_active else ''),
                           winrs_in=extra_in_filter('w.id', flt_active[fwinr] if flt_active else ''),
                           innrs_in = extra_in_filter('s.{}InnNx'.format(market_type_prefix), flt_active[finnr] if flt_active else ''),
                           trnrs_in = extra_in_filter('s.{}TradeNx'.format(market_type_prefix), flt_active[ftrnr] if flt_active else ''),
                           market_type_prefix = market_type_prefix,
                           org_id = org_id)
        else:
            rawmodel = RawModel('select null as name')

        return rawmodel

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(icontains=search)
        return qs

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        if sort_col==0:
            qs = qs.order_by('l.Org_CustNm')
        else:
            qs = qs.order_by('[{0}] {1}'.format(self._columns[sort_col], sort_dir))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = ''
        return context