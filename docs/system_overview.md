# CMR 宇宙挖矿机器人 — 系统总览与内容清单

> 把家用扫地机器人改装为"宇宙挖矿机器人 (Cosmic Mining Robot, CMR)"的完整系统：
> 不锈钢机身 + 西安电子科技大学抗辐射芯片 + 广州第三代半导体编程/制造 + 火星车仿真逻辑
> + 集尘盒视觉识别 + Starlink 星链通讯 + 区块链溯源/售卖。

---

## 1. 系统总体架构（模块清单）

| 层级 | 模块 | 文件 | 作用 | 状态 |
|---|---|---|---|---|
| 硬件-移动底座 | 扫地机器人改装底盘 | `docs/hardware_mod.md` | 差速/轮式底盘、Nav2 全覆盖、LiDAR 建图（源自 oomwoo-main） | 蓝图 |
| 硬件-机身 | 316L 不锈钢外壳 | `docs/hardware_mod.md` 第3.1节 | 散热 + 粒子屏蔽，重量预算 33-49kg | 蓝图 |
| 硬件-算力/电源 | 西电抗辐射 SiC 功率器件 | `docs/hardware_mod.md` 第3.3节 | 抗单粒子电源变换（天舟六号在轨验证） | 调研 |
| 硬件-编程/制造 | 广州第三代半导体 | `docs/guangzhou_semi.md` | 西电广州创新中心(GaN 中试)设计/编译 + 南沙(SiC 衬底/车规芯片)制造 | 调研 |
| 硬件-通讯 | Starlink 用户终端 | `simulation/starlink_comm.py` | Musk 星链 LEO 通讯仿真（过顶窗口/时延/带宽/队列） | 仿真 |
| 软件-世界/决策 | 火星车仿真内核 | `simulation/rover_sim.py` | 勘探-感知-去噪-检测-采掘-中继 状态机 | 可运行 |
| 软件-机载AI | 光谱去噪+源检测 | `simulation/ai_core.py` | ASTERIS 风格去噪 + CIANNA 风格 MLP 矿石分类 | 可运行 |
| 软件-视觉识别 | 集尘盒摄像识别 | `simulation/dustbox_vision.py` | 合成摄像 PNG + 最近质心材质分类 + 资产铸造 | 可运行 |
| 软件-区块链 | 哈希链账本 | `simulation/blockchain_ledger.py` | 溯源/完整性/多机共识（PoW-lite） | 可运行 |
| 数据-链上 | 账本 JSON | `simulation/ledger.json` | 每步/每矿/每资产/每成交区块 | 运行生成 |
| 数据-遥测 | CSV 遥测 | `simulation/telemetry.csv` | 每步位置/动作/电量/集尘盒/星链/销售 | 运行生成 |
| 数据-影像 | 集尘盒快照 | `simulation/snaps/*.png` | 每批内容物真实摄像图（可肉眼查看） | 运行生成 |
| 数据-地图 | SVG 轨迹图 | `simulation/map_*.svg` | 矿脉/轨迹/探测/采矿/机器人(星链在线变绿) | 运行生成 |
| 文档 | 总蓝图/方案 | `README.md` + `docs/*` | 7 份方案文档 | 完成 |

---

## 2. 两大核心场景（本次新增）

| 场景 | 描述 | 实现文件 | 关键流程 | 产出 |
|---|---|---|---|---|
| 集尘盒视觉识别 到 区块链售卖 | 机器人集尘盒内容物经机载摄像头成像，识别材质，每批铸造为可售区块链资产 | `dustbox_vision.py` + `rover_sim.py`(`_empty_dustbox`) | 集尘盒满 到 `CameraSnap.capture()` 合成摄像图(PNG) 到 `ImageClassifier.predict()` 识别材质+置信度 到 `LotMinter.mint()` 写链(`event=asset`) 到 经 Starlink 发布成交(`event=sale`) | `lot_xxx.png` + `ledger.json` 中的 asset/sale 区块 + 销售额(¥) |
| Starlink 星链通讯 | 扫地机器人改装 CMR 通过 Musk 的 Starlink LEO 星座与地面/市场通讯 | `starlink_comm.py` + `rover_sim.py`(`_comms_relay`) | 每步 `Starlink.update()` 刷新过顶窗口 到 online 时 `flush()` 回传缓存的 asset/telemetry 消息 到 成交记录上链 | 覆盖率/时延/带宽统计 + 出网队列 |

> 说明：地球/月球基地场景下 Starlink 直连 LEO 现实可行；火星等深空场景本模块作为"星间/深空中继链路"示意模型（真实时延以分钟计，此处仅做链路调度与队列演示）。

---

## 3. 供应链 / 技术来源

