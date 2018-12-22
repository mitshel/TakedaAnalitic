import json

from widgetpages.BIMonBaseViews import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust, fempa
from widgetpages.BIMonBaseViews import extra_in_filter, OrgMixin, FiltersMixin
from widgetpages.ajaxdatatabe import AjaxRawDatatableView
from widgetpages import queries

from db.rawmodel import RawModel

class FilterListJson(OrgMixin, FiltersMixin, AjaxRawDatatableView):
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

    def addfilters(self, qs, flt_active, org_id, targets):
        # if not flt_active:
        #     return qs

        # if not self.fempa_selected(flt_active, fempa):
        #     qs = qs.filter(employee_in=extra_in_filter('e.employee_id', flt_active[fempl]))

        #if self.kwargs['flt_id'] in (finnr, ftrnr):
        #        qs = qs.filter(market_in=extra_in_filter('m.market_id', flt_active[fmrkt]))

        qs = self.apply_filters(qs, flt_active, org_id, targets)

        return qs

    def get_initial_queryset(self):
        initial_data ={}
        org_id = self.init_dynamic_org()
        targets = self.get_initial_targets()
        flt_active = self.filters_active(org_id, targets)

        if self.kwargs['flt_id'] == finnr:
            initial_data = self.addfilters(self.initial_innr(org_id), flt_active, org_id, targets)
        if self.kwargs['flt_id'] == ftrnr:
            initial_data = self.addfilters(self.initial_trnr(org_id), flt_active, org_id, targets)
        if self.kwargs['flt_id'] == fwinr:
            initial_data = self.addfilters(self.initial_winr(org_id), flt_active, org_id, targets)
        if self.kwargs['flt_id'] == fcust:
            initial_data = self.addfilters(self.initial_cust(org_id), flt_active, org_id, targets)

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
