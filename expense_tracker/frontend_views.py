from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def expenses_view(request):
    return render(request, 'expenses.html')

def advisor_view(request):
    return render(request, 'advisor.html')