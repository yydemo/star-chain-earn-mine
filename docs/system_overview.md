# CMR 宇宙挖矿机器人 — 系统总览与内容清单 / CMR Cosmic Mining Robot — System Overview and Contents

> 语言说明 / Language note：本文中英双语，先中文后英文。 / This document is bilingual: Chinese first, then English.

> 把家用扫地机器人改装为"宇宙挖矿机器人 (Cosmic Mining Robot, CMR)"的完整系统：
> 不锈钢机身 + 西安电子科技大学抗辐射芯片 + 广州第三代半导体编程/制造 + 火星车仿真逻辑
> + 集尘盒视觉识别 + Starlink 星链通讯 + 区块链溯源/售卖。
>
> A complete system for converting a household robot vacuum into a "Cosmic Mining Robot (CMR)":
> stainless-steel body + Xidian University rad-hard chips + Guangzhou third-generation semiconductor programming/manufacturing + Mars-rover simulation logic
> + dust-box visual recognition + Starlink communications + blockchain provenance/sales.

---

## 1. 系统总体架构（模块清单） / 1. Overall System Architecture (Module List)

| 层级 / Layer | 模块 / Module | 文件 / File | 作用 / Purpose | 状态 / Status |
|---|---|---|---|---|
| 硬件-移动底座 / HW – mobile base | 扫地机器人改装底盘 / Converted robot-vacuum chassis | `docs/hardware_mod.md` | 差速/轮式底盘、Nav2 全覆盖、LiDAR 建图（源自 oomwoo-main） / Differential/wheeled chassis, Nav2 full coverage, LiDAR mapping (from oomwoo-main) | 蓝图 / Blueprint |
| 硬件-机身 / HW – body | 316L 不锈钢外壳 / 316L stainless-steel shell | `docs/hardware_mod.md` 第3.1节 / §3.1 | 散热 + 粒子屏蔽，重量预算 33-49kg / Cooling + particle shielding, mass budget 33–49 kg | 蓝图 / Blueprint |
| 硬件-算力/电源 / HW – compute/power | 西电抗辐射 SiC 功率器件 / Xidian rad-hard SiC power devices | `docs/hardware_mod.md` 第3.3节 / §3.3 | 抗单粒子电源变换（天舟六号在轨验证） / Single-event-resistant power conversion (validated in orbit on Tianzhou-6) | 调研 / Research |
| 硬件-编程/制造 / HW – programming/manufacturing | 广州第三代半导体 / Guangzhou 3rd-gen semiconductors | `docs/guangzhou_semi.md` | 西电广州创新中心(GaN 中试)设计/编译 + 南沙(SiC 衬底/车规芯片)制造 / Design/compilation at Xidian Guangzhou Innovation Center (GaN pilot line) + manufacturing in Nansha (SiC substrates / automotive chips) | 调研 / Research |
| 硬件-通讯 / HW – comms | Starlink 用户终端 / Starlink user terminal | `simulation/starlink_comm.py` | Musk 星链 LEO 通讯仿真（过顶窗口/时延/带宽/队列） / Simulation of Musk's Starlink LEO comms (pass windows / latency / bandwidth / queue) | 仿真 / Simulated |
| 软件-世界/决策 / SW – world/decision | 火星车仿真内核 / Rover simulation core | `simulation/rover_sim.py` | 勘探-感知-去噪-检测-采掘-中继 状态机 / explore–sense–denoise–detect–mine–relay state machine | 可运行 / Runnable |
| 软件-机载AI / SW – onboard AI | 光谱去噪+源检测 / Spectral denoising + source detection | `simulation/ai_core.py` | ASTERIS 风格去噪 + CIANNA 风格 MLP 矿石分类 / ASTERIS-style denoising + CIANNA-style MLP ore classification | 可运行 / Runnable |
| 软件-视觉识别 / SW – vision | 集尘盒摄像识别 / Dust-box camera recognition | `simulation/dustbox_vision.py` | 合成摄像 PNG + 最近质心材质分类 + 资产铸造 / Synthetic camera PNG + nearest-centroid material classification + asset minting | 可运行 / Runnable |
| 软件-区块链 / SW – blockchain | 哈希链账本 / Hash-chain ledger | `simulation/blockchain_ledger.py` | 溯源/完整性/多机共识（PoW-lite） / Provenance / integrity / multi-robot consensus (PoW-lite) | 可运行 / Runnable |
| 数据-链上 / Data – on-chain | 账本 JSON / Ledger JSON | `simulation/ledger.json` | 每步/每矿/每资产/每成交区块 / Blocks per step / mine / asset / sale | 运行生成 / Generated at run time |
| 数据-遥测 / Data – telemetry | CSV 遥测 / CSV telemetry | `simulation/telemetry.csv` | 每步位置/动作/电量/集尘盒/星链/销售 / Per-step position / action / battery / dust box / Starlink / sales | 运行生成 / Generated at run time |
| 数据-影像 / Data – images | 集尘盒快照 / Dust-box snapshots | `simulation/snaps/*.png` | 每批内容物真实摄像图（可肉眼查看） / Real camera image of each lot's contents (viewable) | 运行生成 / Generated at run time |
| 数据-地图 / Data – map | SVG 轨迹图 / SVG trajectory map | `simulation/map_*.svg` | 矿脉/轨迹/探测/采矿/机器人(星链在线变绿) / Ore veins / trajectory / detections / mining / rover (green when Starlink online) | 运行生成 / Generated at run time |
| 文档 / Docs | 总蓝图/方案 / Blueprint / plans | `README.md` + `docs/*` | 7 份方案文档 / 7 plan documents | 完成 / Done |

