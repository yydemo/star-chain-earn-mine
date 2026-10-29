"""
rover_sim.py — 宇宙挖矿机器人 (CMR) 本地自主勘探-采矿仿真

不依赖任何付费服务，纯本地运行（仅需 numpy）。演示核心 AI 决策闭环：

  勘探(explore) → 多光谱感知(sense) → ASTERIS风格去噪(denoise)
    → CIANNA风格矿石源检测(detect) → 接近(approach) → 钻采(mine)
    → 样品入库 → 中继回传(relay) → 续航管理 → 循环

两大新增子系统（详见 docs/system_overview.md）：
  · 集尘盒视觉识别 → 区块链售卖：集尘盒满时摄像头成像(真实PNG) → 材质分类 → 铸造可售资产上链
  · Starlink 星链通讯：每步刷新 LEO 过顶窗口，online 时回传缓存的 asset/telemetry 消息

用法:
  python rover_sim.py --steps 400 --out map.svg
  python rover_sim.py --grid 60 --veins 6 --battery 100 --seed 42

输出（写入本目录）:
  map.svg        轨迹 / 矿脉 / 探测点 / 采矿点地图
  telemetry.csv  每步遥测
  summary.txt    任务总结
"""

import argparse
import csv
import math
import os
import random

import numpy as np

from ai_core import OreDetector, denoise_spectrum
from blockchain_ledger import Ledger
from starlink_comm import Starlink
from dustbox_vision import CameraSnap, ImageClassifier, LotMinter, write_png, MATERIALS

# 集尘盒摄像快照输出目录（位于本仿真目录下的 snaps/）
SNAP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snaps")


# ----------------------------------------------------------------------------
# 世界：地外天体表面（网格 + 矿脉 + 多光谱场）
# ----------------------------------------------------------------------------
# 不同目标天体的"环境 + 光谱"配置。generic 保持原月球类默认行为；
# mars 引入红色风化层、含水矿物/水冰信号、尘暴与低重力参数。
WORLD_PROFILES = {
    "generic": {
        "ore_sig":  np.array([0.20, 0.25, 0.85, 0.90, 0.30, 0.15]),  # 金属/稀土特征峰
        "rock_sig": np.array([0.55, 0.50, 0.45, 0.40, 0.35, 0.30]),  # 硅酸盐平缓
        "reg_sig":  np.array([0.70, 0.68, 0.66, 0.64, 0.62, 0.60]),  # 风化层平坦偏亮
        "ore_label": "ore deposit",
        "body": "generic extraterrestrial body",
        "bg": "#0b1020", "reg_tint": "#1b3a6b",
        "sensor_noise": 0.05,
        "day_cycle": 40, "day_frac": 0.7,
        "solar_day": 0.8, "solar_night": 0.1,
        "gravity": 1.62,           # m/s^2，类月
        "dust_storm": None,        # 无尘暴
    },
    "mars": {
        # 火星：含水矿物 / 水冰在近红外有强吸收-陡峰特征；玄武岩围岩偏暗；风化层偏红
        "ore_sig":  np.array([0.30, 0.26, 0.20, 0.92, 0.95, 0.24]),  # 含水矿物/水冰：IR 强峰
        "rock_sig": np.array([0.40, 0.38, 0.36, 0.34, 0.32, 0.30]),  # 玄武岩偏暗
        "reg_sig":  np.array([0.85, 0.70, 0.55, 0.50, 0.45, 0.40]),  # 红色风化层（红高蓝低）
        "ore_label": "water-ice / hydrated mineral",
        "body": "Mars",
        "bg": "#160b06", "reg_tint": "#5a2410",
        "sensor_noise": 0.06,
        "day_cycle": 50, "day_frac": 0.6,    # 火星太阳日 ~24.6h
        "solar_day": 0.7, "solar_night": 0.08,
        "gravity": 3.71,           # m/s^2，火星
        # 全球性尘暴：周期性发生，显著削弱太阳能并抬高传感器噪声
        "dust_storm": {"period": 160, "duration": 22, "noise_mult": 2.3, "solar_mult": 0.18},
    },
    "depot": {
        # 地球/月球基地集尘场景：以扫掠积尘为主，集尘盒视觉识别+星链售卖的主舞台
        "ore_sig":  np.array([0.20, 0.25, 0.85, 0.90, 0.30, 0.15]),
        "rock_sig": np.array([0.55, 0.50, 0.45, 0.40, 0.35, 0.30]),
        "reg_sig":  np.array([0.70, 0.68, 0.66, 0.64, 0.62, 0.60]),
        "ore_label": "lunar/earth regolith dust & ore",
        "body": "Lunar/Earth depot (Starlink relay)",
        "bg": "#0a0e14", "reg_tint": "#243b53",
        "sensor_noise": 0.05,
        "day_cycle": 40, "day_frac": 0.7,
        "solar_day": 0.8, "solar_night": 0.1,
        "gravity": 1.62,           # m/s^2，类月基地
        "dust_storm": None,
    },
}


