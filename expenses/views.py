from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Budget, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from decimal import Decimal 
import calendar
from datetime import datetime
from django.db.models import Value


@login_required
def index(request):
    return redirect('expenses:dashboard')

@login_required
def dashboard(request):
    # Get the current month and year dynamically
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Create a datetime object for the first day of the current month
    current_month_date = datetime(current_year, current_month, 1)

    # Get all transactions for the current month
    transactions = Transaction.objects.filter(
        user=request.user,
        date__year=current_year,
        date__month=current_month
    )

    # Get the last three transactions for the user, ordered by the latest date
    last_three_transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:3]

    # Calculate incoming and outgoing amounts for the Cash Flow card
    cashflow = transactions.aggregate(
        incoming=Sum('amount', filter=Q(transaction_type='Income')) or 0,
        outgoing=Sum('amount', filter=Q(transaction_type='Expense')) or 0
    )

    # Create a dictionary to store days with transactions
    transaction_days = {}
    for transaction in transactions:
        if transaction.date:  # Ensure the transaction has a valid date
            day = transaction.date.day
            if day not in transaction_days:
                transaction_days[day] = []
            transaction_days[day].append(transaction)

    # Generate the calendar for the current month
    cal = calendar.Calendar(firstweekday=6)  # 6 = Sunday
    month_days = cal.itermonthdays2(current_year, current_month)  # (day, weekday)

    context = {
        'username': request.user.username,
        'current_month_date': current_month_date,  # Pass the datetime object
        'current_year': current_year,
        'month_days': month_days,
        'transaction_days': transaction_days,
        'last_three_transactions': last_three_transactions,
        'cashflow': cashflow,
    }
    return render(request, 'expenses/dashboard.html', context)

# @login_required
# def dashboard(request):
#     transactions = Transaction.objects.filter(user=request.user)
#     return render(request, 'expenses/dashboard.html', {
#         'transactions': transactions,
#         'username': request.user.username,  # Pass the username to the template
#     })


@login_required
def all_transactions(request):
    # Fetch all transactions for the user, ordered by the latest date
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'transactions': transactions,
    }
    return render(request, 'expenses/all_transactions.html', context)


# @login_required
# def add_transaction(request):
#     if request.method == 'POST':
#         category = request.POST['category']
#         transaction_type = request.POST['transaction_type']
#         amount = float(request.POST['amount'])

#         # Check if the transaction is an expense and exceeds the budget
#         if transaction_type == 'Expense':
#             budget = Budget.objects.filter(user=request.user, category=category).first()
#             if budget:
#                 total_expenses = Transaction.objects.filter(
#                     user=request.user, category=category, transaction_type='Expense'
#                 ).aggregate(Sum('amount'))['amount__sum'] or 0
#                 if total_expenses + amount > budget.amount:
#                     return render(request, 'expenses/add_transaction.html', {
#                         'categories': Category.objects.all(),
#                         'error': f"Transaction exceeds the budget for {category}."
#                     })

#         # Save the transaction
#         transaction = Transaction(
#             user=request.user,
#             category=category,
#             transaction_type=transaction_type,
#             amount=amount,
#             date=request.POST['date'],
#             description=request.POST.get('description', ''),
#         )
#         transaction.save()
#         return redirect('expenses:dashboard')

#     categories = Category.objects.all()
#     return render(request, 'expenses/add_transaction.html', {'categories': categories})



from decimal import Decimal  # Import Decimal

@login_required
def add_transaction(request):
    if request.method == 'POST':
        category_name = request.POST['category']
        transaction_type = request.POST['transaction_type']
        amount = Decimal(request.POST['amount'])  # Convert amount to Decimal

        # Check if the transaction is an expense and exceeds the budget
        if transaction_type == 'Expense':
            budget = Budget.objects.filter(user=request.user, category__name=category_name).first()
            if budget:
                total_expenses = Transaction.objects.filter(
                    user=request.user, category=category_name, transaction_type='Expense'
                ).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
                if total_expenses + amount > budget.amount:
                    return redirect('expenses:view_budget')  # Redirect with an error message

        # Save the transaction
        transaction = Transaction(
            user=request.user,
            category=category_name,
            transaction_type=transaction_type,
            amount=amount,
            description=request.POST.get('description', ''),
        )
        transaction.save()
        return redirect('expenses:view_budget')

    # Fetch categories from the Budget model
    categories = Budget.objects.filter(user=request.user).values_list('category__name', flat=True)
    return render(request, 'expenses/add_transaction.html', {'categories': categories})

