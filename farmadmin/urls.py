
from django.urls import path

from bi_auth.views import bi_login
from farmadmin import views


urlpatterns = [
    path('employees/', bi_login(views.EmployeesAdminView.as_view()), name='employees'),
    path('employee/<int:pk>/$', bi_login(views.EmployeeAdminView.as_view()), name='employee'),
    path('market/', bi_login(views.MarketsAdminView.as_view()), name='markets'),
]
