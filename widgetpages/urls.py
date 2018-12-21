from django.contrib import admin
from django.urls import path

from bi_auth.views import bi_login
from widgetpages import views
from widgetpages import table_filters

urlpatterns = [
    path('jdata/datatable/<str:flt_id>/', bi_login(table_filters.FilterListJson.as_view()), name='jdata'),
    path('salesshedule/', bi_login(views.SalessheduleView.as_view()), name='salesshedule'),
    path('competitions/lpu/', bi_login(views.CompetitionsLpuView.as_view()), name='competitions_lpu'),
    path('competitions/market/', bi_login(views.CompetitionsMarketView.as_view()), name='competitions_market'),
    path('jcompetitions_lpu/datatable/', bi_login(views.Lpu_CompetitionsAjaxTable.as_view()), name='jcompetitions_lpu'),
    path('jcompetitions_market/datatable/', bi_login(views.Market_CompetitionsAjaxTable.as_view()), name='jcompetitions_market'),
    path('parts/', bi_login(views.PartsView.as_view()), name='parts'),
    path('jparts/datatable1/', bi_login(views.MPartsAjaxTable.as_view()), name='jmparts'),
    path('jparts/datatable2/', bi_login(views.LPartsAjaxTable.as_view()), name='jlparts'),
]
