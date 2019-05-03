import json
import io
import os
import xlsxwriter
import datetime
import decimal
import time

from django.http import JsonResponse
from django.shortcuts import render, render_to_response, reverse, HttpResponse
from django.views.generic import View, TemplateView, DeleteView
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers
from django.conf import settings
from django.utils.cache import add_never_cache_headers
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.utils import timezone

from TakedaAnalitic.celery import app

from .datafields import cache_metadata, get_fieldmeta
from .datafields import fk_mnn, fk_tm, fk_status, fk_region, fk_lpu, fk_fo, fk_budgets, fk_winner, fk_unit, fk_formt, fk_bprog
from .datafields import ft_unknown, ft_none, ft_integer, ft_numeric, ft_date, ft_string, ft_fk
from . import queries

from db.models import InNR, TradeNR, StatusT, Region, Lpu, FO, Budget, WinnerOrg, Unit, FormT, BProg, Filters
from db import models
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
        if kwargs['fk_name'] == fk_tm :
            data = TradeNR.objects.order_by('name').values('id','name').annotate(text=F('name'))
        if kwargs['fk_name'] == fk_status :
            data = StatusT.objects.exclude(id=0).order_by('name').values('id','name').annotate(text=F('name'))
        if kwargs['fk_name'] == fk_region :
            data = Region.objects.filter(reg_id__lt=100).order_by('regnm').values('reg_id','regnm').annotate(id=F('reg_id'),text=F('regnm'))
        if kwargs['fk_name'] == fk_lpu :
            data = Lpu.objects.order_by('name').values('cust_id','name').annotate(id=F('cust_id'),text=F('name'))
        if kwargs['fk_name'] == fk_fo :
            data = FO.objects.filter(id__lte=10).order_by('name').values('id','name').annotate(text=F('name'))
        if kwargs['fk_name'] == fk_budgets :
            data = Budget.objects.order_by('name').values('id','name').annotate(text=F('name'))
        if kwargs['fk_name'] == fk_winner :
            data = WinnerOrg.objects.order_by('name').values('id','name').annotate(text=F('name'))
        if kwargs['fk_name'] == fk_unit :
            data = Unit.objects.exclude(id=0).order_by('shortname').values('id','shortname').annotate(text=F('shortname'))
        if kwargs['fk_name'] == fk_formt :
            data = FormT.objects.exclude(id=0).order_by('name').values('id','name').annotate(text=F('name'))
        if kwargs['fk_name'] == fk_bprog :
            data = BProg.objects.order_by('name').values('id','name').annotate(text=F('name'))

        if search_text!='undefined':
            data = data.filter(name__contains=search_text)
        response = dict({'results':list(data)})
        # response = json.dumps([{'value':item['id'], 'caption':item['name']} for item in data])
        print(search_text,' > ',response)
        return JsonResponse(response)


class FiltersAjaxTable(BaseDatatableView):
    order_columns = ['name']
    columns = ['name','created','report_start','report_finish', 'id', 'status', 'xls_url']
    max_display_length = 500

    def get_initial_queryset(self):
        qs = Filters.objects.filter(user=self.request.user)
        return qs

    def render_column(self, row, column):
        if column!='xls_url':
            return super().render_column(row, column)

        value = getattr(row, column)

        if not value:
            value = self.none_string
        else:
            value = reverse('widgetpages:download_xls', kwargs={'file_name':value, 'remove':0})

        return value

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
                if save_type in (3,4):
                    Filters.objects.update_or_create(name=name, user=self.request.user, defaults ={ 'fields_json':json.dumps(fields), 'filters_json':json.dumps(filters), 'status':0})
                elif save_type == 2:
                    Filters.objects.filter(id=id).update(name=name)

                result = '0'

                print('Save filter: ', name)

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

