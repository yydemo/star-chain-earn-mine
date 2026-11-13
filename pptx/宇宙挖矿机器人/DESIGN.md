> 语言 / Language：本文档为中英双语，中文在前、英文在后。 / This document is bilingual: Chinese first, then English.

# DESIGN.md — 宇宙挖矿机器人 CMR 演示 PPT（科技深空风） / Cosmic Mining Robot (CMR) Presentation Deck (Deep-Space Tech Style)

## 1. 画布与全局母版（默认 1280×720） / 1. Canvas and Global Master (default 1280×720)

| 母版区 / Master region | 位置 / Position | 高度 / Height | 内容 / Content |
|---|---|---|---|
| A 标题块 / A Title block | 0–120px | 120px | 主标题 34–40px bold，左侧 8px 蓝色竖条<br>Main title 34–40px bold, 8px blue vertical bar on the left |
| B 内容区 / B Content area | 120–660px | 540px | 正文/图/卡片<br>Body text / images / cards |
| C 页脚条 / C Footer bar | 660–720px | 60px | 左「CMR · 宇宙挖矿机器人」灰字 + 右页码 `NN / 16`<br>Left: grey text "CMR · 宇宙挖矿机器人" (Cosmic Mining Robot) + right: page number `NN / 16` |
| padding | 上下 20、左右 64px<br>20px top/bottom, 64px left/right | — | 封面/章节/结束页可自定义<br>Cover / section / ending slides may customize |

## 2. 颜色系统（≤4 hex + 中性） / 2. Color System (≤4 hex + neutrals)

| 角色 / Role | hex | 用途 / Usage |
|---|---|---|
| 背景主色 / Primary background | `#0B1120` | 深空底色（封面/章节/结束页满铺）<br>Deep-space base color (full-bleed on cover / section / ending slides) |
| 背景次色 / Secondary background | `#0F1B33` | 卡片底、内容页浅区块<br>Card backgrounds, lighter blocks on content slides |
| 主色 / Primary | `#3B82F6` | 标题条、主线条、链接<br>Title bars, main lines, links |
| 辅色 / Secondary | `#22D3EE` | 青蓝高亮、图表第二色、电路节点<br>Cyan highlights, second chart color, circuit nodes |
| 强调色 / Accent | `#F59E0B` | 关键数据/金句（≤10%，Hero 可 15%）<br>Key data / key quotes (≤10%, up to 15% on Hero slides) |
| 文本主色 / Primary text | `#E5EDF7` | 浅色底上的正文白<br>White body text (on light-colored backgrounds, as in the original) |
| 文本次色 / Secondary text | `#94A3B8` | 注释、页脚灰<br>Notes, footer grey |

- 内容页（4/5/7/8/9/10/12/13/15）背景用 `#0B1120` 深空底 + 浅色文字，保持航天沉浸感；目录/结束可同色系。
  Content slides (4/5/7/8/9/10/12/13/15) use the `#0B1120` deep-space background + light text to keep the space-immersion feel; contents / ending slides may use the same palette.
- 渐变：`linear-gradient(135deg, #3B82F6 0%, #22D3EE 100%)` 用于标题条/卡片头。
  Gradient: `linear-gradient(135deg, #3B82F6 0%, #22D3EE 100%)` for title bars / card headers.
- 半透明：`rgba(59,130,246,0.10)` 卡片描边光晕。
  Translucency: `rgba(59,130,246,0.10)` for card outline glow.

## 3. 字体系统 / 3. Typography

| 层级 / Level | 字号 / Size | 字重 / Weight | 字体 / Font |
|---|---|---|---|
| 封面主标题 / Cover main title | 64–72 | bold | 微软雅黑 / Microsoft YaHei |
| 章节大字 / Section large text | 56–64 | bold | 微软雅黑 / Microsoft YaHei |
| 巨型数据锚点 / Giant data anchor | 72–110 | bold | JetBrains Mono / Consolas（与正文不同字体 / a different font from body text） |
| 页面主标题 / Slide main title | 34–38 | bold | 微软雅黑 / Microsoft YaHei |
| 卡片小标题 / Card subtitle | 24–26 | 600 | 微软雅黑 / Microsoft YaHei |
| 正文 / Body | 20–22 | regular | 微软雅黑 / Microsoft YaHei |
| 脚注/页码 / Footnote / page number | 14 | regular | 微软雅黑 / Microsoft YaHei |

## 4. 动画策略（统一 fadeIn） / 4. Animation Strategy (uniform fadeIn)

- 全篇统一 `animType="fadeIn"`，连续自动播写 `startType="afterPrevious"`，`duration=600`，`delay≤300`。
  Use `animType="fadeIn"` throughout; for continuous auto-play use `startType="afterPrevious"`, `duration=600`, `delay≤300`.
- 应用页面：封面(1)、章节扉页(3/6/11/14) 标题与背景先后浮现；关键数据页(4/12/15) 数字与卡片依次入场。
  Applied to: cover (1) and section title slides (3/6/11/14), where the title and background fade in one after the other; key data slides (4/12/15), where numbers and cards enter in sequence.
