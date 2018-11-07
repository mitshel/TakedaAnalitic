from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Count, Sum, Min, F, Q

from widgetpages.views import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust
from widgetpages.views import FiltersView
from db.models import Hs, Target, Employee, Lpu, Market, StatusT, InNR, TradeNR, WinnerOrg

class FilterListJson(BaseDatatableView):
    columns = ['name', 'ext', 'iid']
    order_columns = ['name', 'ext']

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        #if self.kwargs['tn'] == fcust:
        #    initial_data = FiltersView.filter_cust()
        print(self.kwargs)

        if self.kwargs['flt_id'] == finnr:
            initial_data = InNR.objects.extra(select={'ext': 'CAST(id as varchar)', 'iid': 'id'}).values('name', 'ext', 'iid').order_by('name')
            print(initial_data)
        if self.kwargs['flt_id'] == ftrnr:
            initial_data = TradeNR.objects.extra(select={'ext': 'CAST(id as varchar)', 'iid': 'id'}).values('name', 'ext', 'iid').order_by('name')
        if self.kwargs['flt_id'] == fwinr:
            initial_data = WinnerOrg.objects.values('name', ext=F('inn'), iid=F('id')).order_by('name')
        if self.kwargs['flt_id'] == fcust:
            initial_data = Lpu.objects.exclude(cust_id=0).filter(employee__org=1). \
                    values('name', ext=F('inn'), iid=F('cust_id')).distinct().order_by('name')

        return initial_data

    def filter_queryset(self, qs):
        # use request parameters to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__icontains=search)

        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        print(self.kwargs, '>>', qs)
        json_data = []
        for item in qs:
            json_data.append([
                escape(item['name']), # escape HTML for security reasons
                escape(item['ext']),
                item['iid'],
            ])
        return json_data

    # def render_column(self, row, column):
    #     # We want to render user as a custom column
    #     if column == 'name':
    #         # escape HTML for security reasons
    #         return escape(row['name'])
    #     else:
    #         return super(FilterListJson, self).render_column(row, column)