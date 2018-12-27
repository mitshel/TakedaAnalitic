import datetime
from operator import attrgetter

from django.urls import reverse_lazy
from django.views.generic import TemplateView

from widgetpages.BIMonBaseViews import unique, extra_in_filter, OrgMixin, FiltersView, BaseDatatableYearView
from widgetpages.BIMonBaseViews import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust,fempa, fserv, fbudg
from widgetpages import queries

from db.rawmodel import RawModel

class HomeView(OrgMixin, TemplateView):
    template_name = 'ta_hello.html'

class SalessheduleView(FiltersView):
    filters_list = [fempl, fmrkt, fyear, fcust]
    template_name = 'ta_salesshedule.html'
    ajax_filters_url = reverse_lazy('widgetpages:salesshedule')
    view_id = 'salesshedule'
    view_name = 'График продаж'

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        pivot_data = {}
        hsy_active = self.apply_filters(RawModel(queries.q_sales_year).order_by('1', '2'),flt_active, org_id, targets)
        hsm_active = self.apply_filters(RawModel(queries.q_sales_month).order_by('1', '2'),flt_active, org_id, targets)

        pivot_data['pivot1'] = list (hsy_active.open().fetchall())
        pivot_data['pivot2'] = list (hsm_active.open().fetchall())
        pivot_data['year'] = list( unique([e['iid'] for e in pivot_data['pivot1']]) )
        pivot_data['year'].sort()

        hsy_active.close()
        hsm_active.close()

        return pivot_data

class BudgetsView(FiltersView):
    filters_list = [fempl,fmrkt,fyear,fstat,fbudg,finnr,ftrnr,fwinr,fcust]
    template_name = 'ta_budgets.html'
    ajax_filters_url = reverse_lazy('widgetpages:budgets')
    ajax_datatable_url = reverse_lazy('widgetpages:budgets_table')
    view_id = 'budgets'
    view_name = 'Каналы финансирования'
    select_own = 1
    select_market_type = 1
    default_market_type = 2 # Контракты
    default_own = 3         # Все рынки

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        data = {}
        budgets = self.apply_filters(RawModel(queries.q_budgets_chart).order_by('3'),flt_active, org_id, targets)
        budgets_list = list (budgets.open().fetchall())
        budgets.close()

        data['budgets'] = list(unique([e['budget_name'] for e in budgets_list]))
        data['budgets'].sort()
        years_chart = list(unique([e['iid'] for e in budgets_list]))
        years_chart.sort()

        budgets_dict = {}
        for y in years_chart:
            budgets_dict[y] = []
            for b in data['budgets']:
                b1 = [{'budget_name': e['budget_name'], 'summa': e['summa']} for e in budgets_list if (e['budget_name']==b and e['iid']==y)]
                budgets_dict[y].append(b1[0] if b1 else {'budget_name': b, 'summa': 0})


        if not flt_active.get(fyear):
            years_table = [y['iid'] for y in self.get_filter(flt, fyear)['data']]
        else:
            years_table = flt_active[fyear]['list']

        current_year = datetime.datetime.now().year
        try:
            sort_col = years_table.index(current_year)+3
            sort_dir = 'desc'
        except:
            sort_col = 2
            sort_dir = 'asc'

        data['sort_col'] = sort_col
        data['sort_dir'] = sort_dir
        data['pivot1'] = budgets_dict
        data['year'] = years_chart
        data['years_table'] = years_table
        data['last_column'] = len(years_table)+3

        return data

class BudgetsAjaxTable(BaseDatatableYearView):
    filters_list = [fempl,fmrkt,fyear,fstat,fbudg,finnr,ftrnr,fwinr,fcust]
    datatable_query = queries.q_budgets_table
    datatable_count_query = queries.q_budgets_table_count

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        if sort_col<=3:
            qs = qs.order_by('t.name', 'gr','l.Org_CustNm')
        else:
            qs = qs.order_by('sum([{0}]) over (PARTITION BY nn.id, nn.gr) {1}'.format(self._columns[sort_col], sort_dir), 't.name', 'gr desc', 'l.Org_CustNm')
        return qs


class CompetitionsView(FiltersView):
    template_name = 'ta_competitions.html'
    ajax_filters_url = reverse_lazy('widgetpages:competitions')
    view_id = 'competitions'
    view_name = 'Конкурентный анализ(тыс.руб.)'
    select_market_type = 1
    select_own = 1
    default_market_type = 2 # Контракты
    default_own = 3  # Все рынки

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        data = {}

        if not flt_active.get(fyear):
            years_active = [y['iid'] for y in self.get_filter(flt, fyear)['data']]
        else:
            years_active = flt_active[fyear]['list']

        current_year = datetime.datetime.now().year
        try:
            sort_col = years_active.index(current_year)+3
            sort_dir = 'desc'
        except:
            sort_col = 2
            sort_dir = 'asc'

        data['year'] = years_active
        data['sort_col'] = sort_col
        data['sort_dir'] = sort_dir
        return data

