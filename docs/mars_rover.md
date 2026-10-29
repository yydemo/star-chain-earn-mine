# 火星车场景扩展：把 CMR 仿真搬到火星

> 本项目核心决策闭环（`simulation/rover_sim.py`）现已支持 `--world mars`，可直接在火星参数下跑通勘探—去噪—检测—采矿闭环。
> 本文说明两件事：① 火星世界在仿真里的物理/光谱差异；② 如何用 **MARE 月球车仿真（含玉兔号模型）** 做高保真火星视觉仿真，与 `rover_sim.py` 的 AI 逻辑闭环对接。

---

## 1. 火星世界在 `rover_sim.py` 里的差异（`WORLD_PROFILES["mars"]`）

| 维度 | generic（默认/类月） | mars（火星） |
|---|---|---|
| 风化层光谱 | 平坦偏亮 `0.70…0.60` | **红色** `0.85,0.70,0.55,0.50,0.45,0.40`（红高蓝低） |
| 目标矿 | 金属/稀土 `ore deposit` | **含水矿物 / 水冰** `water-ice / hydrated mineral`（近红外强峰） |
| 围岩 | 硅酸盐平缓 | 玄武岩偏暗 |
| 太阳日 | 40 步，白天占 70% | 50 步（≈火星太阳日 24.6h），白天占 60% |
| 太阳能增益 | 白天 0.8 / 夜 0.1 | 白天 0.7 / 夜 0.08（稀薄大气 + 尘埃衰减） |
| 重力 | 1.62 m/s²（类月） | **3.71 m/s²**（火星，计入统计） |
| 尘暴 | 无 | **周期性全球尘暴**：`period=160 / duration=22` 步，噪声×2.3、太阳能×0.18 |
| 地图配色 | 金→蓝 | 红棕底 + **青→白**（水冰）矿脉 |

尘暴是关键新变量：尘埃遮蔽太阳使充电骤降、同时抬高传感器噪声（仍由 `denoise_spectrum` 去噪兜底）。验证运行（`--world mars --steps 600`）触发 **87 步尘暴**，探测精确率仍达 **1.00**，说明 ASTERIS 风格去噪在噪声放大下依然稳健。

---

## 2. 运行

```bash
cd simulation
pip install -r requirements.txt        # 仅需 numpy
python rover_sim.py --world mars --steps 600 --out map_mars.svg
python rover_sim.py --world generic --steps 400 --out map_generic.svg   # 对照
```

输出：`map_mars.svg`（轨迹/水冰矿脉/采矿点）、`telemetry.csv`（新增 `storm` 列标记尘暴步）、`summary.txt`（含天体/尘暴/重力）。

---

## 3. 与 MARE 月球车仿真对接（高保真火星视觉）

`MARE-Lunar-Simulator-main` 是 Unreal Engine 5 + ROS 2 的**月球车仿真**，内置 **玉兔号（Yutu，嫦娥三号）** 模型与月球地形（环形山、岩石、低太阳角）、5040 帧数据集。把它改造为火星视觉仿真有三步：

1. **换天体与地形**：用 UE5 资产替换月面为火星场景——红色风化层、玄武岩碎石、低大气散射（火星天空偏橙红）、低太阳角。可用 MARE 自带地形生成器改参数（更细的尘埃、更暗的全局光）。
2. **换车**：把 MARE 的 `Yutu` 漫游车（或 Leo_Raph）模型替换为基于 **OOMWOO 底座**改装的 CMR 火星车（不锈钢外壳 + 钻采工具头 + 抗辐射算力板，见 `hardware_mod.md` / `guangzhou_semi.md`）。
3. **接 AI 闭环**：MARE 的 ROS 2 GNC 栈（导航/SLAM）负责"动"，把本项目的 `ai_core.denoise_spectrum` + `OreDetector` 作为**感知插件**挂到相机/光谱 topic 上；`rover_sim.py` 作为**任务级数字孪生**做规划与遥测回放。

> 分工：`rover_sim.py` = 可跑的逻辑闭环 + 决策验证（快、可批量、可上链）；MARE = 高保真视觉/动力学渲染（演示与训练数据）。两者共享同一套矿石光谱签名与状态机语义。

---

## 4. 火星车设计参考（真实巡视器）

| 巡视器 | 可借鉴点 |
|---|---|
| NASA 勇气号/机遇号（MER） | 太阳阵 + 防尘策略、六轮摇臂悬架（适合碎石） |
| 好奇号/毅力号（MER-A/B 后续） | 核电源（RTG，不受尘暴断电影响）、 drill 取芯、样本缓存 |
| 玉兔号（MARE 内模型） | 国产月球车构型参考，可直接在 MARE 中复用其动力学 |

> 诚实提示：火星全球尘暴可持续数周，纯太阳能 CMR 需配合**储能/同位素**冗余（见 `hardware_mod.md` 电源方案），尘暴期的低充电已在仿真中用 `solar_mult` 体现。
