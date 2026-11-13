"""
starlink_comm.py — CMR 星链(Starlink)通讯仿真模块（纯标准库，无外部依赖）

扫地机器人改装后的 CMR 通过 Musk 的 Starlink 低轨(LEO)星座进行通讯：
  · 星座：n_sats 颗 LEO 卫星，错相位过顶形成可见"窗口"
  · 链路：窗口内 online，否则 offline（store-and-forward 队列缓存消息）
  · 指标：时延 latency_ms（直连 20~50ms；跨星中继 +20~40ms）、带宽 bandwidth_mbps
  · 出网：enqueue() 缓存消息，online 时 flush() 批量回传（对应 rover 的中继 RELAY）

说明：对地球/月球基地场景，Starlink 用户终端直连 LEO 是现实可行的；
对深空(火星)场景，本模块作为"星间/深空中继链路"的示意性模型（真实火星链路
需借助深空网络/中继卫星，时延以分钟计，此处仅作链路调度与队列演示）。

用法:
  from starlink_comm import Starlink
  sl = Starlink(seed=42, n_sats=8, pass_period=18, pass_duration=8)
  for step in range(600):
      sl.update(step)
      if sl.online:
          sent = sl.flush()   # 回传缓存的遥测/资产发布消息 / downlink buffered telemetry/asset messages

starlink_comm.py — CMR Starlink communications simulation (standard library only, no external deps)

The converted-vacuum CMR communicates through Musk's Starlink low-Earth-orbit (LEO) constellation:
  · Constellation: n_sats LEO satellites passing overhead out of phase, forming visible "windows"
  · Link: online inside a window, otherwise offline (a store-and-forward queue buffers messages)
  · Metrics: latency_ms (direct 20–50 ms; inter-satellite relay +20–40 ms), bandwidth_mbps
  · Downlink: enqueue() buffers messages, flush() sends them in bulk when online
    (maps to the rover's RELAY action)

Note: for the Earth / lunar-base scenario, a Starlink user terminal linking directly to LEO
is realistic; for deep space (Mars) this module is an illustrative "inter-satellite /
deep-space relay" model (a real Mars link needs the deep-space network / relay satellites,
with latency in minutes; here it only demonstrates link scheduling and queuing).

Usage: see the example above.
"""

import random


class Starlink:
    """Starlink 用户终端链路仿真。 / Starlink user-terminal link simulation."""

    def __init__(self, seed=42, n_sats=8, pass_period=18, pass_duration=8,
                 latency_base=30.0, latency_relay=35.0, bw_min=50.0, bw_max=150.0):
        self.rng = random.Random(seed)
        self.n_sats = n_sats
        self.pass_period = pass_period
        self.pass_duration = pass_duration
        # 每颗卫星错相位，制造多窗口、更平滑的覆盖 / Stagger satellite phases for multiple windows and smoother coverage
        self.phase = [self.rng.uniform(0, pass_period) for _ in range(n_sats)]
        self.latency_base = latency_base
        self.latency_relay = latency_relay
        self.bw_min, self.bw_max = bw_min, bw_max

        self.online = False
        self.latency_ms = 0.0
        self.bandwidth_mbps = 0.0
        self.outbox = []            # 待回传消息队列（离线时积攒） / outbound queue (accumulates while offline)
        self.sent_total = 0
        self.dropped_total = 0
        self.steps_online = 0
        self.steps_total = 0
        self.last_flush = []

    def update(self, step):
        """每仿真步刷新一次链路状态。 / Refresh the link state once per simulation step."""
        self.steps_total += 1
        # 任一卫星可见即视为 online（多星错相位 → 覆盖更连续）
        # Online if any satellite is visible (staggered phases → more continuous coverage)
        visible = any(((step + ph) % self.pass_period) < self.pass_duration
                      for ph in self.phase)
        self.online = visible
        if visible:
            self.steps_online += 1
            # 部分窗口无直连地面站，需星间链路中继 → 时延更高
            # Some windows have no direct ground station and need inter-satellite relay → higher latency
            relay = self.rng.random() < 0.30
            self.latency_ms = self.latency_base + (self.latency_relay if relay else 0.0) \
                              + self.rng.uniform(-5.0, 5.0)
            self.latency_ms = max(15.0, self.latency_ms)
            self.bandwidth_mbps = self.rng.uniform(self.bw_min, self.bw_max)
        else:
            self.latency_ms = 0.0
            self.bandwidth_mbps = 0.0

    def enqueue(self, msg):
        """缓存一条待回传消息（离线时积攒，online 时 flush）。
        Buffer one outbound message (accumulated offline, flushed when online)."""
        self.outbox.append(msg)

    def flush(self, max_msgs=None):
        """online 时批量回传，返回本次发送的消息列表。
        max_msgs 可模拟单步带宽约束（限制每步回传条数）。
        When online, send in bulk and return the messages sent this time.
        max_msgs can model a per-step bandwidth limit (caps messages per step)."""
        if not self.online:
            return []
        if max_msgs is None:
            sent = self.outbox
            self.outbox = []
        else:
            sent = self.outbox[:max_msgs]
            self.outbox = self.outbox[max_msgs:]
        self.sent_total += len(sent)
        self.last_flush = list(sent)
        return sent

    def coverage_ratio(self):
        """在线步数占比。 / Share of steps online."""
        return (self.steps_online / self.steps_total) if self.steps_total else 0.0

    def status(self):
        """链路状态字典。 / Link status dict."""
        return {
            "online": self.online,
            "latency_ms": round(self.latency_ms, 1),
            "bandwidth_mbps": round(self.bandwidth_mbps, 1),
            "queued": len(self.outbox),
            "sent_total": self.sent_total,
            "coverage": round(self.coverage_ratio(), 3),
        }


if __name__ == "__main__":
    sl = Starlink(seed=42, n_sats=8, pass_period=18, pass_duration=8)
    for s in range(60):
        sl.update(s)
        if sl.online:
            sl.flush()
    print("链路状态示例 / Link status example:", sl.status())
    print("覆盖率 / Coverage:", round(sl.coverage_ratio(), 3))
