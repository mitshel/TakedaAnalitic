from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, RedirectView, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from widgetpages.views import OrgMixin

from db.models import Org, Employee, Market, Lpu

class SuccessView(TemplateView):
    template_name = 'fa_ajax_success.html'

class SetupOrgView(OrgMixin, RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        org_id = '0'
        if self.request.method == 'POST':
            org_id = self.request.POST.get('org','0')
        if self.request.method == 'GET':
            org_id = self.request.GET.get('org','0')

        if org_id:
            self.request.session['org'] = org_id
            print('SETUP ORG=', org_id)

        return super().get_redirect_url(*args, **kwargs)


class OrgView(OrgMixin, ListView):
    template_name = 'fa_org_select.html'
    model = Org
    success_url = reverse_lazy('home')

class EmployeesAdminView(OrgMixin, ListView):
    template_name = 'fa_employees.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': ''}]

    def get_queryset(self):
        print('Org=',self.org)
        return Employee.objects.filter(org=self.org)

class EmployeeUpdateAdminView(OrgMixin, UpdateView):
    template_name = 'fa_employee.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')}]
    model = Employee
    fields = ['id','name','parent','istarget','lpu', 'users']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        context['parents'] = Employee.objects.filter(org=self.org).exclude(id=object.id).exclude(parent_id=object.id)
        users_id = Employee.objects.filter(org=self.org).values('users__id').filter(users__id__isnull=False).distinct()
        context['users'] = User.objects.filter(org=self.org).exclude(id__in=users_id)

        return context

    def get_success_url(self):
        return reverse('farmadmin:success')


class EmployeeCreateAdminView(OrgMixin, CreateView):
    template_name = 'fa_employee.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')},
                   {'name': 'Новый сотрудник', 'url': ''}]
    model = Employee
    fields = ['org', 'name','parent','istarget','lpu', 'users']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parents'] = Employee.objects.filter(org=self.org)
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')

class EmployeeDeleteAdminView(OrgMixin, DeleteView):
    template_name = 'fa_employee.html'
    model = Employee

    def get_success_url(self):
        return reverse('farmadmin:success')

# Загрузка полной таблицы со всеми учреждениями
class AjaxLpuAllDatatableView(BaseDatatableView):
    order_columns = ['name','inn']
    columns = ['cust_id','inn','name']

    def get_initial_queryset(self):
        return Lpu.objects.order_by('name', 'inn')

    def paging(self, qs):
        """ Не используем пакинацию, а возвращаем весь датасет """
        return qs

class MarketsAdminView(OrgMixin, ListView):
    template_name = 'fa_layout.html'
    breadcrumbs = [{'name': 'Рынки', 'url': ''}]

    def get_queryset(self):
        return Market.objects.filter(org=self.org)