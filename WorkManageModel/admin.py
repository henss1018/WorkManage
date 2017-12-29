from django.contrib import admin
from WorkManageModel.models import BudgetDO,ContractInfoDO,OrderInfoDO,AccruedExpenseInfoDO,YearBudgetDO


# Register your models here.
class BudgetDOAdmin(admin.ModelAdmin):
    list_display = ('budget_name', 'budget_code')
    search_fields = ('budget_name', 'budget_code')


class OrderInfoDOInline(admin.TabularInline):
    model = OrderInfoDO


class ContractInfoDOAdmin(admin.ModelAdmin):
    list_display = ('contract_name', 'contract_code')
    search_fields = ('contract_name', 'contract_code')
    inlines = [OrderInfoDOInline]


class AccruedExpenseInfoDOInline(admin.TabularInline):
    model = AccruedExpenseInfoDO


class OrderInfoDOAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'order_contract_code')
    search_fields = ('order_code', 'order_contract_code')
 #   inlines = [AccruedExpenseInfoDOInline]



class AccruedExpenseInfoDOAdmin(admin.ModelAdmin):
    list_display = ('contract_code', 'ae_year', 'ae_month', 'ae_amount', 'ae_writeoff_amount')
    search_fields = ('contract_code', 'ae_year', 'ae_month', 'ae_amount', 'ae_writeoff_amount')


class YearBudgetDOAdmin(admin.ModelAdmin):
    list_display = ('budget_code', 'intensive_code', 'year')
    search_fields = ('budget_code', 'intensive_code', 'year')

admin.site.register(BudgetDO, BudgetDOAdmin)
admin.site.register(ContractInfoDO, ContractInfoDOAdmin)
admin.site.register(OrderInfoDO,OrderInfoDOAdmin)
admin.site.register(AccruedExpenseInfoDO,AccruedExpenseInfoDOAdmin)
admin.site.register(YearBudgetDO, YearBudgetDOAdmin)
# admin.site.register([BudgetDO,ContractInfoDO,OrderInfoDO,AccruedExpenseInfoDO,YearBudgetDO],[BudgetDOAdmin,ContractDOAdmin])