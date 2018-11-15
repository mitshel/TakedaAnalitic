from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from db.models import Org

from db.models import Hs_create

class AjaxRawDatatableView(BaseDatatableView):
    Hs = None

    def get_initial_queryset(self):
        org = Org.objects.filter(employee__users=self.request.user)
        print('2==>', org[0].id, org[0].name)
        self.Hs = Hs_create('org_CACHE_{}'.format(org[0].id if org else 0))
        #self.Hs = Hs_create('Test_CACHE_1')
        return []

    def render_column(self, row, column):
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