---

## 2. 两大核心场景（本次新增） / 2. Two Core Scenarios (Newly Added)

| 场景 / Scenario | 描述 / Description | 实现文件 / Files | 关键流程 / Key flow | 产出 / Output |
|---|---|---|---|---|
| 集尘盒视觉识别 到 区块链售卖 / Dust-box vision → blockchain sales | 机器人集尘盒内容物经机载摄像头成像，识别材质，每批铸造为可售区块链资产 / Dust-box contents are imaged by the onboard camera, the material is identified, and each lot is minted as a sellable blockchain asset | `dustbox_vision.py` + `rover_sim.py`(`_empty_dustbox`) | 集尘盒满 到 `CameraSnap.capture()` 合成摄像图(PNG) 到 `ImageClassifier.predict()` 识别材质+置信度 到 `LotMinter.mint()` 写链(`event=asset`) 到 经 Starlink 发布成交(`event=sale`) / Dust box full → `CameraSnap.capture()` synthesizes a camera image (PNG) → `ImageClassifier.predict()` identifies material + confidence → `LotMinter.mint()` writes to chain (`event=asset`) → sale published via Starlink (`event=sale`) | `lot_xxx.png` + `ledger.json` 中的 asset/sale 区块 + 销售额(¥) / asset/sale blocks in `ledger.json` + sales revenue (¥) |
| Starlink 星链通讯 / Starlink communications | 扫地机器人改装 CMR 通过 Musk 的 Starlink LEO 星座与地面/市场通讯 / The converted-vacuum CMR talks to the ground/market via Musk's Starlink LEO constellation | `starlink_comm.py` + `rover_sim.py`(`_comms_relay`) | 每步 `Starlink.update()` 刷新过顶窗口 到 online 时 `flush()` 回传缓存的 asset/telemetry 消息 到 成交记录上链 / Each step `Starlink.update()` refreshes the pass window → when online, `flush()` sends buffered asset/telemetry messages → sale records go on-chain | 覆盖率/时延/带宽统计 + 出网队列 / Coverage / latency / bandwidth stats + outbound queue |

