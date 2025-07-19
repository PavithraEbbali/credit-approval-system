from django.urls import path
from .views import (
    RegisterCustomerView,
    CheckEligibilityView,
    CreateLoanView,
    ViewLoansView,
    ViewCustomerDetailsView,
    MakePaymentView,
)

urlpatterns = [
    path("register", RegisterCustomerView.as_view(), name="register-customer"),
    path("check-eligibility", CheckEligibilityView.as_view(), name="check-eligibility"),
    path("create-loan", CreateLoanView.as_view(), name="create-loan"),
    path("view-loans", ViewLoansView.as_view(), name="view-loans"),
    path("view-customer/<int:customer_id>", ViewCustomerDetailsView.as_view(), name="view-customer"),
    path("make-payment", MakePaymentView.as_view(), name="make-payment"),
]