class World:
    def __init__(self, grid=60, veins=6, seed=7, profile="generic"):
        self.N = grid
        self.profile_name = profile
        self.P = WORLD_PROFILES[profile]
        self.rng = np.random.default_rng(seed)
        self.ore = np.zeros((grid, grid), dtype=float)        # 真实品位 0~1
        self.cls = np.full((grid, grid), 2, dtype=int)        # 0 ore /1 rock /2 regolith
        self.spec = np.zeros((grid, grid, 6), dtype=float)     # 真实 6 通道光谱
        self._generate(veins)
        # 传感器噪声水平（模拟深空弱信号；尘暴时由 Rover 临时放大）
        self.sensor_noise = self.P["sensor_noise"]

    def _generate(self, veins):
        ore_sig = self.P["ore_sig"]
        rock_sig = self.P["rock_sig"]
        reg_sig = self.P["reg_sig"]
        # 背景：风化层
        for i in range(self.N):
            for j in range(self.N):
                self.spec[i, j] = reg_sig.copy()
                self.cls[i, j] = 2
        # 矿脉：高斯团簇
        for _ in range(veins):
            cx, cy = self.rng.integers(4, self.N - 4, size=2)
            sigma = self.rng.uniform(2.0, 4.5)
            peak = self.rng.uniform(0.6, 1.0)
            for i in range(self.N):
                for j in range(self.N):
                    d2 = (i - cx) ** 2 + (j - cy) ** 2
                    g = peak * math.exp(-d2 / (2 * sigma ** 2))
                    if g > self.ore[i, j]:
                        self.ore[i, j] = g
                        if g > 0.25:
                            self.cls[i, j] = 0  # 矿石 / 火星=水冰·含水矿物
                            self.spec[i, j] = ore_sig * (0.55 + 0.45 * g) + 0.05
                        else:
                            self.cls[i, j] = 1  # 围岩
                            self.spec[i, j] = rock_sig.copy()

    def read_spectrum(self, i, j, noise=None):
        """传感器读数：真实光谱 + 噪声（对应"ASTERIS 去噪"的输入）。
        noise 可临时覆盖（如火星尘暴时抬高）。"""
        n = self.sensor_noise if noise is None else noise
        s = self.spec[i, j] + self.rng.normal(0, n, size=6)
        return np.clip(s, 0, None)

    def in_dust_storm(self, step):
        ds = self.P.get("dust_storm")
        if not ds:
            return False
        return (step % ds["period"]) < ds["duration"]

    def ore_rgb(self, g):
        """矿脉/水冰着色：generic=gold，mars=cyan→white"""
        if self.profile_name == "mars":
            r = int(60 + 120 * (1 - g))
            gg = int(160 + 60 * g)
            b = int(200 + 55 * g)
            return r, gg, b
        r = int(40 + 200 * g)
        gg = int(60 + 120 * (1 - g))
        b = int(120 * (1 - g))
        return r, gg, b


