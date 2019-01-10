
from django.urls import path

from bi_auth.views import bi_login
from farmadmin import views


urlpatterns = [
    path('orgselect/', bi_login(views.OrgView.as_view()), name='orgselect'),
    path('setuporg/', bi_login(views.SetupOrgView.as_view()), name='setuporg'),

    path('employees/', bi_login(views.EmployeesAdminView.as_view()), name='employees'),
    #path('employee/<int:pk>/', bi_login(views.EmployeeUpdateAdminView.as_view()), name='employee'),
    path('employee/', bi_login(views.EmployeeCreateBaseAdminView.as_view()), name='employee_base'),
    path('employee/<int:pk>/', bi_login(views.EmployeeUpdateBaseAdminView.as_view()), name='employee_base'),
    path('employee/lpu/<int:pk>/', bi_login(views.EmployeeUpdateLpuAdminView.as_view()), name='employee_lpu'),
    path('employee/user/<int:pk>/', bi_login(views.EmployeeUpdateUserAdminView.as_view()), name='employee_user'),
    path('employee/rm/<int:pk>/', bi_login(views.EmployeeDeleteAdminView.as_view()), name='employee_rm'),

    path('markets/', bi_login(views.MarketsAdminView.as_view()), name='markets'),
    path('market/<int:pk>/', bi_login(views.MarketUpdateAdminView.as_view()), name='market'),
    path('market/rm/<int:pk>/', bi_login(views.MarketDeleteAdminView.as_view()), name='market_rm'),
    path('market/', bi_login(views.MarketCreateAdminView.as_view()), name='market'),

    path('orgs/', bi_login(views.OrgsAdminView.as_view()), name='orgs'),
    path('org/<int:pk>/', bi_login(views.OrgUpdateAdminView.as_view()), name='org'),
    path('org/rm/<int:pk>/', bi_login(views.OrgDeleteAdminView.as_view()), name='org_rm'),
    path('org/', bi_login(views.OrgCreateAdminView.as_view()), name='org'),

    path('jlpuall/datatable/', bi_login(views.AjaxLpuAllDatatableView.as_view()), name='jlpuall'),
    path('success/', views.SuccessView.as_view(), name='success'),
]
