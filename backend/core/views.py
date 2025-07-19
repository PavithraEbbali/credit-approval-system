from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Customer, Loan
from .serializers import CustomerRegisterSerializer



class RegisterCustomerView(APIView):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckEligibilityView(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        loan_amount = float(request.data.get("loan_amount"))
        interest_rate = float(request.data.get("interest_rate"))
        tenure = int(request.data.get("tenure"))

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        # 💡 Credit score calculation
        loans = Loan.objects.filter(customer=customer)
        credit_score = 100

        if customer.current_debt > customer.approved_limit:
            credit_score = 0
        else:
            on_time_loan_ratio = 0
            if loans.exists():
                on_time_loan_ratio = sum(l.emis_paid_on_time for l in loans) / (len(loans) * tenure)

            credit_score -= (len(loans) * 2)  # more loans = more risk
            credit_score += min(20, on_time_loan_ratio * 100)

            current_year = datetime.now().year
            current_year_loans = loans.filter(start_date__year=current_year).count()
            credit_score -= current_year_loans * 5

            past_loan_volume = sum(l.loan_amount for l in loans)
            credit_score += min(20, past_loan_volume / 100000)

        # 🧮 Monthly EMI (compound interest)
        r = interest_rate / (12 * 100)
        emi = loan_amount * r * ((1 + r)**tenure) / (((1 + r)**tenure) - 1)
        monthly_salary = customer.monthly_salary

        # ❌ Reject if EMI > 50% of salary
        if emi > (0.5 * monthly_salary):
            return Response({
                "customer_id": customer.customer_id,
                "approval": False,
                "reason": "EMI exceeds 50% of salary"
            })

        # ✅ Decision based on credit_score
        corrected_interest = interest_rate
        approval = False

        if credit_score > 50:
            approval = True
        elif 30 < credit_score <= 50:
            approval = interest_rate >= 12
            corrected_interest = max(interest_rate, 12)
        elif 10 < credit_score <= 30:
            approval = interest_rate >= 16
            corrected_interest = max(interest_rate, 16)
        else:
            approval = False

        return Response({
            "customer_id": customer.customer_id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest,
            "tenure": tenure,
            "monthly_installment": round(emi, 2),
        })




class CreateLoanView(APIView):
    def post(self, request):
        data = request.data
        try:
            customer = Customer.objects.get(customer_id=data["customer_id"])
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        # 📅 Calculate end_date by adding `tenure` months to today
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=30 * int(data["tenure"]))  # approx.

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=data["loan_amount"],
            tenure=data["tenure"],
            interest_rate=data["interest_rate"],
            monthly_payment=data["monthly_payment"],
            emis_paid_on_time=0,
            start_date=start_date,
            end_date=end_date
        )

        customer.current_debt += float(data["loan_amount"])
        customer.save()

        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer.customer_id,
            "message": "Loan created successfully"
        }, status=201)


class ViewLoansView(APIView):
    def get(self, request):
        customer_id = request.query_params.get("customer_id")
        if not customer_id:
            return Response({"error": "customer_id is required"}, status=400)

        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        loans = Loan.objects.filter(customer=customer)
        loan_data = [
            {
                "loan_id": loan.loan_id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "tenure": loan.tenure,
                "monthly_payment": loan.monthly_payment,
                "emis_paid_on_time": loan.emis_paid_on_time,
                "start_date": loan.start_date,
                "end_date": loan.end_date,
            }
            for loan in loans
        ]

        return Response({
            "customer_id": customer.customer_id,
            "loans": loan_data
        })


class ViewCustomerDetailsView(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        loans = Loan.objects.filter(customer=customer)

        # --- Credit score logic (reuse) ---
        credit_score = 100

        if customer.current_debt > customer.approved_limit:
            credit_score = 0
        else:
            on_time_loan_ratio = 0
            if loans.exists():
                on_time_loan_ratio = sum(l.emis_paid_on_time for l in loans) / (len(loans) * max([l.tenure for l in loans]))
            credit_score -= (len(loans) * 2)
            credit_score += min(20, on_time_loan_ratio * 100)

            current_year_loans = loans.filter(start_date__year=datetime.now().year).count()
            credit_score -= current_year_loans * 5

            past_loan_volume = sum(l.loan_amount for l in loans)
            credit_score += min(20, past_loan_volume / 100000)

        data = {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age,
            "monthly_salary": customer.monthly_salary,
            "approved_limit": customer.approved_limit,
            "current_debt": customer.current_debt,
            "credit_score": round(credit_score, 2)
        }
        return Response(data, status=status.HTTP_200_OK)
    

class MakePaymentView(APIView):
    def post(self, request):
        data = request.data
        try:
            loan = Loan.objects.get(loan_id=data["loan_id"], customer__customer_id=data["customer_id"])
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found for this customer"}, status=404)

        amount = data.get("amount")
        if amount is None or amount <= 0:
            return Response({"error": "Invalid amount"}, status=400)

        # Update loan
        if loan.emis_paid_on_time < loan.tenure:
            loan.emis_paid_on_time += 1
            loan.save()

        # Update customer
        customer = loan.customer
        customer.current_debt = max(0, customer.current_debt - amount)
        customer.save()

        return Response({
            "message": "Payment recorded successfully",
            "customer_id": customer.customer_id,
            "loan_id": loan.loan_id,
            "remaining_debt": customer.current_debt,
            "emis_paid": loan.emis_paid_on_time
        }, status=200)
