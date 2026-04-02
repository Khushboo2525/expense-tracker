from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'category', 'amount', 'month', 'year', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']