# 发射方案：马斯克 / SpaceX Rideshare 与小卫星通道 / Launch Plan: Musk / SpaceX Rideshare and Small-Satellite Channels

> 语言说明 / Language note：本文中英双语，先中文后英文。 / This document is bilingual: Chinese first, then English.

> 核心结论：个人"副业"阶段**不要自己发射**。先用仿真 + 地面原型变现，再去争**高校载荷名额 / 商业航天基金 / 客户预付款**，最后才专属发射。
>
> Core conclusion: at the personal "side-hustle" stage, **do not launch on your own**. First monetize the simulation + ground prototype, then compete for **university payload slots / commercial space funds / customer prepayments**, and only at the end do a dedicated launch.

---

## 1. 发射成本现实账（2026） / 1. Launch Cost Reality (2026)
| 项目 / Item | 数字 / Figure |
|---|---|
| 起步价 / Starting price | **$350,000**（含 50kg 到 SSO / including 50 kg to SSO） |
| 超出重量 / Extra mass | **$7,000 / kg** |
| 任务节奏 / Mission cadence | Transporter 约每 4 个月一班 / Transporter roughly every 4 months |
| 默认轨道 / Default orbit | SSO 525 km / 97.5°（太阳同步 / sun-synchronous） |
| 载荷板 / Payload plates | 1/4 板 50kg / 1/2 板 100kg / 整板 200kg / XL 300kg / 1/4 plate 50 kg / 1/2 plate 100 kg / full plate 200 kg / XL 300 kg |
| 聚合商 / Aggregators | Exolaunch、D-Orbit、NanoAvionics（负责集成与部署 / handle integration and deployment） |

→ 一个 50kg 级 CMR 最低约 **$35 万**；若做到 100kg 约 **$70 万**。远超个人副业预算。

→ A 50 kg-class CMR costs at least about **$350k**; at 100 kg, about **$700k**. Far beyond a personal side-hustle budget.

## 2. 重量与轨道选择 / 2. Mass and Orbit Choices
- **目标天体**：近地小行星（绕飞+表层勘探，难度低于采样返回）或月球南极（水冰/稀土）。
  **Target body**: a near-Earth asteroid (fly-around + surface exploration, easier than sample return) or the lunar south pole (water ice / rare earths).
- **轨道**：先用 SSO/LEO 做**技术验证载荷**（在轨自主导航+探测算法上天），再谈地月转移/小行星任务。
  **Orbit**: first fly a **technology-demonstration payload** in SSO/LEO (putting autonomous navigation + detection algorithms in orbit), then consider trans-lunar / asteroid missions.
- **重量**：按硬件指南把整机压到 **< 50kg**，适配 1/4 板，成本最低。
  **Mass**: following the hardware guide, bring the whole rover to **< 50 kg** to fit a 1/4 plate at the lowest cost.

## 3. 不自己花钱发射的三条路 / 3. Three Ways to Launch Without Paying Yourself
1. **高校 / 科研载荷竞赛**：如立方星（CubeSat）创新大赛、空间科学载荷征集——常附带免费/补贴发射名额。
   **University / research payload competitions**: e.g. CubeSat innovation contests and space-science payload calls — often with free or subsidized launch slots.
2. **商业航天基金与政府课题**：国内商业航天（星河动力、天兵、东方空间等）与"新空间"基金对有在轨验证价值的技术有资助。
   **Commercial space funds and government projects**: Chinese commercial space companies (Galactic Energy, Space Pioneer, Orienspace, etc.) and "NewSpace" funds support technologies with in-orbit validation value.
3. **客户预付款 / 数据订阅**：先卖"在轨自主勘探 AI"与"地外样品数据"订阅，用收入覆盖发射。
   **Customer prepayments / data subscriptions**: sell "in-orbit autonomous exploration AI" and "extraterrestrial sample data" subscriptions first, and cover the launch with the revenue.

## 4. 集成与合规 / 4. Integration and Compliance
- 通过 Exolaunch/D-Orbit 做部署器集成（机械/电气接口、fit check、预发射测试）。
  Use Exolaunch/D-Orbit for deployer integration (mechanical/electrical interfaces, fit check, pre-launch testing).
- 法规：遵守《外空条约》与各国出口/频率管制（ITAR/EAR 类需提前 3–6 月申报）。
  Regulation: comply with the Outer Space Treaty and national export/frequency controls (ITAR/EAR-type filings need 3–6 months' lead time).
- 通信：标配 S 波段数传 + 地面站 / 中继（如中继卫星）回传遥测与样品光谱数据。
  Communications: standard S-band data link + ground stations / relays (e.g. relay satellites) to downlink telemetry and sample spectral data.

## 5. 里程碑 / 5. Milestones
- T0：地面原型 + 仿真（现在，<2 万元） / T0: ground prototype + simulation (now, < 20,000 yuan)
- T+6–12 月：抗辐射化 + 参赛/筹资拿发射名额 / T+6–12 months: radiation hardening + competitions/fundraising for a launch slot
- T+18 月+：专属/搭载发射，在轨验证 / T+18 months+: dedicated/rideshare launch, in-orbit validation
