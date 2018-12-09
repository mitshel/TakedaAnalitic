from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, RedirectView, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from db.models import Org, Employee, Market, Lpu, InNR, TradeNR

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

        # Если текущая организация еще неизвестна, то получаем его по привязке к пользователю
        if (self.SETUP_METHODS & bOrgUSER)>0:
            if not org:
                try:
                    org = Org.objects.filter(users=self.request.user)[0]
                    org_id = org.id
                except:
                    org = None
                    org_id = None

            self.org_id = org_id
            self.org = org

        return org_id

    def dispatch(self, request, *args, **kwargs):
        self.init_dynamic_org()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = self.org
        return context

class OrgAdminMixin(OrgBaseMixin):
    SETUP_METHODS = bOrgSESSION | bOrgUSER

class BreadCrumbMixin(View):
    breadcrumbs = []
    supressorg = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.breadcrumbs
        context['supressorg'] = self.supressorg
        return context

#
# Выбор Организации для Администрирования
#

class SetupOrgView(OrgAdminMixin, RedirectView):
    pattern_name = 'farmadmin:orgselect'

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
    success_url = reverse_lazy('farmadmin:orgselect')

#
# Администрирование СОТРУДНИКОВ
#

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
        context['users'] = User.objects.filter(org=self.org).filter(employee_user__isnull=True).order_by('username')
        print(context)
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
        context['users'] = User.objects.filter(org=self.org).filter(employee_user__isnull=True).order_by('username')
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

#
# Администрирование РЫНКОВ
#

class MarketsAdminView(OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_markets.html'
    breadcrumbs = [{'name': 'Рынки', 'url': ''}]

    def get_queryset(self):
        return Market.objects.filter(org=self.org)

class MarketUpdateAdminView(OrgAdminMixin, BreadCrumbMixin, UpdateView):
    """ TODO: Здесь в дальнейшем при сохранении нужно сделать проверку что добавляемые МНН и ТМ не были добавлены кем-нибудь еще, в течение времени когда выполнялась работа по изменению набора МНН и ТМ в браузере
    """
    template_name = 'fa_market.html'
    breadcrumbs = [{'name': 'Рынки', 'url': reverse_lazy('farmadmin:markets')}]
    model = Market
    fields = ['id', 'org', 'name', 'innrs', 'tmnrs']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ИСключаем все INN и ТМ уже привязанные к рынкам текущей организации
        context['innrs'] = InNR.objects.exclude(market__org=self.org).exclude(id=54656).order_by('name')
        context['tmnrs'] = TradeNR.objects.exclude(market__org=self.org).order_by('name')
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')


class MarketCreateAdminView(OrgAdminMixin, BreadCrumbMixin, CreateView):
    template_name = 'fa_market.html'
    breadcrumbs = [{'name': 'Рынки', 'url': reverse_lazy('farmadmin:markets')},
                   {'name': 'Новый рынок', 'url': ''}]
    model = Market
    fields = ['org', 'name', 'innrs','tmnrs']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ИСключаем все INN и ТМ уже привязанные к рынкам текущей организации
        context['innrs'] = InNR.objects.exclude(market__org=self.org).exclude(id=54656).order_by('name')
        context['tmnrs'] = TradeNR.objects.exclude(market__org=self.org).order_by('name')
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')

class MarketDeleteAdminView(OrgAdminMixin, BreadCrumbMixin, DeleteView):
    template_name = 'fa_market.html'
    model = Market

    def get_success_url(self):
        return reverse('farmadmin:success')


#
# Администрирование ОРГАНИЗАЦИЙ
#
class OrgsAdminView(OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_orgs.html'
    breadcrumbs = [{'name': 'Организации', 'url': ''}]
    supressorg = True

    def get_queryset(self):
        return Org.objects.all()

class OrgUpdateAdminView(OrgAdminMixin, BreadCrumbMixin, UpdateView):
    """ TODO: Нужно добавить проверку, того, что при отвязке какого-либо пользователя от организации проверять не привязан ли он к сотруднику этой организации, если так, то сначала предлагать выполнить отвязку от сотрудника
    """
    template_name = 'fa_org.html'
    breadcrumbs = [{'name': 'Организации', 'url': reverse_lazy('farmadmin:orgs')}]
    supressorg = True
    model = Org
    fields = ['id', 'name', 'sync_time', 'sync_flag', 'users']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(org__isnull=True).order_by('username')
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')


class OrgCreateAdminView(OrgAdminMixin, BreadCrumbMixin, CreateView):
    template_name = 'fa_org.html'
    breadcrumbs = [{'name': 'Организации', 'url': reverse_lazy('farmadmin:orgs')},
                   {'name': 'Новая организация', 'url': ''}]
    supressorg = True
    model = Org
    fields = ['name', 'sync_time', 'sync_flag', 'users']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(org__isnull=True).order_by('username')
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')

class OrgDeleteAdminView(OrgAdminMixin, BreadCrumbMixin, DeleteView):
    template_name = 'fa_org.html'
    model = Org

    def get_success_url(self):
        return reverse('farmadmin:success')