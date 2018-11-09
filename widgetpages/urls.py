from django.contrib import admin
from django.urls import path
from widgetpages import views
from widgetpages import table_filters
from widgetpages import table_competitions

urlpatterns = [
    path('jdata/datatable/<str:flt_id>/', table_filters.FilterListJson.as_view(), name='jdata'),
    path('salesshedule/', views.SalessheduleView.as_view(), name='salesshedule'),
    path('competitions/', views.CompetitionsView.as_view(), name='competitions'),
    path('jcompetitions/datatable/', table_competitions.CompetitionsAjaxTable.as_view(), name='jcompetitions'),
]
