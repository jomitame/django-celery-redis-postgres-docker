from django.contrib import admin
from core.models import Budget, Category, Expense


def right_now(modeladmin, request, queryset):
    from .processor import prin_after_time
    prin_after_time('Sync')

right_now.short_description = "Send Syncronous"

def enqueued(modeladmin, request, queryset):
    from .tasks import call_prin_after_time
    call_prin_after_time.delay('Async')

enqueued.short_description = "Send Asyncronous"

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'base', 'active')
    actions = [right_now, enqueued]


admin.site.register(Category)
admin.site.register(Expense)
