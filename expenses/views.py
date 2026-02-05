from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Budget, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, Value
from django.db.models.functions import Coalesce
from decimal import Decimal 
import calendar
from datetime import datetime, date
from django.http import HttpResponse


def test_tailwind(request):
    """Test page to verify Tailwind CSS is loading"""
    return render(request, 'test_tailwind.html')


def index(request):
    """Landing page - show marketing page if not logged in, otherwise redirect to dashboard"""
    if request.user.is_authenticated:
        return redirect('expenses:dashboard')
    return render(request, 'landing.html')

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
    last_three_transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]

    # Calculate incoming and outgoing amounts for the Cash Flow card using Coalesce
    cashflow = transactions.aggregate(
        incoming=Coalesce(Sum('amount', filter=Q(transaction_type='Income')), Value(Decimal('0.00'))),
        outgoing=Coalesce(Sum('amount', filter=Q(transaction_type='Expense')), Value(Decimal('0.00')))
    )
    
    # Calculate total balance (all-time)
    all_transactions = Transaction.objects.filter(user=request.user)
    total_balance_data = all_transactions.aggregate(
        total_income=Coalesce(Sum('amount', filter=Q(transaction_type='Income')), Value(Decimal('0.00'))),
        total_expense=Coalesce(Sum('amount', filter=Q(transaction_type='Expense')), Value(Decimal('0.00')))
    )
    total_balance = total_balance_data['total_income'] - total_balance_data['total_expense']

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
        'current_month_date': current_month_date,
        'current_year': current_year,
        'current_date': current_date,
        'month_days': month_days,
        'transaction_days': transaction_days,
        'last_three_transactions': last_three_transactions,
        'cashflow': cashflow,
        'total_balance': total_balance,
        'monthly_income': cashflow['incoming'],
        'monthly_expense': cashflow['outgoing'],
        'user_categories': Category.objects.filter(user=request.user).order_by('name'),
    }
    return render(request, 'expenses/dashboard_tailwind.html', context)


@login_required
def all_transactions(request):
    # Fetch all transactions for the user, ordered by the latest date
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'transactions': transactions,
        'user_categories': Category.objects.filter(user=request.user).order_by('name'),
    }
    return render(request, 'expenses/transactions_tailwind.html', context)


from decimal import Decimal

@login_required
def add_transaction(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        transaction_type = request.POST['transaction_type']
        amount = Decimal(request.POST['amount'])

        # Get the category object
        try:
            category = Category.objects.get(id=category_id, user=request.user)
        except Category.DoesNotExist:
            # Fallback: create a new category if it doesn't exist
            category = None

        # Check if the transaction is an expense and exceeds the budget
        if transaction_type == 'Expense' and category:
            budget = Budget.objects.filter(user=request.user, category=category).first()
            if budget:
                total_expenses = Transaction.objects.filter(
                    user=request.user, category=category, transaction_type='Expense'
                ).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
                if total_expenses + amount > budget.amount:
                    categories = Category.objects.filter(user=request.user).order_by('name')
                    return render(request, 'expenses/add_transaction.html', {
                        'categories': categories,
                        'error': f"Transaction exceeds the budget for {category.name}."
                    })

        # Save the transaction
        transaction = Transaction(
            user=request.user,
            category=category,
            transaction_type=transaction_type,
            amount=amount,
            description=request.POST.get('description', ''),
        )
        transaction.save()
        return redirect('expenses:view_budget')

    # Fetch user's categories for the dropdown
    categories = Category.objects.filter(user=request.user).order_by('name')
    return render(request, 'expenses/add_transaction.html', {'categories': categories})

from django.shortcuts import get_object_or_404, redirect

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    transaction.delete()
    
    # If HTMX request, return empty response to remove the element
    if request.htmx:
        return HttpResponse('')
    
    # Otherwise, redirect as before
    return redirect('expenses:transactions')



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
    current_date = date.today()

    # Calculate budget summary with monthly logic
    budget_summary = []
    for budget in budgets:
        spent = budget.get_spent_amount()
        remaining = budget.get_remaining_amount()
        percentage = budget.get_percentage_used()
        period_text = budget.get_period_display_text()
        status_color = budget.get_status_color()
        
        budget_summary.append({
            'id': budget.id,
            'category': budget.category.name,
            'total_budget': budget.amount,
            'total_expenses': spent,
            'remaining_budget': remaining,
            'percentage': percentage,
            'period_text': period_text,
            'status_color': status_color,
            'period': budget.period,
        })

    if request.method == 'POST':
        category_name = request.POST.get('category')
        budget_id = request.POST.get('budget_id')
        amount = request.POST.get('amount')
        period = request.POST.get('period', 'monthly')

        if budget_id:  # Update existing budget
            try:
                budget = Budget.objects.get(id=budget_id, user=request.user)
                # Get or create category
                category, created = Category.objects.get_or_create(
                    user=request.user,
                    name=category_name,
                    defaults={'icon': 'tag', 'color': '#64748b'}
                )
                budget.category = category
                budget.amount = amount
                budget.period = period
                budget.save()
            except Budget.DoesNotExist:
                pass
        else:  # Add new budget
            category, created = Category.objects.get_or_create(
                user=request.user,
                name=category_name,
                defaults={'icon': 'tag', 'color': '#64748b'}
            )
            Budget.objects.create(
                user=request.user,
                category=category,
                amount=amount,
                period=period,
                start_date=current_date
            )

        return redirect('expenses:view_budget')

    context = {
        'budget_summary': budget_summary,
        'categories': Category.objects.filter(user=request.user).order_by('name'),
        'current_date': current_date,
    }
    return render(request, 'expenses/view_budget_tailwind.html', context)

@login_required
def delete_budget(request, budget_id):
    try:
        budget = Budget.objects.get(id=budget_id, user=request.user)
        budget.delete()
        return redirect('expenses:view_budget')
    except Budget.DoesNotExist:
        return redirect('expenses:view_budget')


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


@login_required
def search_transactions(request):
    """Search transactions by category or description"""
    query = request.GET.get('q', '').strip()
    
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    if query:
        transactions = transactions.filter(
            Q(category__name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    return render(request, 'expenses/partials/transaction_list_tailwind.html', {
        'transactions': transactions
    })


@login_required
def quick_add_transaction(request):
    """Quick add transaction via HTMX"""
    if request.method == 'POST':
        category_name = request.POST.get('category', '').strip()
        transaction_type = request.POST.get('transaction_type')
        amount = Decimal(request.POST.get('amount'))
        description = request.POST.get('description', '')
        
        # Get or create the category
        category = None
        if category_name:
            category, created = Category.objects.get_or_create(
                user=request.user,
                name=category_name,
                defaults={'icon': 'tag', 'color': '#64748b'}
            )
        
        # Create the transaction
        transaction = Transaction.objects.create(
            user=request.user,
            category=category,
            transaction_type=transaction_type,
            amount=amount,
            date=date.today(),
            description=description
        )
        
        # Return only the new transaction card for HTMX to prepend
        return render(request, 'expenses/partials/transaction_list_tailwind.html', {
            'transactions': [transaction]
        })
    
    return HttpResponse('', status=400)
