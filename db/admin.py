from django.contrib import admin
from db.models import Org, Employee
from django.contrib.auth.models import User

class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1

class UserInline(admin.TabularInline):
    model = Employee
    extra = 1

class Org_admin(admin.ModelAdmin):
    list_display = ('name','sync_time')
    inlines = (EmployeeInline, )

class Employee_admin(admin.ModelAdmin):
    list_display = ('name','parent')
    inlines = (EmployeeInline, UserInline, )


admin.site.register(Org, Org_admin)
admin.site.register(Employee, Employee_admin)