# tracker/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm, BudgetForm, SignUpForm
from .models import Transaction, Budget, ExpenseCategory, IncomeSource
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.db.models import Sum
import datetime

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after signup
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    # Get totals for income and expenses
    total_income = Transaction.objects.filter(user=user, transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = Transaction.objects.filter(user=user, transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
    savings = total_income - total_expense

    # Prepare data for monthly report (last 6 months)
    today = datetime.date.today()
    report_data = []
    for i in range(6):
        month = (today.month - i - 1) % 12 + 1
        year = today.year - ((today.month - i - 1) // 12)
        month_income = Transaction.objects.filter(user=user, transaction_type='income', date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        month_expense = Transaction.objects.filter(user=user, transaction_type='expense', date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
        report_data.append({
            'year': year,
            'month': month,
            'income': month_income,
            'expense': month_expense,
        })

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'report_data': report_data,
    }
    return render(request, 'dashboard.html', context)

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added successfully.")
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'tracker/transaction_form.html', {'form': form})

@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully.")
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'tracker/transaction_form.html', {'form': form})

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction deleted.")
        return redirect('transaction_list')
    return render(request, 'tracker/transaction_confirm_delete.html', {'transaction': transaction})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budget set successfully.")
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'tracker/budget_form.html', {'form': form})
