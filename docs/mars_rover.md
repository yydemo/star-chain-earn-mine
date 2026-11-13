# 火星车场景扩展：把 CMR 仿真搬到火星 / Mars Rover Scenario: Moving the CMR Simulation to Mars

> 语言说明 / Language note：本文中英双语，先中文后英文。 / This document is bilingual: Chinese first, then English.

> 本项目核心决策闭环（`simulation/rover_sim.py`）现已支持 `--world mars`，可直接在火星参数下跑通勘探—去噪—检测—采矿闭环。
> 本文说明两件事：① 火星世界在仿真里的物理/光谱差异；② 如何用 **MARE 月球车仿真（含玉兔号模型）** 做高保真火星视觉仿真，与 `rover_sim.py` 的 AI 逻辑闭环对接。
>
> The project's core decision loop (`simulation/rover_sim.py`) now supports `--world mars`, running the explore — denoise — detect — mine loop directly with Mars parameters.
> This document covers two things: ① the physical/spectral differences of the Mars world in the simulation; ② how to use the **MARE lunar rover simulator (including the Yutu model)** for high-fidelity Mars visual simulation connected to the AI logic loop of `rover_sim.py`.

---

## 1. 火星世界在 `rover_sim.py` 里的差异（`WORLD_PROFILES["mars"]`） / 1. Mars World Differences in `rover_sim.py` (`WORLD_PROFILES["mars"]`)

| 维度 / Dimension | generic（默认/类月） / generic (default / moon-like) | mars（火星） / mars (Mars) |
|---|---|---|
| 风化层光谱 / Regolith spectrum | 平坦偏亮 `0.70…0.60` / Flat, fairly bright `0.70…0.60` | **红色** `0.85,0.70,0.55,0.50,0.45,0.40`（红高蓝低） / **Red** `0.85,0.70,0.55,0.50,0.45,0.40` (high red, low blue) |
| 目标矿 / Target ore | 金属/稀土 `ore deposit` / Metal / rare earth `ore deposit` | **含水矿物 / 水冰** `water-ice / hydrated mineral`（近红外强峰） / **Hydrated minerals / water ice** `water-ice / hydrated mineral` (strong NIR peak) |
| 围岩 / Host rock | 硅酸盐平缓 / Silicate, gentle | 玄武岩偏暗 / Basalt, darker |
| 太阳日 / Solar day | 40 步，白天占 70% / 40 steps, 70% daylight | 50 步（≈火星太阳日 24.6h），白天占 60% / 50 steps (≈ a 24.6 h Martian sol), 60% daylight |
| 太阳能增益 / Solar gain | 白天 0.8 / 夜 0.1 / Day 0.8 / night 0.1 | 白天 0.7 / 夜 0.08（稀薄大气 + 尘埃衰减） / Day 0.7 / night 0.08 (thin atmosphere + dust attenuation) |
| 重力 / Gravity | 1.62 m/s²（类月 / moon-like） | **3.71 m/s²**（火星，计入统计 / Mars, included in stats） |
| 尘暴 / Dust storms | 无 / None | **周期性全球尘暴**：`period=160 / duration=22` 步，噪声×2.3、太阳能×0.18 / **Periodic global dust storms**: `period=160 / duration=22` steps, noise ×2.3, solar ×0.18 |
| 地图配色 / Map colours | 金→蓝 / Gold → blue | 红棕底 + **青→白**（水冰）矿脉 / Red-brown background + **cyan → white** (water-ice) veins |

尘暴是关键新变量：尘埃遮蔽太阳使充电骤降、同时抬高传感器噪声（仍由 `denoise_spectrum` 去噪兜底）。验证运行（`--world mars --steps 600`）触发 **87 步尘暴**，探测精确率仍达 **1.00**，说明 ASTERIS 风格去噪在噪声放大下依然稳健。

Dust storms are the key new variable: dust blocks the sun so charging drops sharply, while sensor noise rises (still handled by `denoise_spectrum`). A validation run (`--world mars --steps 600`) triggered **87 storm steps** and detection precision still reached **1.00**, showing that ASTERIS-style denoising stays robust under amplified noise.

---

## 2. 运行 / 2. Running

```bash
cd simulation
pip install -r requirements.txt        # 仅需 numpy / only numpy needed
python rover_sim.py --world mars --steps 600 --out map_mars.svg
python rover_sim.py --world generic --steps 400 --out map_generic.svg   # 对照 / baseline
```

输出：`map_mars.svg`（轨迹/水冰矿脉/采矿点）、`telemetry.csv`（新增 `storm` 列标记尘暴步）、`summary.txt`（含天体/尘暴/重力）。

