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

    def get_context_data(self, *args, **kwargs):
        try:
            self.initialize(*args, **kwargs)

            # prepare columns data (for DataTables 1.10+)
            self.columns_data = self.extract_datatables_column_data()

            # prepare list of columns to be returned
            self._columns = self.get_columns()

            # prepare initial queryset
            qs = self.get_initial_queryset()

            # store the total number of records (before filtering)
            #total_records = qs.count()

            # apply filters
            qs = self.filter_queryset(qs)

            # number of records after filtering
            total_display_records = qs.count()

            # apply ordering
            qs = self.ordering(qs)

            # apply pagintion
            qs = self.paging(qs)

            # prepare output data
            data = self.prepare_results(qs)

            ret = {'draw': int(self._querydict.get('draw', 0)),
                   #'recordsTotal': total_records,
                   'recordsFiltered': total_display_records,
                   'data': data
                   }

            return ret
        except Exception as e:
            return self.handle_exception(e)
