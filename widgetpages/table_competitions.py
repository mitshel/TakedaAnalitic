import json
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Count, Sum, Min, F, Q

from widgetpages.views import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust
from widgetpages.views import FiltersView, extra_in_filter
from widgetpages.rawmodel import RawModel
from widgetpages import queries

from db.models import Hs, Target, Employee, Lpu, Market, StatusT, InNR, TradeNR, WinnerOrg

class CompetitionsAjaxTable(BaseDatatableView):
    columns = ['name', 'ext', 'iid']
    order_columns = ['name', 'ext']
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

        pivot_data = {}
        rawmodel = RawModel(queries.q_competitions)
        years_enabled = list([e['iid'] for e in self.get_filter(flt,fyear)['data']])
        years_active = flt_active[fyear]['list'] if flt_active else years_enabled
        years_active = [2015,2016,2017,2018,2019]
        years_intersect = sorted(list(set(years_enabled) & set(years_active)))

        rawmodel = rawmodel.filter(years=years_intersect,
                       markets=','.join([str(e) for e in flt_active[fmrkt]['list']] if flt_active else ''),
                       employees=','.join([str(e) for e in flt_active[fempl]['list']] if flt_active and not (0 in flt_active[fempl]['list']) else ''),
                       lpus_in=extra_in_filter('l','Cust_ID',flt_active[fcust] if flt_active else '')
                       ).order_by('pvt.cust_id', 'pvt.tradeNx')[0:100]

        print('Rawmodel Query ==>',rawmodel.query)
        return rawmodel

    def filter_queryset(self, qs):
        # use request parameters to filter queryset

        # simple example:
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(lpu__icontains=search)

        return qs

    def render_column(self, row, column):
        """ Renders a column on a row. column can be given in a module notation eg. document.invoice.type
        """
        value = row[column]

        if value is None:
            value = self.none_string

        if self.escape_values:
            value = escape(value)
        print("{}:{}".format(column,value))

        return value