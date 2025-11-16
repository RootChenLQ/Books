# 案例20：二维含水层污染羽迁移

## 系统示意图（AI自动生成）

<table>
<tr>
<td width="58%">
<img src="case_20_aquifer_2d_ai_diagram.png" alt="案例20：二维含水层污染羽迁移系统示意图" width="100%"/>
</td>
<td width="42%">

**AI大模型总结要点**

- 案例背景：化工厂渗漏，污染物进入地下水，形成污染羽。
- 核心理论：控制方程**：
- 计算任务：建立2D溶质运移模型
- 使用说明：版本**: v1.0

> 该图由AI图像生成引擎根据案例描述自动创建，呈现输入条件、物理模型、控制策略与关键指标之间的关系，可作为阅读正文前的快速导览。

</td>
</tr>
</table>



## 案例背景
化工厂渗漏，污染物进入地下水，形成污染羽。

## 核心理论

**控制方程**：
```python
∂C/∂t + v·∇C = ∇·(D∇C) - λC
```

## 计算任务
1. 建立2D溶质运移模型
2. 模拟污染羽扩展
3. 预测水井污染风险
4. 评估阻截方案

## 使用说明
```python
from models.aquifer_2d import Aquifer2D

model = Aquifer2D(Lx=500, Ly=300, nx=100, ny=60)
t = np.linspace(0, 365, 200)
t_out, C_history = model.solve_transport(t, vx=0.5, vy=0, Dx=5, Dy=2, source_x=50, source_y=150)
```

**版本**: v1.0