> 说明：地球/月球基地场景下 Starlink 直连 LEO 现实可行；火星等深空场景本模块作为"星间/深空中继链路"示意模型（真实时延以分钟计，此处仅做链路调度与队列演示）。
>
> Note: direct Starlink LEO links are realistic for the Earth / lunar-base scenario; for deep-space scenarios such as Mars this module is an illustrative "inter-satellite / deep-space relay" model (real latency is measured in minutes; here it only demonstrates link scheduling and queuing).

---

## 3. 供应链 / 技术来源 / 3. Supply Chain / Technology Sources

| 环节 / Stage | 主体 / Entity | 地点 / Location | 在 CMR 中的角色 / Role in CMR | 资料 / Reference |
|---|---|---|---|---|
| 抗辐射芯片 / Rad-hard chips | 西安电子科技大学 / Xidian University | 陕西西安（主校）+ 广州黄埔创新中心 / Xi'an, Shaanxi (main campus) + Guangzhou Huangpu Innovation Center | SiC 功率器件抗单粒子；GaN 抗辐射/耐高温器件（设计/编译环节） / SiC power devices resistant to single-event effects; GaN rad-hard / high-temperature devices (design/compilation stage) | `docs/guangzhou_semi.md` |
| 第三代半导体制造 / 3rd-gen semiconductor manufacturing | 芯粤能 / 芯聚能 / 南砂晶圆 (CR Micro-Yueneng / Xinjuneng / Nansha Wafer) | 广州南沙万顷沙 / Wanqingsha, Nansha, Guangzhou | SiC 衬底、车规级主驱芯片、功率模块（制造环节） / SiC substrates, automotive-grade traction chips, power modules (manufacturing stage) | `docs/guangzhou_semi.md` |
| 移动底座 / Mobile base | oomwoo 开源扫地机器人 / oomwoo open-source robot vacuum | 无 / N/A | 树莓派 + 3D 打印 + ROS2 + LiDAR + Nav2 / Raspberry Pi + 3D printing + ROS 2 + LiDAR + Nav2 | `oomwoo-main/` |
| 行星环境仿真 / Planetary environment simulation | MARE Lunar Simulator | 无 / N/A | UE5+ROS2 月球车（含玉兔号），可改造火星视觉 / UE5 + ROS 2 lunar rovers (incl. Yutu), adaptable to Mars visuals | `MARE-Lunar-Simulator-main/` |
| 技术选型库 / Tech selection library | awesome-space-autonomy | 无 / N/A | 飞行软件/自主导航/在轨AI/多机协同资料 / Flight software / autonomous navigation / in-orbit AI / multi-robot collaboration resources | `awesome-space-autonomy-main/` |
| 发射/入轨 / Launch / orbit insertion | SpaceX 拼车 / 天舟 (SpaceX rideshare / Tianzhou) | 无 / N/A | 发射成本参考（35万美元/50kg 2026）；西电器件随天舟六号入轨验证 / Launch cost reference ($350k / 50 kg, 2026); Xidian devices validated in orbit on Tianzhou-6 | `docs/hardware_mod.md` |
| 通讯 / Communications | Starlink (Musk) | 无 / N/A | LEO 星座用户终端 / LEO constellation user terminal | `simulation/starlink_comm.py` |

---

## 4. 仿真世界档（--world） / 4. Simulation World Presets (--world)

| 世界档 / World | 目标天体 / Target body | 矿/目标 / Ore / target | 重力(m/s²) / Gravity (m/s²) | 尘暴 / Dust storms | 集尘盒/星链 / Dust box / Starlink |
|---|---|---|---|---|---|
| `generic` | 类月默认 / Moon-like default | 金属/稀土矿 / Metal / rare-earth ore | 1.62 | 无 / None | 启用 / Enabled |
| `mars` | 火星 / Mars | 水冰/含水矿物 / Water ice / hydrated minerals | 3.71 | 周期性(削弱太阳能+抬高噪声) / Periodic (weakens solar power + raises noise) | 启用 / Enabled |
| `depot` | 地球/月球基地 / Earth / lunar base | 风化层尘埃与矿石 / Regolith dust and ore | 1.62 | 无 / None | 主舞台(集尘售卖) / Main stage (dust collection & sales) |

