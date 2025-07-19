from rest_framework import serializers
from .models import Customer

class CustomerRegisterSerializer(serializers.ModelSerializer):
    monthly_income = serializers.IntegerField(write_only=True)

    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'age', 'phone_number', 'monthly_income', 'approved_limit']
        read_only_fields = ['customer_id', 'approved_limit']

    def create(self, validated_data):
        salary = validated_data.pop('monthly_income')
        approved_limit = round((36 * salary) / 100000) * 100000  # round to nearest lakh
        return Customer.objects.create(monthly_salary=salary, approved_limit=approved_limit, **validated_data)
