# python
import json

# django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView
from django.utils.text import slugify

# core
from .models import Budget, Category, Expense
from .forms import ExpenseForm


def budgets_list(request):
    list_budgets =  Budget.objects.filter(active=True)
    return render(request, 'core/budgets_list.html', {'budgets_list':list_budgets})


def budget_detail(request, budget_slug):
    budget = get_object_or_404(Budget, slug=budget_slug)
    if request.method == 'GET':
        expenses = budget.expense_set.filter(confirmed=False)
        categories_list = Category.objects.filter(active=True)
        return render(request, 'core/budget_detail.html',{
            'budget': budget,
            'expenses_list': expenses,
            'categories_list': categories_list
        })
    elif request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            category =  get_object_or_404(Category, name=category_name)
            Expense.objects.create(
                budget=budget,
                title=title,
                amount=amount,
                category=category
            ).save()
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()

        return HttpResponse('ok')

    return HttpResponseRedirect(budget_slug)


class BudgetCreateView(CreateView):
    model = Budget
    template_name = 'core/add_budget.html'
    fields = ('name', 'base')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category_name in categories:
            category, _ = Category.objects.get_or_create(
                name = category_name
            )
            category.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])
