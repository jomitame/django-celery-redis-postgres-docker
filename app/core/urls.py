from django.urls import path

# core
from .views import budgets_list, budget_detail
from .views import BudgetCreateView

app_name = 'core'
urlpatterns = [
    path('', budgets_list, name='budgets_list'),
    path('add', BudgetCreateView.as_view(), name='add_budget'),
    path('<slug:budget_slug>', budget_detail, name='budget_detail')
]