from django.contrib import admin

from import_export import resources, widgets, fields
from import_export.admin import ImportExportModelAdmin
from db.models import Target, Hs

class TargetResource(resources.ModelResource):
    delete = fields.Field(widget=widgets.BooleanWidget())

    def for_delete(self, row, instance):
        return self.fields['delete'].clean(row)

    class Meta:
        model = Target
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('inn',)
        fields = ('inn', 'entity', 'employee',)

class Target_admin(ImportExportModelAdmin):
    resource_class = TargetResource


class HsResource(resources.ModelResource):

    class Meta:
        model = Hs
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('hs_id',)

class Target_admin(ImportExportModelAdmin):
    resource_class = TargetResource

class Hs_admin(ImportExportModelAdmin):
    resource_class = HsResource

admin.site.register(Target, Target_admin)
admin.site.register(Hs, Hs_admin)