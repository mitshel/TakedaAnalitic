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
    columns = ['Org_CustINN', 'Org_CustNm', 'name', '2018']
    order_columns = ['Org_CustNm', 'name']
    filters_list = [fempl, fmrkt, fyear, fstat, finnr, ftrnr, fwinr, fcust]
    org_id = 1

    def get_initial_queryset(self):
        filters_ajax_request = self.request.POST.get('filters_ajax_request', '')
        print('filters_ajax_request==>',filters_ajax_request)
        flt = json.loads(filters_ajax_request)
        flt_active = {}
        if flt:
            for f in self.filters_list:
                flt_str = flt.get('{}_active'.format(f), '')
                flt_select = flt.get('{}_select'.format(f), '')
                flt_active[f] = {'list':[int(e) for e in flt_str.split(',')] if flt_str else [], 'select': int(flt_select if flt_select else 0)}

        if not flt_active:
            years_active = list(Hs.objects.exclude(PlanTYear__isnull=True).\
                values('PlanTYear').distinct().order_by('PlanTYear').\
                values_list('PlanTYear', flat=True))
        else:
            years_active = flt_active[fyear]['list']

        print('Years active ==>', years_active)
        print('_columns ==>', self.columns_data)

        if years_active:
            rawmodel = RawModel(queries.q_competitions)
            rawmodel = rawmodel.filter(years=years_active,
                           markets=','.join([str(e) for e in flt_active[fmrkt]['list']] if flt_active else ''),
                           status=','.join([str(e) for e in flt_active[fstat]['list']] if flt_active else ''),
                           employees=','.join([str(e) for e in flt_active[fempl]['list']] if flt_active and not (0 in flt_active[fempl]['list']) else ''),
                           lpus_in=extra_in_filter('l','Cust_ID',flt_active[fcust] if flt_active else ''),
                           winrs_in=extra_in_filter('w', 'id', flt_active[fwinr] if flt_active else ''),
                           innrs_in = extra_in_filter('s', 'InnNx', flt_active[finnr] if flt_active else ''),
                           trnrs_in = extra_in_filter('s', 'TradeNx', flt_active[ftrnr] if flt_active else '')
                           ).order_by('l.Org_CustNm', 'pvt.tradeNx')
        else:
            rawmodel = RawModel('select null as Org_CustINN, null as Org_CustNm, null as name')

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
        value = row.get(column,'')

        if value is None:
            value = self.none_string

        if self.escape_values:
            value = escape(value)

        return value

    def prepare_results(self, qs):
        data = []
        rows = qs.open().fetchall()
        for item in rows:
            data.append([self.render_column(item, column['name']) for column in self.columns_data])
        qs.close()
        return data