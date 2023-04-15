from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expenses/', views.add_expenses, name="add-expenses"),
    path('expense-edit/<int:id>/', views.expense_edit, name="expense-edit"),
    path('delete_expenses/<int:id>/', views.delete_expenses, name="delete_expenses")
]
