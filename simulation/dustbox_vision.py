"""
dustbox_vision.py — CMR 集尘盒视觉识别 & 区块链资产化模块（依赖 numpy）

扫地机器人改装后的 CMR，其集尘盒内容物通过机载摄像头成像，
经轻量图像分类器识别材质类别；每一批鉴定结果作为"可售资产"
写入区块链（见 blockchain_ledger.py 的 event="asset"），并可在
Starlink 链路畅通时发布到市场成交（event="sale"）。

  · MATERIALS       —— 材质类别与仿真市场单价(¥/kg)
  · CameraSnap      —— 合成集尘盒"摄像图像"（真实 PNG 文件，可肉眼查看）
  · write_png       —— 纯标准库 PNG 编码器（zlib），把 numpy 数组写成 .png
  · ImageClassifier —— 极简 MLP 图像分类器（训练于合成样本，本地 CPU 可跑）
  · LotMinter       —— 把鉴定批次铸造为区块链资产（含市场估价、可售标记）

用法:
  from dustbox_vision import CameraSnap, ImageClassifier, LotMinter, write_png, MATERIALS
  cam = CameraSnap(seed=7)
  img, _ = cam.capture("rare_earth", 48)   # 合成一帧摄像图 / synthesize one camera frame
  write_png("snap.png", img)               # 落盘为真实 PNG / save as a real PNG
  clf = ImageClassifier(seed=7); clf.fit()
  name, conf = clf.predict(img)
  minter = LotMinter(ledger); lot = minter.mint(name, conf, mass=3.0, "snap.png")

dustbox_vision.py — CMR dust-box visual recognition & blockchain tokenization module (needs numpy)

On the converted-vacuum CMR, the dust-box contents are imaged by the onboard camera and a
lightweight image classifier identifies the material class; each identified lot is written
to the blockchain as a "sellable asset" (event="asset" in blockchain_ledger.py) and can be
published to the market for sale when the Starlink link is up (event="sale").

  · MATERIALS       —— material classes and simulated market prices (¥/kg)
  · CameraSnap      —— synthesizes dust-box "camera images" (real PNG files you can view)
  · write_png       —— standard-library PNG encoder (zlib) that writes numpy arrays as .png
  · ImageClassifier —— minimal image classifier (trained on synthetic samples, runs on a local CPU)
  · LotMinter       —— mints identified lots as blockchain assets (with valuation and sellable flag)

Usage: see the example above (synthesize a frame, save it as PNG, classify, mint).
"""

import os
import struct
import time
import zlib

import numpy as np


# 材质类别与仿真市场单价（¥/kg）。价格为示意，便于演示"可售卖"。
# Material classes and simulated market prices (¥/kg). Prices are illustrative, to demo "sellable".
# "en" 仅用于双语显示，不写入账本。 / "en" is for bilingual display only and is not written to the ledger.
MATERIALS = {
    "rare_earth": {"cn": "稀土氧化物", "en": "Rare-earth oxides", "price": 180.0},
    "metallic":   {"cn": "金属矿",     "en": "Metallic ore", "price": 95.0},
    "silicate":   {"cn": "硅酸盐岩",   "en": "Silicate rock", "price": 12.0},
    "water_ice":  {"cn": "水冰",       "en": "Water ice", "price": 60.0},
    "organic":    {"cn": "有机物/碳质", "en": "Organic / carbonaceous", "price": 140.0},
}

# 各类材质的成像主色（RGB 0~255），用于合成"摄像图像"
# Main imaging colour of each material (RGB 0–255), used to synthesize "camera images"
_MATERIAL_COLORS = {
    "rare_earth": (90, 230, 120),   # 稀土：荧光绿 / rare earth: fluorescent green
    "metallic":   (150, 160, 190),  # 金属：冷银灰 / metal: cool silver-grey
    "silicate":   (165, 120, 80),   # 硅酸盐：土黄棕 / silicate: earthy yellow-brown
    "water_ice":  (225, 240, 255),  # 水冰：冷白 / water ice: cold white
    "organic":    (190, 90, 80),    # 有机物：赭红 / organics: ochre red
}


