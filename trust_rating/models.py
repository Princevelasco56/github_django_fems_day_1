from django.db import models
from django.db import models
from django.urls import path
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

# Create your models here.
# Models
# class Client(models.Model):
#     client_id = models.AutoField(primary_key=True)
#     fullname = models.CharField(max_length=255)

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return self.fullname
    
# class Loan(models.Model):
#     loan_id = models.AutoField(primary_key=True)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     trust_rating = models.FloatField(default=0.0)

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trust_rating = models.FloatField(default=0.0)
    loan_amount = models.FloatField(null=True, blank=True)  # Allow NULL values
    pay_term = models.IntegerField(default=12)  # 12, 24, 36 months
    interest_rate = models.FloatField(default=5.0)  # Default interest rate
    current_payment = models.FloatField(null=True, blank=True)  # Allow NULL values

    def __str__(self):
        return f"Loan {self.loan_id} - {self.client.fullname}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # 'On-time' or other statuses
