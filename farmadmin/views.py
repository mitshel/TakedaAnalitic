import json

from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, RedirectView, View
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.db.models import Q, F, Count
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms
from django.http import JsonResponse

from db.models import Org, Employee, Market, Lpu, InNR, TradeNR, Market_Innrs, Market_Tmnrs, SYNC_STATUS_CHOICES, Org_log, Region
from db.cache import clear_cache

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

        # Если текущая организация еще неизвестна, то получаем ее по привязке к пользователю
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = self.org
        context['org_id'] = self.org.id if self.org else 0
        return context

class OrgAdminMixin(OrgBaseMixin):
    SETUP_METHODS = bOrgSESSION | bOrgUSER

    def dispatch(self, request, *args, **kwargs):
        self.init_dynamic_org()
        return super().dispatch(request, *args, **kwargs)

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

class SetupOrgView(PermissionRequiredMixin, OrgAdminMixin, RedirectView):
    pattern_name = 'farmadmin:orgselect'
    permission_required = ('db.view_org', )

    def get_redirect_url(self, *args, **kwargs):
        org_id = '0'
        if self.request.method == 'POST':
            org_id = self.request.POST.get('org','0')
        if self.request.method == 'GET':
            org_id = self.request.GET.get('org','0')

        if org_id:
            self.request.session['org'] = org_id

        return super().get_redirect_url(*args, **kwargs)

class OrgView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_org_select.html'
    model = Org
    success_url = reverse_lazy('farmadmin:orgselect')
    permission_required = ('db.view_org', )

#
# Администрирование СОТРУДНИКОВ
#

class EmployeesAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_employees.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': ''}]
    permission_required = ('db.view_employee', )

    def get_queryset(self):
        return Employee.objects.filter(org=self.org).annotate(lpu_count=Count('lpu', distinct=True), region_count=Count('region', distinct=True)).prefetch_related('users').select_related('parent')

class EmployeeUpdateAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, UpdateView):
    template_name = 'fa_employee.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')}]
    model = Employee
    fields = ['id','name','parent','istarget','lpu', 'users']
    permission_required = ('db.change_employee',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        context['parents'] = Employee.objects.filter(org=self.org).exclude(id=object.id).exclude(parent_id=object.id)
        context['users'] = User.objects.filter(org=self.org).filter(employee_user__isnull=True).order_by('username')
        return context

    def get_success_url(self):
        clear_cache(0)
        return reverse('farmadmin:success')

class EmployeeCreateAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, CreateView):
    template_name = 'fa_employee.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')},
                   {'name': 'Новый сотрудник', 'url': ''}]
    model = Employee
    fields = ['org', 'name','parent','istarget','lpu', 'users']
    permission_required = ('db.add_employee',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parents'] = Employee.objects.filter(org=self.org)
        context['users'] = User.objects.filter(org=self.org).filter(employee_user__isnull=True).order_by('username')
        return context

    def get_success_url(self):
        clear_cache(0)
        return reverse('farmadmin:success')

class EmployeeUpdateBaseAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, UpdateView):
    template_name = 'fa_employee_base.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')}]
    model = Employee
    fields = ['id','name','parent','istarget']
    permission_required = ('db.change_employee',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        context['parents'] = Employee.objects.filter(org=self.org).exclude(id=object.id).exclude(parent_id=object.id)
        return context

    def get_success_url(self):
        clear_cache(0)
        clear_cache(self.org_id)
        return reverse('farmadmin:employees')

class EmployeeUpdateLpuAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, UpdateView):
    template_name = 'fa_employee_lpu.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')}]
    model = Employee
    fields = ['id','lpu']
    permission_required = ('db.change_employee',)

    def get_success_url(self):
        clear_cache(self.org_id)
        return reverse('farmadmin:success')

class EmployeeUpdateUserAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, UpdateView):
    template_name = 'fa_employee_user.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')}]
    model = Employee
    fields = ['id','users']
    permission_required = ('db.change_employee',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(org=self.org).filter(employee_user__isnull=True).order_by('username')
        return context

    def get_success_url(self):
        """ Чистим кэш организации 0, т.к. запросы по таргетов  в фильтр идут без привязки к организации а только по логину
            т.е. эти запросы попадют в кэш с ID организации = 0
        """
        clear_cache(0)
        return reverse('farmadmin:success')

class EmployeeUpdateRegAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, UpdateView):
    template_name = 'fa_employee_reg.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')}]
    model = Employee
    fields = ['id','region']
    permission_required = ('db.change_employee',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        context['regions'] = Region.objects.exclude(employee=object).order_by('regnm')
        return context

    def form_valid(self, form):
        redirect_url = super(EmployeeUpdateRegAdminView, self).form_valid(form)
        object = self.get_object()
        try:
            empl = Employee.objects.get(id=object.id)
        except:
            empl = None

        if empl:
            lpu_for_delete = empl.lpu.exclude(regcode__in=empl.region.all())
            lpu_for_delete.delete()

        return redirect_url

    def get_success_url(self):
        clear_cache(self.org_id)
        return reverse('farmadmin:success')

class EmployeeQueryRegAdminView(PermissionRequiredMixin, View):
    permission_required = ('db.change_employee',)

    def post(self, request, *args, **kwargs):
        status = 1
        lpu_for_delete = []
        if request.is_ajax():
            if request.POST:
                status = 0
                employee_id = int(request.POST.get('id', 0))
                regions = request.POST.getlist('region', [])

                try:
                    empl = Employee.objects.get(id=employee_id)
                except:
                    empl = None
                    status = 2

                if empl:
                    lpus = empl.lpu.exclude(regcode__in=[int(r) for r in regions])
                    lpu_for_delete = [l.name for l in lpus]

        return JsonResponse({'status':status, 'lpu_for_delete':lpu_for_delete})

class EmployeeCreateBaseAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, CreateView):
    template_name = 'fa_employee_base.html'
    breadcrumbs = [{'name': 'Сотрудники', 'url': reverse_lazy('farmadmin:employees')},
                   {'name': 'Новый сотрудник', 'url': ''}]
    model = Employee
    fields = ['org', 'name','parent','istarget']
    permission_required = ('db.add_employee',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parents'] = Employee.objects.filter(org=self.org)
        return context

    def get_success_url(self):
        clear_cache(self.org_id)
        return reverse('farmadmin:employees')

class EmployeeDeleteAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, DeleteView):
    template_name = 'fa_employee.html'
    model = Employee
    permission_required = ('db.delete_employee',)

    def get_success_url(self):
        clear_cache(self.org_id)
        return reverse('farmadmin:success')

# Загрузка полной таблицы со всеми учреждениями
class AjaxLpuAllDatatableView(BaseDatatableView):
    order_columns = ['name','inn']
    columns = ['cust_id','inn','name','regnm']

    def get_initial_queryset(self):
        employee_id = int(self.request.POST.get('employee', '0'))
        return Lpu.objects.filter(regcode__employee=employee_id).annotate(regnm=F('regcode__regnm')).order_by('name', 'inn')

    def paging(self, qs):
        """ Не используем пакинацию, а возвращаем весь датасет """
        return qs

#
# Администрирование РЫНКОВ
#

class MarketAdminForm(forms.ModelForm):
    class Meta(object):
        model = Market
        fields = ['id', 'org', 'name', 'innrs', 'tmnrs']

class MarketsAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_markets.html'
    breadcrumbs = [{'name': 'Рынки', 'url': ''}]
    permission_required = ('db.view_market', )

    def get_queryset(self):
        return Market.objects.filter(org=self.org).prefetch_related('market_innrs_set__innr','market_tmnrs_set__tradenr')

class MarketUpdateAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, UpdateView):
    """ TODO: Здесь в дальнейшем при сохранении нужно сделать проверку что добавляемые МНН и ТМ не были добавлены кем-нибудь еще, в течение времени когда выполнялась работа по изменению набора МНН и ТМ в браузере
    """
    template_name = 'fa_market.html'
    breadcrumbs = [{'name': 'Рынки', 'url': reverse_lazy('farmadmin:markets')}]
    # form_class = MarketAdminForm
    model = Market
    fields = ['id', 'org', 'name', 'innrs', 'tmnrs']
    permission_required = ('db.change_market', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ИСключаем все INN и ТМ уже привязанные к рынкам текущей организации
        context['innrs'] = InNR.objects.exclude(market__org=self.org).exclude(id=54656).order_by('name')   #
        context['tmnrs'] = TradeNR.objects.exclude(market__org=self.org).order_by('name')
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST:
                status = 'success'
                id = int(request.POST.get('id', 0))
                org = int(request.POST.get('org', 0))
                name = request.POST.get('name', '')
                innrs = json.loads(request.POST.get('innrs', ''))
                tmnrs = json.loads(request.POST.get('tmnrs', ''))
                try:
                    mrkt = Market.objects.get(id=id)
                except:
                    mrkt = None
                    status = 'failed'

                if mrkt:
                    mrkt.org_id = org
                    mrkt.name = name
                    mrkt.save()
                    Market_Innrs.objects.filter(market=mrkt).delete()
                    Market_Innrs.objects.bulk_create(
                        [Market_Innrs(market_id=id, innr_id=int(e['id']), own=e['own']) for e in innrs])
                    Market_Tmnrs.objects.filter(market=mrkt).delete()
                    Market_Tmnrs.objects.bulk_create(
                        [Market_Tmnrs(market_id=id, tradenr_id=int(e['id']), own=e['own']) for e in tmnrs])

                return JsonResponse({'status':status})

        return super().post(request, *args, **kwargs)


class MarketCreateAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, CreateView):
    template_name = 'fa_market.html'
    breadcrumbs = [{'name': 'Рынки', 'url': reverse_lazy('farmadmin:markets')},
                   {'name': 'Новый рынок', 'url': ''}]
    model = Market
    fields = ['org', 'name', 'innrs', 'tmnrs']
    permission_required = ('db.add_market',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ИСключаем все INN и ТМ уже привязанные к рынкам текущей организации
        context['innrs'] = InNR.objects.exclude(market__org=self.org).exclude(id=54656).order_by('name')
        context['tmnrs'] = TradeNR.objects.exclude(market__org=self.org).order_by('name')
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST:
                status = 'success'
                org = int(request.POST.get('org', 0))
                name = request.POST.get('name', '')
                innrs = json.loads(request.POST.get('innrs', ''))
                tmnrs = json.loads(request.POST.get('tmnrs', ''))

                id = Market.objects.create(org_id = org, name = name).id
                Market_Innrs.objects.bulk_create(
                    [Market_Innrs(market_id=id, innr_id=int(e['id']), own=e['own']) for e in innrs])
                Market_Tmnrs.objects.bulk_create(
                    [Market_Tmnrs(market_id=id, tradenr_id=int(e['id']), own=e['own']) for e in tmnrs])

                return JsonResponse({'status':status})

        return super().post(request, *args, **kwargs)

class MarketDeleteAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, DeleteView):
    template_name = 'fa_market.html'
    model = Market
    permission_required = ('db.delete_market',)

    def get_success_url(self):
        return reverse('farmadmin:success')


#
# Администрирование ОРГАНИЗАЦИЙ
#
class OrgsAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, ListView):
    template_name = 'fa_orgs.html'
    breadcrumbs = [{'name': 'Организации', 'url': ''}]
    supressorg = True
    permission_required = ('db.view_org', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sync_status_choices'] = dict(SYNC_STATUS_CHOICES)
        return context

    def get_queryset(self):
        return Org.objects.all().prefetch_related('users')

class OrgUpdateAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, UpdateView):
    """ TODO: Нужно добавить проверку, того, что при отвязке какого-либо пользователя от организации проверять не привязан ли он к сотруднику этой организации, если так, то сначала предлагать выполнить отвязку от сотрудника
    """
    template_name = 'fa_org.html'
    breadcrumbs = [{'name': 'Организации', 'url': reverse_lazy('farmadmin:orgs')}]
    supressorg = True
    model = Org
    fields = ['id', 'name', 'sync_time', 'sync_flag', 'sync_status', 'users']
    permission_required = ('db.change_org', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        context['users'] = User.objects.filter(org__isnull=True).order_by('username')
        context['sync_status_choices'] = SYNC_STATUS_CHOICES
        context['log'] = Org_log.objects.filter(org_id=object.id).order_by('-time')
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')


class OrgCreateAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, CreateView):
    template_name = 'fa_org.html'
    breadcrumbs = [{'name': 'Организации', 'url': reverse_lazy('farmadmin:orgs')},
                   {'name': 'Новая организация', 'url': ''}]
    supressorg = True
    model = Org
    fields = ['name', 'sync_time', 'sync_flag', 'sync_status', 'users']
    permission_required = ('db.add_org',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(org__isnull=True).order_by('username')
        context['sync_status_choices'] = SYNC_STATUS_CHOICES
        return context

    def get_success_url(self):
        return reverse('farmadmin:success')

class OrgDeleteAdminView(PermissionRequiredMixin, OrgAdminMixin, BreadCrumbMixin, DeleteView):
    template_name = 'fa_org.html'
    model = Org
    permission_required = ('db.delete_org',)

    def get_success_url(self):
        return reverse('farmadmin:success')