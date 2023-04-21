from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.utils.timezone import now
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import csv
from django.http import HttpResponse
import xlwt


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
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted')
    return redirect('incomes')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Incomes ' + str(now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Source', 'Date'])

    incomes = Income.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.amount, income.description, income.source, income.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Income ' + str(now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Incomes')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Source', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style.font.bold = xlwt.XFStyle()

    rows = Income.objects.filter(owner=request.user).values_list('amount', 'description', 'source', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response
