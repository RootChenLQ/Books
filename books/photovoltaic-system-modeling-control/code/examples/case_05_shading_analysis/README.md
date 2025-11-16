# 案例5: 遮挡分析与诊断

## 系统示意图（AI自动生成）

<table>
<tr>
<td width="58%">
<img src="case_05_shading_analysis_ai_diagram.png" alt="案例5: 遮挡分析与诊断系统示意图" width="100%"/>
</td>
<td width="42%">

**AI大模型总结要点**

- 📋 案例概述：工程背景**:
- 🔬 理论基础：遮挡效应
- 💻 代码示例：遮挡模式分析
- 📊 遮挡场景对比：典型遮挡场景

> 该图由AI图像生成引擎根据案例描述自动创建，呈现输入条件、物理模型、控制策略与关键指标之间的关系，可作为阅读正文前的快速导览。

</td>
</tr>
</table>



## 📋 案例概述

**工程背景**:
光伏系统运行中常遇到遮挡问题,导致:
- 功率大幅损失
- 热斑效应风险
- 组件永久损坏
- 系统故障停机

**常见遮挡源**:
- 建筑物/树木阴影
- 灰尘/鸟粪/落叶
- 雪覆盖
- 组件老化不均

**学习目标**:
1. 掌握遮挡模式识别方法
2. 学习热斑风险评估技术
3. 理解I-V曲线诊断原理
4. 掌握故障定位方法

---

## 🔬 理论基础

### 遮挡效应

**串联特性影响**:
```python
串联电路: I_string = min(I1, I2, ..., In)
→ 最弱电池限制整串电流
→ 功率损失远大于遮挡面积比例
```

**功率损失非线性**:
- 5%面积遮挡 → 可能损失20-30%功率
- 整组遮挡 → 旁路二极管导通
- 分散遮挡 → 影响更严重

### 热斑效应

**形成机制**:
```python
1. 遮挡电池产生负电压
2. 消耗功率而非产生功率
3. 转化为热量
4. 温度升高(可达150°C)
5. 永久损坏
```

**热斑温度**:
- 正常运行: 40-60°C
- 轻度热斑: 60-80°C
- 严重热斑: 80-120°C
- 危险: >120°C

### I-V曲线特征

**正常曲线**:
- 平滑单调下降
- 无台阶
- FF > 0.70

**遮挡曲线**:
- 出现台阶
- 多个局部峰值
- FF显著下降

**故障曲线**:
- 开路: I ≈ 0
- 短路: V ≈ 0
- 低Rsh: 曲线弯曲
- 高Rs: FF下降

---

## 💻 代码示例

### 1. 遮挡模式分析

```python
from code.models.pv_cell import SingleDiodeModel
from code.models.pv_module import PVModule
from code.models.pv_diagnostics import ShadingAnalyzer

# 创建组件
cell = SingleDiodeModel(Isc=8.0, Voc=0.6, Imp=7.5, Vmp=0.48)
module = PVModule(cell_model=cell, Ns=60, Nb=3)

# 创建分析器
analyzer = ShadingAnalyzer(module)

# 定义遮挡场景
irradiances = [1000.0] * 40 + [200.0] * 20  # 后20片遮挡

# 分析遮挡模式
result = analyzer.analyze_shading_pattern(irradiances)

print(f"遮挡电池数: {result['num_shaded_cells']}/{module.Ns}")
print(f"遮挡比例: {result['shading_ratio']*100:.1f}%")
print(f"严重程度: {result['severity']}")
print(f"受影响组: {result['num_affected_groups']}/{module.Nb}")
```python

输出:
```
遮挡电池数: 20/60
遮挡比例: 33.3%
严重程度: 中度遮挡
受影响组: 1/3
```python

### 2. 热斑风险评估

```python
# 热斑风险检测
hotspot_result = analyzer.detect_hot_spot_risk(irradiances)

print(f"最弱电池: #{hotspot_result['weakest_cell_index']}")
print(f"辐照度: {hotspot_result['weakest_cell_irradiance']} W/m²")
print(f"预估温升: {hotspot_result['estimated_temp_rise']:.1f}°C")
print(f"风险等级: {hotspot_result['risk_level']}")
print(f"旁路激活: {'是' if hotspot_result['will_bypass_activate'] else '否'}")
```python

输出:
```
最弱电池: #59
辐照度: 200.0 W/m²
预估温升: 75.0°C
风险等级: 高风险
旁路激活: 是
```python

### 3. 功率损失估算

```python
# 功率损失分析
loss_result = analyzer.estimate_power_loss(irradiances)

print(f"基准功率: {loss_result['baseline_power']:.2f} W")
print(f"遮挡功率: {loss_result['shaded_power']:.2f} W")
print(f"功率损失: {loss_result['power_loss']:.2f} W")
print(f"损失比例: {loss_result['loss_percentage']:.1f}%")
```python

### 4. I-V曲线诊断

```python
from code.models.pv_diagnostics import IVCurveDiagnostics

# 创建诊断器
diagnostics = IVCurveDiagnostics()

# 获取I-V曲线
V, I = module.get_iv_curve(300)

# 曲线分析
analysis = diagnostics.analyze_curve_shape(V, I)

print(f"Isc: {analysis['Isc']:.2f} A")
print(f"Voc: {analysis['Voc']:.2f} V")
print(f"Pmpp: {analysis['Pmpp']:.2f} W")
print(f"FF: {analysis['FF']:.3f}")
print(f"台阶数: {analysis['num_steps']}")
print(f"遮挡: {'是' if analysis['has_shading'] else '否'}")
```python