# ----------------------------------------------------------------------------
# 机器人：差速底盘（网格化表示）+ 工具头 + 抗辐射电源（简化模型）
# ----------------------------------------------------------------------------
class Rover:
    ACTIONS = ["EXPLORE", "APPROACH", "MINE", "RECHARGE", "RELAY"]

    def __init__(self, world, battery=100, seed=3):
        self.w = world
        self.x = world.N // 2
        self.y = world.N // 2
        self.battery = battery
        self.max_battery = battery
        self.inventory = 0.0          # 已采集品位总量
        self.steps = 0
        self.searched = set()
        self.detected = set()         # 已确认的矿石目标格 (i,j)
        self.resolved = set()         # 已判定为非矿/已采格，避免重复追击导致振荡
        self.mined = []               # (i,j,amount)
        # 检测器签名与世界签名一致（火星场景需重新学习红色风化层/水冰/玄武岩信号）
        sigs = {"ore": world.P["ore_sig"], "rock": world.P["rock_sig"],
                "regolith": world.P["reg_sig"]}
        self.detector = OreDetector(seed=seed, signatures=sigs)
        self.detector.fit()           # 机载模型训练（对应 CIANNA 检测器初始化）
        self.conf_thr = 0.90
        self.cell_name, self.cell_conf = "regolith", 0.0  # 本格预测缓存（避免重复读数抖动）
        self.day_cycle = world.P["day_cycle"]
        self.day_frac = world.P["day_frac"]
        self.solar_day = world.P["solar_day"]
        self.solar_night = world.P["solar_night"]
        self.storm_steps = 0
        self.in_storm = False
        self.rng = random.Random(seed)
        # ---- 新增子系统：集尘盒视觉识别 + 星链通讯 + 区块链资产化 ----
        self.dust_box = 0.0            # 集尘盒当前装载量(kg)
        self.dust_capacity = 12.0      # 集尘盒容量(kg)，满则触发视觉识别/资产化
        self.lots = []                 # 已铸造的资产批次
        self.sales_value = 0.0         # 经星链成交累计销售额(¥)
        self.starlink = Starlink(seed=seed)
        self.cam = CameraSnap(seed=seed)
        self.clf = ImageClassifier(seed=seed)
        self.clf.fit()                 # 机载图像分类器训练（对应集尘盒视觉识别）
        self.ledger = None             # 由 main 注入
        self.minter = None             # 由 main 注入

    def sense(self, radius=3, noise=None):
        """感知周围网格，去噪+检测，记录高置信矿石候选；并缓存本格预测。
        noise 可临时抬高（火星尘暴），传入 World.read_spectrum。"""
        N = self.w.N
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                i, j = self.x + di, self.y + dj
                if 0 <= i < N and 0 <= j < N:
                    self.searched.add((i, j))
                    raw = self.w.read_spectrum(i, j, noise=noise)
                    name, conf = self.detector.predict(raw)
                    if i == self.x and j == self.y:
                        self.cell_name, self.cell_conf = name, conf  # 本格预测缓存
                    if name == "ore" and conf >= self.conf_thr and (i, j) not in self.resolved:
                        self.detected.add((i, j))

    def _move_toward(self, tx, ty):
        """朝目标走一步（差速底盘的网格化近似），耗电"""
        dx = np.sign(tx - self.x)
        dy = np.sign(ty - self.y)
        if dx != 0 and (dy == 0 or self.rng.random() < 0.5):
            self.x += dx
        else:
            self.y += dy
        self.x = max(0, min(self.w.N - 1, self.x))
        self.y = max(0, min(self.w.N - 1, self.y))
        self.battery -= 0.4

    def _nearest_detected(self):
        if not self.detected:
            return None
        return min(self.detected, key=lambda p: abs(p[0] - self.x) + abs(p[1] - self.y))

    def step(self, telemetry):
        self.steps += 1
        # 0) 星链链路状态刷新（每步更新可见窗口/时延/带宽）
        self.starlink.update(self.steps)
        is_day = (self.steps % self.day_cycle) < self.day_cycle * self.day_frac
        action = "EXPLORE"

        # 火星尘暴：周期性削弱太阳能 + 抬高传感器噪声
        self.in_storm = self.w.in_dust_storm(self.steps)
        if self.in_storm:
            self.storm_steps += 1
        ds = self.w.P.get("dust_storm")
        storm_noise = (self.w.sensor_noise * ds["noise_mult"]) if (self.in_storm and ds) else None
        solar_gain = self.solar_day if is_day else self.solar_night
        if self.in_storm and ds:
            solar_gain *= ds["solar_mult"]

        # 1) 续航优先
        if self.battery < 15:
            action = "RECHARGE"
            self.battery = min(self.max_battery, self.battery + (3.0 if is_day else 0.6))
        else:
            # 2) 感知（尘暴时噪声更高，仍由 ASTERIS 去噪兜底）
            self.sense(noise=storm_noise)
            # 3) 集尘盒满 → 视觉识别 + 资产化 + 经星链上链售卖（优先于采掘）
            if self.dust_box >= self.dust_capacity and self.battery > 12:
                self._empty_dustbox()
                action = "EMPTY"
                self.battery -= 1.0
            else:
                # 当前格是否可采
                here_ore = self.w.ore[self.x, self.y]
                name, conf = self.cell_name, self.cell_conf  # 用 sense() 缓存的本格预测
                if name == "ore" and conf >= self.conf_thr and here_ore > 0.25 and self.battery > 18:
                    action = "MINE"
                    amount = here_ore * 0.5
                    self.inventory += amount
                    self.w.ore[self.x, self.y] = max(0.0, here_ore - 0.5)
                    self.w.spec[self.x, self.y] = self.w.P["reg_sig"].copy()  # 恢复风化层光谱
                    self.detected.discard((self.x, self.y))
                    self.resolved.add((self.x, self.y))
                    self.mined.append((self.x, self.y, round(here_ore, 3),
                                       round(amount, 3), self.steps))
                    self.battery -= 2.5
                    self.dust_box += amount  # 采出物进入集尘盒
                    # 采矿事件上链（溯源 + 完整性）
                    self.ledger.add_event("mine", {"cell": [int(self.x), int(self.y)],
                                                   "grade": round(float(here_ore), 3),
                                                   "collected": round(float(amount), 3),
                                                   "step": int(self.steps)})
                else:
                    # 已登记目标但不可采 → 永久解析，杜绝反复追击
                    if (self.x, self.y) in self.detected:
                        self.detected.discard((self.x, self.y))
                        self.resolved.add((self.x, self.y))
                    target = self._nearest_detected()
                    dist = abs(target[0] - self.x) + abs(target[1] - self.y) if target else 0
                    if target and dist > 0:
                        action = "APPROACH"
                        self._move_toward(target[0], target[1])
                    else:
                        action = "EXPLORE"
                        self._explore_move()

            # 扫掠积尘：移动/作业都会向集尘盒积攒内容物（不超过容量）
            self.dust_box = min(self.dust_capacity, self.dust_box + 0.6)
            # 太阳能缓释
            self.battery = min(self.max_battery, self.battery + solar_gain)
            # 星链中继：online 时回传缓存的资产发布/遥测
            self._comms_relay()
            # 周期性中继（记账）
            if self.steps % 25 == 0:
                action = "RELAY"
                self.starlink.enqueue({"type": "telemetry", "step": self.steps,
                                       "battery": round(float(self.battery), 1),
                                       "inventory": round(float(self.inventory), 3)})

        telemetry.append({
            "step": self.steps, "x": int(self.x), "y": int(self.y), "action": action,
            "battery": round(float(self.battery), 1), "inventory": round(float(self.inventory), 3),
            "detected": len(self.detected),
            "mined": len(self.mined),
            "storm": int(self.in_storm),
            "dust_box": round(float(self.dust_box), 2),
            "comms": int(self.starlink.online),
            "lots": len(self.lots),
            "sales": round(float(self.sales_value), 2),
        })

    def _explore_move(self):
        N = self.w.N
        # 朝最近的未探索格移动（边界扩张式覆盖，对应 Nav2 全覆盖勘探）
        candidates = [(i, j) for i in range(N) for j in range(N) if (i, j) not in self.searched]
        if not candidates:
            return
        best = min(candidates, key=lambda p: abs(p[0] - self.x) + abs(p[1] - self.y))
        self._move_toward(best[0], best[1])

    # ---- 集尘盒视觉识别 / 区块链资产化 / 星链售卖 ----
    def _pick_material(self, true_cls):
        """按当前格真实类别与世界档，挑一个"真实主材质"（用于合成摄像图）。"""
        rng = self.rng
        if self.w.profile_name == "mars":
            if true_cls == 0:
                return "water_ice"
            if true_cls == 1:
                return rng.choice(["silicate", "metallic"])
            return rng.choice(["organic", "silicate"])
        # generic / depot
        if true_cls == 0:
            return rng.choice(["rare_earth", "metallic"])
        if true_cls == 1:
            return rng.choice(["metallic", "silicate"])
        return rng.choice(["silicate", "organic", "rare_earth"])

    def _empty_dustbox(self):
        """集尘盒满 → 摄像头成像 → 图像分类 → 铸造可售区块链资产。"""
        true_cls = int(self.w.cls[self.x, self.y])
        mat = self._pick_material(true_cls)
        img, _ = self.cam.capture(mat, size=48)
        # 保存摄像快照（限量前 8 批，避免刷屏），真实 PNG 可肉眼查看
        img_path = ""
        lot_idx = len(self.lots)
        if lot_idx < 8:
            try:
                os.makedirs(SNAP_DIR, exist_ok=True)
                img_path = os.path.join(SNAP_DIR, f"lot_{lot_idx:03d}.png")
                write_png(img_path, img)
            except Exception:
                img_path = ""
        name, conf = self.clf.predict(img)
        grade = min(1.0, conf * (0.6 + 0.4 * (float(self.w.ore[self.x, self.y])
                                              if true_cls == 0 else 0.3)))
        mass = float(self.dust_box)
        lot = self.minter.mint(name, conf, mass, img_path, grade=grade)
        self.lots.append(lot)
        self.dust_box = 0.0
        # 资产已上链(ledger event="asset")；发布到市场需经 Starlink 中继
        self.starlink.enqueue({"type": "asset", "lot": lot})

    def _comms_relay(self):
        """星链畅通时回传缓存的资产发布消息，并记成交(sale)上链。"""
        if not self.starlink.online:
            return
        sent = self.starlink.flush()
        for m in sent:
            if isinstance(m, dict) and m.get("type") == "asset":
                lot = m["lot"]
                self.sales_value += float(lot["value_cny"])
                self.ledger.add_event("sale", {"lot_id": lot["lot_id"],
                                               "value_cny": float(lot["value_cny"]),
                                               "via": "Starlink"})


