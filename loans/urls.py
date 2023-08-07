from django.contrib import admin
from django.urls import path
from loans.views import drinks
from loans.views import LoanFund
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drinks/', drinks.drink_list),
    path('drinks/<int:id>', drinks.drink_detail),
    path('loanFund/', LoanFund.loanfund_list),
    path('loanFund/<int:pk>', LoanFund.loanfund_detail)
]