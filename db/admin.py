from django.contrib import admin
from db.models import Org, Employee
from django.contrib.auth.models import User

class UserInline(admin.StackedInline):
    model = Employee.users.through
    extra = 1
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

class EmployeeInline(admin.TabularInline):
    list_display = ('name', 'parent', 'org')
    model = Employee
    exclude = ['users',]
    extra = 1

class Org_admin(admin.ModelAdmin):
    list_display = ('name','sync_time')
    def queryset(self, request):
        qs = super(Org_admin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        enabled_org = Org.objects.filter(employee__users=request.user)
        return qs.filter(org__in=enabled_org)

class Employee_admin(admin.ModelAdmin):
    list_filter = ['org__name']
    list_display = ('name', 'parent', 'org', 'logons')
    fields = ('name','parent','org')
    readonly_fields = ('logons', )
    exclude = ('users',)
    inlines = (UserInline, )
    search_fields = ['name',]

    def queryset(self, request):
        qs = super(Employee_admin, self).queryset(request)
        print(request)
        if request.user.is_superuser:
            return qs
        enabled_org = Org.objects.filter(employee__users=request.user)
        return qs.filter(org__in=enabled_org)

    def logons(self, obj):
        return ','.join([l.username for l in obj.users.all()])

admin.site.register(Org, Org_admin)
admin.site.register(Employee, Employee_admin)

admin.site.site_header = 'Администрирование FarmAnalitic'
admin.site.site_title = 'Раздел администратора FarmAnalitic'