# CMR 仿真（核心 IP）

纯本地可运行的「宇宙挖矿机器人」自主勘探-采矿仿真，演示 AI 决策闭环：

```
勘探 → 多光谱感知 → ASTERIS风格去噪 → CIANNA风格矿石源检测
    → 接近 → 钻采 → 样品入库 → 中继回传 → 续航管理 → 循环
```

## 运行
```bash
pip install -r requirements.txt
python rover_sim.py --steps 400 --out map.svg
```

## 参数
| 参数 | 默认 | 说明 |
|---|---|---|
| `--steps` | 400 | 仿真步数 |
| `--grid` | 60 | 地图边长（格） |
| `--veins` | 6 | 矿脉数量 |
| `--battery` | 100 | 初始电量(%) |
| `--seed` | 42 | 随机种子 |
| `--out` | map.svg | 地图输出文件名 |
| `--world` | generic | 目标天体：`generic`(类月) / `mars`(火星，含尘暴/低重力/水冰) / `depot`(地球·月球基地集尘售卖主舞台) |

## 输出
- `map.svg` — 矿脉/轨迹/探测点/采矿点地图（机器人**星链在线时变绿**）
- `telemetry.csv` — 每步遥测（位置、动作、电量、采集量、尘暴、`dust_box`、`comms`、`lots`、`sales`）
- `summary.txt` — 任务总结（覆盖率、检测精度、采集量、**集尘盒识别批次/销售额**、**星链覆盖率/时延**、**区块链统计**）
- `ledger.json` — 区块链全量哈希链（mine/asset/sale 区块）
- `snaps/lot_*.png` — 集尘盒内容物摄像快照（真实 PNG，可肉眼查看）

## 模块
- `ai_core.py::denoise_spectrum` — ASTERIS_THU 风格光谱去噪
- `ai_core.py::OreDetector` — CIANNA 风格源检测器（可在线训练的小 MLP；签名随 `--world` 切换）
- `rover_sim.py` — 世界、机器人状态机（含集尘盒排空/星链中继）、评估与 SVG 可视化
- `dustbox_vision.py` — 集尘盒视觉识别：合成摄像 PNG + 最近质心材质分类 + 资产铸造（详见 `docs/system_overview.md` 场景①）
- `starlink_comm.py` — Starlink 星链通讯：LEO 过顶窗口/时延/带宽/离线缓存队列（场景②）
- `blockchain_ledger.py` — 哈希链账本：勘探/采矿/资产/成交事件上链，做溯源、完整性校验、多机共识（详见 `docs/blockchain.md`）

## 示例
```bash
python rover_sim.py --world depot --steps 500 --out map_depot.svg   # 集尘盒视觉识别 + 星链售卖
python rover_sim.py --world mars  --steps 600 --out map_mars.svg    # 火星采矿(含尘暴)
```

> 接真实模型：把 `OreDetector.predict` 换成 AION/ASTERIS/CIANNA 的本地推理接口即可（见根目录 README 第 2 节）。火星视觉仿真见 `docs/mars_rover.md`（用 MARE 月球仿真 + 玉兔号模型改造）。
