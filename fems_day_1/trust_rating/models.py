from django.db import models
from django.db import models
from django.urls import path
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'trust_rating_client'  # Explicitly set the table name

# Loan model with updated field types and relationships
class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)  # Foreign key relationship to the Client model
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_term = models.IntegerField()  # Loan repayment term in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    current_payment = models.DecimalField(max_digits=10, decimal_places=2)

    # Set table name explicitly
    class Meta:
        db_table = 'loan'  # Specify your table name here explicitly

    def __str__(self):
        return f"Loan {self.loan_id} - {self.client.fullname}"


# Payment model with loan_id foreign key reference
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")  # Foreign key relationship with Loan
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payment_date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=[  # Payment status choices
        ('On-time', 'On-time'),
        ('Late', 'Late'),
        ('Missed', 'Missed'),
    ])

    def __str__(self):
        return f"Payment {self.payment_id} for Loan {self.loan.loan_id}"