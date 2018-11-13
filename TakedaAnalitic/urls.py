"""TakedaAnalitic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings

from bi_auth.views import loginView, logoutView, bi_login
from widgetpages.views import Home

urlpatterns = [
    path('', bi_login(Home), name='home'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('page/', include(('widgetpages.urls', 'widgetpages'), namespace='widgetpages')),
    # path('proto/', include(('protocols.urls', 'protocols'), namespace='protocols')),
    path('admin/', admin.site.urls, name='admin'),
]