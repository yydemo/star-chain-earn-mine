> 语言 / Language：本文档为中英双语，中文在前、英文在后。 / This document is bilingual: Chinese first, then English.

# STORY.md — 宇宙挖矿机器人 CMR 演示 PPT / Cosmic Mining Robot (CMR) Presentation Deck

## ① 用户意图对齐 / ① Aligning on User Intent

- **目标受众**：技术评审 / 项目路演 / 开源发布受众（航天爱好者、半导体产业、机器人开发者）。
  **Target audience**: technical reviewers / project roadshows / open-source release audiences (space enthusiasts, the semiconductor industry, robot developers).
- **核心目标**：让观众记住「把家用扫地机器人改装为宇宙挖矿机器人」的完整技术闭环——不锈钢机身 + 西电/广州第三代半导体抗辐射算力 + 火星车仿真 + 星链通讯 + 区块链售卖。
  **Core goal**: make the audience remember the complete technical loop of "converting a household robot vacuum into a cosmic mining robot" — stainless-steel body + Xidian/Guangzhou third-generation-semiconductor radiation-hardened compute + Mars rover simulation + Starlink communication + blockchain sales.
- **PPT 长度**：16 页（4 章节），Hero 页占比约 25%。
  **Deck length**: 16 slides (4 chapters), with Hero slides making up about 25%.
- **视觉调性**：科技未来 / 航天深空 / 工程蓝图——深空蓝底、电路青蓝线条、等宽字体数字。
  **Visual tone**: futuristic tech / deep space / engineering blueprint — deep-space blue background, cyan circuit lines, monospaced numerals.
- **内容边界**：必讲=机器结构、整体结构、西电三代半编程编译、星链覆盖、仿真结果；不讲=发射财务细节深挖、单一芯片物理原理公式。
  **Content scope**: must cover = machine structure, overall structure, Xidian third-gen-semiconductor programming & compilation, Starlink coverage, simulation results; out of scope = deep dives into launch financial details, physics formulas of any single chip.

## ② 页面布局骨架 / ② Slide Layout Skeleton

- **总页数 16，4 章节**：
  **16 slides in total, 4 chapters**:
  - 第 01 章 项目总览 → 第 3 页 section 扉页 / Chapter 01 Project Overview → section title slide on slide 3
  - 第 02 章 机器结构与抗辐射芯片 → 第 6 页 section 扉页 / Chapter 02 Machine Structure & Radiation-Hardened Chips → section title slide on slide 6
  - 第 03 章 通讯与数据闭环 → 第 11 页 section 扉页 / Chapter 03 Communication & Data Loop → section title slide on slide 11
  - 第 04 章 仿真验证与展望 → 第 14 页 section 扉页 / Chapter 04 Simulation Validation & Outlook → section title slide on slide 14
- **Hero 页**：封面(1)、整体架构(4)、星链覆盖(12)、结束页(16)——共 4 页 ≈ 25%，互不相邻。
  **Hero slides**: cover (1), overall architecture (4), Starlink coverage (12), ending (16) — 4 slides ≈ 25%, none adjacent.
- **rhythm**：peak=4,12,16；transition=3,6,11,14；其余 valley。无连续 ≥3 valley。
  **Rhythm**: peak = 4, 12, 16; transition = 3, 6, 11, 14; all others valley. No run of ≥3 consecutive valleys.
- **非对称版式**：4,5,7,8,10,12,13 等采用左大图+右文字 / 非对称双栏，占比 ≥ 40%。
  **Asymmetric layouts**: slides 4, 5, 7, 8, 10, 12, 13 etc. use large-image-left + text-right / asymmetric two-column layouts, ≥ 40% of slides.
- **对称版式**：仅目录(2)、仿真数据(15) 可用，≤2 页。
  **Symmetric layouts**: only the contents slide (2) and simulation data slide (15) may use them, ≤ 2 slides.

## ③ 页面大纲 / ③ Slide Outline