- 单页动画 ≤ 4，装饰/页脚/页码不加动画。
  ≤ 4 animations per slide; no animation on decorations / footers / page numbers.

## 5. 配图清单（全部 SVG，结构化/低语义，允许） / 5. Image List (all SVG, structural / low-semantic, allowed)

| 文件 / File | 类型 / Type | 真实内容 / Actual content | 使用页 / Used on | 已核对 / Checked |
|---|---|---|---|---|
| assets/system_architecture.svg | 架构图 / Architecture diagram | 5 层系统总体架构（底座→机身→算力→通讯→软件）<br>5-layer overall system architecture (base → body → compute → communication → software) | 01/03/04 | 生成后 Read / Read after generation |
| assets/robo_base.svg | 结构爆炸图 / Exploded structure view | 扫地机器人底座：底盘/轮/激光雷达/主板/电池/导航栈<br>Robot vacuum base: chassis / wheels / LiDAR / mainboard / battery / navigation stack | 07 | 生成后 Read / Read after generation |
| assets/cmr_structure.svg | 结构图 / Structure diagram | 改装后：316L外壳/钻采头/样品仓/太阳能阵/抗辐射主板/星链天线<br>After conversion: 316L shell / drill head / sample bay / solar array / radiation-hardened mainboard / Starlink antenna | 08 | 生成后 Read / Read after generation |
| assets/compile_pipeline.svg | 数据流图 / Data-flow diagram | 西电广州GaN设计→交叉编译→中试→南沙量产→辐照试验→上链<br>Xidian Guangzhou GaN design → cross-compilation → pilot production → Nansha mass production → irradiation testing → on-chain | 10 | 生成后 Read / Read after generation |
| assets/starlink_coverage.svg | 关系网络/示意 / Relationship network / schematic | 地球+LEO星链星座+覆盖带+CMR终端链路<br>Earth + LEO Starlink constellation + coverage bands + CMR terminal links | 03/11/12 | 生成后 Read / Read after generation |

## 6. 页面映射表 / 6. Slide Mapping Table

| # | 文件 / File | 类型 / Type | 角色 / Role | 版式 / Layout | L1 | 留白% / Whitespace % | 色彩分配 / Color allocation |
|---|---|---|---|---|---|---|---|
| 01 | 01_cover.slide | cover | hero | 全屏+骑线文字 / Full-screen + overlapping text | system_architecture.svg | 35% | 主色60%+辅色30% / Primary 60% + secondary 30% |
| 02 | 02_catalog.slide | catalog | supporting | 左标题+右内容 / Title left + content right | — | 25% | 主色40%+辅色25% / Primary 40% + secondary 25% |
| 03 | 03_section1.slide | section | transition | 全屏+大标题 / Full-screen + large title | starlink_coverage.svg | 45% | 主色60% / Primary 60% |
| 04 | 04_architecture.slide | content | hero | 左大图+右文字 / Large image left + text right | system_architecture.svg | 25% | 强调色15%爆发 / Accent 15% burst |
| 05 | 05_why.slide | content | supporting | 非对称双栏 / Asymmetric two columns | — | 25% | 主色50%+辅色20% / Primary 50% + secondary 20% |
| 06 | 06_section2.slide | section | transition | 全屏+大标题 / Full-screen + large title | robo_base.svg | 45% | 主色60% / Primary 60% |
| 07 | 07_robo_base.slide | content | hero | 左大图+右文字 / Large image left + text right | robo_base.svg | 25% | 强调色12% / Accent 12% |
| 08 | 08_cmr_structure.slide | content | hero | 上大图+下卡片 / Large image top + cards below | cmr_structure.svg | 30% | 主色55%+辅色25% / Primary 55% + secondary 25% |
| 09 | 09_xidian_chip.slide | content | supporting | 左标题+右内容 / Title left + content right | — | 25% | 主色45%+辅色20% / Primary 45% + secondary 20% |
| 10 | 10_compile.slide | content | hero | 左大图+右文字 / Large image left + text right | compile_pipeline.svg | 25% | 强调色12% / Accent 12% |
| 11 | 11_section3.slide | section | transition | 全屏+大标题 / Full-screen + large title | starlink_coverage.svg | 45% | 主色60% / Primary 60% |
| 12 | 12_starlink.slide | content | hero | 左大图+右指标 / Large image left + metrics right | starlink_coverage.svg | 22% | 强调色15%爆发 / Accent 15% burst |
| 13 | 13_dustchain.slide | content | supporting | 非对称双栏 / Asymmetric two columns | — | 25% | 主色50%+辅色20% / Primary 50% + secondary 20% |
| 14 | 14_section4.slide | section | transition | 全屏+大标题 / Full-screen + large title | system_architecture.svg | 45% | 主色60% / Primary 60% |
| 15 | 15_results.slide | content | supporting | 图表+洞察 / Chart + insights | Chart 柱状 / Bar chart | 28% | 主色45%+辅色25% / Primary 45% + secondary 25% |
| 16 | 16_ending.slide | ending | hero | 居中金句 / Centered key quote | — | 40% | 强调色15% / Accent 15% |
