from django.contrib import admin
from django.urls import path
from loans.views import drinks, LoanFund, users, loan
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drinks/', drinks.drink_list),
    path('drinks/<int:id>', drinks.drink_detail),

    #FUNDS URLS
    path('loanFund/', LoanFund.loanfund_list),
    path('loanFund/<int:pk>', LoanFund.loanfund_detail),

    #USER URLS
    path('user/', users.user_list_create_view),
    path('user/<int:pk>', users.user_detail_view),
    path('user/login/', users.user_login),

    #LOANS URL
    path('loan/', loan.loan_list_create_view),
    path('loan/approve/<int:loan_id>', loan.approve_loan),
    path('loan/reject/<int:loan_id>', loan.reject_loan),
]