class FiltersLoadView(View):
    def post(self, *args, **kwargs):
        result = '1'
        fields = '[]'
        filters = '{}'
        name = ''
        if self.request.is_ajax():
            if self.request.POST:
                id = int(self.request.POST.get('id', '0'))
                filter = Filters.objects.get(id=int(id))
                filters = json.loads(filter.filters_json)
                fields = json.loads(filter.fields_json)
                name = filter.name
                result = '0'
        print(fields)
        print(filters)
        return JsonResponse({'result': result, 'name':name, 'fields': fields, 'filters': filters})

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
            filter += "( {} {} CONVERT(DATETIME,'{}',104) ) {} ".format(field_name, self.oper1map[int(row[0])], row[1], self.logicmap[int(row[2] if row[2]!=None else 0)])

        return '( {} )'.format(filter)

    def create_filter_number(self, field_name, f):
        filter = ''
        for row in f:
            filter += "( {} {} {} ) {} ".format(field_name, self.oper1map[int(row[0])], row[1], self.logicmap[int(row[2] if row[2]!=None else 0)])

        return '( {} )'.format(filter)

    def create_filter_string(self, field_name, f):
        filter = ''
        for row in f:
            filter += "( {} {} ) {} ".format(field_name, self.oper2map[int(row[0])].format(row[1]), self.logicmap[int(row[2] if row[2]!=None else 0)])

        return '( {} )'.format(filter)

    def create_filter_fk(self, field_name, f):
        filter = "{} in ({})".format(field_name, ','.join(e['id'] if e['id'].isnumeric() else "'"+e['id']+"'" for e in f[0][1]))
        return '( {} )'.format(filter)

    def create_filter(self, flt):
        filter = []
        for column in flt.keys():
            field_info = get_fieldmeta(column)
            print(field_info)
            if field_info['type'] == ft_date:
                filter.append(self.create_filter_date(column, flt[column]))

            if (field_info['type'] == ft_integer) or (field_info['type'] == ft_numeric):
                filter.append(self.create_filter_number(column, flt[column]))

            if field_info['type'] == ft_string:
                filter.append(self.create_filter_string(column, flt[column]))

            if field_info['type'] == ft_fk:
                fk_column_name = field_info.get('fk_field','')
                fk_column_name = fk_column_name if fk_column_name else column
                filter.append(self.create_filter_fk(fk_column_name, flt[column]))

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
        print(fld)
        print(flt)
        if fld:
            xls_col_n = 0
            for idx_col, column in enumerate(fld):
                print(idx_col, '>>>>>>>',column)
                field_info = get_fieldmeta(column)
                title = field_info.get('title',column)
                width = field_info.get('width',10)
                worksheet_s.write(4, xls_col_n, title, header)
                worksheet_s.set_column(xls_col_n, xls_col_n, width)
                xls_col_n += 1
                print('ok')

            qs = CachedRawModel(queries.q_dl_table).filter(fields = ', '.join(fld), rows = settings.BI_MAX_DOWNLOAD_ROWS).filter(filters = self.create_filter(flt))
            qs.cache_default_timeout = 3600
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


@app.task
def generate_xls(filter_id):
    try:
        f = Filters.objects.get(id=filter_id)
    except:
        f = None
        return 1

    try:
        dv = DownloadView()
        f.status = models.ST_LOAD
        f.report_start = timezone.now()
        f.save()
        fields = json.loads(f.fields_json)
        filters = json.loads(f.filters_json)
        xlsx_data = dv.WriteToExcel(fields, filters)
        xlsx_file_name = '{}_{}_{}.xlsx'.format('OUTPUT', 'test', datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
        xlsx_file_path = os.path.join(settings.BI_TMP_FILES_DIR, xlsx_file_name)
        fw = open(xlsx_file_path, 'wb')
        fw.write(xlsx_data)
        fw.close()
        #time.sleep(10)
        f.status = models.ST_SUCCESS
        f.report_finish = timezone.now()
        f.xls_url = xlsx_file_name
    except:
        f.status = models.ST_FAILED
        f.xls_url = ""

    f.save()
    return

class DownloadXlsView(View):
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

    def post(self, *args, **kwargs):
        filter_id = int(self.request.POST.get('id', '0'))
        filter_name = self.request.POST.get('name', '')
        try:
            if filter_id != 0:
                f = Filters.objects.get(id=filter_id)
            else:
                f = Filters.objects.get(name=filter_name)
        except:
            f = None
            return self.render_to_response(json.dumps({'result': 'failed'}))

        filter_id = f.id;
        f.status = models.ST_LOAD
        f.report_start = None
        f.report_finish = None
        f.save()

        generate_xls.delay(filter_id)

        return self.render_to_response(json.dumps({'result': 'success'}))