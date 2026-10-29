"""
blockchain_ledger.py — CMR 区块链式分析与数据溯源模块（纯标准库，无外部依赖）

把宇宙挖矿机器人的"遥测 / 采矿 / 样品 / 多机协作"事件写入一条**哈希链**，
用区块链结构做三件事：
  1. 数据溯源 (traceability)   —— 任一矿样都能回溯到 机器人/步/坐标/品位/上链哈希
  2. 完整性校验 (integrity)    —— 任意篡改都会破坏后续区块哈希，立即被发现
  3. 多机器人共识 (consensus)  —— 多台漫游车对同一格的采矿主张，按规则对账定夺

区块结构（简化的 PoW-lite，nonce 满足前导 0 难度即"出块"）：
  Block = { index, ts, prev_hash, rover_id, event, payload, nonce, hash }

用法：
  from blockchain_ledger import Ledger
  ledger = Ledger(difficulty=2)
  ledger.add_event("R1", "mine", {"cell":(3,7),"grade":0.82})
  ledger.validate_chain()      # True / False
  ledger.analyze()             # 统计与溯源摘要
  ledger.to_json("ledger.json")

多机共识见 Ledger.consensus_with() 与模块 __main__ 演示。
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


@dataclass
class Block:
    index: int
    ts: float
    prev_hash: str
    rover_id: str
    event: str
    payload: Dict[str, Any]
    nonce: int = 0
    hash: str = ""

    def serialize_for_hash(self) -> str:
        # 不含 hash 与 nonce 自身的稳定序列化（nonce 在挖矿时迭代）
        body = json.dumps(
            {
                "index": self.index,
                "ts": self.ts,
                "prev_hash": self.prev_hash,
                "rover_id": self.rover_id,
                "event": self.event,
                "payload": self.payload,
                "nonce": self.nonce,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return body

    def mine(self, difficulty: int) -> None:
        prefix = "0" * difficulty
        while True:
            self.hash = _sha256(self.serialize_for_hash())
            if self.hash.startswith(prefix):
                break
            self.nonce += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "ts": self.ts,
            "prev_hash": self.prev_hash,
            "rover_id": self.rover_id,
            "event": self.event,
            "payload": self.payload,
            "nonce": self.nonce,
            "hash": self.hash,
        }


class Ledger:
    """单台/多台漫游车的哈希链账本。"""

    def __init__(self, difficulty: int = 2, rover_id: str = "CMR", genesis_note: str = "CMR genesis"):
        self.difficulty = difficulty
        self.rover_id = rover_id
        self.chain: List[Block] = []
        self._add_genesis(genesis_note)

    # ---- 建链 ----
    def _add_genesis(self, note: str) -> None:
        g = Block(index=0, ts=time.time(), prev_hash="0" * 64,
                  rover_id=self.rover_id, event="genesis", payload={"note": note})
        g.mine(self.difficulty)
        self.chain.append(g)

    def add_event(self, event: str, payload: Dict[str, Any], rover_id: Optional[str] = None) -> Block:
        """追加一个事件区块（采矿/遥测/样品/共识）。"""
        prev = self.chain[-1]
        rid = rover_id or self.rover_id
        b = Block(index=len(self.chain), ts=time.time(),
                  prev_hash=prev.hash, rover_id=rid, event=event, payload=payload)
        b.mine(self.difficulty)
        self.chain.append(b)
        return b

    # ---- 校验 ----
    def validate_chain(self) -> bool:
        """重算每个区块哈希与前导难度、校验 prev_hash 链接，任一不符即 False。"""
        for i, b in enumerate(self.chain):
            if _sha256(b.serialize_for_hash()) != b.hash:
                return False
            if not b.hash.startswith("0" * self.difficulty):
                return False
            if i > 0 and b.prev_hash != self.chain[i - 1].hash:
                return False
        return True

    def tamper_demo(self, index: int, payload_patch: Dict[str, Any]) -> bool:
        """演示篡改：修改某区块 payload 但不重算哈希，校验应失败。"""
        if 0 < index < len(self.chain):
            self.chain[index].payload.update(payload_patch)
            return self.validate_chain()  # 期望 False
        return True

    # ---- 分析 ----
    def analyze(self) -> Dict[str, Any]:
        blocks = self.chain[1:]  # 去掉 genesis
        mining = [b for b in blocks if b.event == "mine"]
        samples = [b for b in blocks if b.event == "sample"]
        assets = [b for b in blocks if b.event == "asset"]
        sales = [b for b in blocks if b.event == "sale"]
        cells = set()
        grades = []
        for b in mining + samples:
            c = b.payload.get("cell")
            if c is not None:
                cells.add(tuple(c) if isinstance(c, list) else c)
            if "grade" in b.payload:
                grades.append(b.payload["grade"])
        asset_value = sum(float(b.payload.get("value_cny", 0.0)) for b in assets)
        per_rover: Dict[str, int] = {}
        for b in blocks:
            per_rover[b.rover_id] = per_rover.get(b.rover_id, 0) + 1
        return {
            "total_blocks": len(self.chain),
            "event_blocks": len(blocks),
            "mining_events": len(mining),
            "sample_events": len(samples),
            "asset_events": len(assets),
            "sale_events": len(sales),
            "asset_value_cny": round(asset_value, 2),
            "unique_cells_mined": len(cells),
            "avg_grade": round(sum(grades) / len(grades), 3) if grades else None,
            "per_rover_blocks": per_rover,
            "integrity_ok": self.validate_chain(),
        }

    def trace_cell(self, cell) -> List[Dict[str, Any]]:
        """溯源：返回涉及某坐标格的所有区块（采矿/样品/争议）。"""
        cell = tuple(cell) if isinstance(cell, list) else cell
        out = []
        for b in self.chain:
            c = b.payload.get("cell")
            if c is not None and (tuple(c) if isinstance(c, list) else c) == cell:
                out.append(b.to_dict())
        return out

    # ---- 多机器人共识 ----
    def consensus_with(self, other: "Ledger",
                       rule: str = "highest_grade") -> Dict[str, Any]:
        """
        与另一台漫游车账本对账：找出"同一坐标格被多方采矿"的冲突，按规则定夺归属。
        rule: "highest_grade"（取品位高者）| "earliest"（取最早步）。
        返回冲突清单与最终归属表，并用一个 "consensus" 事件区块记下裁决。
        """
        mine_of = lambda L: [b for b in L.chain if b.event == "mine"]
        claims = {}  # cell -> list of (rover_id, step, grade, block_index)
        for L, rid in ((self, self.rover_id), (other, other.rover_id)):
            for b in mine_of(L):
                c = b.payload.get("cell")
                if c is None:
                    continue
                c = tuple(c) if isinstance(c, list) else c
                claims.setdefault(c, []).append(
                    (b.rover_id, b.payload.get("step", 0), b.payload.get("grade", 0.0), b.index))

        conflicts = {c: v for c, v in claims.items() if len(v) > 1}
        resolution = {}
        for c, v in conflicts.items():
            if rule == "earliest":
                winner = min(v, key=lambda x: x[1])
            else:  # highest_grade
                winner = max(v, key=lambda x: x[2])
            resolution[str(c)] = {"owner": winner[0], "rule": rule,
                                  "grade": winner[2], "step": winner[1]}
        # 把裁决写入本链（共识事件）
        self.add_event("consensus", {
            "rule": rule,
            "conflict_cells": [str(c) for c in conflicts],
            "resolved": resolution,
        })
        return {
            "conflict_cells": [str(c) for c in conflicts],
            "resolution": resolution,
            "integrity_self": self.validate_chain(),
            "integrity_other": other.validate_chain(),
        }

    def to_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.chain], f, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, path: str) -> "Ledger":
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        L = cls(difficulty=2)  # 重建容器，随后用文件覆盖
        L.chain = []
        for d in raw:
            b = Block(**{k: d[k] for k in ("index", "ts", "prev_hash", "rover_id",
                                           "event", "payload", "nonce", "hash")})
            L.chain.append(b)
        return L


if __name__ == "__main__":
    # 演示：两台漫游车在同一片矿区作业，对其中一格的主张产生冲突，链上对账。
    import random

    r1 = Ledger(difficulty=2, rover_id="R1")
    r2 = Ledger(difficulty=2, rover_id="R2")

    # R1 采矿若干格
    cells = [(3, 4), (3, 5), (7, 8), (10, 2), (3, 4)]  # 注意 (3,4) 重复出现
    for k, c in enumerate(cells):
        r1.add_event("mine", {"cell": list(c), "grade": round(random.uniform(0.5, 0.95), 3), "step": 10 * k})
    # R2 也采到 (3,4)（争议格），以及自己独有格
    for k, c in enumerate([(3, 4), (12, 9), (5, 5)]):
        r2.add_event("mine", {"cell": list(c), "grade": round(random.uniform(0.5, 0.95), 3), "step": 10 * k})

    print("R1 完整性:", r1.validate_chain(), "| R2 完整性:", r2.validate_chain())
    res = r1.consensus_with(r2, rule="highest_grade")
    print("冲突格:", res["conflict_cells"])
    print("裁决:", json.dumps(res["resolution"], ensure_ascii=False))
    print("对账后 R1 完整性:", r1.validate_chain())

    # 篡改演示：改 R1 某区块品位但不重算哈希
    before = r1.validate_chain()
    r1.tamper_demo(2, {"grade": 0.99})
    after = r1.validate_chain()
    print(f"篡改前完整性={before} → 篡改后完整性={after}（应变为 False，证明链不可篡改）")
