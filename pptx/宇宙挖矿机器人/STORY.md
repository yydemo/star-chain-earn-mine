# STORY.md — 宇宙挖矿机器人 CMR 演示 PPT

## ① 用户意图对齐

- **目标受众**：技术评审 / 项目路演 / 开源发布受众（航天爱好者、半导体产业、机器人开发者）。
- **核心目标**：让观众记住「把家用扫地机器人改装为宇宙挖矿机器人」的完整技术闭环——不锈钢机身 + 西电/广州第三代半导体抗辐射算力 + 火星车仿真 + 星链通讯 + 区块链售卖。
- **PPT 长度**：16 页（4 章节），Hero 页占比约 25%。
- **视觉调性**：科技未来 / 航天深空 / 工程蓝图——深空蓝底、电路青蓝线条、等宽字体数字。
- **内容边界**：必讲=机器结构、整体结构、西电三代半编程编译、星链覆盖、仿真结果；不讲=发射财务细节深挖、单一芯片物理原理公式。

## ② 页面布局骨架

- **总页数 16，4 章节**：
  - 第 01 章 项目总览 → 第 3 页 section 扉页
  - 第 02 章 机器结构与抗辐射芯片 → 第 6 页 section 扉页
  - 第 03 章 通讯与数据闭环 → 第 11 页 section 扉页
  - 第 04 章 仿真验证与展望 → 第 14 页 section 扉页
- **Hero 页**：封面(1)、整体架构(4)、星链覆盖(12)、结束页(16)——共 4 页 ≈ 25%，互不相邻。
- **rhythm**：peak=4,12,16；transition=3,6,11,14；其余 valley。无连续 ≥3 valley。
- **非对称版式**：4,5,7,8,10,12,13 等采用左大图+右文字 / 非对称双栏，占比 ≥ 40%。
- **对称版式**：仅目录(2)、仿真数据(15) 可用，≤2 页。

## ③ 页面大纲

| # | title | type | role | rhythm | layout | visual | visual_role | density | anti_pattern |
|---|---|---|---|---|---|---|---|---|---|
| 01 | 从扫地机器人到宇宙挖矿机器人 | cover | hero | peak | 全屏视觉+骑线文字 | L1: system_architecture.svg 背景化 | atmosphere | 30字/1图/35% | 禁止装饰小图、禁止等分双栏 |
| 02 | 目录 | catalog | supporting | valley | 左标题+右内容 | L3 角标 | — | 120字/0图/25% | 禁止 N 卡片横排 |
| 03 | 第01章 项目总览 | section | transition | transition | 全屏视觉+大标题 | L1 背景 | atmosphere | 30字/1图/45% | 禁止四卡片预览 |
| 04 | 整体系统架构 | content | hero | peak | 左大图(架构SVG)+右文字 | L1: system_architecture.svg | anchor | 220字/1图/25% | 禁止等宽卡片横排 |
| 05 | 改装逻辑：为什么是扫地机器人 | content | supporting | valley | 非对称双栏 60:40 | L2 流程 | evidence | 200字/0图/25% | 禁止 50:50 等分 |
| 06 | 第02章 机器结构与抗辐射芯片 | section | transition | transition | 全屏视觉+大标题 | L1 背景 | atmosphere | 30字/1图/45% | 禁止铺满正文 |
| 07 | 扫地机器人底座结构 | content | hero | peak | 左大图(爆炸图SVG)+右文字 | L1: robo_base.svg | anchor | 210字/1图/25% | 禁止把图缩成200×70 |
| 08 | 整体改装结构 | content | hero | peak | 上大图(改装SVG)+下卡片 | L1: cmr_structure.svg | anchor | 200字/1图/30% | 禁止等分双栏 |
| 09 | 西电第三代半导体芯片 | content | supporting | valley | 左标题+右内容 | L2 芯片卡 | evidence | 240字/0图/25% | 禁止 N 卡片横排 |
| 10 | CMR 编程-编译工具链 | content | hero | peak | 左大图(数据流SVG)+右文字 | L1: compile_pipeline.svg | anchor | 220字/1图/25% | 禁止等宽卡片 |
| 11 | 第03章 通讯与数据闭环 | section | transition | transition | 全屏视觉+大标题 | L1 背景 | atmosphere | 30字/1图/45% | 禁止四卡片 |
| 12 | 近地轨道 Starlink 覆盖 | content | hero | peak | 左大图(星链SVG)+右指标 | L1: starlink_coverage.svg | anchor | 180字/1图/22% | 禁止把图缩小 |
| 13 | 集尘盒识别→区块链售卖 | content | supporting | valley | 非对称双栏 60:40 | L2 流程 | evidence | 220字/1图/25% | 禁止 50:50 等分 |
| 14 | 第04章 仿真验证与展望 | section | transition | transition | 全屏视觉+大标题 | L1 背景 | atmosphere | 30字/1图/45% | 禁止铺满正文 |
| 15 | 三场景仿真演示结果 | content | supporting | valley | 图表+洞察 | Chart 柱状 | evidence | 160字/1图/28% | 禁止等宽卡片 |
| 16 | 总结与 GitHub 发布 | ending | hero | peak | 居中金句+落款 | L3 角标 | — | 60字/0图/40% | 禁止装饰小图 |

> 数据落点：每一含关键数据页（4/12/15）均写成「数据 + 判断」两段式。
