from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.utils.timezone import now


@login_required(login_url='auth/login/')
def index(request):
    expense = Expense.objects.filter(owner=request.user)
    context = {
        'expense': expense
    }
    return render(request, 'expenses/index.html', context)


def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        if request.POST['expense_date'] != "":
            date = request.POST['expense_date']
        else:
            date = now()
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')

        Expense.objects.create(owner=request.user, amount=amount, date=date, description=description, category=category)
        messages.success(request, 'New expense added')

        return redirect('expenses')



