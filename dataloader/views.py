import json
import io
import os
import xlsxwriter
import datetime
import decimal

from django.shortcuts import render, render_to_response, reverse, HttpResponse
from django.views.generic import View, TemplateView, DeleteView
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers
from django.conf import settings
from django.utils.cache import add_never_cache_headers
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from .datafields import cache_metadata, get_fieldmeta
from .datafields import fk_mnn, fk_tm
from .datafields import ft_unknown, ft_none, ft_integer, ft_numeric, ft_date, ft_string, ft_fk
from . import queries

from db.models import InNR, TradeNR, Filters
from db.rawmodel import RawModel, CachedRawModel

from widgetpages.ajaxdatatabe import AjaxRawDatatableView
from widgetpages.views import FiltersView

class CacheMetaView(FiltersView):
    template_name = 'cache_fields.html'
    view_id = 'download_data'
    view_name = 'Загрузка данных'

    def get_context_data(self, **kwargs):
        context = super(CacheMetaView, self).get_context_data(**kwargs)
        context['cache_fields'] = cache_metadata
        return context

class FkFieldView(View):

    def get(self, request, *args, **kwargs):
        search_text = kwargs.get('search_text', '')
        if kwargs['fk_name'] == fk_mnn :
            data = InNR.objects.order_by('name').values('id','name').annotate(text=F('name'))
            if search_text!='undefined':
                data = data.filter(name__contains=search_text)
        if kwargs['fk_name'] == fk_tm :
            data = TradeNR.objects.order_by('name').values('id','name').annotate(text=F('name'))
            if search_text!='undefined':
                data = data.filter(name__contains=search_text)
        response = dict({'results':list(data)})
        # response = json.dumps([{'value':item['id'], 'caption':item['name']} for item in data])
        print(search_text,' > ',response)
        return JsonResponse(response)


class FiltersAjaxTable(BaseDatatableView):
    order_columns = ['name']
    columns = ['name','created','id']
    max_display_length = 500

    def get_initial_queryset(self):
        qs = Filters.objects.filter(user=self.request.user)
        return qs

class FiltersSaveView(View):
    def post(self, *args, **kwargs):
        result = '1'
        if self.request.is_ajax():
            if self.request.POST:
                fields = self.request.POST.get('fields', '')
                filters = self.request.POST.get('filters', '')
                name = self.request.POST.get('name', '')
                id = int(self.request.POST.get('id', '0'))
                save_type = int(self.request.POST.get('type', '0'))
                print(self.request.POST)
                print(fields)
                print(filters)
                if save_type == 3:
                    Filters.objects.update_or_create(name=name, user=self.request.user, defaults ={ 'fields_json':json.dumps(fields), 'filters_json':json.dumps(filters), 'status':0})
                elif save_type == 2:
                    Filters.objects.filter(id=id).update(name=name)

                result = '0'

        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps([{'result': result}]))
        return response

class FiltersDeleteView(View):
    def post(self, *args, **kwargs):
        result = '1'
        if self.request.is_ajax():
            if self.request.POST:
                id = self.request.POST.get('id', '0')
                Filters.objects.filter(id=int(id)).delete()
                result = '0'

        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps([{'result': result}]))
        return response

