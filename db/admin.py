from django.contrib import admin
from db.models import Org, Employee, Market

class Org_admin(admin.ModelAdmin):
    list_display = ('name','sync_time')

class Employee_admin(admin.ModelAdmin):
    list_filter = ['org__name']
    list_display = ('name', 'parent', 'org', 'istarget', 'logons')
    fields = ('name','parent','org', 'istarget', 'lpu', 'users')
    readonly_fields = ('logons', )
    filter_horizontal = ('lpu','users',)
    search_fields = ['name',]

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