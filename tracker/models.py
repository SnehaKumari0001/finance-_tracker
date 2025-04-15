from django.db import models
from django.contrib.auth.models import User

TRANSACTION_TYPES = (
    ('income', 'Income'),
    ('expense', 'Expense'),
)

class IncomeSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_sources')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    # Optional receipt upload for expense transactions.
    # Files will be stored in the 'receipts/' folder under your MEDIA_ROOT.
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    # Linking to an income source or an expense category.
    income_source = models.ForeignKey(IncomeSource, on_delete=models.SET_NULL, null=True, blank=True)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.expense_category.name} Budget"
