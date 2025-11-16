# 案例21：多层含水层垂向迁移

## 系统示意图（AI自动生成）

<table>
<tr>
<td width="58%">
<img src="case_21_multilayer_aquifer_ai_diagram.png" alt="案例21：多层含水层垂向迁移系统示意图" width="100%"/>
</td>
<td width="42%">

**AI大模型总结要点**

- 案例背景：垃圾填埋场渗滤液污染潜水和承压含水层。
- 核心理论：多层含水层系统
- 计算任务：建立多层模型
- 使用说明：版本**: v1.0

> 该图由AI图像生成引擎根据案例描述自动创建，呈现输入条件、物理模型、控制策略与关键指标之间的关系，可作为阅读正文前的快速导览。

</td>
</tr>
</table>



## 案例背景
垃圾填埋场渗滤液污染潜水和承压含水层。

## 核心理论
- 多层含水层系统
- 垂向扩散
- 隔水层保护

## 计算任务
1. 建立多层模型
2. 模拟垂向迁移
3. 评估隔水层保护效果

## 使用说明
```python
from models.multilayer_aquifer import MultilayerAquifer

model = MultilayerAquifer(layers=20, dz=2)
t = np.linspace(0, 365, 200)
t_out, z_out, C_history = model.solve(t, Kz=0.1, theta=0.3)
```

**版本**: v1.0
