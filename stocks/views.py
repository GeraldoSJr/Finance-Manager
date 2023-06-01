from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Stock
from django.contrib import messages
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPreference
import csv
from django.http import HttpResponse
import xlwt
import os
import json
from django.conf import settings
import datetime
import requests


def search_stocks(request):

    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Stock.objects.filter(amount__istartswith=search_str, owner=request.user) | \
                   Stock.objects.filter(date__istartswith=search_str, owner=request.user) | \
                   Stock.objects.filter(ticker__icontains=search_str, owner=request.user) | \
                   Stock.objects.filter(price__icontains=search_str, owner=request.user)

        data = expenses.values()

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
    return render(request, 'stocks/list_stocks.html', context)


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
        ticker = request.POST['ticker']
        amount = request.POST['amount']
        price = request.POST['price']
        if request.POST['stock_date'] != "":
            date = request.POST['stock_date']
        else:
            date = now()
        if not amount:
            messages.error(request, 'Amount is required')

        if Stock.objects.filter(owner=request.user, ticker=ticker).exists():
            stock = Stock.objects.get(owner=request.user, ticker=ticker)
            stock.amount += float(amount)
            stock.price = round((stock.price * stock.previous_times + float(price)) / (stock.previous_times + 1))
            stock.previous_times += 1
            stock.save()
        else:
            Stock.objects.create(owner=request.user, amount=amount, date=date, ticker=ticker, price=price, previous_times=1)
        messages.success(request, 'New stock added')

        return redirect('stocks')


def search_stock_info(request):
    stock_data = []
    file_path = os.path.join(settings.BASE_DIR, 'stock-info.csv')
    context = {
        'stocks': stock_data
    }

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            stock_data.append({'name': row[0], 'value': row[1]})

    if request.method == 'POST':
        stock_selected = request.POST['stock_selected']
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_selected}&apikey=U00L0SDG2G52QNZH"
        r = requests.get(url)
        info = r.json()
        context['info'] = info
        return render(request, 'stocks/search_stocks.html', context)

    if request.method == 'GET':
        return render(request, 'stocks/search_stocks.html', context)



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

