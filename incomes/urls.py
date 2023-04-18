from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="incomes"),
    path('add-income/', views.add_incomes, name="add-incomes"),
    path('income-edit/<int:id>/', views.income_edit, name="income-edit"),
    path('delete_incomes/<int:id>/', views.delete_incomes, name="delete_incomes"),
    path('search-incomes/', csrf_exempt(views.search_incomes), name="search-incomes"),
]