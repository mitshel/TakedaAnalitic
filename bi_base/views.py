from django.shortcuts import render
from django.conf import settings
from TakedaAnalitic.settings_db import DBINFO
from db.models import DB_VERSION

# Create your views here.
def bi_processor(request):
    args={}
    args['bi_auth'] = settings.BI_AUTH
    args['BI_MAX_EMPLOYEE_LPU']=settings.BI_MAX_EMPLOYEE_LPU
    args['BI_MAX_EMPLOYEE_LOGIN']=settings.BI_MAX_EMPLOYEE_LOGIN
    args['datasource'] = DBINFO
    args['db_version'] = DB_VERSION
    #args.update(csrf(request))
    return args
