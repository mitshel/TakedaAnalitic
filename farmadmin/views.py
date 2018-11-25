from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from db.models import Org, Employee, Market
from django.urls import reverse_lazy

# Create your views here.
class FarmAdminListView(ListView):
    template_name = 'fa_layout.html'
    breadcrumbs = []
    org = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.org = Org.objects.get(users=self.request.user)
        except:
            self.org = None

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = self.org
        context['breadcrumbs'] = self.breadcrumbs

        return context

class EmployeesAdminView(FarmAdminListView):
    template_name = 'fa_employees.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': ''}]

    def get_queryset(self):
        return Employee.objects.filter(org=self.org)


class MarketsAdminView(FarmAdminListView):
    template_name = 'fa_layout.html'
    breadcrumbs = [{'name': 'Рынки', 'url': ''}]

    def get_queryset(self):
        return Market.objects.filter(org=self.org)


class FarmAdminDetailView(DetailView):
    template_name = 'fa_layout.html'
    breadcrumbs = []

    def dispatch(self, request, *args, **kwargs):
        try:
            self.org = Org.objects.get(users=self.request.user)
        except:
            self.org = None

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = self.org
        context['breadcrumbs'] = self.breadcrumbs

        return context

class EmployeeAdminView(FarmAdminDetailView):
    template_name = 'fa_employee.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')}]
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parents'] = Employee.objects.filter(org=self.org).exclude(id=kwargs['object'].id)

        return context
