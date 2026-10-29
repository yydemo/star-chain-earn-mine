# DESIGN.md — 宇宙挖矿机器人 CMR 演示 PPT（科技深空风）

## 1. 画布与全局母版（默认 1280×720）

| 母版区 | 位置 | 高度 | 内容 |
|---|---|---|---|
| A 标题块 | 0–120px | 120px | 主标题 34–40px bold，左侧 8px 蓝色竖条 |
| B 内容区 | 120–660px | 540px | 正文/图/卡片 |
| C 页脚条 | 660–720px | 60px | 左「CMR · 宇宙挖矿机器人」灰字 + 右页码 `NN / 16` |
| padding | 上下 20、左右 64px | — | 封面/章节/结束页可自定义 |

## 2. 颜色系统（≤4 hex + 中性）

| 角色 | hex | 用途 |
|---|---|---|
| 背景主色 | `#0B1120` | 深空底色（封面/章节/结束页满铺） |
| 背景次色 | `#0F1B33` | 卡片底、内容页浅区块 |
| 主色 | `#3B82F6` | 标题条、主线条、链接 |
| 辅色 | `#22D3EE` | 青蓝高亮、图表第二色、电路节点 |
| 强调色 | `#F59E0B` | 关键数据/金句（≤10%，Hero 可 15%） |
| 文本主色 | `#E5EDF7` | 浅色底上的正文白 |
| 文本次色 | `#94A3B8` | 注释、页脚灰 |

- 内容页（4/5/7/8/9/10/12/13/15）背景用 `#0B1120` 深空底 + 浅色文字，保持航天沉浸感；目录/结束可同色系。
- 渐变：`linear-gradient(135deg, #3B82F6 0%, #22D3EE 100%)` 用于标题条/卡片头。
- 半透明：`rgba(59,130,246,0.10)` 卡片描边光晕。

## 3. 字体系统

| 层级 | 字号 | 字重 | 字体 |
|---|---|---|---|
| 封面主标题 | 64–72 | bold | 微软雅黑 / Microsoft YaHei |
| 章节大字 | 56–64 | bold | 微软雅黑 |
| 巨型数据锚点 | 72–110 | bold | JetBrains Mono / Consolas（与正文不同字体） |
| 页面主标题 | 34–38 | bold | 微软雅黑 |
| 卡片小标题 | 24–26 | 600 | 微软雅黑 |
| 正文 | 20–22 | regular | 微软雅黑 |
| 脚注/页码 | 14 | regular | 微软雅黑 |

## 4. 动画策略（统一 fadeIn）

- 全篇统一 `animType="fadeIn"`，连续自动播写 `startType="afterPrevious"`，`duration=600`，`delay≤300`。
- 应用页面：封面(1)、章节扉页(3/6/11/14) 标题与背景先后浮现；关键数据页(4/12/15) 数字与卡片依次入场。
- 单页动画 ≤ 4，装饰/页脚/页码不加动画。

## 5. 配图清单（全部 SVG，结构化/低语义，允许）

| 文件 | 类型 | 真实内容 | 使用页 | 已核对 |
|---|---|---|---|---|
| assets/system_architecture.svg | 架构图 | 5 层系统总体架构（底座→机身→算力→通讯→软件） | 01/03/04 | 生成后 Read |
| assets/robo_base.svg | 结构爆炸图 | 扫地机器人底座：底盘/轮/激光雷达/主板/电池/导航栈 | 07 | 生成后 Read |
| assets/cmr_structure.svg | 结构图 | 改装后：316L外壳/钻采头/样品仓/太阳能阵/抗辐射主板/星链天线 | 08 | 生成后 Read |
| assets/compile_pipeline.svg | 数据流图 | 西电广州GaN设计→交叉编译→中试→南沙量产→辐照试验→上链 | 10 | 生成后 Read |
| assets/starlink_coverage.svg | 关系网络/示意 | 地球+LEO星链星座+覆盖带+CMR终端链路 | 03/11/12 | 生成后 Read |

## 6. 页面映射表

| # | 文件 | 类型 | 角色 | 版式 | L1 | 留白% | 色彩分配 |
|---|---|---|---|---|---|---|---|
| 01 | 01_cover.slide | cover | hero | 全屏+骑线文字 | system_architecture.svg | 35% | 主色60%+辅色30% |
| 02 | 02_catalog.slide | catalog | supporting | 左标题+右内容 | — | 25% | 主色40%+辅色25% |
| 03 | 03_section1.slide | section | transition | 全屏+大标题 | starlink_coverage.svg | 45% | 主色60% |
| 04 | 04_architecture.slide | content | hero | 左大图+右文字 | system_architecture.svg | 25% | 强调色15%爆发 |
| 05 | 05_why.slide | content | supporting | 非对称双栏 | — | 25% | 主色50%+辅色20% |
| 06 | 06_section2.slide | section | transition | 全屏+大标题 | robo_base.svg | 45% | 主色60% |
| 07 | 07_robo_base.slide | content | hero | 左大图+右文字 | robo_base.svg | 25% | 强调色12% |
| 08 | 08_cmr_structure.slide | content | hero | 上大图+下卡片 | cmr_structure.svg | 30% | 主色55%+辅色25% |
| 09 | 09_xidian_chip.slide | content | supporting | 左标题+右内容 | — | 25% | 主色45%+辅色20% |
| 10 | 10_compile.slide | content | hero | 左大图+右文字 | compile_pipeline.svg | 25% | 强调色12% |
| 11 | 11_section3.slide | section | transition | 全屏+大标题 | starlink_coverage.svg | 45% | 主色60% |
| 12 | 12_starlink.slide | content | hero | 左大图+右指标 | starlink_coverage.svg | 22% | 强调色15%爆发 |
| 13 | 13_dustchain.slide | content | supporting | 非对称双栏 | — | 25% | 主色50%+辅色20% |
| 14 | 14_section4.slide | section | transition | 全屏+大标题 | system_architecture.svg | 45% | 主色60% |
| 15 | 15_results.slide | content | supporting | 图表+洞察 | Chart 柱状 | 28% | 主色45%+辅色25% |
| 16 | 16_ending.slide | ending | hero | 居中金句 | — | 40% | 强调色15% |
