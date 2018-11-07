from django.contrib import admin
from django.urls import path
from widgetpages import views
from widgetpages import datatable

urlpatterns = [
    path('salesshedule/', views.SalessheduleView.as_view(), name='salesshedule'),
    path('competitions/', views.CompetitionsView.as_view(), name='competitions'),
    path('jdata/datatable/<str:flt_id>/', datatable.FilterListJson.as_view(), name='jdata'),
]