# ----------------------------------------------------------------------------
# 最小可用 PNG 编码器（纯标准库：zlib + struct），把 (H,W,3) uint8 写成真彩 PNG
# Minimal PNG encoder (standard library: zlib + struct) writing (H,W,3) uint8 as true-colour PNG
# ----------------------------------------------------------------------------
def write_png(path: str, arr: np.ndarray) -> None:
    """把 RGB 数组写成 PNG。 / Write an RGB array as PNG."""
    arr = np.asarray(arr, dtype=np.uint8)
    if arr.ndim != 3 or arr.shape[2] != 3:
        raise ValueError("arr 必须是 (H, W, 3) 的 uint8 数组 / arr must be a (H, W, 3) uint8 array")
    H, W, _ = arr.shape
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # 每行前缀 filter type 0 (None) / each row is prefixed with filter type 0 (None)
        raw.extend(arr[y].tobytes())
    comp = zlib.compressobj(9)
    data = comp.compress(bytes(raw)) + comp.flush()

    def _chunk(typ: bytes, body: bytes) -> bytes:
        return (struct.pack(">I", len(body)) + typ + body
                + struct.pack(">I", zlib.crc32(typ + body) & 0xFFFFFFFF))

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)  # 8bit, color type 2 (RGB)
    with open(path, "wb") as f:
        f.write(sig)
        f.write(_chunk(b"IHDR", ihdr))
        f.write(_chunk(b"IDAT", data))
        f.write(_chunk(b"IEND", b""))


# ----------------------------------------------------------------------------
# 摄像头：合成集尘盒"摄像图像"（真实可查看的 PNG）
# Camera: synthesize dust-box "camera images" (real, viewable PNGs)
# ----------------------------------------------------------------------------
class CameraSnap:
    """合成一帧集尘盒内部的彩色颗粒图像。 / Synthesize one colour image of grains inside the dust box."""

    def __init__(self, seed=7):
        self.rng = np.random.default_rng(seed)

    def capture(self, material: str, size: int = 48):
        """返回 (图像, 材质)。 / Return (image, material)."""
        base = np.array(_MATERIAL_COLORS[material], dtype=float)
        # 盒内底色（暗灰塑料） / box background (dark grey plastic)
        img = np.full((size, size, 3), 42, dtype=np.float32)
        n_grains = int(self.rng.integers(120, 260))
        for _ in range(n_grains):
            cy = int(self.rng.integers(0, size))
            cx = int(self.rng.integers(0, size))
            r = float(self.rng.uniform(1.5, 4.0))
            # 一簇颗粒（圆斑） / a cluster of grains (round spot)
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    yy, xx = cy + dy, cx + dx
                    if 0 <= yy < size and 0 <= xx < size and (dx * dx + dy * dy) <= r * r:
                        tint = base + self.rng.normal(0, 35, 3)
                        img[yy, xx] = np.clip(tint, 0, 255)
        # 传感器噪声 / sensor noise
        img = np.clip(img + self.rng.normal(0, 8, img.shape), 0, 255).astype(np.uint8)
        return img, material


