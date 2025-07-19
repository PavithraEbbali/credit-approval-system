from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def load_customer_data():
    df = pd.read_excel('/app/data/customer_data.xlsx')
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['Customer ID'],
            defaults={
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'phone_number': row['Phone Number'],
                'monthly_salary': row['Monthly Salary'],
                'approved_limit': row['Approved Limit'],
                'current_debt': 0.0,
                'age': row['Age']
            }
        )

@shared_task
def load_loan_data():
    df = pd.read_excel('/app/data/loan_data.xlsx')
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['Customer ID'])
            Loan.objects.update_or_create(
                loan_id=row['Loan ID'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_payment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'start_date': pd.to_datetime(row['Date of Approval']).date(),
                    'end_date': pd.to_datetime(row['End Date']).date(),
                }
            )
        except Customer.DoesNotExist:
            continue
from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def load_customer_data():
    df = pd.read_excel('/app/data/customer_data.xlsx')
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['Customer ID'],
            defaults={
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'phone_number': row['Phone Number'],
                'monthly_salary': row['Monthly Salary'],
                'approved_limit': row['Approved Limit'],
                'current_debt': 0.0,
                'age': row['Age']
            }
        )

@shared_task
def load_loan_data():
    df = pd.read_excel('/app/data/loan_data.xlsx')
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['Customer ID'])
            Loan.objects.update_or_create(
                loan_id=row['Loan ID'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_payment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'start_date': pd.to_datetime(row['Date of Approval']).date(),
                    'end_date': pd.to_datetime(row['End Date']).date(),
                }
            )
        except Customer.DoesNotExist:
            continue
