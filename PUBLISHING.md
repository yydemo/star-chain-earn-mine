# 发布到 GitHub（指引）

本仓库已在本地完成 `git init` 并**初次提交**。现账号已确定：**yydemo**（邮箱 yaoliang@263.net）。

> ⚠️ 远端仓库名这里按惯例设为 `cosmic-mining-robot`。若你在 GitHub 上新建的仓库名不同，把下面命令里的仓库名替换成你的实际仓库名即可。

## 方式一：在 GitHub 网页新建仓库后推送（推荐）

1. 打开 https://github.com/new
2. 仓库名：`cosmic-mining-robot`（或你自己命名的仓库）
3. **不要**勾选 "Initialize with README / .gitignore / LICENSE"（本地已含）
4. 创建后，执行：

```bash
cd D:/program/扫地机转宇宙挖矿/cosmic_mining_robot
git remote add origin https://github.com/yydemo/cosmic-mining-robot.git
git branch -M main
git push -u origin main
```

## 方式二：用 GitHub CLI

```bash
gh repo create cosmic-mining-robot --public --source=. --remote=origin --push
```

## 发布前自检

- [ ] 已填写 `README.md` 顶部的 `<OOMWOO>` 真实仓库地址（第 6 节）
- [ ] 确认 `docs/guangzhou_semi.md` / `docs/hardware_mod.md` 中的产业事实仍是最新（联网核实日期见文档内）
- [ ] 可选：补充 `LICENSE`（建议 MIT 或 Apache-2.0）
- [ ] 可选：补一张 `assets/` 架构图到 README

## 仓库内容速览

```
cosmic-mining-robot/
├── README.md                 # 总蓝图（含现实可行性体检）
├── docs/
│   ├── system_overview.md     # 系统总览与内容清单（整体架构/两大场景/供应链/运行表）
│   ├── hardware_mod.md        # 不锈钢外壳 / 西电抗辐射电源算力 / 工具头
│   ├── guangzhou_semi.md      # 广州第三代半导体（西电创新中心+南沙SiC链）
│   ├── mars_rover.md          # 火星车场景 + MARE 改造
│   ├── blockchain.md          # 区块链分析模块说明
│   ├── launch_plan.md         # 发射方案与重量预算
│   └── monetization.md        # 变现路径
├── simulation/
│   ├── rover_sim.py           # 火星车仿真内核（含集尘盒/星链）
│   ├── ai_core.py             # ASTERIS 去噪 + CIANNA 矿石源检测
│   ├── dustbox_vision.py      # 集尘盒摄像识别 + 区块链资产化
│   ├── starlink_comm.py       # Starlink 星链通讯仿真
│   ├── blockchain_ledger.py   # 哈希链账本
│   └── README.md
└── assets/                    # 架构与改装可视化图
```

> 运行产物（map.svg / telemetry.csv / summary.txt / ledger.json / snaps/）已被 `.gitignore` 排除，运行时自动生成。
