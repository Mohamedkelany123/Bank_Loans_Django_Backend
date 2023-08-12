from django.contrib import admin
from django.urls import path
from loans.views import LoanFund, users, loan

urlpatterns = [
    path('admin/', admin.site.urls),

    #FUNDS URLS
    path('loanFund/', LoanFund.loanfund_list, name="loanfund_list"),
    path('loanFund/<int:pk>', LoanFund.loanfund_detail, name="loanfund_detail"),

    #USER URLS
    path('user/', users.user_list_create_view, name="user_list_create_view"),
    path('user/<int:pk>', users.user_detail_view, name="user_detail_view"),
    path('user/login/', users.user_login, name = "user_login"),

    #LOANS URL
    path('loan/', loan.loan_list_create_view, name="loan_list_create_view"),
    path('loan/approve/<int:loan_id>', loan.approve_loan, name = "approve_loan" ),
    path('loan/reject/<int:loan_id>', loan.reject_loan, name = "reject_loan"),
    path('loan/delete/<int:loan_id>', loan.deleteLoan, name="deleteLoan"),
    path('loan/<str:username>/', loan.get_loans_by_username, name = "get_loans_by_username"),

]