from django.urls import path
from .views import ExpenseListCreateView, ExpenseDetailView, ExpenseSummaryView, ExpenseExportView

urlpatterns = [
    path('', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('summary/', ExpenseSummaryView.as_view(), name='expense-summary'),
    path('export/', ExpenseExportView.as_view(), name='expense-export'),
]