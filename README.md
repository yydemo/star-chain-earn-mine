# 🛰️ 宇宙挖矿机器人 Cosmic Mining Rover (CMR)

> 语言说明 / Language note：本仓库文档、代码注释与程序输出均为中英双语，一般先中文后英文。 / All documentation, code comments and program output in this repository are bilingual (Chinese–English), usually Chinese first, then English.

> 把一台开源扫地机器人，改装成一台能在地外天体表面自主勘探、识别并采集资源的 AI 挖矿机器人。
> 配合西安电子科技大学（西电）三代半（SiC/GaN）抗辐射功率器件、不锈钢轻量化外壳，以及 SpaceX rideshare 发射通道，构建一条「地面原型 → 在轨/月面验证 → 商业航天服务」的可执行路线。
>
> Convert an open-source robot vacuum into an AI mining rover that can autonomously explore, identify and collect resources on the surface of extraterrestrial bodies.
> Combined with Xidian University's (西电) third-generation semiconductor (SiC/GaN) radiation-hardened power devices, a lightweight stainless-steel shell, and the SpaceX rideshare launch channel, it builds an executable path of "ground prototype → in-orbit/lunar-surface validation → commercial space services".

---

## 0. 先说真话（现实可行性体检） / 0. The Honest Truth (Reality Check)

把机器人送上天不是"副业玩具"，而是**商业航天级别**的工程。先把账算清楚，再决定怎么玩：

Sending a robot into space is not a "side-hustle toy" but **commercial-spaceflight-grade** engineering. Do the maths first, then decide how to play:

| 项目 / Item | 真实数字（2026） / Real figures (2026) | 来源 / Source |
|---|---|---|
| 最低发射门槛 / Minimum launch threshold | **$350,000 起**，含 50kg 到太阳同步轨道（SSO） / **From $350,000**, including 50 kg to sun-synchronous orbit (SSO) | SpaceX Rideshare |
| 超出重量单价 / Price per extra kg | **$7,000 / kg** | SpaceX Rideshare 2026 |
| 发射节奏 / Launch cadence | Transporter 任务约每 4 个月一班，SSO 525km / 97.5° / Transporter missions roughly every 4 months, SSO 525 km / 97.5° | SpaceX |
| 载荷板配置 / Payload plate options | 1/4 板 50kg / 1/2 板 100kg / 整板 200kg / XL 300kg / 1/4 plate 50 kg / 1/2 plate 100 kg / full plate 200 kg / XL 300 kg | SpaceX |
| 西电抗辐射器件 / Xidian rad-hard devices | 抗辐射 SiC 功率器件已随**天舟六号**入空间站、在 LEO 卫星验证 / Rad-hard SiC power devices went to the space station on **Tianzhou-6** and were validated on LEO satellites | 西电芜湖研究院 / Xidian Wuhu Research Institute |
| 开源底座成本 / Open-source base cost | ROS 2 扫地机器人整机硬件可压到**千元级** / Complete ROS 2 robot-vacuum hardware can be brought down to **around a thousand yuan** | 开源社区 / Open-source community |

**结论**：对个人/小团队而言，**真正的轨道发射（35 万美元起）不是"副业"能负担的**。但——

**Conclusion**: for individuals or small teams, **a real orbital launch (from $350k) is not something a "side hustle" can afford**. But —

> 你真正能卖、能立刻开工的，是这套**自主勘探+AI 识别+在轨算力**的技术栈，以及它的**数字孪生与仿真 IP**。发射是这条技术链成熟后的"毕业典礼"，不是起点。
>
> What you can actually sell and start on right away is this **autonomous exploration + AI recognition + in-orbit computing** tech stack, plus its **digital twin and simulation IP**. Launch is the "graduation ceremony" once this tech chain matures, not the starting point.

所以本项目采用**三段式路线**：先造能在地面跑的真原型 + 高保真仿真（现在就能做、现在就能变现），再找高校载荷竞赛/商业航天基金/科研客户做在轨验证，最后才是自己发射。

So this project follows a **three-stage path**: first build a real prototype that runs on the ground plus a high-fidelity simulation (doable and monetizable now), then seek in-orbit validation via university payload competitions / commercial space funds / research customers, and only finally launch on our own.

---

