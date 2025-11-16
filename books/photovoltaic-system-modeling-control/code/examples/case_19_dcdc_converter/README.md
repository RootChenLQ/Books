# 案例19: DC/DC变换器建模

## 系统示意图（AI自动生成）

<table>
<tr>
<td width="58%">
<img src="case_19_dcdc_converter_ai_diagram.png" alt="案例19: DC/DC变换器建模系统示意图" width="100%"/>
</td>
<td width="42%">

**AI大模型总结要点**

- 📖 教学目标：掌握DC/DC变换器的工作原理和数学模型，理解不同拓扑的特点，能够进行仿真分析。
- 🎯 核心理论：DC/DC变换器基本原理
- 💻 代码实现：Boost变换器
- 🧪 实验内容：实验1: Boost升压特性

> 该图由AI图像生成引擎根据案例描述自动创建，呈现输入条件、物理模型、控制策略与关键指标之间的关系，可作为阅读正文前的快速导览。

</td>
</tr>
</table>



## 📖 教学目标

掌握DC/DC变换器的工作原理和数学模型，理解不同拓扑的特点，能够进行仿真分析。

**核心内容**:
1. Boost升压变换器
2. Buck降压变换器
3. Buck-Boost升降压变换器
4. 状态空间平均模型

---

## 🎯 核心理论

### 1. DC/DC变换器基本原理

#### 功能
将直流电压从一个电平转换到另一个电平

**主要类型**:
- **Boost (升压)**: \( V_{out} > V_{in} \)
- **Buck (降压)**: \( V_{out} < V_{in} \)
- **Buck-Boost (升降压)**: \( V_{out} \) 可大可小，但极性反转

#### 工作方式
通过开关管的周期性开关，配合储能元件（电感、电容），实现电压变换

### 2. Boost升压变换器

#### 电路拓扑

```python
Vin --L-- Diode --+-- Cout -- Rload
            |     |
           SW     ⏚
```

#### 工作原理

**开关闭合 (t = D·Ts)**:
- 电感储能: \( v_L = V_{in} \)
- 输出由电容维持

**开关断开 (t = (1-D)·Ts)**:
- 电感放能: \( v_L = V_{in} - V_{out} \)
- 电感电流流向负载

#### 状态空间模型

\[
\begin{cases}
\frac{di_L}{dt} = \frac{1}{L} [V_{in} - (1-d) \cdot v_C] \\
\frac{dv_C}{dt} = \frac{1}{C} [(1-d) \cdot i_L - \frac{v_C}{R}]
\end{cases}
\]

#### 稳态特性

\[
\frac{V_{out}}{V_{in}} = \frac{1}{1 - D}
\]

**特点**:
- 升压比 > 1
- 输入电流连续
- 适合低压输入场景

### 3. Buck降压变换器

#### 电路拓扑

```python
Vin --SW--+-- L --+-- Cout -- Rload
          |       |
        Diode     ⏚
```

#### 状态空间模型

\[
\begin{cases}
\frac{di_L}{dt} = \frac{1}{L} [d \cdot V_{in} - v_C] \\
\frac{dv_C}{dt} = \frac{1}{C} [i_L - \frac{v_C}{R}]
\end{cases}
\]

#### 稳态特性

\[
\frac{V_{out}}{V_{in}} = D
\]

**特点**:
- 降压比 < 1
- 输出电流连续
- 效率高

### 4. Buck-Boost升降压变换器

#### 电路拓扑

```python
Vin --SW--+
          |
          L
          |
     Diode--+-- Cout -- Rload
            |
            ⏚
```

#### 状态空间模型

\[
\begin{cases}
\frac{di_L}{dt} = \frac{1}{L} [d \cdot V_{in} - (1-d) \cdot |v_C|] \\
\frac{dv_C}{dt} = \frac{1}{C} [-(1-d) \cdot i_L - \frac{v_C}{R}]
\end{cases}
\]

#### 稳态特性

\[
\frac{V_{out}}{V_{in}} = -\frac{D}{1 - D}
\]

**特点**:
- 升降压灵活
- 输出极性反转
- 隔离性好

---

## 💻 代码实现

### 1. Boost变换器

