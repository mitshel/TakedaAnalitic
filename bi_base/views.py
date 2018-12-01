from django.shortcuts import render
from django.conf import settings

# Create your views here.
def bi_processor(request):
    args={}
    args['bi_auth'] = settings.BI_AUTH
    args['BI_MAX_EMPLOYEE_LPU']=settings.BI_MAX_EMPLOYEE_LPU
    return args
