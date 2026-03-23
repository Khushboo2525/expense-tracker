import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from groq import Groq
from django.db.models import Sum
from expenses.models import Expense
from .models import Conversation
from .serializers import ConversationSerializer


def get_expense_context(user):
    expenses = Expense.objects.filter(user=user)
    total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    category_summary = {}
    for category, label in Expense.CATEGORY_CHOICES:
        cat_total = expenses.filter(category=category).aggregate(
            total=Sum('amount'))['total'] or 0
        if cat_total > 0:
            category_summary[label] = float(cat_total)

    recent_expenses = expenses[:5]
    recent_list = []
    for exp in recent_expenses:
        recent_list.append(f"- {exp.title} ({exp.category}): ₹{exp.amount} on {exp.date}")

    context = f"""
User's Expense Summary:
Total Spent: ₹{total}

Category Breakdown:
{chr(10).join([f"- {cat}: ₹{amt}" for cat, amt in category_summary.items()])}

Recent Expenses:
{chr(10).join(recent_list)}
"""
    return context


class AskAdvisorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)

        expense_context = get_expense_context(request.user)

        system_prompt = f"""You are a helpful personal finance advisor.
You have access to the user's expense data and help them understand their spending patterns,
give budgeting advice, and suggest ways to save money.
Always respond in a friendly, concise and practical manner.
Always use Indian Rupee (₹) for currency.

{expense_context}"""

        try:
            client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
            response = client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=1024
            )
            answer = response.choices[0].message.content

            conversation = Conversation.objects.create(
                user=request.user,
                question=question,
                answer=answer
            )

            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversationHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(user=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)