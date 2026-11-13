# 发布到 GitHub（指引） / Publishing to GitHub (Guide)

> 语言说明 / Language note：中英双语，先中文后英文。 / Bilingual: Chinese first, then English.

本仓库已在本地完成 `git init` 并**初次提交**。现账号已确定：**yydemo**（邮箱 yaoliang@263.net）。

This repository has been `git init`-ed locally with an **initial commit**. The account is now set: **yydemo** (email yaoliang@263.net).

> ⚠️ 远端仓库名已设为 `star-chain-earn-mine`（中文展示名：**星链赚大矿**）。若你在 GitHub 上新建的仓库名不同，把下面命令里的仓库名替换成你的实际仓库名即可。
>
> ⚠️ The remote repository name is set to `star-chain-earn-mine` (Chinese display name: **星链赚大矿**, "Starlink Big Mining Earnings"). If the repository you create on GitHub has a different name, replace it in the commands below.

## 方式一：在 GitHub 网页新建仓库后推送（推荐） / Option 1: Create the repo on the GitHub website, then push (recommended)

1. 打开 / Open https://github.com/new
2. 仓库名 / Repository name：`star-chain-earn-mine`（或你自己命名的仓库 / or your own name）
3. **不要**勾选 "Initialize with README / .gitignore / LICENSE"（本地已含） / Do **not** tick "Initialize with README / .gitignore / LICENSE" (already present locally)
4. 创建后，执行 / After creating it, run:

```bash
cd D:/program/扫地机转宇宙挖矿/cosmic_mining_robot
git remote add origin https://github.com/yydemo/star-chain-earn-mine.git
git branch -M main
git push -u origin main
```

## 方式二：用 GitHub CLI / Option 2: Use the GitHub CLI

```bash
gh repo create star-chain-earn-mine --public --source=. --remote=origin --push
```

## 发布前自检 / Pre-publish checklist

- [ ] 已填写 `README.md` 顶部的 `<OOMWOO>` 真实仓库地址（第 6 节） / Filled in the real repository URL for `<OOMWOO>` in `README.md` (section 6)
- [ ] 确认 `docs/guangzhou_semi.md` / `docs/hardware_mod.md` 中的产业事实仍是最新（联网核实日期见文档内） / Confirmed the industry facts in `docs/guangzhou_semi.md` / `docs/hardware_mod.md` are still current (verification dates are in the documents)
- [ ] 可选：补充 `LICENSE`（建议 MIT 或 Apache-2.0） / Optional: add a `LICENSE` (MIT or Apache-2.0 suggested)
- [ ] 可选：补一张 `assets/` 架构图到 README / Optional: add an `assets/` architecture diagram to the README

## 仓库内容速览 / Repository overview

```
star-chain-earn-mine/
├── README.md                 # 总蓝图（含现实可行性体检） / master blueprint (incl. reality check)
├── docs/
│   ├── system_overview.md     # 系统总览与内容清单 / system overview and contents
│   ├── hardware_mod.md        # 不锈钢外壳 / 西电抗辐射电源算力 / 工具头 / stainless shell, Xidian rad-hard power & compute, tool head
│   ├── guangzhou_semi.md      # 广州第三代半导体（西电创新中心+南沙SiC链） / Guangzhou 3rd-gen semiconductors (Xidian Innovation Center + Nansha SiC chain)
│   ├── mars_rover.md          # 火星车场景 + MARE 改造 / Mars rover scenario + MARE adaptation
│   ├── blockchain.md          # 区块链分析模块说明 / blockchain analysis module
│   ├── launch_plan.md         # 发射方案与重量预算 / launch plan and mass budget
│   ├── monetization.md        # 变现路径 / monetization paths
│   └── manufacturing_credentials.md  # 制造与技术背书 / manufacturing and technical credentials
├── simulation/
│   ├── rover_sim.py           # 火星车仿真内核（含集尘盒/星链） / rover simulation core (dust box / Starlink)
│   ├── ai_core.py             # ASTERIS 去噪 + CIANNA 矿石源检测 / ASTERIS denoising + CIANNA ore-source detection
│   ├── dustbox_vision.py      # 集尘盒摄像识别 + 区块链资产化 / dust-box camera recognition + blockchain tokenization
│   ├── starlink_comm.py       # Starlink 星链通讯仿真 / Starlink communications simulation
│   ├── blockchain_ledger.py   # 哈希链账本 / hash-chain ledger
│   └── README.md
└── assets/                    # 架构与改装可视化图 / architecture and modification diagrams
```

> 运行产物（map.svg / telemetry.csv / summary.txt / ledger.json / snaps/）已被 `.gitignore` 排除，运行时自动生成。
>
> Run outputs (map.svg / telemetry.csv / summary.txt / ledger.json / snaps/) are excluded by `.gitignore` and generated automatically at run time.
