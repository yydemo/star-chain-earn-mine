"""
ai_core.py — CMR 机载 AI 内核（纯 numpy，无外部付费依赖）

两个模块，分别对应开源天文 AI 工具的"轻量化移植"思路：
  · denoise_spectrum()  —— 对应 ASTERIS_THU：自监督成像/光谱去噪，提升弱信号探测极限
  · OreDetector         —— 对应 CIANNA：YOLO 风格"源检测器"的极简可运行版
                           （这里用一个小 MLP 做矿石源的多光谱分类）

所有运算可在本地 CPU 跑；若换 GPU + 真实模型权重，可直接替换为
AION / ASTERIS / CIANNA 的推理接口（见 README 第 2 节）。
"""

import numpy as np


# ----------------------------------------------------------------------------
# 1) ASTERIS_THU 风格去噪：中值滤波 + 轻量平滑（抑制传感器噪声，提弱信号）
# ----------------------------------------------------------------------------
def denoise_spectrum(spectrum: np.ndarray, median_k: int = 3, smooth: float = 0.15) -> np.ndarray:
    """
    对一维光谱做去噪：先中值滤波去脉冲噪声，再做轻微均值平滑。
    spectrum: shape (B,) 的多光谱/高光谱向量
    返回去噪后的向量（同 shape）
    """
    s = np.asarray(spectrum, dtype=float)
    B = s.shape[0]
    pad = median_k // 2
    padded = np.concatenate([s[:pad][::-1], s, s[-pad:][::-1]])
    med = np.empty(B, dtype=float)
    for i in range(B):
        win = padded[i:i + median_k]
        med[i] = np.median(win)
    # 轻量平滑：与原始做加权，保留边缘（mode="same" 直接对齐长度）
    smoothed = np.convolve(med, np.array([0.25, 0.5, 0.25]), mode="same")
    out = (1.0 - smooth) * med + smooth * smoothed
    return out


# ----------------------------------------------------------------------------
# 2) CIANNA 风格"源检测器"：多光谱矿石分类小网络（可在线训练）
# ----------------------------------------------------------------------------
def extract_features(spectrum: np.ndarray) -> np.ndarray:
    """
    从 B 通道光谱中提取固定维度特征。
    波段比值（band ratio）正是真实矿物遥感的核心手段（如氧化铁、含水矿物指数）。
    """
    s = np.asarray(spectrum, dtype=float)
    B = s.shape[0]
    feats = [float(np.mean(s)), float(np.std(s))]
    # 选取若干波段比值/差值，鲁棒处理除零
    idx = [(min(2, B - 1), 0), (min(4, B - 1), 1), (min(3, B - 1), max(0, B - 1))]
    for hi, lo in idx:
        denom = s[lo] if abs(s[lo]) > 1e-6 else 1e-6
        feats.append(float((s[hi] - s[lo])))
        feats.append(float((s[hi] / denom)))
    return np.array(feats, dtype=float)


class OreDetector:
    """
    极简 2 层 MLP（输入特征 -> hidden -> 3 类：矿石 / 岩石 / 风化层）。
    初始化时用"物理动机"的合成光谱签名训练，使它能够区分三类地物。
    """

    CLASSES = ["ore", "rock", "regolith"]

    def __init__(self, hidden: int = 12, seed: int = 7, signatures: dict | None = None):
        self.hidden = hidden
        self.rng = np.random.default_rng(seed)
        self.W1 = None
        self.b1 = None
        self.W2 = None
        self.b2 = None
        # 三类地物的"平均光谱签名"（6 通道示意：可见-近红外-热）
        # 默认（generic / 月面类）签名；火星等场景可由调用方传入，使检测器与真实世界签名一致
        self._signatures = signatures or {
            "ore":      np.array([0.20, 0.25, 0.85, 0.90, 0.30, 0.15]),  # 金属/稀土特征峰
            "rock":     np.array([0.55, 0.50, 0.45, 0.40, 0.35, 0.30]),  # 硅酸盐平缓
            "regolith": np.array([0.70, 0.68, 0.66, 0.64, 0.62, 0.60]),  # 风化层平坦偏亮
        }

    # ---- 内部：前向 ----
    def _forward(self, x):
        z1 = self.W1 @ x + self.b1
        a1 = np.tanh(z1)
        z2 = self.W2 @ a1 + self.b2
        a2 = z2 - np.max(z2)
        p = np.exp(a2)
        p = p / np.sum(p)
        return a1, p

    # ---- 训练：在合成数据上做 SGD（与推理一致：先去噪再提特征）----
    def fit(self, epochs: int = 600, lr: float = 0.05, n_per_class: int = 150):
        # 构造训练集：每类按签名 + 高斯噪声采样，经去噪后提特征
        X, Y = [], []
        for ci, name in enumerate(self.CLASSES):
            base = self._signatures[name]
            for _ in range(n_per_class):
                spec = base + self.rng.normal(0, 0.07, size=base.shape)
                X.append(extract_features(denoise_spectrum(spec)))
                Y.append(ci)
        X = np.array(X)
        Y = np.array(Y)
        n_feat = X.shape[1]
        self.W1 = self.rng.standard_normal((self.hidden, n_feat)) * 0.5
        self.b1 = np.zeros(self.hidden)
        self.W2 = self.rng.standard_normal((len(self.CLASSES), self.hidden)) * 0.5
        self.b2 = np.zeros(len(self.CLASSES))

        for ep in range(epochs):
            perm = self.rng.permutation(len(X))
            for i in perm:
                x = X[i]
                a1, p = self._forward(x)
                # 交叉熵梯度
                y_onehot = np.zeros(len(self.CLASSES))
                y_onehot[Y[i]] = 1.0
                dz2 = p - y_onehot
                dW2 = np.outer(dz2, a1)
                db2 = dz2
                da1 = self.W2.T @ dz2
                dz1 = da1 * (1.0 - a1 ** 2)
                dW1 = np.outer(dz1, x)
                db1 = dz1
                self.W2 -= lr * dW2
                self.b2 -= lr * db2
                self.W1 -= lr * dW1
                self.b1 -= lr * db1

    # ---- 推理 ----
    def predict(self, spectrum: np.ndarray):
        """返回 (类名, 置信度 0~1)"""
        spec_dn = denoise_spectrum(np.asarray(spectrum, dtype=float))
        feat = extract_features(spec_dn)
        _, p = self._forward(feat)
        ci = int(np.argmax(p))
        return self.CLASSES[ci], float(p[ci])
