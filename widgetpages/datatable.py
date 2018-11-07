import json
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Count, Sum, Min, F, Q

from widgetpages.views import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust
from widgetpages.views import FiltersView
from db.models import Hs, Target, Employee, Lpu, Market, StatusT, InNR, TradeNR, WinnerOrg

class FilterListJson(BaseDatatableView):
    columns = ['name', 'ext', 'iid']
    order_columns = ['name', 'ext']
    org_id = 1

    def filter_innr(self, flt_active=None):
        if not flt_active:
            innr_enabled = InNR.objects.all().values('name',iid=F('id')).order_by('name')
        else:
            innr_enabled = InNR.objects.all().values(iid=F('id'))
        return list(innr_enabled)

    def filter_trnr(self, flt_active=None):
        if not flt_active:
            trnr_enabled = TradeNR.objects.all().values('name',iid=F('id')).order_by('name')
        else:
            trnr_enabled = TradeNR.objects.all().values(iid=F('id'))
        return list(trnr_enabled)


    def filter_winr(self, flt_active=None):
        if not flt_active:
            winr_enabled = WinnerOrg.objects.all().values('name',iid=F('id'),ext=F('inn')).order_by('name')
        else:
            winr_enabled = WinnerOrg.objects.all().values(iid=F('id'))
        return list(winr_enabled)

    def filter_cust(self, flt_active=None):
        if not flt_active:
            lpu_enabled = Lpu.objects.exclude(cust_id=0).filter(employee__org=self.org_id). \
                values('name', ext=F('inn'), iid=F('cust_id')).distinct().order_by('name')
        else:
            lpu_enabled = Lpu.objects.filter(employee__in=flt_active[fempl]['list']).exclude(cust_id=0). \
                values('name', ext=F('inn'), iid=F('cust_id')).distinct().order_by('name')
        return lpu_enabled

    def get_initial_queryset(self):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        flt = json.loads(filters_ajax_request)
        flt_active = {}
        if flt:
            for f in [fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust]:
                flt_str = flt.get('{}_active'.format(f), '')
                flt_select = flt.get('{}_select'.format(f), '')
                flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select if flt_select else 0)}

        print(flt_active)


        if self.kwargs['flt_id'] == finnr:
            initial_data = InNR.objects.values('name', iid=F('id')).order_by('name')
        if self.kwargs['flt_id'] == ftrnr:
            initial_data = TradeNR.objects.values('name', iid=F('id')).order_by('name')
        if self.kwargs['flt_id'] == fwinr:
            initial_data = WinnerOrg.objects.values('name', ext=F('inn'), iid=F('id')).order_by('name')
        if self.kwargs['flt_id'] == fcust:
            initial_data = self.filter_cust(flt_active)

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