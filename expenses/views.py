from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)

        # Filter by category
        category = request.query_params.get('category')
        if category:
            expenses = expenses.filter(category=category)

        # Filter by date range
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)

        # Filter by month and year
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if month:
            expenses = expenses.filter(date__month=month)
        if year:
            expenses = expenses.filter(date__year=year)

        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Expense.objects.get(pk=pk, user=user)
        except Expense.DoesNotExist:
            return None

    def get(self, request, pk):
        expense = self.get_object(pk, request.user)
        if not expense:
            return Response({'error': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def put(self, request, pk):
        expense = self.get_object(pk, request.user)
        if not expense:
            return Response({'error': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        expense = self.get_object(pk, request.user)
        if not expense:
            return Response({'error': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = self.get_object(pk, request.user)
        if not expense:
            return Response({'error': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
        expense.delete()
        return Response({'message': 'Expense deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ExpenseSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)

        # Filter by month and year
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if month:
            expenses = expenses.filter(date__month=month)
        if year:
            expenses = expenses.filter(date__year=year)

        # Total spent
        total = expenses.aggregate(total=Sum('amount'))['total'] or 0

        # Total per category
        category_summary = {}
        for category, _ in Expense.CATEGORY_CHOICES:
            cat_total = expenses.filter(category=category).aggregate(
                total=Sum('amount'))['total'] or 0
            if cat_total > 0:
                category_summary[category] = float(cat_total)

        return Response({
            'total': float(total),
            'category_summary': category_summary,
            'month': month,
            'year': year,
        })