from django.contrib import admin
from django.urls import path

from bi_auth.views import bi_login
from widgetpages import views
from widgetpages import table_filters
from widgetpages import table_competitions

urlpatterns = [
    path('jdata/datatable/<str:flt_id>/', bi_login(table_filters.FilterListJson.as_view()), name='jdata'),
    path('salesshedule/', bi_login(views.SalessheduleView.as_view()), name='salesshedule'),
    path('competitions/lpu/', bi_login(views.CompetitionsLpuView.as_view()), name='competitions_lpu'),
    path('competitions/market/', bi_login(views.CompetitionsMarketView.as_view()), name='competitions_market'),
    path('jcompetitions/datatable/', bi_login(table_competitions.CompetitionsAjaxTable.as_view()), name='jcompetitions'),
]
