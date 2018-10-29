from django.core.management.base import BaseCommand
from db.models import Employee, Target

class Command(BaseCommand):
    help = 'Load Employees Data'

    def handle(self, *args, **options):
        # Employee.objects.all().delete()
        # emp_list = Target.objects.values('employee_name').distinct().order_by('employee_name')
        # Employee.objects.bulk_create([Employee(name=i['employee_name'],) for i in emp_list])
        # Target.employee.through.objects.all().delete()
        # target_list = Target.objects.exclude(employee_name__isnull=True)
        # for t in target_list:
        #     emp = Employee.objects.filter(name=t.employee_name)
        #     if emp:
        #         t.employee.add(emp[0])
        pass