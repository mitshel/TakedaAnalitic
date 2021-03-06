import json

from widgetpages.views import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust, fempa
from widgetpages.views import extra_in_filter
from db.rawmodel import RawModel
from widgetpages import queries
from widgetpages.ajaxdatatabe import AjaxRawDatatableView
from widgetpages.views import OrgMixin, TargetsMixin

class CompetitionsAjaxTable(OrgMixin, TargetsMixin, AjaxRawDatatableView):
    order_columns = ['Org_CustNm', 'name']
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]
    org_id = 1

    def get_initial_queryset(self):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        self.view_id = self.request.POST.get('view_id', 'competitions_lpu')
        market_type = '1'
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
            targets = self.get_initial_targets()
            flt_active[fempl] = self.targets_in_filter(targets)
            flt_active[fempa] = {'list': [], 'select': 0}
            years_active = RawModel(queries.q_years_hs_empl).filter(fields="PlanTYear as iid",org_id=org_id, \
                                                                   employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))
            flt_active[fyear] = {'list':[e['iid'] for e in years_active.open().fetchall()], 'select':0}
            years_active.close()

        market_type_prefix = 'Order_' if market_type == '1' else 'Contract_'

        if flt_active[fyear]['list']:
            q_competitions = queries.q_competitions_lpu if self.view_id == 'competitions_lpu' else queries.q_competitions_market
            rawmodel = RawModel(q_competitions)
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
            rawmodel = RawModel('select null as Org_CustINN, null as Org_CustNm, null as name')

        return rawmodel

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(icontains=search)
        return qs

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        if sort_col<=3:
            qs = qs.order_by('l.Org_CustNm' if self.view_id == 'competitions_lpu' else 'nn.id', 'gr','t.name')
        else:
            qs = qs.order_by('sum([{0}]) over (PARTITION BY nn.id, nn.gr) {1}'.format(self._columns[sort_col], sort_dir), 'l.Org_CustNm' if self.view_id == 'competitions_lpu' else 'nn.id', 'gr','t.name')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = ''
        return context