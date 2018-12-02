from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from db.models import Org, Employee, Market, Lpu

class SuccessView(TemplateView):
    template_name = 'fa_ajax_success.html'

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

class EmployeeUpdateAdminView(UpdateView):
    template_name = 'fa_employee.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')}]
    model = Employee
    fields = ['id','name','parent','istarget','lpu']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.org = Org.objects.get(users=self.request.user)
        except:
            self.org = None

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        context['org'] = self.org
        context['breadcrumbs'] = self.breadcrumbs
        context['parents'] = Employee.objects.filter(org=self.org).exclude(id=object.id).exclude(parent_id=object.id)
        context['users'] = User.objects.filter(org=self.org)

        return context

    def get_success_url(self):
        return reverse('farmadmin:success')


class EmployeeCreateAdminView(CreateView):
    template_name = 'fa_employee.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')},
                   {'name': 'Новый сотрудник', 'url': ''}]
    model = Employee
    fields = ['id','org', 'name','parent','istarget','lpu']

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
        context['parents'] = Employee.objects.filter(org=self.org)

        return context

    def get_success_url(self):
        return reverse('farmadmin:success')

class EmployeeDeleteAdminView(DeleteView):
    template_name = 'fa_employee.html'
    model = Employee

    def dispatch(self, request, *args, **kwargs):
        try:
            self.org = Org.objects.get(users=self.request.user)
        except:
            self.org = None

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = self.org
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')

# Загрузка полной таблицы со всеми учреждениями
class AjaxLpuAllDatatableView(BaseDatatableView):
    order_columns = ['name','inn']
    columns = ['cust_id','inn','name']

    def get_initial_queryset(self):
        return Lpu.objects.order_by('name', 'inn')

    def paging(self, qs):
        """ Не используем пакинацию, а возвращаем весь датасет
        """
        return qs


class MarketsAdminView(FarmAdminListView):
    template_name = 'fa_layout.html'
    breadcrumbs = [{'name': 'Рынки', 'url': ''}]

    def get_queryset(self):
        return Market.objects.filter(org=self.org)