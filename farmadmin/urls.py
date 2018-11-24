
from django.urls import path

from bi_auth.views import bi_login
from farmadmin import views


urlpatterns = [
    path('employee/', bi_login(views.EmployeeAdminView.as_view()), name='employee'),
    path('market/', bi_login(views.MarketAdminView.as_view()), name='market'),
]
