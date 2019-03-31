import json
import io
import os
import xlsxwriter
import datetime
import decimal

from django.shortcuts import render, render_to_response, reverse, HttpResponse
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers
from django.conf import settings
from django.utils.cache import add_never_cache_headers

from .datafields import cache_metadata, get_fieldmeta
from .datafields import fk_mnn, fk_tm
from . import queries

from db.models import InNR, TradeNR
from db.rawmodel import RawModel, CachedRawModel

from widgetpages.views import FiltersView
from widgetpages.BIMonBaseViews import fempl,fmrkt,fyear,fstat,finnr,ftrnr,fwinr,fcust,fempa, fserv, fbudg, fdosg, fform

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

class DownloadView(View):

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

        worksheet_s.merge_range('A1:H1', 'BI Monitor ({})'.format('Takeda'), bi_title)

        fld = json.loads(fields) if fields else []
        if fld:
            xls_col_n = 0
            for idx_col, column in enumerate(fld):
                field_info = get_fieldmeta(column)
                title = field_info.get('title',column)
                width = field_info.get('width',10)
                worksheet_s.write(4, xls_col_n, title, header)
                worksheet_s.set_column(xls_col_n, xls_col_n, width)
                xls_col_n += 1

            qs = CachedRawModel(queries.q_dl_table).filter(fields = ', '.join(fld))
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
        print(fields)
        print(filters)
        xlsx_data = self.WriteToExcel(fields, filters)
        xlsx_file_name = '{}_{}_{}.xlsx'.format('OUTPUT', 'test', datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
        xlsx_file_path = os.path.join(settings.BI_TMP_FILES_DIR,xlsx_file_name)
        fw = open(xlsx_file_path, 'wb')
        fw.write(xlsx_data)
        fw.close()
        response = {'download_url':reverse('widgetpages:download_xls', kwargs={'file_name':xlsx_file_name})}
        dump = json.dumps(response)
        return self.render_to_response(dump)
