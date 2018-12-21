import json

from widgetpages.BIMonBaseViews import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust, fempa
from widgetpages.BIMonBaseViews import extra_in_filter, OrgMixin, TargetsMixin
from widgetpages.ajaxdatatabe import AjaxRawDatatableView
from widgetpages import queries

from db.rawmodel import RawModel

class FilterListJson(OrgMixin, TargetsMixin, AjaxRawDatatableView):
    columns = ['name', 'ext', 'iid']
    order_columns = ['name']
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]

    def initial_innr(self, org_id=0):
        innr_enabled = RawModel(queries.q_innr_hs).filter(fields='a.id as iid, a.name', org_id=org_id)
        return innr_enabled

    def initial_trnr(self, org_id=0):
        trnr_enabled = RawModel(queries.q_tradenr_hs).filter(fields='a.id as iid, a.name', org_id=org_id)
        return trnr_enabled

    def initial_winr(self, org_id=0):
        winr_enabled = RawModel(queries.q_winner_hs).filter(fields='a.id as iid, a.inn as ext, a.name', org_id=org_id)
        return winr_enabled

    def initial_cust(self, org_id=0):
        lpu_enabled = RawModel(queries.q_lpu_hs).filter(fields='a.cust_id as iid, a.Org_CustInn as ext, a.Org_CustNm as name', org_id=org_id)
        return lpu_enabled

    def addfilters(self, qs, flt_active):
        if not flt_active:
            return qs

        if not self.fempa_selected(flt_active, fempa):
            qs = qs.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))

        #if self.kwargs['flt_id'] in (finnr, ftrnr):
        #        qs = qs.filter(market_in=extra_in_filter('m.market_id', flt_active[fmrkt]))

        return qs

    def get_initial_queryset(self):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        flt = json.loads(filters_ajax_request)
        flt_active = {}
        if flt:
            for f in self.filters_list:
                flt_str = flt.get('{}_active'.format(f), '')
                flt_select = flt.get('{}_select'.format(f), '')
                flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select if flt_select else 0)}
                flt_active[fempa] = {'list': [], 'select': int(flt.get('empl_all', '0'))}
        else:
            targets = self.get_initial_targets()
            flt_active[fempl] = self.targets_in_filter(targets)
            flt_active[fempa] = {'list': [], 'select': 0}

        initial_data ={}
        org_id = self.init_dynamic_org()

        if self.kwargs['flt_id'] == finnr:
            initial_data = self.addfilters(self.initial_innr(org_id), flt_active)
        if self.kwargs['flt_id'] == ftrnr:
            initial_data = self.addfilters(self.initial_trnr(org_id), flt_active)
        if self.kwargs['flt_id'] == fwinr:
            initial_data = self.addfilters(self.initial_winr(org_id), flt_active)
        if self.kwargs['flt_id'] == fcust:
            initial_data = self.addfilters(self.initial_cust(org_id), flt_active)

        return initial_data

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(name__icontains=search)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = ''
        return context