```python
from models.dcdc_converter import BoostConverter

# 创建Boost变换器
boost = BoostConverter(
    L=100e-6,   # 100uH电感
    C=100e-6,   # 100uF电容
    R=10.0      # 10Ω负载
)

# 仿真
V_in = 12.0  # 12V输入
d = 0.5      # 50%占空比
dt = 1e-6    # 1us时间步长

for _ in range(10000):
    i_L, v_C = boost.update(V_in, d, dt)

print(f"输出电压: {v_C:.2f}V")
print(f"理论值: {V_in/(1-d):.2f}V")
```python

### 2. Buck变换器

```python
from models.dcdc_converter import BuckConverter

buck = BuckConverter(L=100e-6, C=100e-6, R=10.0)

V_in = 24.0
d = 0.5

for _ in range(10000):
    i_L, v_C = buck.update(V_in, d, dt)

print(f"输出电压: {v_C:.2f}V")
print(f"理论值: {d*V_in:.2f}V")
```python

### 3. Buck-Boost变换器

```python
from models.dcdc_converter import BuckBoostConverter

buck_boost = BuckBoostConverter(L=100e-6, C=100e-6, R=10.0)

V_in = 20.0
d = 0.5

for _ in range(10000):
    i_L, v_C = buck_boost.update(V_in, d, dt)

print(f"输出电压: {abs(v_C):.2f}V (负极性)")
print(f"理论值: {abs(d/(1-d)*V_in):.2f}V")
```matlab

---

## 🧪 实验内容

### 实验1: Boost升压特性

**实验目的**: 验证Boost变换器的升压特性

**实验步骤**:
1. 设置参数: L=100uH, C=100uF, R=10Ω, Vin=12V
2. 测试不同占空比: D = 0.3, 0.5, 0.7, 0.8
3. 记录稳态输出电压
4. 对比理论值

**预期结果**:
| 占空比 | 理论Vout | 实际Vout | 升压比 |
|--------|----------|----------|--------|
| 0.3 | 17.1V | ~17V | 1.43 |
| 0.5 | 24.0V | ~24V | 2.00 |
| 0.7 | 40.0V | ~40V | 3.33 |
| 0.8 | 60.0V | ~60V | 5.00 |

### 实验2: Buck降压特性

**实验目的**: 验证Buck变换器的降压特性

**实验步骤**:
1. 设置参数: L=100uH, C=100uF, R=10Ω, Vin=24V
2. 测试不同占空比: D = 0.2, 0.4, 0.6, 0.8
3. 记录稳态输出电压
4. 对比理论值

**预期结果**:
| 占空比 | 理论Vout | 实际Vout | 降压比 |
|--------|----------|----------|--------|
| 0.2 | 4.8V | ~4.8V | 0.20 |
| 0.4 | 9.6V | ~9.6V | 0.40 |
| 0.6 | 14.4V | ~14.4V | 0.60 |
| 0.8 | 19.2V | ~19.2V | 0.80 |

### 实验3: 三种拓扑对比

**实验目的**: 对比三种拓扑的性能

**实验设置**: 统一条件
- Vin = 20V
- D = 0.5
- L = 100uH, C = 100uF, R = 10Ω

**预期结果**:
| 拓扑 | 输出电压 | 特点 |
|------|----------|------|
| Boost | 40V | 升压，>Vin |
| Buck | 10V | 降压，<Vin |
| Buck-Boost | 20V | 升降压，极性反 |

---

## 📊 性能指标

### 1. 稳态性能

| 指标 | 要求 | 说明 |
|------|------|------|
| 电压精度 | < 5% | 与理论值偏差 |
| 纹波电压 | < 2% | 输出电压波动 |
| 效率 | > 90% | 考虑损耗 |

### 2. 动态性能

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 启动时间 | < 10ms | 达到稳态 |
| 负载响应 | < 5ms | 负载变化 |
| 占空比变化响应 | < 2ms | 参考变化 |

### 3. 参数设计

**电感选择**:
\[
L = \frac{V_{in} \cdot D}{f_s \cdot \Delta i_L}
\]

**电容选择**:
\[
C = \frac{I_{out} \cdot D}{f_s \cdot \Delta v_C}
\]