### 5. 故障检测

```python
# 参考参数(正常条件)
reference = {
    'Voc': 36.0,
    'Isc': 8.0,
    'FF': 0.75
}

# 故障检测
faults = diagnostics.detect_faults(V, I, reference)

print("故障诊断:")
for fault in faults:
    print(f"  • {fault}")
```python

输出:
```
故障诊断:
  • 检测到遮挡特征 - 3个台阶
  • 短路电流过低 - 可能遮挡或污染
```python

### 6. 性能评估

```python
from code.models.pv_diagnostics import PerformanceEvaluator

evaluator = PerformanceEvaluator()

# 系统健康评估
health = evaluator.evaluate_system_health(
    current_power=850,      # 当前功率(W)
    rated_power=1000,       # 额定功率(W)
    irradiance=1000,        # 辐照度(W/m²)
    temperature=25          # 温度(°C)
)

print(f"当前功率: {health['current_power']} W")
print(f"期望功率: {health['expected_power']:.0f} W")
print(f"性能比: {health['pr_percentage']:.1f}%")
print(f"健康评级: {health['health_grade']}")
```matlab

---

## 📊 遮挡场景对比

### 典型遮挡场景

| 场景 | 遮挡面积 | 遮挡分布 | 功率损失 | 热斑风险 | 旁路导通 |
|------|----------|----------|----------|----------|----------|
| 无遮挡 | 0% | - | 0% | 无 | 否 |
| 轻度 | 5-10% | 分散 | 10-20% | 低 | 否 |
| 中度 | 20-30% | 集中 | 30-50% | 中 | 可能 |
| 严重 | 30-50% | 整组 | 50-70% | 高 | 是 |
| 极端 | >50% | 多组 | >70% | 极高 | 是 |

### 遮挡源对比

| 遮挡源 | 持续时间 | 可预测性 | 清洁难度 | 预防措施 |
|--------|----------|----------|----------|----------|
| 建筑阴影 | 每日/季节 | 高 | N/A | 选址优化 |
| 树木阴影 | 每日/季节 | 中 | N/A | 修剪/移除 |
| 灰尘 | 长期 | 低 | 中 | 定期清洗 |
| 鸟粪 | 短期 | 低 | 易 | 驱鸟装置 |
| 积雪 | 季节 | 中 | 难 | 倾角设计 |
| 落叶 | 季节 | 中 | 易 | 定期清理 |

---

## 🎯 诊断流程

### 现场诊断步骤

```
步骤1: 目视检查
  → 观察组件表面
  → 识别明显遮挡物
  → 检查接线盒

步骤2: 红外热成像
  → 扫描组件表面温度
  → 识别热斑位置
  → 评估严重程度

步骤3: I-V曲线测试
  → 测量组串I-V曲线
  → 对比标准曲线
  → 识别异常特征

步骤4: 故障定位
  → 确定问题组件
  → 分析故障原因
  → 制定修复方案

步骤5: 验证修复
  → 清理/更换组件
  → 重新测试
  → 确认性能恢复
```

### 诊断工具

**必备工具**:
- I-V曲线测试仪
- 红外热像仪
- 万用表
- 钳形电流表

**辅助工具**:
- 无人机(屋顶巡检)
- 清洁工具
- 记录表格

---

## 💡 最佳实践

### 预防措施

**1. 选址阶段**
- 避开高大建筑/树木
- 评估全年阴影
- 预留安全距离

**2. 设计阶段**
- 优化组件布局
- 合理配置旁路二极管
- 考虑清洁通道

**3. 运维阶段**
- 定期清洗(每季度)
- 定期巡检(每月)
- 及时修剪树木

### 清洁频率

**建议周期**:
- 沙尘地区: 每月1次
- 普通地区: 每季度1次
- 清洁地区: 每半年1次
- 雨季后: 加强清洗

**清洁方法**:
- 纯水冲洗(推荐)
- 软毛刷清扫
- 专业清洗剂
- 避免硬物刮擦

### 监控告警

**设置阈值**:
- 功率下降>10%: 警告
- 功率下降>20%: 告警
- 热斑温度>80°C: 紧急
- FF<0.65: 异常

---

## 📝 思考题

1. **为什么5%的遮挡可能导致30%的功率损失?**

2. **旁路二极管能完全消除遮挡影响吗?**

3. **如何区分遮挡和组件老化?**

4. **什么情况下应立即停机检修?**

---

## 📚 作业

### 基础题

**作业1**: 分析不同遮挡模式(集中vs分散)的功率损失差异。

**作业2**: 设计一个热斑检测算法,基于温度阈值。

**作业3**: 编写I-V曲线自动诊断程序。

### 进阶题

**作业4**: 建立遮挡-功率损失预测模型。

**作业5**: 设计基于无人机的光伏电站巡检方案。

**作业6**: 开发光伏电站健康监控系统。

---

## ✅ 检查清单

完成本案例后,你应该能够:

- [ ] 识别不同遮挡模式
- [ ] 评估热斑风险等级
- [ ] 分析I-V曲线异常
- [ ] 进行故障诊断定位
- [ ] 估算功率损失
- [ ] 制定预防措施
- [ ] 设计监控告警系统

---

**案例5完成!** 🎉

下一步: [案例6 - 参数辨识方法](../case_06_parameter_identification/README.md)
