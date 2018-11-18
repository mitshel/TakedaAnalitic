import json

from widgetpages.views import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust
from widgetpages.views import extra_in_filter
from db.rawmodel import RawModel
from widgetpages import queries
from widgetpages.ajaxdatatabe import AjaxRawDatatableView

class CompetitionsAjaxTable(AjaxRawDatatableView):
    order_columns = ['Org_CustNm', 'name']
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]
    org_id = 1

    def get_initial_queryset(self):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        flt = json.loads(filters_ajax_request)
        flt_active = {}
        if flt:
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

        if years_active:
            rawmodel = RawModel(queries.q_competitions)
            rawmodel = rawmodel.filter(years=years_active,
                           markets=','.join([str(e) for e in flt_active[fmrkt]['list']] if flt_active else ''),
                           status=','.join([str(e) for e in flt_active[fstat]['list']] if flt_active else ''),
                           employees=','.join([str(e) for e in flt_active[fempl]['list']] if flt_active and not (0 in flt_active[fempl]['list']) else ''),
                           lpus_in=extra_in_filter('l.Cust_ID',flt_active[fcust] if flt_active else ''),
                           winrs_in=extra_in_filter('w.id', flt_active[fwinr] if flt_active else ''),
                           innrs_in = extra_in_filter('s.InnNx', flt_active[finnr] if flt_active else ''),
                           trnrs_in = extra_in_filter('s.TradeNx', flt_active[ftrnr] if flt_active else ''),
                           org_id = org_id,
                           ).order_by('l.Org_CustNm', 'pvt.tradeNx')
        else:
            rawmodel = RawModel('select null as Org_CustINN, null as Org_CustNm, null as name')

        return rawmodel

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(lpu__icontains=search)

        return qs