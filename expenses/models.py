from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from decimal import Decimal
from datetime import date

class Category(models.Model):
    """User-specific categories for organizing transactions and budgets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, default='tag')  # Bootstrap icon name
    color = models.CharField(max_length=7, default='#4f46e5')  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ['user', 'name']
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        if self.user:
            return f"{self.name} ({self.user.username})"
        return self.name

class Budget(models.Model):
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('one-time', 'One-Time'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    start_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category.name}: ₹{self.amount} ({self.get_period_display()})"

    def get_spent_amount(self, target_date=None):
        """
        Calculate spent amount for the current budget period
        
        Args:
            target_date: Optional date to calculate for (defaults to today)
        
        Returns:
            Decimal: Total spent in the current period
        """
        if target_date is None:
            target_date = date.today()
        
        # Get transactions for this category and user
        transactions = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type='Expense'
        )
        
        # Filter by period
        if self.period == 'monthly':
            # Current month and year
            transactions = transactions.filter(
                date__year=target_date.year,
                date__month=target_date.month
            )
        elif self.period == 'yearly':
            # Current year
            transactions = transactions.filter(
                date__year=target_date.year
            )
        elif self.period == 'one-time':
            # All time since start_date
            transactions = transactions.filter(
                date__gte=self.start_date
            )
        
        # Calculate total with Coalesce to handle None
        total = transactions.aggregate(
            total=Coalesce(Sum('amount'), Decimal('0.00'))
        )['total']
        
        return total

    def get_remaining_amount(self, target_date=None):
        """
        Calculate remaining budget amount
        
        Returns:
            Decimal: Remaining budget (can be negative if over budget)
        """
        spent = self.get_spent_amount(target_date)
        return self.amount - spent

    def get_percentage_used(self, target_date=None):
        """
        Calculate percentage of budget used
        
        Returns:
            int: Percentage used (0-100+)
        """
        if self.amount == 0:
            return 0
        
        spent = self.get_spent_amount(target_date)
        percentage = (spent / self.amount) * 100
        return int(percentage)

    def get_period_display_text(self, target_date=None):
        """
        Get human-readable period text
        
        Returns:
            str: e.g., "February 2026", "2026", "Since Jan 1, 2026"
        """
        if target_date is None:
            target_date = date.today()
        
        if self.period == 'monthly':
            return target_date.strftime('%B %Y')
        elif self.period == 'yearly':
            return str(target_date.year)
        elif self.period == 'one-time':
            return f"Since {self.start_date.strftime('%b %d, %Y')}"
        
        return "Current Period"

    def is_over_budget(self, target_date=None):
        """
        Check if budget is exceeded
        
        Returns:
            bool: True if over budget
        """
        return self.get_spent_amount(target_date) > self.amount

    def get_status_color(self, target_date=None):
        """
        Get color based on budget status
        
        Returns:
            str: 'emerald' (< 80%), 'amber' (80-99%), 'rose' (100%+)
        """
        percentage = self.get_percentage_used(target_date)
        
        if percentage >= 100:
            return 'rose'
        elif percentage >= 80:
            return 'amber'
        else:
            return 'emerald'


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Keep old string category temporarily
    category_string = models.CharField(max_length=100, null=True, blank=True)
    # New ForeignKey category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=now)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        if self.category:
            category_name = self.category.name
        elif self.category_string:
            category_name = self.category_string
        else:
            category_name = 'Uncategorized'
        return f"{category_name} - {self.transaction_type}: {self.amount}"
    


