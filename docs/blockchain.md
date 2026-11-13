# 区块链结构分析模块（simulation/blockchain_ledger.py） / Blockchain Analysis Module (simulation/blockchain_ledger.py)

> 语言说明 / Language note：本文中英双语，先中文后英文。 / This document is bilingual: Chinese first, then English.

> 把宇宙挖矿机器人的勘探过程写入一条**哈希链**，用区块链结构做数据溯源、完整性校验与多机器人共识对账。
> 纯标准库实现（无 numpy 依赖），可直接被 `rover_sim.py` 调用，也可独立用于多机仿真。
>
> Writes the cosmic mining robot's exploration process into a **hash chain**, using a blockchain structure for data provenance, integrity checks and multi-robot consensus reconciliation.
> Implemented with the standard library only (no numpy dependency); it can be called directly by `rover_sim.py` or used on its own for multi-robot simulation.

---

## 1. 区块结构 / 1. Block Structure

```
Block = { index, ts, prev_hash, rover_id, event, payload, nonce, hash }
```

- `event`：事件类型，目前有 `genesis`（创世）、`telemetry`（周期遥测快照）、`mine`（采矿动作）、`sample`（样品登记）、`consensus`（多机对账裁决）。
  `event`: event type; currently `genesis`, `telemetry` (periodic telemetry snapshot), `mine` (mining action), `sample` (sample registration) and `consensus` (multi-robot reconciliation ruling).
- `payload`：业务数据（坐标、品位、步号、电量等，全部原生 Python 类型以便 JSON 序列化）。
  `payload`: business data (coordinates, grade, step number, battery, etc., all native Python types for JSON serialization).
- `hash = SHA256(index|ts|prev_hash|rover_id|event|payload|nonce)`，满足前导 `difficulty` 个 `0`（默认 2）即"出块"（轻量 PoW-lite）。
  `hash = SHA256(index|ts|prev_hash|rover_id|event|payload|nonce)`; a block is "produced" once it has `difficulty` leading `0`s (default 2) — a lightweight PoW-lite.
- 每个区块的 `prev_hash` 指向前一区块哈希，形成**不可篡改链**。
  Each block's `prev_hash` points to the previous block's hash, forming a **tamper-evident chain**.

---

## 2. 用区块链做的三类分析 / 2. Three Kinds of Analysis with the Blockchain

### ① 数据溯源（traceability） / ① Data provenance (traceability)
任一矿样都能沿链回溯：`Ledger.trace_cell((x,y))` 返回涉及该坐标格的全部区块，得到
**机器人 ID → 步号 → 坐标 → 品位 → 上链哈希** 的完整证据链。样品数据上传西电广州平台或交付科研客户时，这条链就是可信凭证。

Any ore sample can be traced back along the chain: `Ledger.trace_cell((x,y))` returns all blocks involving that grid cell, giving a complete evidence chain of
**rover ID → step number → coordinates → grade → on-chain hash**. When sample data is uploaded to the Xidian Guangzhou platform or delivered to research customers, this chain is the trusted proof.

### ② 完整性校验（integrity） / ② Integrity checks
`Ledger.validate_chain()` 重算每个区块哈希与前导难度、校验 `prev_hash` 链接。任意字段（哪怕一个品位数字）被改且未重算哈希，校验立即返回 `False`。
模块 `__main__` 内置篡改演示：`tamper_demo()` 改数据后完整性由 `True → False`。

`Ledger.validate_chain()` recomputes every block hash and the leading difficulty, and checks the `prev_hash` links. If any field (even one grade number) is changed without recomputing the hash, validation immediately returns `False`.
The module's `__main__` includes a tamper demo: after `tamper_demo()` changes data, integrity goes from `True → False`.

### ③ 多机器人共识（consensus） / ③ Multi-robot consensus
多台漫游车同一片矿区作业，可能对**同一坐标格**都宣称采矿。`Ledger.consensus_with(other, rule)` 找出冲突格并按规则定夺：

When several rovers work the same mining area, they may all claim to have mined **the same grid cell**. `Ledger.consensus_with(other, rule)` finds conflicting cells and decides by rule:
- `highest_grade`：品位高者归属（默认） / the higher grade wins (default)
- `earliest`：最早到达者归属 / the earliest arrival wins

裁决结果写入一条 `consensus` 事件区块，并返回冲突清单与归属表。这对应真实"多机器人协同勘探 + 数据确权"的需求。

The ruling is written into a `consensus` event block, and a list of conflicts and an ownership table are returned. This corresponds to the real need for "multi-robot collaborative exploration + data ownership confirmation".

---

## 3. 运行 / 3. Running

```bash
cd simulation
pip install -r requirements.txt

# 随仿真自动上链：每次运行都会生成 ledger.json 并输出区块链分析
# Automatically on-chain with the simulation: every run generates ledger.json and prints a blockchain analysis
python rover_sim.py --world mars --steps 600        # 火星场景，含尘暴/水冰 / Mars scenario with dust storms / water ice
python rover_sim.py --world generic --steps 400     # 类月对照 / moon-like baseline

# 独立演示：多机共识 + 篡改检测 / Standalone demo: multi-robot consensus + tamper detection
python blockchain_ledger.py
```

仿真输出新增 / New simulation outputs:
- `ledger.json` — 完整区块数组（可直接 `json.load` 复盘） / the full block array (replay directly with `json.load`)
- `summary.txt` 新增 `[区块链分析]` 行：区块数 / 采矿事件 / 唯一矿格 / 平均品位 / 完整性校验 / `summary.txt` gains a `[区块链分析 / Blockchain analysis]` line: block count / mining events / unique ore cells / average grade / integrity check

---

## 4. 与整体架构的衔接 / 4. Fit with the Overall Architecture

| 系统环节 / System stage | 区块链角色 / Blockchain role |
|---|---|
| 勘探-采矿-样品（rover_sim） / Exploration – mining – samples (rover_sim) | 每个动作上链，生成不可篡改作业日志 / Every action goes on-chain, producing a tamper-evident work log |
| 抗辐射算力（hardware_mod / guangzhou_semi） / Rad-hard compute (hardware_mod / guangzhou_semi) | 辐照试验、流片记录可上链做供应链溯源 / Irradiation tests and tape-out records can go on-chain for supply-chain provenance |
| 火星视觉仿真（mars_rover / MARE） / Mars vision simulation (mars_rover / MARE) | 高保真数据回灌，哈希归档供审计 / High-fidelity data fed back in, hash-archived for audit |
| 商业/科研交付（monetization） / Commercial / research delivery (monetization) | 链上矿样数据 = 稀缺资产凭证，支撑订阅/交易 / On-chain ore-sample data = proof of scarce assets, supporting subscriptions/trading |

> 诚实边界：这是**单机/小集群的本地轻量账本**（PoW-lite 演示），不是分布式公链；若要跨机构可信共享，可把本模块的区块结构对接到真实联盟链（如 Hyperledger）做节点同步。
>
> Honest limits: this is a **local lightweight ledger for a single machine / small cluster** (a PoW-lite demo), not a distributed public chain; for trusted cross-organization sharing, connect this module's block structure to a real consortium chain (e.g. Hyperledger) for node synchronization.
