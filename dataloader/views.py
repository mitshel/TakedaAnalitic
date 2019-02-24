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
            data = InNR.objects.filter(name__contains=search_text).order_by('name').values('id','name')
        if kwargs['fk_name'] == fk_tm :
            data = TradeNR.objects.filter(name__contains=search_text).order_by('name').values('id','name')
        response = dict({'items':list(data)})
        # response = json.dumps([{'value':item['id'], 'caption':item['name']} for item in data])
        print(search_text,' > ',response)
        return JsonResponse(response)
