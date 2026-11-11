# 通用财务指标计算核心库

本仓库仅为财务指标计算核心，采用 MIT 开源许可；桌面软件闭源商用版见辅之以效官网。

本项目只提供纯函数形式的财务指标计算逻辑，可独立运行和测试，不包含 GUI、Excel 导入导出、文件读写、网络请求、授权校验或任何交互功能。

## 功能清单

- 14 项通用财务指标计算
- 多年度指标与平均列计算
- 纯函数实现，无文件读写、无网络请求
- 仅使用 Python 标准库

## 快速示例

```python
from finance_calc_core import compute_indicators

data = {
    "paid_in_capital": 100,
    "liability_total": 200,
    "asset_total": 500,
    "current_assets": 150,
    "current_liabilities": 80,
    "inventory": 40,
    "revenue": 600,
    "operating_profit": 90,
    "net_profit": 60,
    "equity_begin": 280,
    "equity_end": 300,
}

rows = compute_indicators({"2024": data}, ["2024"])
for row in rows:
    print(row)
```

## 免责声明

计算结果仅供参考，不构成审计、税务或法律意见，使用者需自行核验结果。详见 [DISCLAIMER.md](./DISCLAIMER.md)。

## 协议

本项目采用 MIT 协议，详见 [LICENSE](./LICENSE)。
