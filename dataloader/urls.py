from django.contrib import admin
from django.urls import path

from bi_auth.views import bi_login
from dataloader import views

urlpatterns = [
    path('meta/', bi_login(views.CacheMetaView.as_view()), name='meta'),
]
