# 案例22：抽出-处理修复方案优化

## 系统示意图（AI自动生成）

<table>
<tr>
<td width="58%">
<img src="case_22_pump_and_treat_ai_diagram.png" alt="案例22：抽出-处理修复方案优化系统示意图" width="100%"/>
</td>
<td width="42%">

**AI大模型总结要点**

- 案例背景：污染场地修复，通过抽水井抽出污染地下水处理。
- 核心理论：抽出-处理技术
- 计算任务：模拟抽水修复效果
- 使用说明：版本**: v1.0

> 该图由AI图像生成引擎根据案例描述自动创建，呈现输入条件、物理模型、控制策略与关键指标之间的关系，可作为阅读正文前的快速导览。

</td>
</tr>
</table>



## 案例背景
污染场地修复，通过抽水井抽出污染地下水处理。

## 核心理论
- 抽出-处理技术
- 修复优化
- 费用-效益分析

## 计算任务
1. 模拟抽水修复效果
2. 优化抽水井位置
3. 预测修复时间

## 使用说明
```python
from models.pump_and_treat import PumpAndTreat

model = PumpAndTreat(Lx=200, Ly=200, nx=50, ny=50)
t = np.linspace(0, 365, 200)
t_out, C_history, mass_removed = model.simulate_remediation(t, pump_x=100, pump_y=100, Q_pump=50)
```

**版本**: v1.0
