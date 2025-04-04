from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import models
from django.urls import path
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from .models import Client, Loan, Payment
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# API Views
@api_view(['GET'])
def check_trust_rating(request, client_id):
    loans = Loan.objects.filter(client__client_id=client_id)  # Get loans related to the client
    payments = Payment.objects.filter(loan__in=loans)

    total_payments = payments.count()
    on_time_payments = payments.filter(status='On-time').count()
    
    trust_rating = (on_time_payments / total_payments) * 100 if total_payments > 0 else 0

    # Update trust rating for all client loans
    loans.update(trust_rating=trust_rating)
    
    return Response({
        "trust_rating": trust_rating,
        "eligible": trust_rating >= 80
    })

def loan_history(request, client_id):
    client = Client.objects.get(client_id=client_id)
    loans = Loan.objects.filter(client=client)

    loan_data = []
    for loan in loans:
        loan_data.append({
            'loan_id': loan.loan_id,
            'loan_amount': float(loan.loan_amount),
            'pay_term': loan.pay_term,
            'interest_rate': float(loan.interest_rate),
            'current_payment': float(loan.current_payment),
        })

    return JsonResponse(loan_data, safe=False)

@api_view(['GET'])
def get_clients(request):
    clients = Client.objects.values("client_id", "fullname")
    return Response(list(clients))

# Frontend View
def index(request):
    return render(request, 'index.html')

def create_loan(client_id, trust_rating):
    """Assigns loan amount based on the trust rating."""
    if trust_rating >= 90:
        loan_amount = 50000  # High trust rating gets more loan
    elif trust_rating >= 75:
        loan_amount = 30000  # Medium trust rating
    else:
        loan_amount = 10000  # Low trust rating gets a smaller loan

    return loan_amount

def add_loan(request, client_id):
    client = Client.objects.get(client_id=client_id)
    
    # Get trust rating
    trust_rating = client.loan_set.latest('loan_id').trust_rating if client.loan_set.exists() else 0
    
    # Determine loan amount based on trust rating
    loan_amount = create_loan(client_id, trust_rating)
    
    # Create a new loan entry
    loan = Loan.objects.create(
        client=client,
        trust_rating=trust_rating,
        loan_amount=loan_amount,
        pay_term=24,  # Default to 24 months
        interest_rate=7.5,  # Example: default interest rate
        current_payment=loan_amount / 24  # Monthly payment
    )

    return JsonResponse({'message': 'Loan added successfully!', 'loan_id': loan.loan_id})

def get_loan_history(request, client_id):
    """Fetch all loan records for a client"""
    loans = Loan.objects.filter(client__client_id=client_id).values(  # Correct field reference
        "loan_id", "loan_amount", "pay_term", "interest_rate", "current_payment"
    )
    
    return JsonResponse(list(loans), safe=False)