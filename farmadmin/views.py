from django.shortcuts import render
from django.views.generic import View, TemplateView

# Create your views here.
class EmployeeAdminView(TemplateView):
    template_name = 'fa_layout.html'

class MarketAdminView(TemplateView):
    template_name = 'fa_layout.html'