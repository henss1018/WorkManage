# -*- coding: UTF-8 -*-
from django.db import models


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=2)
    fdate = models.DateField(null=True)
    score = models.FloatField(max_length=4)
    age = models.IntegerField(default=30)


# 预算项目模型类
class BudgetDO(models.Model):
# admin管理页面显示名称
    class Meta:
        verbose_name = '预算项目信息'
        verbose_name_plural = '预算项目信息'
    # 预算项目名称
    budget_name = models.CharField('预算项目名称',max_length=50)
    # 预算项目编码
    budget_code = models.CharField('预算项目编码',max_length=30,unique=True)
    # 集约化编码
    intensive_code = models.CharField('集约化编码',max_length=30,default='0')
    # 开始时间
    start_date = models.DateField('开始时间')
    # 结束时间
    end_date = models.DateField('结束时间')
    # 项目总金额
    budget_amount = models.FloatField('项目总金额',max_length=15)
    # 开发金额
    dev_budget = models.FloatField('开发金额',max_length=15)
    # 维护金额
    mt_budget = models.FloatField('维护金额',max_length=15)
    # 预算会纪要
    doc = models.CharField('预算会纪要',max_length=100)
    # 项目状态（0未开展、1预算会、2采购中、3执行中、4已完成）
    status = models.CharField('项目状态',max_length=10)
    # 项目类型（0框架、1项目）
    type = models.CharField('项目类型',max_length=10)
    # 项目负责人
    leader = models.CharField('项目负责人',max_length=10)

    def __str__(self):
        return self.budget_name


# 自然年预算模型类
class YearBudgetDO(models.Model):
    class Meta:
        verbose_name = '自然年项目预算信息'
        verbose_name_plural = '自然年项目预算信息'
    # 预算编码外键
    budget = models.ForeignKey(BudgetDO, to_field='budget_code', related_name='year_budget_set')
    # 预算项目编码
    budget_code = models.CharField('预算项目编码',max_length=30)
    # 集约化编码
    intensive_code = models.CharField('集约化编码',max_length=30)
    # 自然年度
    year = models.CharField('年度',max_length=10)
    # 年度预算金额
    budget_amount = models.FloatField('年度预算金额',max_length=15)
    # 年度开发金额
    dev_budget = models.FloatField('年度开发金额',max_length=15)
    # 年度维护金额
    mt_budget = models.FloatField('年度维护金额',max_length=15)
    # 已核定未提订单金额
    checked_no_order_amount = models.FloatField('已核定未提订单金额',max_length=15)
    # 已发生未核定金额
    unchecked_amount = models.FloatField('已发生未核定金额',max_length=15)

    def __str__(self):
        return self.budget


# 合同信息模型类
class ContractInfoDO(models.Model):
    class Meta:
        verbose_name = '合同信息'
        verbose_name_plural = '合同信息'
    # 预算编码外键
    budget = models.ForeignKey(BudgetDO, to_field='budget_code', related_name='contract_budget_set')
    # 预算项目编码
    budget_code = models.CharField('预算项目编码',max_length=30)
    # 合同名称
    contract_name = models.CharField('合同名称',max_length=100)
    # 合同编号
    contract_code = models.CharField('合同编号',max_length=30, unique=True)
    # 合同金额
    contract_amount = models.FloatField('合同金额',max_length=15)
    # 开发单价
    dev_price = models.FloatField('开发单价',max_length=15)
    # 维护单价
    mt_price = models.FloatField('维护单价',max_length=15)
    # 开发人天
    dev_workload = models.FloatField('开发人天',max_length=10)
    # 维护人天
    mt_workload = models.FloatField('维护人天',max_length=10)
    # 合作商名称
    vendor_name = models.CharField('合作商名称',max_length=40)
    # 合作商商务联系人
    vendor_contactor = models.CharField('商务联系人',max_length=10)
    # 合作商商务联系电话
    vendor_contactor_phone = models.CharField('联系电话',max_length=20)
    # 合同开始时间
    start_date = models.DateField('合同开始时间')
    # 合同结束时间
    end_date = models.DateField('合同结束时间')
    # 合同状态（执行中、已完成）
    contract_status = models.CharField('合同状态',max_length=10)

    def __str__(self):
        return self.contract_name


# 合同订单模型类
class OrderInfoDO(models.Model):
    class Meta:
        verbose_name = '合同订单信息'
        verbose_name_plural = '合同订单信息'
    # 合同编码外键
    contract = models.ForeignKey(ContractInfoDO, to_field='contract_code',
                                 related_name='contract_order_set')
    # 合同编码
    contract_code = models.CharField('框架合同编码',max_length=30)
    # 订单号
    order_code = models.CharField('订单号',max_length=30)
    # 订单合同编码
    order_contract_code = models.CharField('订单子合同编码',max_length=30)
    # 订单金额
    order_amount = models.FloatField('订单金额',max_length=15)
    # 结算开始时间
    start_date = models.DateField('结算开始时间')
    # 结算结束时间
    end_date = models.DateField('结算结束时间')
    # 是否已核定工作量（0未核定，1已核定）
    workload_checked = models.IntegerField('是否已核定工作量（0未核定，1已核定）')


# 预提信息模型类
class AccruedExpenseInfoDO(models.Model):
    class Meta:
        verbose_name = '合同订单预提信息'
        verbose_name_plural = '合同订单预提信息'
    # 合同编码外键
    contract = models.ForeignKey(ContractInfoDO, to_field='contract_code',
                                 related_name='contract_ae_set')
    # 预提年份
    ae_year = models.CharField('年份',max_length=10)
    # 预提月份
    ae_month = models.CharField('月份',max_length=10)
    # 预提金额
    ae_amount = models.FloatField('预提金额',max_length=15)
    # 冲销金额
    ae_writeoff_amount = models.FloatField('冲销金额',max_length=15)
    # 预提订单编号
    ae_order_code = models.CharField('预提订单子合同编号',max_length=30)
    # 冲销订单编号
    ae_writeoff_order_code = models.CharField('冲销订单子合同编号',max_length=30)
    # 框架合同编号
    contract_code = models.CharField('框架合同编号',max_length=30)
