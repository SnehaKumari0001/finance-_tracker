# tracker/urls.py
from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # Web interface
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    path('budgets/add/', views.budget_create, name='budget_create'),

    # API endpoints
    path('api/transactions/', api_views.TransactionListCreateAPIView.as_view(), name='api_transaction_list'),
    path('api/transactions/<int:pk>/', api_views.TransactionRetrieveUpdateDestroyAPIView.as_view(), name='api_transaction_detail'),
]