## 制造与技术背书 / Manufacturing and Technical Credentials

团队已具备工业产品识别、5G 终端硬件、多模态感知与数据安全的实际专利与软著积累（详见 [`docs/manufacturing_credentials.md`](docs/manufacturing_credentials.md)），可直接支撑 CMR 地面原型的传感器、样品识别与加密回传模块的自主设计与制造。抗辐射器件与发射环节将与国内高校第三代半导体研究机构及商业发射服务商按计划推进合作。

The team already holds real patents and software copyrights in industrial product identification, 5G terminal hardware, multimodal sensing and data security (see [`docs/manufacturing_credentials.md`](docs/manufacturing_credentials.md)), which directly support the in-house design and manufacture of the CMR ground prototype's sensors, sample identification and encrypted downlink modules. For radiation-hardened devices and launch, cooperation with a domestic university third-generation semiconductor research institute and a commercial launch provider is being advanced as planned.

## 1. 概念：扫地机器人 → 宇宙挖矿机器人 / 1. Concept: Robot Vacuum → Cosmic Mining Rover

扫地机器人和行星探测车（rover）在底层**高度同构**：

Robot vacuums and planetary rovers are **highly isomorphic** at the base level:

| 扫地机器人能力 / Robot-vacuum capability | 对应挖矿机器人能力 / Corresponding mining-rover capability |
|---|---|
| 差速底盘 + 轮编码器里程计 / Differential chassis + wheel-encoder odometry | 月/小行星表面移动与定位 / Movement and localization on lunar/asteroid surfaces |
| 2D LiDAR / ToF / 视觉 SLAM / 2D LiDAR / ToF / visual SLAM | 地表障碍规避、地形建图 / Surface obstacle avoidance, terrain mapping |
| ROS 2 导航栈（Nav2）+ 全覆盖路径规划 / ROS 2 navigation stack (Nav2) + full-coverage path planning | 矿产区域覆盖勘探 / Coverage exploration of mineral areas |
| 离心风机 + 尘盒（吸尘） / Centrifugal fan + dust box (vacuuming) | 替换为**钻取/研磨/采集工具头** / Replaced by a **drilling/grinding/collecting tool head** |
| Raspberry Pi 主控 + Arduino 底层 / Raspberry Pi main controller + Arduino low level | 替换为**抗辐射计算 + 电源模组** / Replaced by **rad-hard computing + power modules** |
| 回充基站 / Charging dock | 替换为**太阳能/同位素电池 + 数据中继** / Replaced by **solar/radioisotope batteries + data relay** |

**改装三板斧 / Three key modifications**：
1. 拆掉吸尘系统，装上轻量化**钻探/抓取工具头** + 样品仓。
   Remove the vacuum system and fit a lightweight **drilling/grabbing tool head** + sample bay.
2. 外壳换成**316L 不锈钢 / 钛合金**轻量化结构（抗温差、抗微流星、可焊接）。
   Replace the shell with a lightweight **316L stainless steel / titanium alloy** structure (resists temperature swings and micrometeoroids, weldable).
3. 主控与电源换成**西电抗辐射 SiC 功率器件 + 抗辐射计算 SoC**，并用导热不锈钢骨架做散热/辐射屏蔽。
   Replace the main controller and power with **Xidian rad-hard SiC power devices + a rad-hard computing SoC**, using a thermally conductive stainless-steel frame for heat dissipation / radiation shielding.

---

