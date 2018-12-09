
from django.urls import path

from bi_auth.views import bi_login
from farmadmin import views


urlpatterns = [
    path('org/', bi_login(views.OrgView.as_view()), name='org'),
    path('setuporg/', bi_login(views.SetupOrgView.as_view()), name='setuporg'),

    path('employees/', bi_login(views.EmployeesAdminView.as_view()), name='employees'),
    path('employee/<int:pk>/', bi_login(views.EmployeeUpdateAdminView.as_view()), name='employee'),
    path('employee/rm/<int:pk>/', bi_login(views.EmployeeDeleteAdminView.as_view()), name='employee_rm'),
    path('employee/', bi_login(views.EmployeeCreateAdminView.as_view()), name='employee'),

    path('markets/', bi_login(views.MarketsAdminView.as_view()), name='markets'),
    path('market/<int:pk>/', bi_login(views.MarketUpdateAdminView.as_view()), name='market'),
    path('market/rm/<int:pk>/', bi_login(views.MarketDeleteAdminView.as_view()), name='market_rm'),
    path('market/', bi_login(views.MarketCreateAdminView.as_view()), name='market'),

    path('jlpuall/datatable/', bi_login(views.AjaxLpuAllDatatableView.as_view()), name='jlpuall'),
    path('success/', views.SuccessView.as_view(), name='success'),
]
