import json

from widgetpages.BIMonBaseViews import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust, fdosg, fform, fempa, fbudg
from widgetpages.BIMonBaseViews import extra_in_filter, OrgMixin, FiltersMixin
from widgetpages.ajaxdatatabe import AjaxRawDatatableView
from widgetpages import queries

from db.rawmodel import RawModel, CachedRawModel

class FilterListJson(OrgMixin, FiltersMixin, AjaxRawDatatableView):
    columns = ['name', 'ext', 'iid']
    order_columns = ['name']

    def initial_dosg(self, org_id=0):
        dosg_enabled = CachedRawModel(queries.q_dosage_hs).filter(fields='a.id as iid, a.name', org_id=org_id)
        return dosg_enabled

    def initial_form(self, org_id=0):
        form_enabled = CachedRawModel(queries.q_form_hs).filter(fields='a.id as iid, a.name', org_id=org_id)
        return form_enabled

    def initial_innr(self, org_id=0):
        innr_enabled = CachedRawModel(queries.q_innr_hs).filter(fields='a.id as iid, a.name', org_id=org_id)
        return innr_enabled

    def initial_trnr(self, org_id=0):
        trnr_enabled = CachedRawModel(queries.q_tradenr_hs).filter(fields='a.id as iid, a.name', org_id=org_id)
        return trnr_enabled

    def initial_winr(self, org_id=0):
        winr_enabled = CachedRawModel(queries.q_winner_hs).filter(fields='a.id as iid, a.inn as ext, a.name', org_id=org_id)
        return winr_enabled

    def initial_cust(self, org_id=0):
        lpu_enabled = CachedRawModel(queries.q_lpu_hs).filter(fields='a.cust_id as iid, a.Org_CustInn as ext, a.Org_CustNm as name', org_id=org_id)
        return lpu_enabled

    def addfilters(self, qs, flt_active, org_id, targets):
        qs = self.apply_filters(qs, flt_active, org_id, targets)

        return qs

    def get_initial_queryset(self):
        initial_data ={}
        flt_id = self.request.POST.get('flt_id','')
        self.init_view_properties()
        org_id = self.init_dynamic_org()
        targets = self.get_initial_targets()
        flt_active = self.filters_active(org_id, targets)

        # self.kwargs['flt_id']
        if flt_id == fdosg:
            initial_data = self.addfilters(self.initial_dosg(org_id), flt_active, org_id, targets)
        if flt_id == fform:
            initial_data = self.addfilters(self.initial_form(org_id), flt_active, org_id, targets)
        if flt_id == finnr:
            initial_data = self.addfilters(self.initial_innr(org_id), flt_active, org_id, targets)
        if flt_id == ftrnr:
            initial_data = self.addfilters(self.initial_trnr(org_id), flt_active, org_id, targets)
        if flt_id == fwinr:
            initial_data = self.addfilters(self.initial_winr(org_id), flt_active, org_id, targets)
        if flt_id == fcust:
            initial_data = self.addfilters(self.initial_cust(org_id), flt_active, org_id, targets)

        return initial_data

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(name__icontains=search)

        return qs

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        qs = qs.order_by('[{}] {}'.format(self._columns[sort_col], sort_dir))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = ''
        return context


class PassportFilterListJson(FilterListJson):
    def initial_cust(self, org_id=0):
        lpu_enabled = CachedRawModel(queries.q_lpu_passport).filter(fields='l.cust_id as iid, l.Org_CustInn as ext, l.Org_CustNm as name').order_by('l.Org_CustNm')
        return lpu_enabled