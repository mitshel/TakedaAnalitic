from django.contrib import admin
from django.urls import path

from bi_auth.views import bi_login
from widgetpages import views
from widgetpages import table_filters

urlpatterns = [
    path('jdata/datatable/', bi_login(table_filters.FilterListJson.as_view()), name='jdata'),
    path('jdata/passport/', bi_login(table_filters.PassportFilterListJson.as_view()), name='jdata_passport'),
    path('salesshedule/', bi_login(views.SalessheduleView.as_view()), name='salesshedule'),
    path('competitions/lpu/', bi_login(views.CompetitionsLpuView.as_view()), name='competitions_lpu'),
    path('competitions/market/', bi_login(views.CompetitionsMarketView.as_view()), name='competitions_market'),
    path('jcompetitions_lpu/datatable/', bi_login(views.Lpu_CompetitionsAjaxTable.as_view()), name='jcompetitions_lpu'),
    path('jcompetitions_market/datatable/', bi_login(views.Market_CompetitionsAjaxTable.as_view()), name='jcompetitions_market'),
    path('avg/market/', bi_login(views.AvgMarketView.as_view()), name='avg_price'),
    path('javg_market/datatable/', bi_login(views.AvgAjaxTable.as_view()),name='javg_price'),
    path('pkgs/market/', bi_login(views.PackagesView.as_view()), name='packages'),
    path('jpkgs/datatable/', bi_login(views.PackagesAjaxTable.as_view()), name='jpackages'),
    path('parts/', bi_login(views.PartsView.as_view()), name='parts'),
    path('jparts/datatable1/', bi_login(views.MPartsAjaxTable.as_view()), name='jmparts'),
    path('jparts/datatable2/', bi_login(views.LPartsAjaxTable.as_view()), name='jlparts'),
    path('sales_analysis/', bi_login(views.SalesAnlysisView.as_view()), name='sales_analysis'),
    path('jsales_analysis/datatable/', bi_login(views.SalesAnlysisAjaxTable.as_view()), name='jsales_analysis'),
    path('budgets/', bi_login(views.BudgetsView.as_view()), name='budgets'),
    path('budgets/datatable/', bi_login(views.BudgetsAjaxTable.as_view()), name='budgets_table'),
    path('passport/', bi_login(views.PassportView.as_view()), name='passport'),
    path('passport/datatable/winners/', bi_login(views.PassportWinnersAjaxTable.as_view()), name='passport_winners_table'),
]
