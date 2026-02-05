from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('view_budget/', views.view_budget, name='view_budget'),
    path('delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),
    path('transactions/', views.all_transactions, name='transactions'),
    path('transactions/delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('transactions/search/', views.search_transactions, name='search_transactions'),
    path('transactions/quick-add/', views.quick_add_transaction, name='quick_add_transaction'),
    path('test-tailwind/', views.test_tailwind, name='test_tailwind'),
]