| 环节 | 主体 | 地点 | 在 CMR 中的角色 | 资料 |
|---|---|---|---|---|
| 抗辐射芯片 | 西安电子科技大学 | 陕西西安（主校）+ 广州黄埔创新中心 | SiC 功率器件抗单粒子；GaN 抗辐射/耐高温器件（设计/编译环节） | `docs/guangzhou_semi.md` |
| 第三代半导体制造 | 芯粤能 / 芯聚能 / 南砂晶圆 | 广州南沙万顷沙 | SiC 衬底、车规级主驱芯片、功率模块（制造环节） | `docs/guangzhou_semi.md` |
| 移动底座 | oomwoo 开源扫地机器人 | 无 | 树莓派 + 3D 打印 + ROS2 + LiDAR + Nav2 | `oomwoo-main/` |
| 行星环境仿真 | MARE Lunar Simulator | 无 | UE5+ROS2 月球车（含玉兔号），可改造火星视觉 | `MARE-Lunar-Simulator-main/` |
| 技术选型库 | awesome-space-autonomy | 无 | 飞行软件/自主导航/在轨AI/多机协同资料 | `awesome-space-autonomy-main/` |
| 发射/入轨 | SpaceX 拼车 / 天舟 | 无 | 发射成本参考（35万美元/50kg 2026）；西电器件随天舟六号入轨验证 | `docs/hardware_mod.md` |
| 通讯 | Starlink (Musk) | 无 | LEO 星座用户终端 | `simulation/starlink_comm.py` |

---

## 4. 仿真世界档（--world）

| 世界档 | 目标天体 | 矿/目标 | 重力(m/s²) | 尘暴 | 集尘盒/星链 |
|---|---|---|---|---|---|
| `generic` | 类月默认 | 金属/稀土矿 | 1.62 | 无 | 启用 |
| `mars` | 火星 | 水冰/含水矿物 | 3.71 | 周期性(削弱太阳能+抬高噪声) | 启用 |
| `depot` | 地球/月球基地 | 风化层尘埃与矿石 | 1.62 | 无 | 主舞台(集尘售卖) |

---

## 5. 运行方式

```bash
# 需 numpy（已建隔离 venv）
VENV="C:/Users/user/.workbuddy/binaries/python/envs/cmr/Scripts/python.exe"

# 火星采矿 + 集尘盒识别 + 星链售卖
$VENV rover_sim.py --world mars --steps 600 --out map_mars.svg
# 地球/月球基地集尘售卖场景
$VENV rover_sim.py --world depot --steps 500 --out map_depot.svg
# 默认类月
$VENV rover_sim.py --world generic --steps 400
```

| 参数 | 默认 | 说明 |
|---|---|---|
| `--steps` | 800 | 仿真步数 |
| `--grid` | 60 | 地图边长 |
| `--veins` | 6 | 矿脉数量 |
| `--battery` | 100 | 初始电量(%) |
| `--seed` | 42 | 随机种子 |
| `--world` | generic | generic / mars / depot |
| `--out` | map.svg | 地图文件名 |

---

## 6. 区块链数据结构（区块）

```
Block = { index, ts, prev_hash, rover_id, event, payload, nonce, hash }
event 属于 { genesis, telemetry, mine, asset, sale, consensus, sample }
- mine   : { cell:[i,j], grade, collected, step }          # 采矿溯源
- asset  : { lot_id, material, cn_name, conf, mass_kg, grade,
             price_per_kg, value_cny, image, sellable }    # 可售资产
- sale   : { lot_id, value_cny, via:"Starlink" }           # 经星链成交
```

完整性：SHA256 哈希链 + 前导 0 难度出块；任意篡改即校验失败（见 `blockchain_ledger.py` 篡改演示）。

---

## 7. 输出文件

| 文件 | 说明 |
|---|---|
| `simulation/ledger.json` | 全量哈希链（溯源/审计/共识） |
| `simulation/telemetry.csv` | 每步遥测（含 dust_box / comms / lots / sales） |
| `simulation/summary.txt` | 任务总结 |
| `simulation/map_*.svg` | 轨迹/矿脉/探测/采矿/机器人(星链在线变绿) |
| `simulation/snaps/lot_*.png` | 集尘盒内容物真实摄像快照（可肉眼查看） |

---

## 8. 后续可扩展

- [ ] 把火星场景真正导入 MARE 做 UE5 可视化渲染
- [ ] 区块链对接真实联盟链（Hyperledger Fabric）
- [ ] 集尘盒分类器替换为真实 CNN（PyTorch/TensorFlow）并接入真实摄像头
- [ ] Starlink 深空链路时延模型（光行时 + 深空网络）
- [ ] 多机器人协作（已支持 `consensus_with()` 多机对账）
