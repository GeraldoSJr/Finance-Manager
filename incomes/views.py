from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.utils.timezone import now
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference


def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        incomes = Income.objects.filter(amount__istartswith=search_str, owner=request.user) | \
                   Income.objects.filter(date__istartswith=search_str, owner=request.user) | \
                   Income.objects.filter(description__icontains=search_str, owner=request.user) | \
                   Income.objects.filter(source__icontains=search_str, owner=request.user)

        data = incomes.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='auth/login/')
def index(request):
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


def income_edit(request, id):
    sources = Source.objects.all()
    income = Income.objects.get(pk=id)
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        messages.info(request, 'Handling post form')
        return render(request, 'income/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        description = request.POST['description']
        if request.POST['income_date'] != "":
            date = request.POST['income_date']
        else:
            date = now()
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.description = description
        income.source = source

        income.save()
        messages.success(request, 'Income Updated')

        return redirect('incomes')


def add_incomes(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        if request.POST['income_date'] != "":
            date = request.POST['income_date']
        else:
            date = now()
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')

        Income.objects.create(owner=request.user, amount=amount, date=date, description=description, source=source)
        messages.success(request, 'New income added')

        return redirect('incomes')


def delete_incomes(request, id):
    income = Source.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted')
    return redirect('incomes')
