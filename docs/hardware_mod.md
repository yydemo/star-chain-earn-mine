# 硬件改装指南：扫地机器人 → 宇宙挖矿机器人 / Hardware Modification Guide: Robot Vacuum → Cosmic Mining Robot

> 语言说明 / Language note：本文中英双语，先中文后英文。 / This document is bilingual: Chinese first, then English.

目标：以开源扫地机器人为**移动底座**，保留其差速底盘与导航能力，替换为"挖矿"执行端与"抗辐射"算力/电源，使其能在地外环境作业。

Goal: use an open-source robot vacuum as the **mobile base**, keep its differential chassis and navigation, and replace the rest with a "mining" end-effector and "radiation-hardened" compute/power so it can work in extraterrestrial environments.

---

## 1. 保留（直接复用扫地机器人底座） / 1. Keep (Reuse the Robot-Vacuum Base Directly)
| 子系统 / Subsystem | 说明 / Description | 来源 / Source |
|---|---|---|
| 差速底盘 + 轮编码器 / Differential chassis + wheel encoders | 表面移动与里程计 / Surface movement and odometry | OOMWOO / Robovacuum_Robot |
| 2D LiDAR / ToF / IMU | 避障与建图 / Obstacle avoidance and mapping | 底座自带 / Built into the base |
| ROS 2 + Nav2 | 导航与全覆盖路径规划 / Navigation and full-coverage path planning | 开源导航栈 / Open-source navigation stack |
| 电源管理框架 / Power management framework | 电池/充电逻辑（改为太阳能） / Battery/charging logic (switched to solar) | 底座改造 / Modified base |

## 2. 移除 / 2. Remove
- 离心风机 + 尘盒（吸尘系统） / Centrifugal fan + dust box (vacuum system)
- 滚刷/边刷（清扫机构） / Roller brush / side brushes (cleaning mechanism)
- 回充基站（改为太阳能阵 + 同位素/二次电池） / Charging dock (replaced by a solar array + radioisotope/rechargeable batteries)

## 3. 新增 / 替换 / 3. Add / Replace
### 3.1 不锈钢轻量化外壳（316L 或钛合金） / 3.1 Lightweight stainless-steel shell (316L or titanium alloy)
- 作用：抗月面/小行星昼夜 ±150℃ 温差、抗微流星撞击、可焊接维修。
  Purpose: withstand ±150 °C day-night swings on the Moon/asteroids, resist micrometeoroid impacts, and allow weld repairs.
- 工艺：激光切割 + 折弯 + TIG 焊接；内部用不锈钢骨架兼作**散热鳍片**与**被动粒子屏蔽层**。
  Process: laser cutting + bending + TIG welding; an internal stainless-steel frame doubles as **cooling fins** and a **passive particle-shielding layer**.
- 减重要点：薄壁蜂窝夹层结构；非承力件用工程塑料/铝。
  Weight-saving tips: thin-walled honeycomb sandwich structures; engineering plastics/aluminium for non-load-bearing parts.

### 3.2 挖矿工具头（替换吸尘） / 3.2 Mining tool head (replaces vacuuming)
- 钻探/研磨头（旋转冲击钻，针对风化层/岩石） / Drilling/grinding head (rotary percussion drill for regolith/rock)
- 样品仓（分格存储，按品位分类） / Sample bay (compartmentalized storage, sorted by grade)
- 可选：爪式抓取臂（小行星漂浮采样） / Optional: claw-type grabbing arm (floating sampling on asteroids)

### 3.3 抗辐射算力与电源（西电三代半 + 广州产业链） / 3.3 Rad-hard compute and power (Xidian 3rd-gen semiconductors + Guangzhou industry chain)
> 关键事实：西安电子科技大学芜湖研究院的**抗辐射 SiC 功率器件**已随**天舟六号**入空间站、在 LEO 卫星验证；西电**广州第三代半导体创新中心**（黄埔·中新知识城，郝跃院士领衔）已通线 **6–8 英寸 GaN 全流程中试线**，且官方明确 GaN 具备**抗辐射/耐高温/耐高压/大功率**特性；**南沙万顷沙**是国内首个第三代半导体全产业链（南砂晶圆 12 英寸 SiC 衬底、芯粤能车规级 SiC 芯片、芯聚能 SiC 功率模块）。详见 `docs/guangzhou_semi.md`。
>
> Key facts: the **rad-hard SiC power devices** of Xidian University's Wuhu Research Institute went to the space station on **Tianzhou-6** and were validated on LEO satellites; Xidian's **Guangzhou Third-Generation Semiconductor Innovation Center** (Huangpu, Sino-Singapore Guangzhou Knowledge City, led by Academician Hao Yue) has brought a **6–8-inch full-process GaN pilot line** into operation, and officially states that GaN is **radiation-resistant / high-temperature / high-voltage / high-power**; **Wanqingsha in Nansha** is China's first complete third-generation semiconductor industry chain (Nansha Wafer 12-inch SiC substrates, Xinyueneng automotive-grade SiC chips, Xinjuneng SiC power modules). See `docs/guangzhou_semi.md`.

