import xlsxwriter
import io
import datetime
import decimal
import re
import os
import json

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse_lazy, reverse

class AjaxRawDatatableView(BaseDatatableView):
    max_display_length = 1000
    orderable = 1

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
            if self.orderable:
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


class DatatableXlsMixin(object):
    fields_description = {}

    def get_xls_data(self, *args, **kwargs):
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
            #total_display_records = qs.count()

            # apply ordering
            qs = self.ordering(qs)

            return qs

        except Exception as e:
            return self.handle_exception(e)

    def WriteToExcel(self, data, view_id='report'):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet_s = workbook.add_worksheet(view_id)

        # Here we will adding the code to add data

        bi_title = workbook.add_format({
            'bold': True,
            'color': 'blue',
            'font_size': 18,
            'align': 'left',
            'valign': 'vcenter'
        })

        title = workbook.add_format({
            'font_size': 16,
            'align': 'left',
            'valign': 'vcenter'
        })

        header = workbook.add_format({
            'bg_color': '#AAAAAA',
            'bold': True,
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'text_wrap': True,
            'border': 1
        })

        cell = workbook.add_format({
            'color': 'black',
            'align': 'left',
            'border': 1
        })

        numeric_cell = workbook.add_format({
            'color': 'black',
            'align': 'right',
            'border': 1
        })

        worksheet_s.merge_range('A1:H1', 'BI Monitor', bi_title)
        worksheet_s.merge_range('A2:H2', 'ID отчета: ' + view_id, title)
        hide_columns = []

        if len(data)>0:
            xls_col_n = 0
            columns = data[0].keys()
            for idx_col, column in enumerate(columns):
                title = column
                width = 10
                hide = 0
                for r in self.fields_description.keys():
                    if re.match(r,column,re.IGNORECASE):
                        title = re.sub(r,self.fields_description[r]['title'], column,1,re.IGNORECASE)
                        width = self.fields_description[r]['width']
                        cont = self.fields_description[r].get('continue',0)
                        hide = self.fields_description[r].get('hide',0)
                        if not cont:
                            break
                if not hide:
                    worksheet_s.write(3, xls_col_n, title, header)
                    worksheet_s.set_column(xls_col_n,xls_col_n,width)
                    xls_col_n += 1
                    #print('{} {}'.format(column, type(data[0][column])))
                else:
                    hide_columns.append(idx_col)

            for idx_row, row in enumerate(data):
                 if idx_row > settings.BI_MAX_XLS_ROWS:
                     break
                 rown = 4 + idx_row
                 xls_col_n = 0
                 for idx_col, column in enumerate(columns):
                    if not idx_col in hide_columns:
                        if isinstance(row[column], (datetime.date,datetime.datetime)):
                            worksheet_s.write(rown, xls_col_n, row[column].strftime('%d.%m.%Y'), cell)
                        elif isinstance(row[column], (int,decimal.Decimal)):
                            worksheet_s.write_number(rown, xls_col_n, row[column], numeric_cell)
                        else:
                            worksheet_s.write(rown, xls_col_n, row[column], cell)

                        xls_col_n += 1

        workbook.close()
        xlsx_data = output.getvalue()
        # xlsx_data contains the Excel file
        return xlsx_data


    # def post(self, *args, **kwargs):
    #     if not ('excel' in self.request.POST):
    #         return self.get(*args, **kwargs)
    #
    #     view_id = self.request.POST.get('view_id', 'report')
    #     qs = self.get_xls_data(*args, **kwargs)
    #     data = qs.open().fetchall()
    #     qs.close()
    #
    #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  #application/vnd.ms-excel
    #     response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(view_id)
    #     response['Set-Cookie'] = 'fileDownload = true;  path = /'
    #     xlsx_data = self.WriteToExcel(data, view_id)
    #
    #     response.write(xlsx_data)
    #     return response

    def post(self, *args, **kwargs):
        if not ('excel' in self.request.POST):
            return self.get(*args, **kwargs)

        view_id = self.request.POST.get('view_id', 'report')
        qs = self.get_xls_data(*args, **kwargs)
        data = qs.open().fetchall()
        qs.close()

        xlsx_data = self.WriteToExcel(data, view_id)
        xlsx_file_name = '{}_{}_{}.xlsx'.format(view_id, self.request.user, datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
        xlsx_file_path = os.path.join(settings.BI_TMP_FILES_DIR,xlsx_file_name)
        fw = open(xlsx_file_path, 'wb')
        fw.write(xlsx_data)
        fw.close()
        response = {'download_url':reverse('widgetpages:download_xls', kwargs={'file_name':xlsx_file_name})}
        dump = json.dumps(response)
        return self.render_to_response(dump)
