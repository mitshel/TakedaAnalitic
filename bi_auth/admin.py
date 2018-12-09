from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
from db.models import Org
from django.db.models import Q, F

# Register your models here.
class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'

# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_orgadmin', 'org_names')
    inlines = (UserInline,)

    def is_orgadmin(self, obj):
        result = False
        try:
            result = UserProfile.objects.get(user=obj).is_orgadmin
            #result = obj.user_profile.is_orgadmin
        except:
            pass
        return result

    def org_names(self, obj):
        return ','.join([o.name for o in obj.org_set.all()])

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)