Outputs: `map_mars.svg` (trajectory / water-ice veins / mining points), `telemetry.csv` (new `storm` column marking storm steps), `summary.txt` (body / dust storms / gravity).

---

## 3. 与 MARE 月球车仿真对接（高保真火星视觉） / 3. Connecting to the MARE Lunar Rover Simulator (High-Fidelity Mars Visuals)

`MARE-Lunar-Simulator-main` 是 Unreal Engine 5 + ROS 2 的**月球车仿真**，内置 **玉兔号（Yutu，嫦娥三号）** 模型与月球地形（环形山、岩石、低太阳角）、5040 帧数据集。把它改造为火星视觉仿真有三步：

`MARE-Lunar-Simulator-main` is an Unreal Engine 5 + ROS 2 **lunar rover simulator** with a built-in **Yutu (Chang'e-3)** model, lunar terrain (craters, rocks, low sun angle) and a 5,040-frame dataset. Adapting it into a Mars visual simulation takes three steps:

1. **换天体与地形**：用 UE5 资产替换月面为火星场景——红色风化层、玄武岩碎石、低大气散射（火星天空偏橙红）、低太阳角。可用 MARE 自带地形生成器改参数（更细的尘埃、更暗的全局光）。
   **Swap the body and terrain**: replace the lunar surface with a Mars scene using UE5 assets — red regolith, basalt rubble, low atmospheric scattering (orange-red Martian sky), low sun angle. MARE's built-in terrain generator can be re-parameterized (finer dust, darker global light).
2. **换车**：把 MARE 的 `Yutu` 漫游车（或 Leo_Raph）模型替换为基于 **OOMWOO 底座**改装的 CMR 火星车（不锈钢外壳 + 钻采工具头 + 抗辐射算力板，见 `hardware_mod.md` / `guangzhou_semi.md`）。
   **Swap the rover**: replace MARE's `Yutu` rover (or Leo_Raph) model with the CMR Mars rover converted from the **OOMWOO base** (stainless-steel shell + drilling tool head + rad-hard compute board; see `hardware_mod.md` / `guangzhou_semi.md`).
3. **接 AI 闭环**：MARE 的 ROS 2 GNC 栈（导航/SLAM）负责"动"，把本项目的 `ai_core.denoise_spectrum` + `OreDetector` 作为**感知插件**挂到相机/光谱 topic 上；`rover_sim.py` 作为**任务级数字孪生**做规划与遥测回放。
   **Connect the AI loop**: MARE's ROS 2 GNC stack (navigation/SLAM) handles "motion"; attach this project's `ai_core.denoise_spectrum` + `OreDetector` as **perception plugins** on the camera/spectral topics; `rover_sim.py` serves as the **mission-level digital twin** for planning and telemetry replay.

> 分工：`rover_sim.py` = 可跑的逻辑闭环 + 决策验证（快、可批量、可上链）；MARE = 高保真视觉/动力学渲染（演示与训练数据）。两者共享同一套矿石光谱签名与状态机语义。
>
> Division of labour: `rover_sim.py` = runnable logic loop + decision validation (fast, batchable, on-chain); MARE = high-fidelity visual/dynamics rendering (demos and training data). Both share the same ore spectral signatures and state-machine semantics.

---

## 4. 火星车设计参考（真实巡视器） / 4. Mars Rover Design References (Real Rovers)

| 巡视器 / Rover | 可借鉴点 / Takeaways |
|---|---|
| NASA 勇气号/机遇号（MER） / NASA Spirit/Opportunity (MER) | 太阳阵 + 防尘策略、六轮摇臂悬架（适合碎石） / Solar arrays + dust strategy, six-wheel rocker-bogie suspension (good on rubble) |
| 好奇号/毅力号（MER-A/B 后续） / Curiosity/Perseverance (successors to MER-A/B) | 核电源（RTG，不受尘暴断电影响）、 drill 取芯、样本缓存 / Nuclear power (RTG, unaffected by dust-storm outages), drill coring, sample caching |
| 玉兔号（MARE 内模型） / Yutu (model in MARE) | 国产月球车构型参考，可直接在 MARE 中复用其动力学 / Reference configuration of a Chinese lunar rover; its dynamics can be reused directly in MARE |

> 诚实提示：火星全球尘暴可持续数周，纯太阳能 CMR 需配合**储能/同位素**冗余（见 `hardware_mod.md` 电源方案），尘暴期的低充电已在仿真中用 `solar_mult` 体现。
>
> Honest note: Martian global dust storms can last weeks, so a purely solar CMR needs **energy-storage / radioisotope** redundancy (see the power plan in `hardware_mod.md`); low charging during storms is already modelled in the simulation via `solar_mult`.