## 2. 系统架构 / 2. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Cosmic Mining Rover (CMR)                  │
├─────────────────────────────────────────────────────────────┤
│  感知层 (Sensing)                                            │
│   · 多光谱/高光谱相机 Multispectral/hyperspectral camera     │
│     (AION 启发的 39 类模态统一表征 / AION-inspired unified   │
│      representation of 39 modalities)                        │
│   · 2D LiDAR / ToF / IMU  (来自扫地机器人底座 / from the     │
│     robot-vacuum base)                                       │
│   · 钻探振动谱 + 样品近红外 Drill vibration spectrum +       │
│     sample NIR (ASTERIS 风格去噪 / ASTERIS-style denoising)  │
├─────────────────────────────────────────────────────────────┤
│  AI 决策层 (Autonomy Stack) —— 本项目的核心 IP / core IP     │
│   · 矿石源检测 Ore-source detection ← CIANNA                 │
│     (YOLO 风格星系/源探测器 / YOLO-style galaxy/source det.) │
│   · 多模态理解 Multimodal understanding ← AION               │
│     (全模态基础模型 天体识别/分类 / omni-modal foundation    │
│      model for object recognition/classification)            │
│   · 图像去噪 Image denoising ← ASTERIS_THU                   │
│     (JWST 验证, +1 星等探测极限 / JWST-validated, +1 mag)    │
│   · 任务看板/预测 Mission dashboard/forecast ← AstroIntel    │
│     (NASA 数据/随机森林预测 / NASA data, random forest)      │
│   · 自主导航 Autonomous navigation ← Nav2 + 全覆盖勘探       │
│     full-coverage exploration (来自扫地机器人 / from vacuum) │
├─────────────────────────────────────────────────────────────┤
│  执行层 (Actuation)                                          │
│   · 差速底盘 (保留) Differential chassis (kept)              │
│   · 钻探/研磨工具头 (新增) Drill/grind tool head (new)       │
│   · 样品仓 (新增) Sample bay (new)                           │
│   · 太阳能阵/电池 (替换回充基站) Solar array/battery         │
│     (replaces charging dock)                                 │
├─────────────────────────────────────────────────────────────┤
│  抗辐射算力与电源 (Rad-Hard Core) —— 西电三代半              │
│  (Xidian third-generation semiconductors)                    │
│   · 抗辐射 SiC MOSFET 功率级 Rad-hard SiC MOSFET power stage │
│     (西电芜湖研究院, 已在轨验证 / Xidian Wuhu Research       │
│      Institute, validated in orbit)                          │
│   · 抗辐射计算 SoC Rad-hard computing SoC                    │
│     (Xilinx Zynq UltraScale+ / Microchip)                    │
│   · 不锈钢导热骨架兼具散热与部分粒子屏蔽                     │
│     Stainless-steel thermal frame for cooling and partial    │
│     particle shielding                                       │
└─────────────────────────────────────────────────────────────┘
```

### 开源天文 AI 工具如何接入 / How the open-source astronomy AI tools plug in
| 工具 / Tool | 在本项目中的角色 / Role in this project | 接入方式 / Integration |
|---|---|---|
| **AION** (PolymathicAI) | 多模态"天体/矿物"基础模型，统一成像/光谱/星表表征 / Multimodal "celestial object/mineral" foundation model unifying imaging/spectra/catalogue representations | 本地 GPU 推理，做样品多模态分类 / Local GPU inference for multimodal sample classification |
| **ASTERIS_THU** | 自监督成像去噪，提升弱信号探测极限 / Self-supervised imaging denoising that improves the faint-signal detection limit | 对相机/光谱图做去噪预处理 / Denoising pre-processing of camera/spectral images |
| **CIANNA** | GPU 加速深度学习 + YOLO 风格源检测器 / GPU-accelerated deep learning + YOLO-style source detector | 移植其 detector 做"矿石源"检测 head / Port its detector as an "ore-source" detection head |
| **AstroIntel** | NASA 数据看板 + 随机森林预测 / NASA data dashboard + random-forest forecasting | 地面任务规划/遥测可视化参考架构 / Reference architecture for ground mission planning / telemetry visualization |

---

## 3. 开源底座选型（现在就能 clone 跑） / 3. Open-Source Base Options (Clone and Run Today)

| 项目 / Project | 特点 / Features | 用于 CMR / Use for CMR |
|---|---|---|
| **OOMWOO** | 从零开源扫地机器人：3D 打印结构→电机→RPi/ESP32→ROS 2→SLAM→Nav2；提供 Docker + Gazebo 仿真 / A fully open-source robot vacuum from scratch: 3D-printed structure → motors → RPi/ESP32 → ROS 2 → SLAM → Nav2; ships Docker + Gazebo simulation | **首选底座**，结构/导航全开源、可改 / **Preferred base**: structure and navigation fully open and modifiable |
| **Vaid777/Robovacuum_Robot** | ROS 2 + Visual SLAM + AI 导航，RPi+Arduino，Kalman 融合 / ROS 2 + visual SLAM + AI navigation, RPi + Arduino, Kalman fusion | 导航/感知栈参考 / Navigation/perception stack reference |
| **Jack23162329/robot-vacuum** | Fusion 360 模型 + ROS Noetic + Gazebo + LiDAR / Fusion 360 model + ROS Noetic + Gazebo + LiDAR | CAD/仿真参考 / CAD/simulation reference |

> 建议：先基于 **OOMWOO 的 Gazebo 仿真**把"吸尘"行为替换为"勘探+采矿"行为，验证 AI 决策闭环（见 `simulation/`），再过渡到真实硬件改装。
>
> Suggestion: start from **OOMWOO's Gazebo simulation**, replace the "vacuuming" behaviour with "exploration + mining", validate the AI decision loop (see `simulation/`), then move on to real hardware modification.

---

## 4. AI 决策闭环（已做成可运行仿真） / 4. AI Decision Loop (Runnable Simulation)

`simulation/rover_sim.py` 是一个**不依赖任何付费服务、纯本地可跑**的高保真仿真，演示 CMR 的核心闭环：

`simulation/rover_sim.py` is a high-fidelity simulation that **runs purely locally with no paid services**, demonstrating the CMR core loop:

```
勘探(explore) → 多光谱感知(sense) → ASTERIS风格去噪(denoise)
   → CIANNA风格矿石源检测(detect) → 接近(approach) → 钻采(mine)
   → 样品入库(store sample) → 中继回传(relay) → 续航管理(energy management) → 返回勘探(back to explore)

