from django.db import models
from django.conf import settings
from expenses.models import Expense


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=50, choices=Expense.CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'category', 'month', 'year']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.user.email} - {self.category} - {self.month}/{self.year} - ₹{self.amount}"