# ----------------------------------------------------------------------------
# 图像分类器：极简 MLP（输入=块平均特征，隐藏层，输出=5 类材质）
# Image classifier: minimal MLP (input = block-average features, hidden layer, output = 5 material classes)
# ----------------------------------------------------------------------------
class ImageClassifier:
    """集尘盒材质分类器（当前实现为最近质心）。 / Dust-box material classifier (currently nearest-centroid)."""

    CLASSES = list(MATERIALS.keys())

    def __init__(self, seed=7, hidden=20):
        self.rng = np.random.default_rng(seed)
        self.hidden = hidden
        self.W1 = None
        self.b1 = None
        self.W2 = None
        self.b2 = None

    @staticmethod
    def _feat(img: np.ndarray):
        """4x4 块平均/通道 + 通道均值/标准差，作为图像特征（54 维）。
        4x4 block averages per channel + per-channel mean/std as image features (54-dim)."""
        H, W, _ = img.shape
        bs = max(1, H // 4)
        small = img.reshape(4, bs, 4, bs, 3).mean(axis=(1, 3))  # (4, 4, 3)
        f = small.flatten().astype(float).tolist()
        for c in range(3):
            f.append(float(img[:, :, c].mean()))
            f.append(float(img[:, :, c].std()))
        return np.array(f, dtype=float) / 255.0

    def fit(self, n_per_class: int = 60):
        """训练 = 计算每类材质在特征空间中的质心（最近质心分类器）。
        材质基础色差异显著，质心法稳定且无需梯度优化，适合'简单识别'场景。
        Training = computing each material's centroid in feature space (nearest-centroid classifier).
        Base colours differ strongly, so the centroid method is stable and needs no gradient
        optimization — suitable for 'simple recognition'."""
        cam = CameraSnap(seed=int(self.rng.integers(0, 1_000_000)))
        feats = {ci: [] for ci in range(len(self.CLASSES))}
        for ci, name in enumerate(self.CLASSES):
            for _ in range(n_per_class):
                img, _ = cam.capture(name, size=48)
                feats[ci].append(self._feat(img))
        self.centroids = [np.mean(np.array(feats[ci], dtype=float), axis=0)
                          for ci in range(len(self.CLASSES))]

    def predict(self, img: np.ndarray):
        """返回 (材质, 置信度)。 / Return (material, confidence)."""
        x = self._feat(np.asarray(img, dtype=np.uint8))
        d = np.array([float(np.linalg.norm(x - c)) for c in self.centroids])
        ci = int(np.argmin(d))
        # 置信度：用距离的倒数归一（越近越可信） / confidence: normalized inverse distance (closer = more confident)
        inv = 1.0 / (d + 1e-6)
        conf = float(inv[ci] / inv.sum())
        return self.CLASSES[ci], conf


# ----------------------------------------------------------------------------
# 资产铸造：把一批鉴定结果写入区块链（可售）
# Asset minting: write one identified lot to the blockchain (sellable)
# ----------------------------------------------------------------------------
class LotMinter:
    """把鉴定批次铸造为链上资产。 / Mint identified lots as on-chain assets."""

    def __init__(self, ledger, seq=0):
        self.ledger = ledger
        self.seq = seq

    def mint(self, material: str, conf: float, mass_kg: float,
             image_path: str, grade: float = 0.5):
        """铸造一批资产并上链，返回批次字典。 / Mint one lot on-chain and return the lot dict."""
        info = MATERIALS[material]
        # 市场估价：单价 × 质量 × 品位系数（品位越高越值钱）
        # Market valuation: unit price × mass × grade factor (higher grade = more valuable)
        value = info["price"] * mass_kg * (0.5 + 0.5 * grade)
        self.seq += 1
        lot = {
            "lot_id": f"LOT-{self.seq:05d}",
            "material": material,
            "cn_name": info["cn"],
            "conf": round(float(conf), 3),
            "mass_kg": round(float(mass_kg), 3),
            "grade": round(float(grade), 3),
            "price_per_kg": info["price"],
            "value_cny": round(float(value), 2),
            "image": os.path.basename(image_path) if image_path else "",
            "sellable": True,
            "ts": time.time(),
        }
        # 资产上链：溯源 + 完整性（任一矿样可沿哈希链回溯）
        # Put the asset on-chain: provenance + integrity (any sample can be traced along the hash chain)
        self.ledger.add_event("asset", lot)
        return lot


if __name__ == "__main__":
    cam = CameraSnap(seed=7)
    clf = ImageClassifier(seed=7)
    clf.fit()
    ok = 0
    n = 50
    for name in ImageClassifier.CLASSES:
        for _ in range(n // len(ImageClassifier.CLASSES)):
            img, true = cam.capture(name, 48)
            pred, conf = clf.predict(img)
            if pred == true:
                ok += 1
    print(f"分类器自测准确率 / Classifier self-test accuracy: {ok}/{n} = {ok / n:.2f}")
