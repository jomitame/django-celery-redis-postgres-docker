from django.db import models
from django.utils.text import slugify


class Budget(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    base = models.IntegerField()
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Budget, self).save(*args, **kwargs)

    def base_left(self):
        expense_list = Expense.objects.filter(budget=self)
        total_amount = 0
        for expense in expense_list:
            total_amount += expense.amount
        return self.base - total_amount

    def total_transactions(self):
        return Expense.objects.filter(budget=self).count()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attachment = models.FileField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
