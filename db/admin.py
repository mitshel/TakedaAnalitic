from django.contrib import admin
from db.models import Org, Employee, Market, InNR, TradeNR

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

class Employee_admin(admin.ModelAdmin):
    list_filter = ['org__name']
    list_display = ('name', 'parent', 'org', 'istarget', 'logons')
    fields = ('name','parent','org', 'istarget', 'users')
    readonly_fields = ('logons', )
    filter_horizontal = ('users',)
    search_fields = ['name',]

    #def queryset(self, request):
    #    qs = super(Employee_admin, self).queryset(request)
    #    if request.user.is_superuser:
    #        return qs
    #    enabled_org = Org.objects.filter(employee__users=request.user)
    #    return qs.filter(org__in=enabled_org)

    def logons(self, obj):
        return ','.join([l.username for l in obj.users.all()])

class Market_admin(admin.ModelAdmin):
    list_filter = ['org__name']
    list_display = ('name','org')
    fields = ('name', 'org', 'innrs','tmnrs')
    filter_horizontal = ('innrs','tmnrs',)


admin.site.register(Org, Org_admin)
admin.site.register(Employee, Employee_admin)
admin.site.register(Market, Market_admin)

admin.site.site_header = 'Администрирование FarmAnalitic'
admin.site.site_title = 'Раздел администратора FarmAnalitic'