# ----------------------------------------------------------------------------
# 评估 & 可视化
# ----------------------------------------------------------------------------
def evaluate(rover, world):
    """用已探索区域对比检测精度（ground truth vs 检测）"""
    tp = fp = fn = 0
    for (i, j) in rover.searched:
        true_ore = world.cls[i, j] == 0
        pred_ore = (i, j) in rover.detected
        if true_ore and pred_ore:
            tp += 1
        elif (not true_ore) and pred_ore:
            fp += 1
        elif true_ore and (not pred_ore):
            fn += 1
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return tp, fp, fn, prec, rec


def make_svg(world, rover, path, out_path):
    N = world.N
    cell = 9
    size = N * cell + 20
    bg = world.P["bg"]
    reg_tint = world.P["reg_tint"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
             f'viewBox="0 0 {size} {size}" font-family="monospace">']
    parts.append(f'<rect width="{size}" height="{size}" fill="{bg}"/>')
    # 矿脉底色（按品位着色：generic=gold，mars=cyan→white）
    for i in range(N):
        for j in range(N):
            g = world.ore[i, j]
            if g > 0.05:
                r, gg, b = world.ore_rgb(g)
                parts.append(f'<rect x="{10 + j * cell}" y="{10 + i * cell}" '
                             f'width="{cell}" height="{cell}" fill="rgb({r},{gg},{b})" opacity="0.9"/>')
    # 已探索区域（淡色）
    for (i, j) in rover.searched:
        parts.append(f'<rect x="{10 + j * cell}" y="{10 + i * cell}" width="{cell}" '
                     f'height="{cell}" fill="{reg_tint}" opacity="0.18"/>')
    # 轨迹
    if len(path) > 1:
        pts = " ".join(f"{10 + p[1] * cell + cell / 2},{10 + p[0] * cell + cell / 2}" for p in path)
        parts.append(f'<polyline points="{pts}" fill="none" stroke="#39d0ff" '
                     f'stroke-width="1.2" opacity="0.7"/>')
    # 探测点（青圈）
    for (i, j) in rover.detected:
        parts.append(f'<circle cx="{10 + j * cell + cell / 2}" cy="{10 + i * cell + cell / 2}" '
                     f'r="3" fill="none" stroke="#00ffc8" stroke-width="1.2"/>')
    # 采矿点（红叉）
    for (i, j, *_) in rover.mined:
        cx, cy = 10 + j * cell + cell / 2, 10 + i * cell + cell / 2
        parts.append(f'<line x1="{cx - 3}" y1="{cy - 3}" x2="{cx + 3}" y2="{cy + 3}" stroke="#ff5a5a" stroke-width="1.5"/>')
        parts.append(f'<line x1="{cx - 3}" y1="{cy + 3}" x2="{cx + 3}" y2="{cy - 3}" stroke="#ff5a5a" stroke-width="1.5"/>')
    # 机器人（星链在线=绿，离线=黄）
    rx, ry = 10 + rover.y * cell + cell / 2, 10 + rover.x * cell + cell / 2
    robot_color = "#39ff88" if getattr(rover.starlink, "online", False) else "#ffd54a"
    parts.append(f'<circle cx="{ry}" cy="{rx}" r="4" fill="{robot_color}" stroke="#fff" stroke-width="1"/>')
    world_tag = world.P["body"]
    sl = getattr(rover, "starlink", None)
    cov = f" starlink_cov={sl.coverage_ratio():.2f}" if sl else ""
    parts.append(f'<text x="10" y="{size - 4}" fill="#9fb3c8" font-size="11">'
                 f'CMR · {world_tag} · explored={len(rover.searched)} · detected={len(rover.detected)} '
                 f'· mined={len(rover.mined)} · lots={len(getattr(rover, "lots", []))} '
                 f'· sales=¥{getattr(rover, "sales_value", 0):.0f}{cov}</text>')
    parts.append('</svg>')
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


