from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .frontend_views import login_view, register_view, dashboard_view, expenses_view, advisor_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/advisor/', include('ai_advisor.urls')),
    path('api/budgets/', include('budgets.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('expenses/', expenses_view, name='expenses'),
    path('advisor/', advisor_view, name='advisor'),
]