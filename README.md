# 城市共振：时空噪声色谱

## 项目概述

「城市共振」是一个交互式数据可视化项目，将武汉市噪音投诉数据以矿物色谱和克拉尼图案的形式呈现在地图上。通过时间轴播放，用户可以观察城市噪音在不同时间、不同区域的分布模式和传播特征。

**核心概念**：将每一个噪音投诉事件视为一个「脉冲」，脉冲在空间和时间中扩散，形成类似克拉尼板振动图案的波纹，从而直观展现城市声学空间的共振特性。

---

## 数据结构

### 噪音投诉数据

```json
{
  "lon": 114.3055,        // 经度
  "lat": 30.5928,         // 纬度
  "category_id": 9,       // 噪音类别 (0-17)
  "timestamp": 1664217600, // Unix 时间戳
  "weight": 4.5            // 权重
}
```

### 18 类噪音类型与矿物色谱

| ID | 名称 | 矿物色 | 说明 |
|----|------|--------|------|
| 0 | 基础施工 | 石青 | 大型基础设施建设产生的噪音 |
| 1 | 室内装修 | 石绿 | 住宅/商业室内装修噪音 |
| 2 | 拆除工程 | 石蓝 | 拆迁、破坏性施工 |
| 3 | 工厂运行 | 焦墨 | 工业生产噪音 |
| 4 | 非法排污 | 煤黑 | 工业污染相关 |
| 5 | 中央空调/风机 | 玄青 | HVAC 系统噪音 |
| 6 | 车辆鸣笛 | 铅灰 | 交通噪音-鸣笛 |
| 7 | 重型卡车 | 铁灰 | 货运车辆噪音 |
| 8 | 刹车尖鸣 | 银灰 | 车辆刹车系统 |
| 9 | 广场舞 | 曙红 | 公共活动噪音 |
| 10 | 商业扩音 | 朱砂 | 商铺宣传噪音 |
| 11 | 露天夜市 | 胭脂 | 夜市嘈杂 |
| 12 | 宠物犬吠 | 赭石 | 动物噪音 |
| 13 | 邻里纠纷 | 茶色 | 邻里冲突引发的噪音 |
| 14 | 空调滴水 | 檀棕 | 低频持续噪音 |
| 15 | 救护车/警笛 | 紫檀 | 应急车辆 |
| 16 | 轨道交通 | 青紫 | 地铁/轻轨噪音 |
| 17 | 垃圾清运 | 藕荷 | 环卫作业噪音 |

---

## 核心算法：克拉尼脉冲模型

### 什么是克拉尼图案？

克拉尼图案（Chladni Patterns）是由德国物理学家恩斯特·克拉尼（Ernst Chladni）在18世纪末发现的。当金属板被弓弦激发振动时，细沙会聚集在振动幅度最小的位置（波节），形成美丽对称的几何图案。

**本项目的核心创新**：将这一物理现象反演——不是观察静态的振动模式，而是观察脉冲如何在空间中随时间扩散和衰减。

### 脉冲生成算法

每个噪音投诉事件触发一个「脉冲」对象：

```javascript
class Pulse {
  constructor(x, y, categoryId, weight, pixelRadius) {
    this.x = x;                    // 投诉地点像素坐标 X
    this.y = y;                    // 投诉地点像素坐标 Y
    this.categoryId = categoryId;  // 噪音类别
    this.weight = weight;          // 权重（基于时间）
    this.maxRadius = pixelRadius;  // 最大扩散半径（像素）
    this.radius = 0;               // 当前扩散半径
    this.opacity = 1.0;           // 当前透明度
    this.active = true;           // 是否活跃
    this.phase = random(TWO_PI);  // 随机相位
    this.waveCount = 4-8;         // 波纹层数
    this.wavePhase = 0;            // 波纹相位
    this.dampingPhase = 0;         // 衰减相位
  }
}
```

### 波纹绘制算法

```javascript
drawChladniWave(r, mode) {
  // r: 当前波纹半径
  // mode: 波纹模式 (0, 1, 2, ...)
  beginShape();
  for (let a = 0; a < TWO_PI; a += 0.1) {
    // 克拉尼位移公式
    const displacement = 
      sin(a * (mode + 2) * 2 + phase) * 
      cos(a * (mode + 1) + phase * 0.7);
    
    // 计算波纹上的点
    const px = cos(a) * (r + displacement * 10);
    const py = sin(a) * (r + displacement * 10);
    vertex(px, py);
  }
  endShape(CLOSE);
}
```

### 数学原理解释

**为什么是克拉尼图案？**

克拉尼图案的数学基础是正交的二维波动方程的解：

```
∂²u/∂t² = c²(∂²u/∂x² + ∂²u/∂y²)
```

边界条件决定了节点线的形状。对于圆形区域，解可以写成极坐标形式：

```
u(r, θ, t) = Jₙ(kr)·cos(nθ)·cos(ωt)
```

其中 `Jₙ` 是 n 阶贝塞尔函数。

**本项目的简化模型**：

```javascript
// 位移 = sin(角度 * 频率1 + 相位1) * cos(角度 * 频率2 + 相位2)
displacement = sin(θ × 2n + φ) × cos(θ × n + 0.7φ)
```

这个简化的非线性组合产生了类似克拉尼的复杂但有规律的图案。


