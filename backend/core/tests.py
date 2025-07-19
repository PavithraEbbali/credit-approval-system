from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer, Loan

class CreditSystemTests(APITestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            phone_number="9999999999",
            age=30,
            monthly_salary=50000,
            approved_limit=150000,
            current_debt=0,
        )

    def test_register_customer(self):
        url = reverse('register-customer')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "phone_number": 1234567890,
            "monthly_income": 50000,
            "approved_limit": 100000
        }
        response = self.client.post(url, data, format='json')
        print("REGISTER RESPONSE:", response.data)  # 👈 this is what we need to debug it
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_check_eligibility(self):
        url = reverse('check-eligibility')
        data = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 100000,
            "interest_rate": 10,
            "tenure": 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("approval", response.data)

    def test_create_loan(self):
        url = reverse('create-loan')
        data = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 50000,
            "interest_rate": 10,
            "tenure": 12,
            "monthly_payment": 4395.79
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)

    def test_get_customer_loans(self):
        loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=50000,
            interest_rate=10,
            tenure=12,
            monthly_payment=4395.79,
            emis_paid_on_time=0,
            start_date="2025-07-01",
            end_date="2026-07-01"
        )
        url = reverse('view-loans')
        response = self.client.get(url, {'customer_id': self.customer.customer_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["loans"]), 1)

    def test_make_payment(self):
        loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=50000,
            interest_rate=10,
            tenure=12,
            monthly_payment=4395.79,
            emis_paid_on_time=0,
            start_date="2025-07-01",
            end_date="2026-07-01"
        )
        url = reverse('make-payment')
        data = {
            "customer_id": self.customer.customer_id,
            "loan_id": loan.loan_id,
            "amount": 5000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        loan.refresh_from_db()
        self.assertEqual(loan.emis_paid_on_time, 1)
