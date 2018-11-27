from django.views.generic import View, TemplateView, ListView, DetailView
from db.models import Org, Employee, Market, Lpu
from django.urls import reverse_lazy
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

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
        context['lpu'] = Lpu.objects.filter(employee__id=kwargs['object'].id).order_by('name','inn')

        return context


class AjaxLpuAllDatatableView(BaseDatatableView):
    order_columns = ['name','inn']
    columns = ['cust_id','inn','name']

    def get_initial_queryset(self):
        employee = self.request.POST.get('employee', '0')
        return Lpu.objects.order_by('name', 'inn')
        #return Lpu.objects.exclude(employee=employee).order_by('name','inn')

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__icontains=search)|Q(inn__icontains=search))

        return qs

# class AjaxLpuEmpDatatableView(BaseDatatableView):
#     order_columns = ['name','inn']
#     columns = ['id','inn','name']
#
#     def get_initial_queryset(self):
#         employee = self.request.POST.get('employee','0')
#         return Lpu.objects.filter(employee=employee).order_by('name','inn')
#
#     def filter_queryset(self, qs):
#         search = self.request.POST.get('search[value]', None)
#         if search:
#             qs = qs.filter(Q(name__icontains=search)|Q(inn__icontains=search))
#
#         return qs