# ----------------------------------------------------------------------------
# 主程序
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Cosmic Mining Rover simulation")
    ap.add_argument("--steps", type=int, default=800)
    ap.add_argument("--grid", type=int, default=60)
    ap.add_argument("--veins", type=int, default=6)
    ap.add_argument("--battery", type=float, default=100)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default="map.svg")
    ap.add_argument("--world", type=str, default="generic",
                    choices=["generic", "mars", "depot"],
                    help="世界配置档：generic(类月默认) / mars(火星) / depot(地球月球基地集尘场景)")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    world = World(grid=args.grid, veins=args.veins, seed=args.seed, profile=args.world)
    rover = Rover(world, battery=args.battery, seed=args.seed)
    # 区块链账本：溯源 + 完整性 + 多机共识（见 blockchain_ledger.py）
    ledger = Ledger(difficulty=2, rover_id="CMR")
    rover.ledger = ledger
    rover.minter = LotMinter(ledger)
    telemetry = []

    path = [(rover.x, rover.y)]
    for _ in range(args.steps):
        rover.step(telemetry)
        path.append((rover.x, rover.y))

    # 输出 CSV
    csv_path = os.path.join(here, "telemetry.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["step", "x", "y", "action", "battery",
                                          "inventory", "detected", "mined", "storm",
                                          "dust_box", "comms", "lots", "sales"])
        w.writeheader()
        w.writerows(telemetry)

    # 输出 SVG
    svg_path = os.path.join(here, args.out)
    make_svg(world, rover, path, svg_path)

    # 区块链：采矿/资产/销售事件已在前面的 step() 内即时上链
    ledger_json_path = os.path.join(here, "ledger.json")
    ledger.to_json(ledger_json_path)
    analysis = ledger.analyze()

    # 评估
    tp, fp, fn, prec, rec = evaluate(rover, world)
    explored_pct = 100.0 * len(rover.searched) / (args.grid * args.grid)
    storm_note = f"{rover.storm_steps} 步处于尘暴" if world.P["dust_storm"] else "无尘暴"
    sl = rover.starlink
    summary = (
        f"==== Cosmic Mining Rover — 任务总结 ====\n"
        f"目标天体        : {world.P['body']} (profile={args.world})\n"
        f"步数            : {rover.steps}\n"
        f"地图尺寸        : {args.grid}x{args.grid}\n"
        f"探索覆盖率      : {explored_pct:.1f}%\n"
        f"目标类型        : {world.P['ore_label']}\n"
        f"矿石检出(去重)  : {len(rover.detected)}\n"
        f"已采矿点        : {len(rover.mined)}\n"
        f"采集品位总量    : {rover.inventory:.3f}\n"
        f"剩余电量        : {rover.battery:.1f}%\n"
        f"尘暴影响        : {storm_note}\n"
        f"检测精度        : 精确率={prec:.2f} 召回率={rec:.2f} (TP={tp} FP={fp} FN={fn})\n"
        f"重力(参考)      : {world.P['gravity']} m/s^2\n"
        f"--------------------------------------\n"
        f"[集尘盒视觉] 排空批次={len(rover.lots)} 经星链成交销售额=¥{rover.sales_value:.2f}\n"
        f"  示例批次: " + "; ".join(
            f"{l['lot_id']}:{l['cn_name']}(conf={l['conf']},¥{l['value_cny']})"
            for l in rover.lots[:5]) + "\n"
        f"[星链通讯] 覆盖率={sl.coverage_ratio():.2f} 回传消息={sl.sent_total} "
        f"当前缓存={len(sl.outbox)} 时延≈{sl.latency_ms:.0f}ms\n"
        f"--------------------------------------\n"
        f"[区块链分析] 区块数={analysis['total_blocks']} 采矿={analysis['mining_events']} "
        f"资产={analysis['asset_events']} 成交={analysis['sale_events']} "
        f"资产估值=¥{analysis['asset_value_cny']}\n"
        f"  唯一矿格={analysis['unique_cells_mined']} 平均品位={analysis['avg_grade']} "
        f"完整性={'通过' if analysis['integrity_ok'] else '失败'}\n"
        f"--------------------------------------\n"
        f"输出文件        : {svg_path}\n"
        f"                : {csv_path}\n"
        f"                : {ledger_json_path}\n"
        f"                : {SNAP_DIR} (集尘盒摄像快照 PNG)\n"
    )
    sum_path = os.path.join(here, "summary.txt")
    with open(sum_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
