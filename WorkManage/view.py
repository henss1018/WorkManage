# -*- coding: utf-8 -*-

# from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import HttpResponse
from WorkManageModel.models import BudgetDO, ContractInfoDO, YearBudgetDO, AccruedExpenseInfoDO, OrderInfoDO
from WorkManage.commons import AccruedExpense, YearAmount, OrderAE
import WorkManage.commons


def hello(request):
    # context = {}
    # context['hello'] = "Hello World!"
    context = {'hello': 'Hello World!'}
    return render(request, 'project-manage.html', context)


# 预算项目详情
def budget_info(request):
    context = {}
    budget_list = BudgetDO.objects.order_by('-status').all()
    context['budget_list'] = budget_list
    amount_list = []
    year_amount_list = []
    for b in budget_list:
        c = b.contract_budget_set.all()
        if(c):
            a = AccruedExpense(c[0].contract_code,'2017')
        else:
            a = AccruedExpense('','2017')
        amount_list.append(a)
        year_amount = YearAmount(b.budget_code,'2017')
        year_amount_list.append(year_amount)

    context['amount_list'] = amount_list
    context['year_amount_list']= year_amount_list
    context['budget_url'] = '/budget_detail/?budget_code='

    return render(request, 'budget-info.html', context)


# 年度预算信息详情
def budget_info_detail(request):
    context = {}
    in_budget_code = request.GET['budget_code']
    budget_info_detail_list = YearBudgetDO.objects.filter(budget_code=in_budget_code)
   # test1 = budget_info_detail_list[0]
    budget_info = BudgetDO.objects.get(budget_code=in_budget_code)
    ae_list = []
    for y in budget_info_detail_list:
        if(budget_info.contract_budget_set.all()):
            year_amount = AccruedExpense(budget_info.contract_budget_set.all()[0].contract_code, y.year)
        else:
            year_amount = AccruedExpense('',y.year)
        ae_list.append(year_amount)
    context['budget_info_detail_list'] = budget_info_detail_list
    context['ae_list'] = ae_list

    return render(request, 'budget-detail.html', context)


# 合同信息详情
def contract_info(request):
    context = {}
    contract_list = ContractInfoDO.objects.order_by('-contract_status').all()
    context['contract_list'] = contract_list
    ae_amount_list = []
    for b in contract_list:
        # c = b.contract_budget_set.all()
        a = AccruedExpense(b.contract_code,'0')
        ae_amount_list.append(a)

    context['ae_amount_list'] = ae_amount_list
    context['order_url'] = '/contract_order/?contract_code='
    context['aeinfo_url'] = '/contract_aeinfo/?contract_code='

    return render(request, 'contract-info.html', context)

# 合同订单详情
def contract_order(request):
    context = {}
    in_contract_code = request.GET['contract_code']
    contract_order_list = OrderInfoDO.objects.filter(contract_code=in_contract_code)
    ae_order_list = []
    for b in contract_order_list:
        # c = b.contract_budget_set.all()
        a = OrderAE(b.order_contract_code)
        ae_order_list.append(a)
    context['contract_order_list'] = contract_order_list
    context['ae_order_list'] = ae_order_list
    order_amount_workloadchecked = WorkManage.commons.get_order_amount(in_contract_code, '1')
    order_amount = WorkManage.commons.get_order_amount(in_contract_code, '2')
    contract_balance = WorkManage.commons.get_contract_balance(in_contract_code)
    context['order_amount'] = round(order_amount, 2)
    context['order_amount_workloadchecked'] = round(order_amount_workloadchecked, 2)
    context['contract_balance'] = round(contract_balance, 2)
    context['contract_per'] = WorkManage.commons.get_percentage(
        (order_amount_workloadchecked+contract_balance), order_amount_workloadchecked)
    context['contract_amount'] = round(contract_balance + order_amount_workloadchecked, 2)

    return render(request, 'contract-order.html', context)


# 合同预提详情
def contract_aeinfo(request):
    context = {}
    in_contract_code = request.GET['contract_code']
    contract_aeinfo_list = AccruedExpenseInfoDO.objects.filter(contract_code=in_contract_code).order_by('ae_order_code')
    # contract_code_list = AccruedExpenseInfoDO.objects.filter(contract_code=in_contract_code)
    # test1 = budget_info_detail_list[0]
    # budget_info = BudgetDO.objects.get(budget_code=in_budget_code)
   # ae_amount_list = []
    #for b in contract_aeinfo_list:
        # c = b.contract_budget_set.all()
        #a = AccruedExpense(b.contract_code, '0')
        #ae_amount_list.append(a)

    ae_amount = AccruedExpense(in_contract_code, '0')
    if(contract_aeinfo_list.all()):
        ae_diff = ae_amount.ae_sum - contract_aeinfo_list.all()[0].contract.contract_amount
    else:
        ae_diff = 0
    context['contract_aeinfo_list'] = contract_aeinfo_list
    #context['ae_amount_list'] = ae_amount_list
    context['ae_amount'] = ae_amount
    context['ae_diff'] = float(int(ae_diff*1000)/1000)

    return render(request, 'contract-aeinfo.html', context)