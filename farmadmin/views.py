from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, RedirectView, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from db.models import Org, Employee, Market, Lpu

bOrgPOST = 4
bOrgSESSION = 2
bOrgUSER = 1

class SuccessView(TemplateView):
    template_name = 'fa_ajax_success.html'


class OrgBaseMixin(View):
    org = None
    org_id = None
    SETUP_METHODS = 7

    def init_dynamic_org(self):
        user = self.request.user
        org_id = None
        org = None

        print('SETUP METHODS >',self.SETUP_METHODS)
        # Сначала получаем информацию об организации из запроса GET или POST
        if (self.SETUP_METHODS & bOrgPOST)>0:
            if self.request.method == 'GET':
                org_id = self.request.GET.get('org_id','0')
            if self.request.method == 'POST':
                org_id = self.request.POST.get('org_id','0')

            if org_id:
                try:
                    org_id = int(org_id)
                    org = Org.objects.get(id=org_id)
                except:
                    org_id = None
                    org = None
                print('POST >',org_id)

        # Если пользователь администратор пытаемся получить текущую организацию из сессии
        if (self.SETUP_METHODS & bOrgSESSION)>0:
            if not org:
                if (user.is_superuser or user.is_staff):
                    try:
                        org_id = int(self.request.session['org'])
                        org = Org.objects.get(id=org_id)
                    except:
                        org = None
                        org_id = None
                print('SESSION >', org_id)

        # Если текущая организация еще неизвестна, то получаем его по привязке к пользователю
        if (self.SETUP_METHODS & bOrgUSER)>0:
            if not org:
                try:
                    org = Org.objects.filter(users=self.request.user)[0]
                    org_id = org.id
                except:
                    org = None
                    org_id = None
                print('USER >', org_id)

            self.org_id = org_id
            self.org = org

        return org_id

    def dispatch(self, request, *args, **kwargs):
        self.init_dynamic_org()
        return super().dispatch(request, *args, **kwargs)

class OrgAdminMixin(OrgBaseMixin):
    SETUP_METHODS = bOrgSESSION | bOrgUSER

class BreadCrumbMixin(View):
    breadcrumbs = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = self.org
        context['breadcrumbs'] = self.breadcrumbs
        return context

class SetupOrgView(OrgAdminMixin, RedirectView):
    pattern_name = 'farmadmin:org'

    def get_redirect_url(self, *args, **kwargs):
        org_id = '0'
        if self.request.method == 'POST':
            org_id = self.request.POST.get('org','0')
        if self.request.method == 'GET':
            org_id = self.request.GET.get('org','0')

        if org_id:
            self.request.session['org'] = org_id

        return super().get_redirect_url(*args, **kwargs)

class OrgView(OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_org_select.html'
    model = Org
    success_url = reverse_lazy('farmadmin:porg')

class EmployeesAdminView(OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_employees.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': ''}]

    def get_queryset(self):
        return Employee.objects.filter(org=self.org)

class EmployeeUpdateAdminView(OrgAdminMixin, BreadCrumbMixin, UpdateView):
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


class EmployeeCreateAdminView(OrgAdminMixin, BreadCrumbMixin, CreateView):
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

class EmployeeDeleteAdminView(OrgAdminMixin, BreadCrumbMixin, DeleteView):
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

class MarketsAdminView(OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_layout.html'
    breadcrumbs = [{'name': 'Рынки', 'url': ''}]

    def get_queryset(self):
        return Market.objects.filter(org=self.org)