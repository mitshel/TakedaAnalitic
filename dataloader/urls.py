from django.contrib import admin
from django.urls import path

from bi_auth.views import bi_login
from dataloader import views

urlpatterns = [
    path('filters/', bi_login(views.FiltersAjaxTable.as_view()), name='filters'),
    path('meta/', bi_login(views.CacheMetaView.as_view()), name='meta'),
    path('fk/<str:fk_name>/', bi_login(views.FkFieldView.as_view()), name='fk'),
    path('fk/<str:fk_name>/<str:search_text>/', bi_login(views.FkFieldView.as_view()), name='fk'),
    path('dl/', bi_login(views.DownloadView.as_view()), name='dl'),
]