explore → multispectral sensing → ASTERIS-style denoising
   → CIANNA-style ore-source detection → approach → mine
   → store sample → relay downlink → energy management → back to explore
```

它输出：轨迹地图（SVG）、遥测日志（CSV）、每步决策摘要。**这就是你可以立刻交付、演示、甚至拿去参赛/卖给科研客户的"技术内核"。**

It outputs a trajectory map (SVG), a telemetry log (CSV) and a per-step decision summary. **This is the "technical core" you can deliver, demo, enter in competitions or even sell to research customers right away.**

在火星车仿真逻辑之上，本仓库已扩展两大子系统（详见 `docs/system_overview.md`）：

On top of the rover simulation logic, this repository adds two major subsystems (see `docs/system_overview.md`):

- **① 集尘盒视觉识别 → 区块链售卖**（`simulation/dustbox_vision.py`）：集尘盒满时由机载摄像头成像（生成真实 PNG 快照）→ 最近质心分类器识别材质 → 每批铸造为可售区块链资产（`ledger.json` 中 `asset`/`sale` 区块），并给出市场估价(¥)。
  **① Dust-box vision recognition → blockchain sales** (`simulation/dustbox_vision.py`): when the dust box is full, the onboard camera images it (producing a real PNG snapshot) → a nearest-centroid classifier identifies the material → each lot is minted as a sellable blockchain asset (`asset`/`sale` blocks in `ledger.json`) with a market valuation (¥).
- **② Starlink 星链通讯**（`simulation/starlink_comm.py`）：扫地机器人改装 CMR 通过 Musk 的 Starlink LEO 星座通讯，模拟过顶窗口、时延、带宽与离线缓存队列（`store-and-forward`）。
  **② Starlink communications** (`simulation/starlink_comm.py`): the converted-vacuum CMR communicates via Musk's Starlink LEO constellation, simulating pass windows, latency, bandwidth and an offline buffer queue (`store-and-forward`).

三个世界档：`generic`(类月) / `mars`(火星，含尘暴) / `depot`(地球·月球基地集尘售卖主舞台)。

Three world presets: `generic` (moon-like) / `mars` (Mars, with dust storms) / `depot` (Earth/lunar base — main stage for dust collection and sales).

---

## 5. 路线图（三阶段） / 5. Roadmap (Three Stages)

**阶段 A — 地面原型 + 仿真（0–6 个月，现在开始，< 2 万元）**

**Stage A — Ground prototype + simulation (0–6 months, start now, < 20,000 yuan)**
- clone OOMWOO，Gazebo 里把吸尘替换为勘探/采矿行为 / Clone OOMWOO and replace vacuuming with exploration/mining in Gazebo
- 跑通 `rover_sim.py`，沉淀 AI 决策栈（去噪+源检测+导航） / Get `rover_sim.py` running and build up the AI decision stack (denoising + source detection + navigation)
- 3D 打印不锈钢/PLA 外壳原型，装测试工具头 / 3D-print a stainless-steel/PLA shell prototype and fit a test tool head
- **变现点**：仿真软件授权、教育套件、技术咨询 / **Monetization**: simulation software licences, education kits, technical consulting

**阶段 B — 抗辐射化 + 立方星/载荷验证（6–18 个月）**

**Stage B — Radiation hardening + CubeSat/payload validation (6–18 months)**
- 引入西电抗辐射 SiC 功率器件 + 抗辐射 SoC，做电源/算力板 / Bring in Xidian rad-hard SiC power devices + a rad-hard SoC to build power/compute boards
- 参加高校/商业航天载荷竞赛（如 立方星、空间科学载荷），争取发射名额与赞助 / Enter university/commercial space payload competitions (e.g. CubeSats, space-science payloads) to win launch slots and sponsorship
- **变现点**：科研载荷设计服务、在轨验证数据产品 / **Monetization**: research payload design services, in-orbit validation data products

**阶段 C — 专属发射（18 个月+，需融资/客户预付款）**

**Stage C — Dedicated launch (18+ months, needs funding / customer prepayment)**
- 通过 SpaceX rideshare（≥$350k / 50kg）或国内商业航天（星河动力/天兵等）发射 / Launch via SpaceX rideshare (≥ $350k / 50 kg) or Chinese commercial launchers (Galactic Energy / Space Pioneer, etc.)
- 目标天体：近地小行星（采样返回难度高，先做绕飞+表层勘探）或月球南极（水冰/稀土） / Targets: near-Earth asteroids (sample return is hard, so fly-around + surface exploration first) or the lunar south pole (water ice / rare earths)
- **变现点**：稀缺地外样品、在轨算力租赁、科研数据订阅 / **Monetization**: rare extraterrestrial samples, in-orbit compute rental, research data subscriptions

---

## 6. 现在就开始（你的第一步） / 6. Start Now (Your First Step)

```bash
# 1) 跑通 AI 挖矿机器人仿真（纯本地，仅需 numpy）
#    Run the AI mining-rover simulation (purely local, only numpy needed)
cd simulation
pip install -r requirements.txt
python rover_sim.py --world depot --steps 500 --out map_depot.svg   # 集尘盒售卖主舞台 / dust-box sales main stage
python rover_sim.py --world mars  --steps 600 --out map_mars.svg   # 火星采矿(含尘暴) / Mars mining (with dust storms)
python rover_sim.py --world generic --steps 400                    # 类月默认 / moon-like default

