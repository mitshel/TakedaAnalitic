from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

class AjaxRawDatatableView(BaseDatatableView):
    max_display_length = 1000

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
