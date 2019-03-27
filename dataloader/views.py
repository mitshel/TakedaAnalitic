import json

from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.db.models import F
from django.core import serializers

from .datafields import cache_metadata
from .datafields import fk_mnn, fk_tm

from db.models import InNR, TradeNR

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


    def post(self, *args, **kwargs):
        # qs = self.get_xls_data(*args, **kwargs)
        # data = qs.open().fetchall()
        # qs.close()

        # xlsx_data = self.WriteToExcel(data, view_id, view_name)
        # xlsx_file_name = '{}_{}_{}.xlsx'.format(view_id, self.request.user, datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
        # xlsx_file_path = os.path.join(settings.BI_TMP_FILES_DIR,xlsx_file_name)
        # fw = open(xlsx_file_path, 'wb')
        # fw.write(xlsx_data)
        # fw.close()
        # response = {'download_url':reverse('widgetpages:download_xls', kwargs={'file_name':xlsx_file_name})}
        # dump = json.dumps(response)
        # return self.render_to_response(dump)
        pass