---

## 5. 运行方式 / 5. How to Run

```bash
# 需 numpy（已建隔离 venv） / Requires numpy (isolated venv already set up)
VENV="C:/Users/user/.workbuddy/binaries/python/envs/cmr/Scripts/python.exe"

# 火星采矿 + 集尘盒识别 + 星链售卖 / Mars mining + dust-box recognition + Starlink sales
$VENV rover_sim.py --world mars --steps 600 --out map_mars.svg
# 地球/月球基地集尘售卖场景 / Earth / lunar-base dust-collection sales scenario
$VENV rover_sim.py --world depot --steps 500 --out map_depot.svg
# 默认类月 / Default moon-like
$VENV rover_sim.py --world generic --steps 400
```

| 参数 / Parameter | 默认 / Default | 说明 / Description |
|---|---|---|
| `--steps` | 800 | 仿真步数 / Simulation steps |
| `--grid` | 60 | 地图边长 / Map side length |
| `--veins` | 6 | 矿脉数量 / Number of ore veins |
| `--battery` | 100 | 初始电量(%) / Initial battery (%) |
| `--seed` | 42 | 随机种子 / Random seed |
| `--world` | generic | generic / mars / depot |
| `--out` | map.svg | 地图文件名 / Map file name |

---

## 6. 区块链数据结构（区块） / 6. Blockchain Data Structure (Blocks)

```
Block = { index, ts, prev_hash, rover_id, event, payload, nonce, hash }
event 属于 / is one of { genesis, telemetry, mine, asset, sale, consensus, sample }
- mine   : { cell:[i,j], grade, collected, step }          # 采矿溯源 / mining provenance
- asset  : { lot_id, material, cn_name, conf, mass_kg, grade,
             price_per_kg, value_cny, image, sellable }    # 可售资产 / sellable asset
- sale   : { lot_id, value_cny, via:"Starlink" }           # 经星链成交 / sale via Starlink
```

完整性：SHA256 哈希链 + 前导 0 难度出块；任意篡改即校验失败（见 `blockchain_ledger.py` 篡改演示）。

Integrity: a SHA256 hash chain + leading-zero difficulty for block production; any tampering fails verification (see the tamper demo in `blockchain_ledger.py`).

---

## 7. 输出文件 / 7. Output Files

| 文件 / File | 说明 / Description |
|---|---|
| `simulation/ledger.json` | 全量哈希链（溯源/审计/共识） / Full hash chain (provenance / audit / consensus) |
| `simulation/telemetry.csv` | 每步遥测（含 dust_box / comms / lots / sales） / Per-step telemetry (incl. dust_box / comms / lots / sales) |
| `simulation/summary.txt` | 任务总结 / Mission summary |
| `simulation/map_*.svg` | 轨迹/矿脉/探测/采矿/机器人(星链在线变绿) / Trajectory / veins / detections / mining / rover (green when Starlink online) |
| `simulation/snaps/lot_*.png` | 集尘盒内容物真实摄像快照（可肉眼查看） / Real camera snapshots of dust-box contents (viewable) |

---

## 8. 后续可扩展 / 8. Future Extensions

- [ ] 把火星场景真正导入 MARE 做 UE5 可视化渲染 / Import the Mars scenario into MARE for UE5 visual rendering
- [ ] 区块链对接真实联盟链（Hyperledger Fabric） / Connect the blockchain to a real consortium chain (Hyperledger Fabric)
- [ ] 集尘盒分类器替换为真实 CNN（PyTorch/TensorFlow）并接入真实摄像头 / Replace the dust-box classifier with a real CNN (PyTorch/TensorFlow) and connect a real camera
- [ ] Starlink 深空链路时延模型（光行时 + 深空网络） / Starlink deep-space link latency model (light time + deep-space network)
- [ ] 多机器人协作（已支持 `consensus_with()` 多机对账） / Multi-robot collaboration (`consensus_with()` multi-robot reconciliation already supported)
