from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="stocks"),
    path('add-transactions/', views.add_stocks, name="add-transaction"),
    path('transaction-edit/<int:id>/', views.stock_edit, name="transaction-edit"),
    path('delete_stock/<int:id>/', views.delete_stocks(), name="delete_transaction"),
    path('search-stock/', csrf_exempt(views.search_stocks), name="search-stocks"),
    path('export-csv/', views.export_csv, name="export-csv"),
    path('export-excel/', views.export_excel, name="export-excel"),
]