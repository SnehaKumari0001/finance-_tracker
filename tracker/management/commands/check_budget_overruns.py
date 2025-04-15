# tracker/management/commands/check_budget_overruns.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from tracker.models import Budget, Transaction
from django.db.models import Sum
import datetime

class Command(BaseCommand):
    help = "Check budget overruns and notify users via email."

    def handle(self, *args, **kwargs):
        today = datetime.date.today()
        for budget in Budget.objects.all():
            total_expense = Transaction.objects.filter(
                user=budget.user,
                transaction_type='expense',
                expense_category=budget.expense_category,
                date__year=today.year,
                date__month=today.month
            ).aggregate(total=Sum('amount'))['total'] or 0

            if total_expense > budget.monthly_limit:
                subject = "Budget Overrun Alert"
                message = (
                    f"Hi {budget.user.username},\n\n"
                    f"You have exceeded your budget for {budget.expense_category.name}. "
                    f"Your current expenses: ${total_expense} exceed your monthly limit of ${budget.monthly_limit}."
                )
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [budget.user.email])
                self.stdout.write(self.style.SUCCESS(
                    f"Email sent to {budget.user.email} for {budget.expense_category.name} overrun."
                ))
