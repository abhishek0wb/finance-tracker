# from django.urls import path
# from . import views

# app_name = 'expenses'

# urlpatterns = [
#     path('', views.dashboard, name='dashboard'),  # Maps to 'expenses:dashboard'
#     path('add/', views.add_expense, name='add_expense'),
#     path('add_budget/', views.add_budget, name='add_budget'),
#     path('view_budget/', views.view_budget, name='view_budget'),
# ]

from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('view_budget/', views.view_budget, name='view_budget'),
    path('transactions/', views.all_transactions, name='transactions'),
]

