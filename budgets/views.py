from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from expenses.models import Expense
from .models import Budget
from .serializers import BudgetSerializer


class BudgetListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if month:
            budgets = budgets.filter(month=month)
        if year:
            budgets = budgets.filter(year=year)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BudgetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Budget.objects.get(pk=pk, user=user)
        except Budget.DoesNotExist:
            return None

    def get(self, request, pk):
        budget = self.get_object(pk, request.user)
        if not budget:
            return Response({'error': 'Budget not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BudgetSerializer(budget)
        return Response(serializer.data)

    def patch(self, request, pk):
        budget = self.get_object(pk, request.user)
        if not budget:
            return Response({'error': 'Budget not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        budget = self.get_object(pk, request.user)
        if not budget:
            return Response({'error': 'Budget not found'}, status=status.HTTP_404_NOT_FOUND)
        budget.delete()
        return Response({'message': 'Budget deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class BudgetStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response({'error': 'month and year are required'}, status=status.HTTP_400_BAD_REQUEST)

        budgets = Budget.objects.filter(user=request.user, month=month, year=year)
        category = request.query_params.get('category')
        if category:
            budgets = budgets.filter(category=category)
        status_list = []

        for budget in budgets:
            spent = Expense.objects.filter(
                user=request.user,
                category=budget.category,
                date__month=month,
                date__year=year
            ).aggregate(total=Sum('amount'))['total'] or 0

            remaining = float(budget.amount) - float(spent)
            exceeded = remaining < 0

            status_list.append({
                'category': budget.category,
                'budget': float(budget.amount),
                'spent': float(spent),
                'remaining': float(remaining),
                'exceeded': exceeded,
                'percentage_used': round((float(spent) / float(budget.amount)) * 100, 2) if budget.amount > 0 else 0
            })

        return Response({
            'month': month,
            'year': year,
            'budgets': status_list
        })