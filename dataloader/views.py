from django.shortcuts import render
from django.views.generic import View, TemplateView

from .datafields import cache_metadata
from widgetpages.views import OrgMixin

class CacheMetaView(OrgMixin, TemplateView):
    template_name = 'cache_fields.html'

    def get_context_data(self, **kwargs):
        context = super(CacheMetaView, self).get_context_data(**kwargs)
        context['cache_fields'] = cache_metadata
        return context
