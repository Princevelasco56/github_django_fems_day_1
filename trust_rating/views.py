# views.py
from django.shortcuts import render, get_object_or_404
from .models import Client, Loan, Payment

def client_history(request):
    # Get all clients for the dropdown
    clients = Client.objects.all()

    selected_client = None
    trust_rating = 0.0
    loans = []

    # Check if client is selected from the dropdown
    if request.GET.get('client_id'):
        client_id = request.GET['client_id']
        selected_client = get_object_or_404(Client, client_id=client_id)

        # Get the trust rating and loan history for the selected client
        loans = Loan.objects.filter(client=selected_client)
        
        if loans.exists():
            trust_rating = loans.aggregate(models.Avg('trust_rating'))['trust_rating__avg']

    return render(
        request,
        'client_history.html', 
        {
            'clients': clients,
            'selected_client': selected_client,
            'trust_rating': trust_rating,
            'loans': loans,
            'eligible': trust_rating >= 80  # Assume eligibility is based on a 80% trust rating
        }
    )
