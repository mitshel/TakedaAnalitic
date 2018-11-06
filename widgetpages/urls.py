from django.contrib import admin
from django.urls import path
from widgetpages import views

urlpatterns = [
    path('salesshedule/', views.SalessheduleView.as_view(), name='salesshedule'),
    path('competitions/', views.CompetitionsView.as_view(), name='competitions'),
]
