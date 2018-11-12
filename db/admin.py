from django.contrib import admin
from db.models import Org, Employee
from django.contrib.auth.models import User

class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1

class UserInline(admin.TabularInline):
    model = Employee.users.through
    extra = 1
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

class Org_admin(admin.ModelAdmin):
    list_display = ('name','sync_time')
    inlines = (EmployeeInline, )

class Employee_admin(admin.ModelAdmin):
    list_filter = ['org__name']
    list_display = ('name','parent', 'org')
    exclude = ('users',)
    inlines = (UserInline, )


admin.site.register(Org, Org_admin)
admin.site.register(Employee, Employee_admin)