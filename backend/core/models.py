from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField(unique=True)
    age = models.IntegerField()
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()
    current_debt = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.FloatField()
    tenure = models.IntegerField()  # in months
    interest_rate = models.FloatField()
    monthly_payment = models.FloatField()
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} - {self.customer.first_name}"
