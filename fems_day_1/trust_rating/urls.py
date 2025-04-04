from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, get_clients, check_trust_rating, loan_history, add_loan, get_loan_history   # Import views

urlpatterns = [
    path('', index, name='index'),
    # path('get-clients/', get_clients, name='get_clients'),
    # path('check-trust-rating/<int:client_id>/', check_trust_rating, name='check_trust_rating'),
    path('loan-history/<int:client_id>/', loan_history, name='loan_history'),
    path('add-loan/<int:client_id>/', add_loan, name='add_loan'),
    path('get-loan-history/<int:client_id>/', get_loan_history, name='get_loan_history'),
    path('get-clients/', get_clients, name='get_clients'),
    path('check-trust-rating/<int:client_id>/', check_trust_rating, name='check_trust_rating'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