**物理类比**：
- 脉冲中心 = 噪音发生源
- 扩散半径 = 噪音传播距离
- 图案变形 = 克拉尼共振模式
- 透明度衰减 = 噪音能量耗散

---

## 参数系统

### 穿透力参数

每种噪音类型有不同的「穿透力」——影响其扩散半径和线条粗细：

```javascript
const PENETRATION = {
  // 基础施工 > 拆除 > 工厂 > 非法排污 > ... > 空调滴水
  baseRadius: [15, 12, 15, 18, 16, 14, 10, 14, 8, 8, 7, 6, 5, 4, 3, 12, 10, 6],
  // 权重也影响线条粗细
  lineWidth: [1, 1, 1, 1.5, 1.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
};
```

**权重计算**：

```javascript
// 基础权重由噪音类型决定
const basePen = [5, 3, 5, 5, 5, 4, 4, 5, 4, 3, 3, 3, 2, 2, 2, 4, 4, 3][categoryId];

// 时间加权：夜间噪音权重更高
if (hour >= 22 || hour <= 5) {
  timeWeight = 3.0;  // 深夜最高
} else if (hour >= 18 && hour < 22) {
  timeWeight = 1.5 + (hour - 18) * 0.375;  // 晚间递增
}

weight = basePen * timeWeight;
```

### 衰减参数

```javascript
// 半径扩张速度 (每帧)
this.radius += (maxRadius - this.radius) * 0.08;

// 衰减速度控制
this.dampingPhase += 0.11;
this.opacity = Math.exp(-this.dampingPhase * 0.15);

// 约4秒后透明度降至 2%，脉冲消失
```

---

## 时间轴系统

### 时间粒度

- 播放模式：每5帧（约12天/秒）前进1天
- 测试模式：静态显示指定日期的所有投诉

### 数据结构优化

```javascript
// 使用指针避免重复遍历
let dataPointer = 0;

function triggerPulsesForDay(dayStart, dayEnd) {
  while (dataPointer < noiseData.length && 
         noiseData[dataPointer].timestamp < dayEnd) {
    // 只处理未触发的数据
    if (!noiseData[dataPointer].triggered) {
      createPulse(noiseData[dataPointer]);
      noiseData[dataPointer].triggered = true;
    }
    dataPointer++;
  }
}
```

---

## 性能优化

### 脉冲数量限制

```javascript
// 限制最大脉冲数量
if (pulses.length > 100) {
  pulses.splice(0, pulses.length - 100);
}
```

### 脉冲生命周期

```
活跃状态: opacity > 0.02
    ↓
更新半径: radius += (maxRadius - radius) * 0.08
    ↓
更新透明度: opacity = exp(-dampingPhase * 0.15)
    ↓
透明度 < 0.02 → 移除脉冲
```

---

## 视觉效果解读

### 波纹形态

当前实现中，所有脉冲以同心圆方式向外扩散，图案的不规则变形由**克拉尼波函数**产生，而非真实物理模拟。

| 视觉元素 | 来源 |
|----------|------|
| 圆形基础 | 脉冲以圆环方式扩散 |
| 不规则图案 | 克拉尼公式 `sin(θ×2n+φ) × cos(θ×n+0.7φ)` |
| 多层嵌套 | 每个脉冲有多层波纹 (4-8层) |
| 颜色差异 | 噪音类别对应的矿物色谱 |
| 透明度变化 | 随时间指数衰减 |

### 叠加原理

当多个脉冲重叠时：
- 颜色混合产生新色调
- 图案干涉产生复杂纹理
- 模拟城市中多噪音源同时作用的效果

> ⚠️ **简化说明**：当前版本使用简化的同心圆扩散模型，未考虑建筑物遮挡、地形阻隔等物理因素。这是有意为之的艺术化处理，而非物理模拟。如需真实声波传播模拟，可接入城市建筑数据进行路径追踪计算。

---

## 扩展方向

1. **声音模拟**: 接入 Web Audio API，根据噪音类型播放对应声音
2. **3D 模式**: 使用 Three.js 实现立体克拉尼图案
3. **建筑物遮挡**: 接入城市建筑 GIS 数据，模拟声波绕过障碍物传播
4. **历史对比**: 添加多城市对比视图
5. **实时数据**: 对接政务 API 实现实时投诉可视化

---

## 技术栈

- **地图引擎**: Mapbox GL JS (CARTO 暗色底图)
- **动画引擎**: p5.js (HTML5 Canvas)
- **数据格式**: JSON
- **开发语言**: 原生 JavaScript

---

## 使用说明

1. **播放/暂停**: 控制时间轴播放
2. **测试第一天**: 查看数据起始日的投诉分布
3. **测试指定日期**: 查看任意日期的投诉分布
4. **拖拽地图**: 缩放和移动视图

---

## 扩展方向

1. **声音模拟**: 接入 Web Audio API，根据噪音类型播放对应声音
2. **3D 模式**: 使用 Three.js 实现立体克拉尼图案
3. **历史对比**: 添加多城市对比视图
4. **实时数据**: 对接政务 API 实现实时投诉可视化
5. **建筑影响**：考虑建筑物等障碍物影响声波传播

---

## 参考文献

1. Chladni, E. F. F. (1787). *Entdeckungen über die Theorie des Klanges*
2. Rossing, T. D. (1982). *Chladni's Law and the Modern Physics of Vibration*
3. Mapbox GL JS Documentation
4. p5.js Reference Documentation
