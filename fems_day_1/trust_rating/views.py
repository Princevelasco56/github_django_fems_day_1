from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.db import models
from rest_framework.response import Response
from django.urls import path
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from .models import Client, Loan, Payment

# Create your views here.
# API Views
@api_view(['GET'])
def check_trust_rating(request, client_id):
    try:
        # Fetch loans for the client
        loans = Loan.objects.filter(client_id=client_id)
        
        if not loans:
            return Response({"error": "No loans found for this client."}, status=404)
        
        payments = Payment.objects.filter(loan__in=loans)
        
        # Calculate trust rating
        total_payments = payments.count()
        on_time_payments = payments.filter(status='On-time').count()

        trust_rating = (on_time_payments / total_payments) * 100 if total_payments > 0 else 0

        return Response({
            "trust_rating": round(trust_rating, 2),
            "eligible": trust_rating >= 80  # Eligible if trust rating >= 80
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
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

def loan_application(request):
    return render(request, 'loan_application.html')

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

@api_view(['GET'])
def get_loan_history(request, client_id):
    try:
        # Fetch loans for the client
        loans = Loan.objects.filter(client_id=client_id)  # Query from the 'loan' table
        
        loan_data = []
        for loan in loans:
            loan_data.append({
                'loan_id': loan.loan_id,
                'loan_amount': float(loan.loan_amount),
                'pay_term': loan.pay_term,
                'interest_rate': float(loan.interest_rate),
                'current_payment': float(loan.current_payment),
                # 'status': loan.status,  # Add status if you have it defined in the Loan model
                # 'trust_rating': calculate_trust_rating(loan)  # You can include trust rating calculation here if needed
            })
        
        return Response(loan_data)
    except Loan.DoesNotExist:
        return Response({"error": "Client or loans not found"}, status=404)

    try:
        client = Client.objects.get(client_id=client_id)
        loans = Loan.objects.filter(client=client)
        loan_data = []
        for loan in loans:
            # Optionally, get the latest payment status:
            latest_payment = Payment.objects.filter(loan=loan).order_by('-payment_date').first()
            status = latest_payment.status if latest_payment else "No payments"
            loan_data.append({
                'loan_id': loan.loan_id,
                'loan_amount': float(loan.loan_amount),
                'pay_term': loan.pay_term,
                'interest_rate': float(loan.interest_rate),
                'current_payment': float(loan.current_payment),
                'status': status,
                'trust_rating': float(loan.trust_rating),
            })
        return JsonResponse(loan_data, safe=False)
    except Client.DoesNotExist:
        return JsonResponse({"error": "Client not found"}, status=404)

    try:
        client = Client.objects.get(client_id=client_id)
        loans = Loan.objects.filter(client=client)

        loan_data = [
            {
                'loan_id': loan.loan_id,
                'loan_amount': float(loan.loan_amount),
                'pay_term': loan.pay_term,
                'interest_rate': float(loan.interest_rate),
                'current_payment': float(loan.current_payment),
            }
            for loan in loans
        ]

        return JsonResponse(loan_data, safe=False)
    except Client.DoesNotExist:
        return JsonResponse({"error": "Client not found"}, status=404)
    
def loan_application(request):
    clients = Client.objects.all()
    return render(request, 'loan_application.html', {'clients': clients})