- **功率级**：采用西电抗辐射 SiC MOSFET（裂栅加固、抗单粒子）做电源变换（太阳能 MPPT、电机驱动、二次电源）。
  **Power stage**: use Xidian rad-hard SiC MOSFETs (split-gate hardened, single-event resistant) for power conversion (solar MPPT, motor drive, secondary power).
- **计算 SoC（GaN 基底）**：在西电广州创新中心完成抗辐射 SoC/功率器件的电路设计与 FPGA/固件**交叉编译**，搭配商用抗辐射 SoC（如 Xilinx Zynq UltraScale+ MPSoC 宇航级、Microchip RTG4 / PolarFire，或 BAE RAD750）。
  **Compute SoC (GaN base)**: do the circuit design of the rad-hard SoC/power devices and FPGA/firmware **cross-compilation** at the Xidian Guangzhou Innovation Center, paired with a commercial rad-hard SoC (e.g. space-grade Xilinx Zynq UltraScale+ MPSoC, Microchip RTG4 / PolarFire, or BAE RAD750).
- **自研板卡**：用西电 SiC 功率器件 + 上述 SoC 设计"电源-算力合一"主板，不锈钢骨架散热；小批量中试走西电广州线，放量制造走南沙供应链。
  **In-house boards**: design a "power + compute in one" mainboard using Xidian SiC power devices + the SoC above, cooled by the stainless-steel frame; small pilot batches on the Xidian Guangzhou line, volume manufacturing through the Nansha supply chain.
- **注意**：西电公开的是功率器件/中试平台，不是完整主板，完整飞行计算机需自行集成并做辐照试验（可借助高校/院所辐照平台，试验数据建议上链，见 `docs/blockchain.md`）。
  **Note**: what Xidian has published are power devices / a pilot platform, not a complete mainboard; a full flight computer must be integrated and irradiation-tested ourselves (using university/institute irradiation facilities; putting test data on-chain is recommended, see `docs/blockchain.md`).

## 4. 重量预算（参考，目标 < 50kg 以适配 SpaceX 1/4 板） / 4. Mass Budget (Reference; Target < 50 kg to Fit a SpaceX 1/4 Plate)
| 项 / Item | 估重 / Est. mass |
|---|---|
| 底盘+电机+轮 / Chassis + motors + wheels | 8–12 kg |
| 不锈钢外壳 / Stainless-steel shell | 6–10 kg |
| 工具头+样品仓 / Tool head + sample bay | 3–5 kg |
| 电池+太阳能阵 / Batteries + solar array | 8–12 kg |
| 抗辐射主板+载荷 / Rad-hard mainboard + payload | 3–5 kg |
| 结构余量 / Structural margin | 5 kg |
| **合计 / Total** | **33–49 kg** |

## 5. 改装验证路线 / 5. Modification Validation Path
1. 地面：不锈钢外壳 + 测试工具头，在室内/沙地验证钻采与导航。
   Ground: stainless-steel shell + test tool head; validate drilling and navigation indoors / on sand.
2. 热真空：小 chamber 做 -150~+120℃ 循环，验证材料与电子。
   Thermal vacuum: cycle −150 to +120 °C in a small chamber to validate materials and electronics.
3. 辐照：送样到辐照平台做总剂量/单粒子试验（西电/院所）。
   Irradiation: send samples to an irradiation facility for total-dose / single-event tests (Xidian / institutes).
4. 飞行件：定版后进入发射集成。
   Flight hardware: after design freeze, proceed to launch integration.
