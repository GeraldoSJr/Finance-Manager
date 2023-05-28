import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Stock
from django.contrib import messages
from django.utils.timezone import now
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import csv
from django.http import HttpResponse
import xlwt


def search_stocks(request):

    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        stocks = Stock.objects.filter(amount__istartswith=search_str, owner=request.user) | \
                   Stock.objects.filter(date__istartswith=search_str, owner=request.user) | \
                   Stock.objects.filter(ticker__icontains=search_str, owner=request.user)

        data = stocks.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='auth/login/')
def index(request):
    stock = Stock.objects.filter(owner=request.user)
    paginator = Paginator(stock, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'stock': stock,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'stocks/list_transactions.html', context)


def stock_edit(request, id):
    stock = Stock.objects.get(pk=id)
    context = {
        'stock': stock,
        'values': stock,
    }
    if request.method == 'GET':
        messages.info(request, 'Handling post form')
        return render(request, 'stocks/edit_transaction.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        ticker = request.POST['ticker']
        if request.POST['stock_date'] != "":
            date = request.POST['stock_date']
        else:
            date = now()
        if not amount:
            messages.error(request, 'Amount is required')

        stock.owner = request.user
        stock.amount = amount
        stock.date = date
        stock.ticker = ticker

        stock.save()
        messages.success(request, 'stock Updated')

        return redirect('stocks')


def add_stocks(request):
    if request.method == 'GET':
        return render(request, 'stocks/add_transaction.html')

    if request.method == 'POST':
        amount = request.POST['amount']
        ticker = request.POST['ticker']
        if request.POST['stock_date'] != "":
            date = request.POST['stock_date']
        else:
            date = now()
        if not amount:
            messages.error(request, 'Amount is required')

        Stock.objects.create(owner=request.user, amount=amount, date=date, ticker=ticker)
        messages.success(request, 'New stock added')

        return redirect('stocks')


def delete_stocks(request, id):
    stock = Stock.objects.get(pk=id)
    stock.delete()
    messages.success(request, 'stock deleted')
    return redirect('stocks')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stocks ' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'ticker', 'Date'])

    stocks = Stock.objects.filter(owner=request.user)

    for stock in stocks:
        writer.writerow([stock.amount, stock.ticker, stock.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=stocks ' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('stocks')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'ticker', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style.font.bold = xlwt.XFStyle()

    rows = Stock.objects.filter(owner=request.user).values_list('amount', 'ticker', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response