class DownloadView(View):
    oper1map = {1:"=",2:"<>",3:">",4:">=",5:"<",6:"<="}
    oper2map = {1: "like '%{}%'", 2: "not like '%{}%'", 3: "like '{}%'", 4: "like '%{}'", 5: "= '{}'", 6: "<> '{}'"}
    logicmap = {0:"",1:"and",2:"or"}

    def render_to_response(self, context):
        """ Returns a JSON response containing 'context' as payload
        """
        return self.get_json_response(context)

    def get_json_response(self, content, **httpresponse_kwargs):
        """ Construct an `HttpResponse` object.
        """
        response = HttpResponse(content,
                                content_type='application/json',
                                **httpresponse_kwargs)
        add_never_cache_headers(response)
        return response

    def create_filter_date(self, field_name, f):
        filter = ''
        for row in f:
            filter += "( {} {} CONVERT(DATETIME,'{}',104) ) {} ".format(field_name, self.oper1map[int(row[0])], row[1], self.logicmap[int(row[2])])

        return '( {} )'.format(filter)

    def create_filter_number(self, field_name, f):
        filter = ''
        for row in f:
            filter += "( {} {} {} ) {} ".format(field_name, self.oper1map[int(row[0])], row[1], self.logicmap[int(row[2])])

        return '( {} )'.format(filter)

    def create_filter_string(self, field_name, f):
        filter = ''
        for row in f:
            filter += "( {} {} ) {} ".format(field_name, self.oper2map[int(row[0])].format(row[1]), self.logicmap[int(row[2])])

        return '( {} )'.format(filter)

    def create_filter_fk(self, field_name, f):
        filter = "{} in ({})".format(field_name, ','.join(f[0][1]))
        return '( {} )'.format(filter)

    def create_filter(self, flt):
        filter = []
        for column in flt.keys():
            field_info = get_fieldmeta(column)
            if field_info['type'] == ft_date:
                filter.append(self.create_filter_date(column, flt[column]))

            if (field_info['type'] == ft_integer) or (field_info['type'] == ft_numeric):
                filter.append(self.create_filter_number(column, flt[column]))

            if field_info['type'] == ft_string:
                filter.append(self.create_filter_string(column, flt[column]))

            if field_info['type'] == ft_fk:
                filter.append(self.create_filter_fk(column, flt[column]))

        return ' and '.join(filter)


    def WriteToExcel(self, fields, filters):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet_s = workbook.add_worksheet('OUTPUT')

        bi_title = workbook.add_format({
            'bold': True,
            'color': 'blue',
            'font_size': 18,
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

        worksheet_s.merge_range('A1:H1', 'BI Monitor ({})'.format('Выгрузка данных'), bi_title)

        fld = json.loads(fields) if fields else []
        flt = json.loads(filters) if filters else []
        if fld:
            xls_col_n = 0
            for idx_col, column in enumerate(fld):
                field_info = get_fieldmeta(column)
                title = field_info.get('title',column)
                width = field_info.get('width',10)
                worksheet_s.write(4, xls_col_n, title, header)
                worksheet_s.set_column(xls_col_n, xls_col_n, width)
                xls_col_n += 1

            qs = CachedRawModel(queries.q_dl_table).filter(fields = ', '.join(fld), rows = settings.BI_MAX_DOWNLOAD_ROWS).filter(filters = self.create_filter(flt))
            print(qs.query)
            data = qs.open().fetchall()
            for idx_row, row in enumerate(data):
                if idx_row > settings.BI_MAX_XLS_ROWS:
                    break
                rown = 5 + idx_row
                xls_col_n = 0
                for idx_col, column in enumerate(fld):
                    if isinstance(row[column], (datetime.date, datetime.datetime)):
                        worksheet_s.write(rown, xls_col_n, row[column].strftime('%d.%m.%Y'), cell)
                    elif isinstance(row[column], (int, decimal.Decimal)):
                        worksheet_s.write_number(rown, xls_col_n, row[column], numeric_cell)
                    else:
                        worksheet_s.write(rown, xls_col_n, row[column], cell)

                    xls_col_n += 1
            qs.close();

        workbook.close()
        xlsx_data = output.getvalue()
        return xlsx_data

    def post(self, *args, **kwargs):
        fields = self.request.POST.get('fields', '')
        filters = self.request.POST.get('filters', '')
        xlsx_data = self.WriteToExcel(fields, filters)
        xlsx_file_name = '{}_{}_{}.xlsx'.format('OUTPUT', 'test', datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
        xlsx_file_path = os.path.join(settings.BI_TMP_FILES_DIR,xlsx_file_name)
        fw = open(xlsx_file_path, 'wb')
        fw.write(xlsx_data)
        fw.close()
        response = {'download_url':reverse('widgetpages:download_xls', kwargs={'file_name':xlsx_file_name})}
        dump = json.dumps(response)
        return self.render_to_response(dump)
