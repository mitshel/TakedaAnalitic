import json
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Count, Sum, Min, F, Q

from widgetpages.views import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust
from widgetpages.views import FiltersView, extra_in_filter
from db.models import Hs, Target, Employee, Lpu, Market, StatusT, InNR, TradeNR, WinnerOrg

class FilterListJson(BaseDatatableView):
    columns = ['name', 'ext', 'iid']
    order_columns = ['name', 'ext']
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]
    org_id = 1

    def initial_innr(self):
        innr_enabled = InNR.objects.distinct().values('name', iid=F('id')).order_by('name')
        # if flt_active and not (0 in flt_active[fempl]['list']):
        #     innr_enabled = innr_enabled.filter(hs__cust_id__employee__in=flt_active[fempl]['list'])
        return innr_enabled

    def initial_trnr(self):
        trnr_enabled = TradeNR.objects.distinct().values('name', iid=F('id')).order_by('name')
        # if flt_active and not (0 in flt_active[fempl]['list']):
        #     trnr_enabled = trnr_enabled.filter(hs__cust_id__employee__in=flt_active[fempl]['list'])
        return trnr_enabled

    def initial_winr(self):
        winr_enabled = WinnerOrg.objects.distinct().exclude(id=0).values('name', iid=F('id'), ext=F('inn')).order_by('name')
        # if flt_active and not (0 in flt_active[fempl]['list']):
        #     winr_enabled = winr_enabled.filter(hs__cust_id__employee__in=flt_active[fempl]['list'])
        return winr_enabled

    def initial_cust(self):
        lpu_enabled = Lpu.objects.distinct().exclude(cust_id=0).values('name', ext=F('inn'), iid=F('cust_id')).distinct().order_by('name')
        # if flt_active and not (0 in flt_active[fempl]['list']):
        #     lpu_enabled = lpu_enabled.filter(employee__in=flt_active[fempl]['list'])
        return lpu_enabled

    def addfilters(self, qs, flt_active):
        if not flt_active:
            return qs

        if not (0 in flt_active[fempl]['list']):
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
        # use request parameters to filter queryset

        # simple example:
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

    # def render_column(self, row, column):
    #     # We want to render user as a custom column
    #     if column == 'name':
    #         # escape HTML for security reasons
    #         return escape(row['name'])
    #     else:
    #         return super(FilterListJson, self).render_column(row, column)