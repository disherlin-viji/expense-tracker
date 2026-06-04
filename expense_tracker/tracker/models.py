from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TYPE_CHOICES = [
    ('Income','Income'),
    ('Expense','Expense'),
]

CATEGORY_CHOICES = [
    ('Food','Food'),
    ('Bills','Bills'),
    ('Shopping','Shopping'),
    ('Travel','Travel'),
    ('Salary','Salary'),
    ('Others','Others'),
]

PAYMENT_CHOICES = [
    ('UPI','UPI'),
    ('Cash','Cash'),
    ('Card','Card'),
]

class Transaction(models.Model):
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=10,choices=TYPE_CHOICES)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    payment_method = models.CharField(max_length=10,choices=PAYMENT_CHOICES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"