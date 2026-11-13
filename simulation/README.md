> 语言 / Language：本文档为中英双语，中文在前、英文在后。 / This document is bilingual: Chinese first, then English.

# CMR 仿真（核心 IP） / CMR Simulation (Core IP)

纯本地可运行的「宇宙挖矿机器人」自主勘探-采矿仿真，演示 AI 决策闭环：

A fully local "Cosmic Mining Robot" autonomous prospecting-and-mining simulation that demonstrates the AI decision loop:

```
勘探 → 多光谱感知 → ASTERIS风格去噪 → CIANNA风格矿石源检测
    → 接近 → 钻采 → 样品入库 → 中继回传 → 续航管理 → 循环

Explore → multispectral sensing → ASTERIS-style denoising → CIANNA-style ore source detection
    → approach → drill/mine → store sample → relay downlink → endurance management → loop
```

## 运行 / Run
```bash
pip install -r requirements.txt
python rover_sim.py --steps 400 --out map.svg
```

## 参数 / Parameters
| 参数 / Parameter | 默认 / Default | 说明 / Description |
|---|---|---|
| `--steps` | 400 | 仿真步数 / Number of simulation steps |
| `--grid` | 60 | 地图边长（格） / Map side length (cells) |
| `--veins` | 6 | 矿脉数量 / Number of ore veins |
| `--battery` | 100 | 初始电量(%) / Initial battery (%) |
| `--seed` | 42 | 随机种子 / Random seed |
| `--out` | map.svg | 地图输出文件名 / Map output file name |
| `--world` | generic | 目标天体：`generic`(类月) / `mars`(火星，含尘暴/低重力/水冰) / `depot`(地球·月球基地集尘售卖主舞台)<br>Target body: `generic` (Moon-like) / `mars` (Mars, with dust storms / low gravity / water ice) / `depot` (Earth·lunar base dust-collection-and-sales main stage) |

## 输出 / Outputs
- `map.svg` — 矿脉/轨迹/探测点/采矿点地图（机器人**星链在线时变绿**）
  Map of ore veins / trajectory / detection points / mining points (the rover **turns green when Starlink is online**)
- `telemetry.csv` — 每步遥测（位置、动作、电量、采集量、尘暴、`dust_box`、`comms`、`lots`、`sales`）
  Per-step telemetry (position, action, battery, amount collected, dust storm, `dust_box`, `comms`, `lots`, `sales`)
- `summary.txt` — 任务总结（覆盖率、检测精度、采集量、**集尘盒识别批次/销售额**、**星链覆盖率/时延**、**区块链统计**）
  Mission summary (coverage, detection accuracy, amount collected, **dust-box recognized lots / sales**, **Starlink coverage / latency**, **blockchain statistics**)
- `ledger.json` — 区块链全量哈希链（mine/asset/sale 区块）
  Full blockchain hash chain (mine/asset/sale blocks)
- `snaps/lot_*.png` — 集尘盒内容物摄像快照（真实 PNG，可肉眼查看）
  Camera snapshots of dust-box contents (real PNGs, viewable by eye)

## 模块 / Modules
- `ai_core.py::denoise_spectrum` — ASTERIS_THU 风格光谱去噪 / ASTERIS_THU-style spectral denoising
- `ai_core.py::OreDetector` — CIANNA 风格源检测器（可在线训练的小 MLP；签名随 `--world` 切换） / CIANNA-style source detector (a small online-trainable MLP; signatures switch with `--world`)
- `rover_sim.py` — 世界、机器人状态机（含集尘盒排空/星链中继）、评估与 SVG 可视化 / World, rover state machine (including dust-box emptying / Starlink relay), evaluation and SVG visualization
- `dustbox_vision.py` — 集尘盒视觉识别：合成摄像 PNG + 最近质心材质分类 + 资产铸造（详见 `docs/system_overview.md` 场景①） / Dust-box visual recognition: synthetic camera PNG + nearest-centroid material classification + asset minting (see `docs/system_overview.md`, Scenario ①)
- `starlink_comm.py` — Starlink 星链通讯：LEO 过顶窗口/时延/带宽/离线缓存队列（场景②） / Starlink communication: LEO pass windows / latency / bandwidth / offline buffer queue (Scenario ②)
- `blockchain_ledger.py` — 哈希链账本：勘探/采矿/资产/成交事件上链，做溯源、完整性校验、多机共识（详见 `docs/blockchain.md`） / Hash-chain ledger: records prospecting / mining / asset / sale events on-chain for provenance, integrity checks and multi-rover consensus (see `docs/blockchain.md`)

## 示例 / Examples
```bash
python rover_sim.py --world depot --steps 500 --out map_depot.svg   # 集尘盒视觉识别 + 星链售卖 / dust-box vision + Starlink sales
python rover_sim.py --world mars  --steps 600 --out map_mars.svg    # 火星采矿(含尘暴) / Mars mining (with dust storms)
```

> 接真实模型：把 `OreDetector.predict` 换成 AION/ASTERIS/CIANNA 的本地推理接口即可（见根目录 README 第 2 节）。火星视觉仿真见 `docs/mars_rover.md`（用 MARE 月球仿真 + 玉兔号模型改造）。
>
> Using real models: simply replace `OreDetector.predict` with the local inference interface of AION/ASTERIS/CIANNA (see Section 2 of the root README). For the Mars vision simulation see `docs/mars_rover.md` (adapted from the MARE lunar simulation + the Yutu rover model).