| # | title 标题 | type 类型 | role 角色 | rhythm 节奏 | layout 版式 | visual 视觉 | visual_role 视觉作用 | density 密度 | anti_pattern 禁忌 |
|---|---|---|---|---|---|---|---|---|---|
| 01 | 从扫地机器人到宇宙挖矿机器人<br>From Robot Vacuum to Cosmic Mining Robot | cover | hero | peak | 全屏视觉+骑线文字<br>Full-screen visual + overlapping text | L1: system_architecture.svg 背景化<br>L1: system_architecture.svg as background | atmosphere | 30字/1图/35%<br>30 chars / 1 image / 35% | 禁止装饰小图、禁止等分双栏<br>No small decorative images, no equal two-column split |
| 02 | 目录<br>Contents | catalog | supporting | valley | 左标题+右内容<br>Title left + content right | L3 角标<br>L3 corner mark | — | 120字/0图/25%<br>120 chars / 0 images / 25% | 禁止 N 卡片横排<br>No horizontal row of N cards |
| 03 | 第01章 项目总览<br>Chapter 01 Project Overview | section | transition | transition | 全屏视觉+大标题<br>Full-screen visual + large title | L1 背景<br>L1 background | atmosphere | 30字/1图/45%<br>30 chars / 1 image / 45% | 禁止四卡片预览<br>No four-card preview |
| 04 | 整体系统架构<br>Overall System Architecture | content | hero | peak | 左大图(架构SVG)+右文字<br>Large image left (architecture SVG) + text right | L1: system_architecture.svg | anchor | 220字/1图/25%<br>220 chars / 1 image / 25% | 禁止等宽卡片横排<br>No row of equal-width cards |
| 05 | 改装逻辑：为什么是扫地机器人<br>Conversion Logic: Why a Robot Vacuum | content | supporting | valley | 非对称双栏 60:40<br>Asymmetric two columns 60:40 | L2 流程<br>L2 flow | evidence | 200字/0图/25%<br>200 chars / 0 images / 25% | 禁止 50:50 等分<br>No 50:50 split |
| 06 | 第02章 机器结构与抗辐射芯片<br>Chapter 02 Machine Structure & Radiation-Hardened Chips | section | transition | transition | 全屏视觉+大标题<br>Full-screen visual + large title | L1 背景<br>L1 background | atmosphere | 30字/1图/45%<br>30 chars / 1 image / 45% | 禁止铺满正文<br>No body text filling the slide |
| 07 | 扫地机器人底座结构<br>Robot Vacuum Base Structure | content | hero | peak | 左大图(爆炸图SVG)+右文字<br>Large image left (exploded-view SVG) + text right | L1: robo_base.svg | anchor | 210字/1图/25%<br>210 chars / 1 image / 25% | 禁止把图缩成200×70<br>Do not shrink the image to 200×70 |
| 08 | 整体改装结构<br>Overall Conversion Structure | content | hero | peak | 上大图(改装SVG)+下卡片<br>Large image top (conversion SVG) + cards below | L1: cmr_structure.svg | anchor | 200字/1图/30%<br>200 chars / 1 image / 30% | 禁止等分双栏<br>No equal two-column split |
| 09 | 西电第三代半导体芯片<br>Xidian Third-Generation Semiconductor Chips | content | supporting | valley | 左标题+右内容<br>Title left + content right | L2 芯片卡<br>L2 chip cards | evidence | 240字/0图/25%<br>240 chars / 0 images / 25% | 禁止 N 卡片横排<br>No horizontal row of N cards |
| 10 | CMR 编程-编译工具链<br>CMR Programming-Compilation Toolchain | content | hero | peak | 左大图(数据流SVG)+右文字<br>Large image left (data-flow SVG) + text right | L1: compile_pipeline.svg | anchor | 220字/1图/25%<br>220 chars / 1 image / 25% | 禁止等宽卡片<br>No equal-width cards |
| 11 | 第03章 通讯与数据闭环<br>Chapter 03 Communication & Data Loop | section | transition | transition | 全屏视觉+大标题<br>Full-screen visual + large title | L1 背景<br>L1 background | atmosphere | 30字/1图/45%<br>30 chars / 1 image / 45% | 禁止四卡片<br>No four cards |
| 12 | 近地轨道 Starlink 覆盖<br>Low-Earth-Orbit Starlink Coverage | content | hero | peak | 左大图(星链SVG)+右指标<br>Large image left (Starlink SVG) + metrics right | L1: starlink_coverage.svg | anchor | 180字/1图/22%<br>180 chars / 1 image / 22% | 禁止把图缩小<br>Do not shrink the image |
| 13 | 集尘盒识别→区块链售卖<br>Dust-Box Recognition → Blockchain Sales | content | supporting | valley | 非对称双栏 60:40<br>Asymmetric two columns 60:40 | L2 流程<br>L2 flow | evidence | 220字/1图/25%<br>220 chars / 1 image / 25% | 禁止 50:50 等分<br>No 50:50 split |
| 14 | 第04章 仿真验证与展望<br>Chapter 04 Simulation Validation & Outlook | section | transition | transition | 全屏视觉+大标题<br>Full-screen visual + large title | L1 背景<br>L1 background | atmosphere | 30字/1图/45%<br>30 chars / 1 image / 45% | 禁止铺满正文<br>No body text filling the slide |
| 15 | 三场景仿真演示结果<br>Three-Scenario Simulation Results | content | supporting | valley | 图表+洞察<br>Chart + insights | Chart 柱状<br>Bar chart | evidence | 160字/1图/28%<br>160 chars / 1 image / 28% | 禁止等宽卡片<br>No equal-width cards |
| 16 | 总结与 GitHub 发布<br>Summary & GitHub Release | ending | hero | peak | 居中金句+落款<br>Centered key quote + sign-off | L3 角标<br>L3 corner mark | — | 60字/0图/40%<br>60 chars / 0 images / 40% | 禁止装饰小图<br>No small decorative images |

> 数据落点：每一含关键数据页（4/12/15）均写成「数据 + 判断」两段式。
>
> Data placement: every slide with key data (4/12/15) is written in a two-part "data + judgment" form.
