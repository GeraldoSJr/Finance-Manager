import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.utils.timezone import now
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import csv
from django.http import HttpResponse


def search_expenses(request):

    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | \
                   Expense.objects.filter(date__istartswith=search_str, owner=request.user) | \
                   Expense.objects.filter(description__icontains=search_str, owner=request.user) | \
                   Expense.objects.filter(category__icontains=search_str, owner=request.user)

        data = expenses.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='auth/login/')
def index(request):
    expense = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expense, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expense': expense,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        messages.info(request, 'Handling post form')
        return render(request, 'expenses/edit_expense.html', context)

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

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.category = category

        expense.save()
        messages.success(request, 'Expense Updated')

        return redirect('expenses')


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


def delete_expenses(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted')
    return redirect('expenses')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses ' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response
