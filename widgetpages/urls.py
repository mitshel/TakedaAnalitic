from django.contrib import admin
from django.urls import path

from bi_auth.views import bi_login
from widgetpages import views
from widgetpages import table_filters
from widgetpages import table_competitions

urlpatterns = [
    path('jdata/datatable/<str:flt_id>/', bi_login(table_filters.FilterListJson.as_view()), name='jdata'),
    path('salesshedule/', bi_login(views.SalessheduleView.as_view()), name='salesshedule'),
    path('competitions/', bi_login(views.CompetitionsView.as_view()), name='competitions'),
    path('jcompetitions/datatable/', bi_login(table_competitions.CompetitionsAjaxTable.as_view()), name='jcompetitions'),
]