# 2) 看输出 / Check the outputs
#    - map_*.svg        轨迹与矿脉地图（机器人星链在线时变绿） / trajectory and ore map (rover turns green when Starlink is online)
#    - telemetry.csv    每步遥测（含 dust_box / comms / lots / sales） / per-step telemetry (incl. dust_box / comms / lots / sales)
#    - summary.txt      任务总结（含集尘盒识别/星链/区块链统计） / mission summary (dust-box recognition / Starlink / blockchain stats)
#    - ledger.json      区块链全量哈希链 / full blockchain hash chain
#    - snaps/lot_*.png  集尘盒内容物摄像快照（真实 PNG，可肉眼查看） / camera snapshots of dust-box contents (real PNGs you can view)

# 3) 把"吸尘"换成"采矿"——clone 开源底座
#    Swap "vacuuming" for "mining" — clone the open-source base
git clone https://github.com/<OOMWOO>/OOMWOO   # 见 docs 选型 / see the options in docs
```

> 本机已建隔离 venv（含 numpy）：`C:/Users/user/.workbuddy/binaries/python/envs/cmr/Scripts/python.exe rover_sim.py ...`
>
> An isolated venv (with numpy) was set up on the original development machine: `C:/Users/user/.workbuddy/binaries/python/envs/cmr/Scripts/python.exe rover_sim.py ...`

---

## 7. 风险与诚实清单 / 7. Risks and Honesty Checklist

- ❗ 发射成本（$350k 起）远超个人"副业"预算 → 用阶段 A/B 的技术产品先变现再发射。
  ❗ Launch cost (from $350k) far exceeds a personal "side-hustle" budget → monetize Stage A/B tech products first, then launch.
- ⚠️ 西电目前公开的是**抗辐射 SiC 功率器件**，不是完整抗辐射主板 → 需自研电源/算力板并搭配商用抗辐射 SoC。
  ⚠️ What Xidian has published so far are **rad-hard SiC power devices**, not a complete rad-hard mainboard → we need our own power/compute boards paired with a commercial rad-hard SoC.
- ⚠️ 真实地外采矿涉及采样返回、能源、通信、法规（外空条约）→ 阶段 C 前需法律与工程尽调。
  ⚠️ Real extraterrestrial mining involves sample return, energy, communications and regulation (the Outer Space Treaty) → legal and engineering due diligence is needed before Stage C.
- ✅ 阶段 A 的仿真 + 原型是**真实可交付资产**，不依赖发射也能产生价值。
  ✅ The Stage A simulation + prototype are **real deliverable assets** that create value without any launch.

---

## 目录 / Contents
- `README.md` — 本蓝图 / This blueprint
- `docs/system_overview.md` — 系统总览与内容清单（整体架构 / 两大场景 / 供应链 / 运行表） / System overview and contents (architecture / two scenarios / supply chain / run table)
- `docs/hardware_mod.md` — 硬件改装：不锈钢外壳 / 西电+广州第三代半导体抗辐射电源算力 / 工具头 / Hardware modification: stainless-steel shell / Xidian + Guangzhou third-generation semiconductor rad-hard power and compute / tool head
- `docs/guangzhou_semi.md` — 广州（黄埔西电创新中心 + 南沙万顷沙）第三代半导体产业链如何承接 CMR 的"设计—编程编译—制造"环节 / How Guangzhou's third-generation semiconductor industry chain (Huangpu Xidian Innovation Center + Nansha Wanqingsha) takes on CMR's "design — programming/compilation — manufacturing" stages
- `docs/mars_rover.md` — 火星车场景：`rover_sim.py --world mars` 参数差异 + 用 MARE 月球仿真（含玉兔号）改造火星视觉仿真 / Mars rover scenario: `rover_sim.py --world mars` parameter differences + adapting the MARE lunar simulation (incl. Yutu) into a Mars vision simulation
- `docs/blockchain.md` — 区块链分析模块：勘探过程上链，做数据溯源 / 完整性校验 / 多机器人共识对账 / Blockchain analysis module: putting exploration on-chain for data provenance / integrity checks / multi-robot consensus reconciliation
- `docs/launch_plan.md` — 发射方案与重量预算（马斯克/SpaceX rideshare） / Launch plan and mass budget (Musk / SpaceX rideshare)
- `docs/monetization.md` — 变现路径（科研服务 / 数据标注 / 教育套件 / 在轨算力） / Monetization paths (research services / data labelling / education kits / in-orbit compute)
- `docs/manufacturing_credentials.md` — 制造与技术背书：专利、软著、论文与省科技计划项目，及其与 CMR 的对应关系 / Manufacturing and technical credentials: patents, software copyrights, papers and a provincial S&T programme project, and how they map to CMR
- `simulation/rover_sim.py` — 火星车仿真内核（含集尘盒/星链） / Rover simulation core (with dust box / Starlink)
- `simulation/ai_core.py` — 机载 AI：ASTERIS 去噪 + CIANNA 矿石源检测 / Onboard AI: ASTERIS denoising + CIANNA ore-source detection
- `simulation/dustbox_vision.py` — 集尘盒摄像识别 + 区块链资产化 / Dust-box camera recognition + blockchain tokenization
- `simulation/starlink_comm.py` — Starlink 星链通讯仿真 / Starlink communications simulation
- `simulation/blockchain_ledger.py` — 哈希链账本（溯源/完整性/共识） / Hash-chain ledger (provenance / integrity / consensus)
- `simulation/snaps/` — 集尘盒摄像快照 PNG（运行生成） / Dust-box camera snapshot PNGs (generated at run time)
- `assets/` — 架构与改装可视化图 / Architecture and modification diagrams
- `pptx/宇宙挖矿机器人/` — 演示文稿源文件（STORY.md / DESIGN.md / slides）与生成的 .pptx / Presentation sources (STORY.md / DESIGN.md / slides) and the generated .pptx
