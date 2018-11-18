import json
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import F

from widgetpages.views import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust
from widgetpages.views import FiltersView, extra_in_filter
from widgetpages.ajaxdatatabe import AjaxRawDatatableView
from db.models import Hs_create, Lpu, InNR, TradeNR, WinnerOrg

class FilterListJson(AjaxRawDatatableView):
    columns = ['name', 'ext', 'iid']
    order_columns = ['name', 'ext']
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]

    def zero_in(self, flt_active, fname):
        return ((flt_active[fname]['select'] == 1) and not (0 in flt_active[fname]['list'])) or \
               ((flt_active[fname]['select'] == 0) and (0 in flt_active[fname]['list']))

    def initial_innr(self):
        innr_enabled = InNR.objects.filter(hs__isnull=False).distinct().values('name', iid=F('id')).order_by('name')
        return innr_enabled

    def initial_trnr(self):
        trnr_enabled = TradeNR.objects.filter(hs__isnull=False).distinct().values('name', iid=F('id')).order_by('name')
        return trnr_enabled

    def initial_winr(self):
        winr_enabled = WinnerOrg.objects.distinct().exclude(id=0).filter(hs__isnull=False).values('name', iid=F('id'), ext=F('inn')).order_by('name')
        return winr_enabled

    def initial_cust(self):
        lpu_enabled = Lpu.objects.distinct().exclude(cust_id=0).values('name', ext=F('inn'), iid=F('cust_id')).distinct().order_by('name')
        return lpu_enabled

    def addfilters(self, qs, flt_active):
        if not flt_active:
            return qs

        if not self.zero_in(flt_active, fempl):
            if self.kwargs['flt_id'] == fcust:
                qs = qs.filter(employee__in=flt_active[fempl]['list'])
            else:
                qs = qs.filter(hs__cust_id__employee__in=flt_active[fempl]['list'])

        #qs = qs.filter(hs__market_id__in=flt_active[fmrkt]['list'])
        #qs = qs.filter(hs__PlanTYear__in=flt_active[fyear]['list'])
        #qs = qs.filter(hs__StatusT_ID__in=flt_active[fstat]['list'])
        #if self.kwargs['flt_id'] != fcust
        return qs

    def get_initial_queryset(self):
        super(FilterListJson, self).get_initial_queryset()
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        flt = json.loads(filters_ajax_request)
        flt_active = {}
        if flt:
            for f in self.filters_list:
                flt_str = flt.get('{}_active'.format(f), '')
                flt_select = flt.get('{}_select'.format(f), '')
                flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select if flt_select else 0)}

        initial_data ={}

        if self.kwargs['flt_id'] == finnr:
            initial_data = self.addfilters(self.initial_innr(), flt_active)
        if self.kwargs['flt_id'] == ftrnr:
            initial_data = self.addfilters(self.initial_trnr(), flt_active)
        if self.kwargs['flt_id'] == fwinr:
            initial_data = self.addfilters(self.initial_winr(), flt_active)
        if self.kwargs['flt_id'] == fcust:
            initial_data = self.addfilters(self.initial_cust(), flt_active)

        return initial_data

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(name__icontains=search)

        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                escape(item['name'] if 'name' in item else ''), # escape HTML for security reasons
                escape(item['ext'] if 'ext' in item else ''),
                item['iid'] if 'iid' in item else 0,
            ])
        return json_data