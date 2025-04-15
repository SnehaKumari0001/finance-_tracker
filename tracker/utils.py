# tracker/utils.py
from django.core.mail import send_mail
from django.conf import settings
from .models import Budget, Transaction
from django.db.models import Sum
import datetime

def check_budget_overruns():
    today = datetime.date.today()
    for budget in Budget.objects.all():
        # Sum expenses for the given category for the current month
        total_expense = Transaction.objects.filter(
            user=budget.user,
            transaction_type='expense',
            expense_category=budget.expense_category,
            date__year=today.year,
            date__month=today.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if total_expense > budget.monthly_limit:
            subject = "Budget Overrun Alert"
            message = f"Hi {budget.user.username},\n\nYou have exceeded your budget for {budget.expense_category.name}."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [budget.user.email])
