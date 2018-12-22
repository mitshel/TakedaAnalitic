from django.shortcuts import render
from django.conf import settings
from TakedaAnalitic.settings_db import DBHOST

# Create your views here.
def bi_processor(request):
    args={}
    args['bi_auth'] = settings.BI_AUTH
    args['BI_MAX_EMPLOYEE_LPU']=settings.BI_MAX_EMPLOYEE_LPU
    args['BI_MAX_EMPLOYEE_LOGIN']=settings.BI_MAX_EMPLOYEE_LOGIN
    args['datasource'] = DBHOST
    #args.update(csrf(request))
    return args