from django.shortcuts import get_object_or_404, redirect

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    transaction.delete()
    return redirect('expenses:transactions')  # Redirect to 'transactions'



@login_required
def add_expense(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        transaction_type = request.POST.get('transaction_type', 'Expense')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')

        Transaction.objects.create(
            user=request.user,
            category=category,
            transaction_type=transaction_type,
            amount=amount,
            date=date,
            description=description
        )
        return redirect('expenses:dashboard')  # Redirect back to dashboard

    return render(request, 'expenses/add_transaction.html')


@login_required
def view_budget(request):
    budgets = Budget.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user, transaction_type='Expense')

    # Calculate total expenses for each budget category
    budget_summary = []
    for budget in budgets:
        total_expenses = transactions.filter(category=budget.category.name).aggregate(Sum('amount'))['amount__sum'] or 0
        remaining_budget = budget.amount - total_expenses
        budget_summary.append({
            'id': budget.id,
            'category': budget.category.name,
            'total_budget': budget.amount,
            'total_expenses': total_expenses,
            'remaining_budget': remaining_budget,
        })

    if request.method == 'POST':
        category_name = request.POST.get('category')
        budget_id = request.POST.get('budget_id')
        amount = request.POST.get('amount')

        if budget_id:  # Update existing budget
            try:
                budget = Budget.objects.get(id=budget_id, user=request.user)
                budget.category.name = category_name  # Update the category name
                budget.amount = amount  # Update the budget amount
                budget.category.save()
                budget.save()
            except Budget.DoesNotExist:
                pass
        else:  # Add new budget
            category, created = Category.objects.get_or_create(name=category_name)
            Budget.objects.create(user=request.user, category=category, amount=amount)

        return redirect('expenses:view_budget')

    context = {
        'budget_summary': budget_summary,
        'categories': Category.objects.all(),
    }
    return render(request, 'expenses/view_budget.html', context)

@login_required
def delete_budget(request, budget_id):
    try:
        budget = Budget.objects.get(id=budget_id, user=request.user)
        budget.delete()
        return redirect('expenses:view_budget')
    except Budget.DoesNotExist:
        return redirect('expenses:view_budget')  # Redirect if the budget does not exist

# @login_required
# def view_budget(request):
#     # Fetch all budgets for the user
#     budgets = Budget.objects.filter(user=request.user)
#     transactions = Transaction.objects.filter(user=request.user, transaction_type='Expense')

#     # Calculate total expenses for each budget category
#     budget_summary = []
#     for budget in budgets:
#         total_expenses = transactions.filter(category=budget.category).aggregate(Sum('amount'))['amount__sum'] or 0
#         remaining_budget = budget.amount - total_expenses
#         budget_summary.append({
#             'category': budget.category,
#             'total_budget': budget.amount,
#             'total_expenses': total_expenses,
#             'remaining_budget': remaining_budget,
#         })

#     if request.method == 'POST':
#         # Handle adding a new budget
#         category = request.POST.get('category')
#         amount = request.POST.get('amount')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')

#         # Check if a budget for the category already exists
#         existing_budget = Budget.objects.filter(user=request.user, category=category).first()
#         if existing_budget:
#             existing_budget.amount = amount
#             existing_budget.start_date = start_date
#             existing_budget.end_date = end_date
#             existing_budget.save()
#         else:
#             Budget.objects.create(
#                 user=request.user,
#                 category=category,
#                 amount=amount,
#                 start_date=start_date,
#                 end_date=end_date,
#             )
#         return redirect('expenses:view_budget')

#     context = {
#         'budget_summary': budget_summary,
#     }
#     return render(request, 'expenses/view_budget.html', context)



@login_required
def add_budget(request):
    if request.method == 'POST':
        category = Category.objects.get(id=request.POST['category'])
        amount = request.POST['amount']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        Budget.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('expenses:view_budget')

    categories = Category.objects.all()
    return render(request, 'expenses/add_budget.html', {'categories': categories})

@login_required
def view_report(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'expenses/report.html', {'transactions': transactions})
