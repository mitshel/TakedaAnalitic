from django.contrib import admin
from django.urls import path
from widgetpages import views

urlpatterns = [
    #path('salesshedule/', views.sales_shedule, name='salesshedule'),
    path('salesshedule/', views.SalessheduleView.as_view(), name='salesshedule'),
    path('fltrsupd/', views.filters_update, name='fltrsupd'),
    path('f_emplsupd/', views.filters_employee, name='f_emplsupd'),
    path('competitions/', views.CompetitionsView.as_view(), name='competitions'),
    #path('competitions/', views.competitions, name='competitions'),
]
