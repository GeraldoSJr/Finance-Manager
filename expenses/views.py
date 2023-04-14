from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages


@login_required(login_url='auth/login/')
def index(request):
    exps = Expense.objects.all()
    context = {
        'expenses': exps
    }
    return render(request, 'expenses/index.html', context)


def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
        else:
            messages.success(request, 'New expense added')
        return render(request, 'expenses/add_expenses.html', context)
    return render(request, 'expenses/add_expenses.html', context)



