from django.shortcuts import render
from django.views.generic import View, TemplateView

from .datafields import cache_metadata

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
