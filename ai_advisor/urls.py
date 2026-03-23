from django.urls import path
from .views import AskAdvisorView, ConversationHistoryView

urlpatterns = [
    path('ask/', AskAdvisorView.as_view(), name='ask-advisor'),
    path('history/', ConversationHistoryView.as_view(), name='conversation-history'),
]