class CompetitionsLpuView(CompetitionsView):
    ajax_filters_url = reverse_lazy('widgetpages:competitions_lpu')
    ajax_datatable_url = reverse_lazy('widgetpages:jcompetitions_lpu')
    view_id = 'competitions_lpu'
    view_name = 'Конкурентный анализ по ЛПУ (тыс.руб.)'

class CompetitionsMarketView(CompetitionsView):
    ajax_filters_url = reverse_lazy('widgetpages:competitions_market')
    ajax_datatable_url = reverse_lazy('widgetpages:jcompetitions_market')
    view_id = 'competitions_market'
    view_name = 'Конкурентный анализ по рынкам (тыс.руб.)'

class Lpu_CompetitionsAjaxTable(BaseDatatableYearView):
    order_columns = ['Org_CustNm', 'name']
    datatable_query = queries.q_competitions_lpu
    empty_datatable_query = 'select null as Org_CustINN, null as Org_CustNm, null as name '

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        if sort_col<=3:
            qs = qs.order_by('l.Org_CustNm', 'gr','t.name')
        else:
            qs = qs.order_by('sum([{0}]) over (PARTITION BY nn.id, nn.gr) {1}'.format(self._columns[sort_col], sort_dir), 'l.Org_CustNm', 'gr','t.name')
        return qs

class Market_CompetitionsAjaxTable(BaseDatatableYearView):
    order_columns = ['name']
    datatable_query = queries.q_competitions_market

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        if sort_col<=3:
            qs = qs.order_by('nn.id', 'gr','t.name')
        else:
            qs = qs.order_by('sum([{0}]) over (PARTITION BY nn.id, nn.gr) {1}'.format(self._columns[sort_col], sort_dir), 'nn.id', 'gr','t.name')
        return qs


class PartsView(FiltersView):
    template_name = 'ta_parts.html'
    ajax_filters_url = reverse_lazy('widgetpages:parts')
    view_id = 'parts'
    view_name = 'Доля (тыс.руб.)'
    select_market_type = 1
    default_market_type = 2 # Контракты

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        data = {}

        if not flt_active.get(fyear):
            years_active = [y['iid'] for y in self.get_filter(flt, fyear)['data']]
        else:
            years_active = flt_active[fyear]['list']

        current_year = datetime.datetime.now().year
        try:
            sort_col = years_active.index(current_year)*3+1
            sort_dir = 'desc'
        except:
            sort_col = 1
            sort_dir = 'asc'

        data['year'] = years_active
        data['sort_col'] = sort_col
        data['sort_dir'] = sort_dir
        return data

class MPartsAjaxTable(BaseDatatableYearView):
    datatable_query = queries.q_mparts
    datatable_count_query =  queries.q_mparts_count

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        if sort_col==0:
            qs = qs.order_by('gr', 'mt.name')
        else:
            qs = qs.order_by('gr','[{0}] {1}'.format(self._columns[sort_col], sort_dir))
        return qs


class LPartsAjaxTable(BaseDatatableYearView):
    datatable_query = queries.q_lparts
    datatable_count_query =  queries.q_lparts_count

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        if sort_col==0:
            qs = qs.order_by('l.Org_CustNm')
        else:
            qs = qs.order_by('[{0}] {1}'.format(self._columns[sort_col], sort_dir))
        return qs


class SalesAnlysisView(FiltersView):
    template_name = 'ta_sales_analysis.html'
    ajax_filters_url = reverse_lazy('widgetpages:sales_analysis')
    ajax_datatable_url = reverse_lazy('widgetpages:jsales_analysis')
    view_id = 'sales_analysis'
    view_name = 'Анализ продаж'
    select_own = 1
    select_market_type = 1
    default_market_type = 2 # Контракты
    default_own = 1         # Свой рынок

    def data(self, flt=None, flt_active=None, org_id=0, targets = []):
        data = {}

        data['sort_col'] = 0
        data['sort_dir'] = 'desc'
        return data

class SalesAnlysisAjaxTable(BaseDatatableYearView):
    datatable_query = queries.q_sales_analysis

    def ordering(self, qs):
        sort_col = int(self._querydict.get('order[0][column]'))
        sort_dir = self._querydict.get('order[0][dir]')
        qs = qs.order_by('[{0}] {1}'.format(self._columns[sort_col], sort_dir))
        return qs
