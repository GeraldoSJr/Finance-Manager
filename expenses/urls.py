from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expenses/', views.add_expenses, name="add-expenses"),
    path('expense-edit/<int:id>/', views.expense_edit, name="expense-edit"),
    path('delete_expenses/<int:id>/', views.delete_expenses, name="delete_expenses"),
    path('search-expenses/', csrf_exempt(views.search_expenses), name="search-expenses"),
    path('export-csv/', views.export_csv, name="export-csv"),
]
