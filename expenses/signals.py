from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Category


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    """
    Create default categories for new users
    """
    if created:
        default_categories = [
            {
                'name': 'Food & Dining',
                'icon': 'utensils',
                'color': '#ef4444'  # Rose
            },
            {
                'name': 'Transportation',
                'icon': 'car-front',
                'color': '#f59e0b'  # Amber
            },
            {
                'name': 'Shopping',
                'icon': 'bag-fill',
                'color': '#8b5cf6'  # Purple
            },
            {
                'name': 'Bills & Utilities',
                'icon': 'receipt',
                'color': '#3b82f6'  # Blue
            },
            {
                'name': 'Entertainment',
                'icon': 'film',
                'color': '#ec4899'  # Pink
            },
            {
                'name': 'Healthcare',
                'icon': 'heart-pulse',
                'color': '#10b981'  # Emerald
            },
            {
                'name': 'Income',
                'icon': 'cash-coin',
                'color': '#059669'  # Green
            },
            {
                'name': 'Savings',
                'icon': 'piggy-bank',
                'color': '#0f172a'  # Navy
            },
        ]
        
        for category_data in default_categories:
            Category.objects.create(
                user=instance,
                name=category_data['name'],
                icon=category_data['icon'],
                color=category_data['color']
            )