其中:
- \( f_s \): 开关频率
- \( \Delta i_L \): 电感电流纹波
- \( \Delta v_C \): 电容电压纹波

---

## ⚙️ 工程应用

### 1. 光伏系统中的应用

**Boost变换器**:
- 低压光伏板升压到高压直流母线
- 典型: 30V → 400V

**Buck变换器**:
- 直流母线降压给电池充电
- 典型: 400V → 48V

**Buck-Boost**:
- 电池电压范围宽，需升降压
- 典型: 36-60V → 48V稳定输出

### 2. 参数设计示例

```python
# 光伏Boost设计
V_pv = 30.0  # 光伏电压
V_dc = 400.0  # 直流母线电压
P_rated = 3000.0  # 额定功率3kW
f_s = 20e3  # 20kHz开关频率

# 占空比
D = 1 - V_pv / V_dc  # = 0.925

# 电感设计 (纹波20%)
I_avg = P_rated / V_pv  # 100A
di_L = 0.2 * I_avg  # 20A
L = V_pv * D / (f_s * di_L)  # = 69uH

# 电容设计 (纹波1%)
I_out = P_rated / V_dc  # 7.5A
dv_C = 0.01 * V_dc  # 4V
C = I_out * D / (f_s * dv_C)  # = 86uF

print(f"设计结果: L={L*1e6:.0f}uH, C={C*1e6:.0f}uF")
```python

### 3. 控制策略

**电压模式控制**:
```python
# PI控制器调节占空比
V_ref = 400.0  # 参考电压
V_out = measure_voltage()

error = V_ref - V_out
d = Kp * error + Ki * integral

d = np.clip(d, 0, 0.95)  # 限幅
```

---

## 🎓 作业练习

### 练习1: 参数计算
Boost变换器: Vin=15V, Vout=30V, P=100W
1. 计算占空比
2. 若fs=50kHz，纹波20%，计算L
3. 电容纹波1%，计算C

### 练习2: 拓扑选择
以下场景选择合适拓扑：
1. 12V电池 → 24V负载 (?)
2. 48V母线 → 12V负载 (?)
3. 20-60V输入 → 48V稳定输出 (?)

### 练习3: 性能分析
对比Boost和Buck-Boost升压:
- 效率差异
- 电流应力
- 成本考虑

### 练习4: 仿真实验
修改代码，增加电感ESR (r_L=0.1Ω):
1. 观察效率变化
2. 计算功率损耗
3. 分析温升影响

---

## 📚 扩展阅读

### 进阶拓扑
- Cuk变换器
- SEPIC变换器
- Zeta变换器
- 全桥/半桥拓扑

### 控制策略
- 电流模式控制
- 滑模控制
- 数字控制技术

### 设计优化
- 软开关技术 (ZVS/ZCS)
- 同步整流
- 交错并联

---

## ❓ 常见问题

**Q1: 为什么Boost占空比不能接近1？**
A: 
- D→1时，增益→∞，实际不可能
- 电感电流过大
- 损耗剧增
- 一般限制D<0.9

**Q2: Buck-Boost为什么极性反转？**
A:
- 电路拓扑决定
- 开关闭合：电感储能
- 开关断开：电感反向放电
- 可通过变压器实现同极性

**Q3: 如何选择开关频率？**
A: 权衡考虑：
- 频率高：元件小，响应快，但损耗大
- 频率低：损耗小，但元件大，响应慢
- 一般选择10-100kHz

**Q4: 状态空间模型的假设？**
A:
- 开关理想（无损耗）
- 连续导通模式（CCM）
- 平均化处理
- 小纹波假设

**Q5: 如何提高效率？**
A:
- 选择低导通电阻开关管
- 减小ESR (电感/电容)
- 优化开关频率
- 采用同步整流
- 软开关技术

---

## 📖 参考文献

1. Erickson, R.W., "Fundamentals of Power Electronics"
2. Mohan, N., "Power Electronics"
3. Hart, D.W., "Power Electronics"
4. IEEE标准: IEEE 1547 (并网要求)

---

**实验时间**: 1.5-2小时  
**难度等级**: ⭐⭐  
**前置知识**: 电力电子基础、状态空间模型

**🎊 进入阶段四：直流侧控制的第一步！**
