# -*- coding: utf-8 -*-

from WorkManageModel.models import AccruedExpenseInfoDO,ContractInfoDO,BudgetDO,YearBudgetDO,OrderInfoDO
import datetime


# 计算合同某年度的预提总数，包括冲销金额，如果输入为‘0’则返回全部预提总额
def get_accrued_expense(in_contract_code, in_ae_year):
    if(in_ae_year == '0'):
        ae_expenses = AccruedExpenseInfoDO.objects.filter(contract_code=in_contract_code)
    else:
        ae_expenses = AccruedExpenseInfoDO.objects.filter(contract_code=in_contract_code).filter(ae_year=in_ae_year)
    ae_sum = 0
    if(ae_expenses):
        for i in ae_expenses:
            ae_sum = ae_sum + int(i.ae_amount*1000) + int(i.ae_writeoff_amount*1000)
    else:
        ae_sum = 0
    ae_sum = float(ae_sum/1000)
    return ae_sum


# 计算订单的预提总数
def get_order_ae(in_order_code):
    ae_expenses = AccruedExpenseInfoDO.objects.filter(ae_order_code=in_order_code)
    ae_sum = 0
    for i in ae_expenses:
        ae_sum = ae_sum + int(i.ae_amount*1000)
    ae_sum = float(ae_sum/1000)
    return ae_sum


# 计算订单的冲销总数
def get_order_writeoff_ae(in_order_code):
    ae_expenses = AccruedExpenseInfoDO.objects.filter(ae_writeoff_order_code=in_order_code)
    ae_sum = 0
    for i in ae_expenses:
        ae_sum = ae_sum + i.ae_writeoff_amount
    return ae_sum


# 查询预算项目某年的预算金额
def get_year_amount(in_budegt_code, in_budget_year):
    year_amount_list = YearBudgetDO.objects.filter(budget_code=in_budegt_code).filter(year=in_budget_year)
    year_amount = 0
    for i in year_amount_list:
        year_amount = year_amount + i.budget_amount
    return year_amount

# 计算合同订单总金额（in_workload_checked，1：已核定订单；0：未核定订单；2：全部订单）
def get_order_amount(in_contract_code, in_workload_checked):
    order_amount_list = 0
    if(in_workload_checked == '1'):
        order_amount_list = OrderInfoDO.objects.filter(contract_code=in_contract_code).filter(
            workload_checked=int(in_workload_checked))
    elif(in_workload_checked == '2'):
        order_amount_list = OrderInfoDO.objects.filter(contract_code=in_contract_code)
    elif(in_workload_checked == '0'):
        order_amount_list = OrderInfoDO.objects.filter(contract_code=in_contract_code).filter(
            workload_checked=int(in_workload_checked))
    order_amount = 0.0
    if(len(order_amount_list) > 0):
        for i in order_amount_list:
            order_amount += i.order_amount

    return order_amount

# 计算合同剩余可支付金额,合同金额-已核定订单总金额
def get_contract_balance(in_contract_code):
    contract_amount = ContractInfoDO.objects.filter(contract_code=in_contract_code)[0].contract_amount
    contract_order_amount = get_order_amount(in_contract_code, '1')
    return contract_amount - contract_order_amount

# 获取进度数据
def get_percentage(in_amount, in_per):
    amount = float(in_amount)
    per = float(in_per)
    return '{0:.2f}%'.format(per/amount*100)

# 计算两个日期之间的天数
def get_differ_days(in_start_date, in_end_date):
    start_date = datetime.datetime(in_start_date)
    end_date = datetime.datetime(in_end_date)
    return (end_date-start_date).days


# 计算合同某年度全部的预提总数，包括冲销金额
class AccruedExpense:
    contract_code = ''
    ae_year = ''
    ae_sum = 0

    def __init__(self, in_contract_code, in_ae_year):
        self.contract_code = in_contract_code
        self.ae_year = in_ae_year
        self.ae_sum = get_accrued_expense(self.contract_code,self.ae_year)


# 获取预算项目某个年度的预算金额
class YearAmount:
    budget_code = ''
    budget_year = ''
    year_amount = 0

    def __init__(self, in_budget_code, in_budget_year):
        self.budget_code = in_budget_code
        self.budget_year = in_budget_year
        self.year_amount = get_year_amount(self.budget_code,self.budget_year)


# 获取订单的预提和冲销金额
class OrderAE:
    order_code = ''
    ae_sum = 0
    ae_writeoff_sum = 0
    ae_diff = 0
    order_date_differ = 0
    order_todo = ''

    def __init__(self, in_order_code):
        self.order_code = in_order_code
        self.ae_sum = get_order_ae(in_order_code)
        self.ae_writeoff_sum = get_order_writeoff_ae(in_order_code)
        self.ae_diff = self.ae_sum + self.ae_writeoff_sum - OrderInfoDO.objects.get(order_contract_code=in_order_code).order_amount
        self.ae_diff = float(int(self.ae_diff*1000)/1000)
        self.order_date_differ = (datetime.date.today() - OrderInfoDO.objects.get(
                                     order_contract_code=in_order_code).end_date).days
        if(self.order_date_differ > 0 and self.order_date_differ < 30):
            self.order_todo = '过工作量会'
        elif(self.order_date_differ >= 30 and self.order_date_differ < 60):
            self.order_todo = '付款'
        elif(self.order_date_differ >= 60 ):
            self.order_todo = '已完成'
        else:
            self.order_todo = '执行中'




