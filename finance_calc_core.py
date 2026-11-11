# Copyright (c) 2026 张家口海昂网络科技有限公司
# Licensed under the MIT License. See the LICENSE file for details.

"""通用财务指标计算核心库。

本文件只提供纯函数形式的财务指标计算逻辑，不包含图形界面、
文件读写、Excel 导入导出、授权验证或任何交互功能。
"""

from __future__ import annotations


INDICATOR_LABELS = [
    "实收资本（或股本）（万元）",
    "负债总额（万元）",
    "资产总额（万元）",
    "资产负债率",
    "流动资产（万元）",
    "流动负债（万元）",
    "流动比率",
    "速动比率",
    "营业利润（万元）",
    "营业收入净额（万元）",
    "营业利润率",
    "净利润（万元）",
    "平均所有者权益（万元）",
    "净资产收益率"
]


def _safe_div(numerator, denominator):
    """安全除法，除数为 0 或任一入参为空时返回 None。"""
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def _mean(values):
    """计算可参与平均值的数值，忽略 None。"""
    available = [value for value in values if value is not None]
    if not available:
        return None
    return sum(available) / len(available)


def _average_equity(equity_begin, equity_end):
    """计算期初、期末所有者权益的平均值。"""
    if equity_begin is None or equity_end is None:
        return None
    return (equity_begin + equity_end) / 2.0


def compute_indicators_for_year(data):
    """根据单一年度原始科目计算 14 项通用财务指标。

    入参 data 需要包含以下可选键（缺失时按 None 处理）：
        paid_in_capital: 实收资本/股本
        liability_total: 负债总额
        asset_total: 资产总额
        current_assets: 流动资产
        current_liabilities: 流动负债
        inventory: 存货
        revenue: 营业收入
        operating_profit: 营业利润
        net_profit: 净利润
        equity_begin: 年初所有者权益
        equity_end: 年末所有者权益

    出参为长度 14 的列表，顺序与 INDICATOR_LABELS 一致。
    """
    paid = data.get("paid_in_capital")
    liability = data.get("liability_total")
    asset = data.get("asset_total")
    current_assets = data.get("current_assets")
    current_liabilities = data.get("current_liabilities")
    inventory = data.get("inventory")
    revenue = data.get("revenue")
    operating_profit = data.get("operating_profit")
    net_profit = data.get("net_profit")
    equity_begin = data.get("equity_begin")
    equity_end = data.get("equity_end")

    quick_numerator = None
    if current_assets is not None and inventory is not None:
        quick_numerator = current_assets - inventory

    average_equity = _average_equity(equity_begin, equity_end)

    return [
        paid,
        liability,
        asset,
        _safe_div(liability, asset),
        current_assets,
        current_liabilities,
        _safe_div(current_assets, current_liabilities),
        _safe_div(quick_numerator, current_liabilities),
        operating_profit,
        revenue,
        _safe_div(operating_profit, revenue),
        net_profit,
        average_equity,
        _safe_div(net_profit, average_equity),
    ]


def compute_indicators(records, years):
    """计算多个年度的通用财务指标并附带平均列。

    入参：
        records: 年份到原始科目的映射，例如 {"2024": {...}, "2025": {...}}
        years: 有序年份列表，决定输出列顺序。

    出参：
        二维列表，每行第一项为指标名称，随后为各年度数值，
        最后一列为年度平均值。
    """
    rows = [[label] + [None] * (len(years) + 1) for label in INDICATOR_LABELS]

    for col_index, year in enumerate(years):
        values = compute_indicators_for_year(records.get(year, {}))
        for row_index, value in enumerate(values):
            rows[row_index][col_index + 1] = value

    for row_index, row in enumerate(rows):
        year_values = row[1 : 1 + len(years)]
        rows[row_index][1 + len(years)] = _mean(year_values)

    return rows
