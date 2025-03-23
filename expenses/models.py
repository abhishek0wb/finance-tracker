from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically save the creation time

    def __str__(self):
        return f"{self.category.name}: {self.amount}"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=now)  # Ensure a default value for the date
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.transaction_type}: {self.amount}"
    


# class Expense(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField()
#     description = models.TextField(blank=True, null=True)    

    # def __str__(self):
    #     return f"{self.category}: {self.amount}"



