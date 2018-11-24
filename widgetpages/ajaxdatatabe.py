from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from db.models import Org

class AjaxRawDatatableView(BaseDatatableView):
    def init_dynamic_org(self):
        org = Org.objects.filter(users=self.request.user)
        org_id = org[0].id if org else 0
        return org_id

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