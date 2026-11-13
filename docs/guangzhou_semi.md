# 广州第三代半导体：CMR 抗辐射算力的"编程—编译—制造"环节 / Guangzhou Third-Generation Semiconductors: The "Programming — Compilation — Manufacturing" Stages of CMR's Rad-Hard Compute

> 语言说明 / Language note：本文中英双语，先中文后英文。 / This document is bilingual: Chinese first, then English.

> 本文把"宇宙挖矿机器人（CMR）"的抗辐射算力板，落到**广州（黄埔 + 南沙）的第三代半导体产业链**上：
> 设计/编译在西电广州第三代半导体创新中心（GaN，抗辐射/耐高温），量产制造走南沙万顷沙"国内首个第三代半导体全产业链"。
> 它与 `docs/hardware_mod.md` 里的"西电抗辐射 SiC 功率器件"是**同一母体**——西电广州研究院就是西安电子科技大学的广州分支，郝跃院士团队同时覆盖 SiC（功率）与 GaN（抗辐射 SoC 基底）。
>
> This document maps the "Cosmic Mining Robot (CMR)" rad-hard compute board onto **Guangzhou's (Huangpu + Nansha) third-generation semiconductor industry chain**:
> design/compilation at the Xidian Guangzhou Third-Generation Semiconductor Innovation Center (GaN, radiation-resistant / high-temperature), and volume manufacturing through Wanqingsha, Nansha — "China's first complete third-generation semiconductor industry chain".
> It shares **the same parent** as the "Xidian rad-hard SiC power devices" in `docs/hardware_mod.md`: the Xidian Guangzhou Institute is Xidian University's Guangzhou branch, and Academician Hao Yue's team covers both SiC (power) and GaN (rad-hard SoC base).

---

## 0. 一句话结论（已联网核实，2026-10-29） / 0. Bottom Line (Verified Online, 2026-10-29)

- **西电广州第三代半导体创新中心**（黄埔·中新知识城）= 西电与广州开发区共建的**宽禁带半导体国家工程研究中心广州分中心**，郝跃院士领衔，**6–8 英寸 GaN 晶圆生长 + 工艺 + 封测全流程中试线已通线**，且官方明确 GaN 具备**抗辐射、耐高温、耐高压、大功率**特性——正是 CMR 抗辐射计算基底的最佳落脚点。
  The **Xidian Guangzhou Third-Generation Semiconductor Innovation Center** (Huangpu, Sino-Singapore Guangzhou Knowledge City) = the **Guangzhou branch of the National Engineering Research Center for Wide-Bandgap Semiconductors**, co-built by Xidian and Guangzhou Development District and led by Academician Hao Yue. Its **6–8-inch GaN full-process pilot line (wafer growth + processing + packaging/testing) is in operation**, and it officially states that GaN is **radiation-resistant, high-temperature, high-voltage and high-power** — the ideal home for CMR's rad-hard compute base.
- **南沙万顷沙集成电路产业园** = **国内首个第三代半导体全产业链布局区域**（设计→材料→制造→封测），龙头**南砂晶圆（12 英寸 SiC 衬底）、芯粤能（车规级 SiC 主驱芯片，已量产/全球独角兽）、芯聚能（SiC 功率模块规模化上车）**串珠成链。这是 CMR 从"样片"到"批量抗辐射板"的量产通道。
  The **Wanqingsha Integrated Circuit Industrial Park in Nansha** = **China's first region laid out with a complete third-generation semiconductor chain** (design → materials → manufacturing → packaging/testing), with leaders **Nansha Wafer (12-inch SiC substrates), Xinyueneng (automotive-grade SiC traction chips, in mass production, a global unicorn) and Xinjuneng (SiC power modules installed in vehicles at scale)** linked into one chain. This is CMR's volume path from "samples" to "batches of rad-hard boards".
- 因此 CMR 的"编程/编译"环节应定义为：**在西电广州创新中心的 GaN 平台上做抗辐射 SoC/功率器件的电路设计与 FPGA/固件编译，再经南沙供应链流片封测，与西电主校 SiC 功率器件合成为"电源—算力合一"主板**（见 `hardware_mod.md` §3.3）。
  So CMR's "programming/compilation" stage should be defined as: **circuit design and FPGA/firmware compilation of the rad-hard SoC/power devices on the GaN platform of the Xidian Guangzhou Innovation Center, then tape-out and packaging/testing through the Nansha supply chain, combined with SiC power devices from Xidian's main campus into a "power + compute in one" mainboard** (see `hardware_mod.md` §3.3).

---

## 1. 产业链地图（核实来源） / 1. Industry Chain Map (Verified Sources)

| 环节 / Stage | 广州承载主体 / Guangzhou entity | 关键事实（来源） / Key facts (sources) | 对 CMR 的作用 / Role for CMR |
|---|---|---|---|
| **设计 / 中试线 / Design / pilot line** | **广州第三代半导体创新中心**（黄埔·中新知识城，西电广州研究院） / **Guangzhou Third-Generation Semiconductor Innovation Center** (Huangpu, Sino-Singapore Knowledge City, Xidian Guangzhou Institute) | 西电与广州开发区共建，郝跃院士领衔；6–8 英寸 GaN 晶圆生长/工艺/封测全流程研发与技术服务；2023-09 中试线通线；省内工程技术研究中心已获批[¹][²][³] / Co-built by Xidian and Guangzhou Development District, led by Academician Hao Yue; full-process R&D and technical services for 6–8-inch GaN wafer growth/processing/packaging; pilot line opened 2023-09; approved as a provincial engineering technology research center[¹][²][³] | CMR 抗辐射 SoC/功率器件**电路设计、固件与 FPGA 编译、小批量中试** / **Circuit design, firmware and FPGA compilation, small pilot batches** for CMR rad-hard SoC/power devices |
| **材料（衬底） / Materials (substrates)** | **南砂晶圆**（南沙万顷沙） / **Nansha Wafer** (Wanqingsha, Nansha) | SEMICON China 2026 展示 **12 英寸 SiC 衬底**，导入 AI 芯片封装头部企业[⁴][⁵] / Showed **12-inch SiC substrates** at SEMICON China 2026, adopted by leading AI-chip packaging companies[⁴][⁵] | 提供 SiC 单晶衬底，供给芯片制造 / Supplies SiC single-crystal substrates for chip manufacturing |
| **芯片制造 / Chip manufacturing** | **芯粤能**（南沙万顷沙） / **Xinyueneng** (Wanqingsha, Nansha) | 自主研发**车规级碳化硅主驱芯片**量产、获多家车企定点，跻身全球独角兽[⁴][⁵] / Self-developed **automotive-grade SiC traction chips** in mass production, selected by several automakers, now a global unicorn[⁴][⁵] | CMR 抗辐射功率芯片的**量产制造** / **Volume manufacturing** of CMR rad-hard power chips |
| **功率模块 / Power modules** | **芯聚能**（南沙万顷沙） / **Xinjuneng** (Wanqingsha, Nansha) | SiC 功率模块在新能源汽车主驱逆变器规模化应用，并拓展低空经济/AI 数据中心[⁶] / SiC power modules used at scale in EV traction inverters, expanding into the low-altitude economy / AI data centers[⁶] | CMR 电源变换模块（MPPT/电机驱动/二次电源） / CMR power-conversion modules (MPPT / motor drive / secondary power) |
| **协同平台 / Collaboration platform** | 广州南沙产业园（开建·芯动力科技城） / Guangzhou Nansha Industrial Park (Kaijian Xindongli Tech City) | 集研发、中试、规模生产、总部集聚，覆盖"技术研发→中试→产业应用→规模生产"[⁶] / Combines R&D, pilot production, volume production and HQs, covering "R&D → pilot → industrial application → volume production"[⁶] | CMR 板卡从样品到批量的**产业化载体** / **Industrialization vehicle** taking CMR boards from samples to volume |

**来源 / Sources**
- [¹] 西电广州研究院·广州市第三代半导体创新中心简介 / Xidian Guangzhou Institute — Guangzhou Third-Generation Semiconductor Innovation Center overview：https://gzyjy.xidian.edu.cn/info/1211/5310.htm
- [²] 西电广州研究院获批广东省工程技术研究中心 / Xidian Guangzhou Institute approved as a Guangdong engineering technology research center：https://gzyjy.xidian.edu.cn/info/1028/7231.htm
- [³] 西电广州第三代半导体创新中心正式通线（郝跃：GaN 抗辐射/耐高温） / Xidian Guangzhou Third-Generation Semiconductor Innovation Center line officially opened (Hao Yue: GaN radiation-resistant / high-temperature)：https://news.xidian.edu.cn/info/1371/225903.htm
- [⁴] 万顷沙集成电路产业园"芯"潮澎湃（南砂晶圆 12 英寸 SiC、芯粤能独角兽） / Wanqingsha IC Industrial Park chip boom (Nansha Wafer 12-inch SiC, Xinyueneng unicorn)：https://m.thepaper.cn/newsDetail_forward_33001234
- [⁵] 图南七园行·万顷沙 / Tour of Nansha's seven parks — Wanqingsha：https://static.nfnews.com/content/202604/13/c12333723.html
- [⁶] 南沙亮相链博会·第三代半导体产业协同 / Nansha at the China International Supply Chain Expo — third-generation semiconductor collaboration：https://www.chinatradenews.com.cn/article/headlines/177646

---

## 2. 为什么是 GaN（而非纯 SiC）做"抗辐射计算基底" / 2. Why GaN (Not Just SiC) as the "Rad-Hard Compute Base"

西电广州创新中心的重点是 **GaN（氮化镓）射频/电力电子/光电子**；西电主校（天舟六号在轨验证）的重点是 **SiC（碳化硅）功率器件**。两者在 CMR 上分工：

The Xidian Guangzhou Innovation Center focuses on **GaN (gallium nitride) RF / power electronics / optoelectronics**; Xidian's main campus (validated in orbit on Tianzhou-6) focuses on **SiC (silicon carbide) power devices**. They divide the work on CMR as follows:

| 器件 / Device | 角色 / Role | 抗辐射要点 / Radiation-hardness notes |
|---|---|---|
| **SiC 功率器件**（西电主校） / **SiC power devices** (Xidian main campus) | 电源变换：太阳能 MPPT、电机驱动、二次电源 / Power conversion: solar MPPT, motor drive, secondary power | 裂栅加固、抗单粒子，已随天舟六号 LEO 验证 / Split-gate hardening, single-event resistant, validated in LEO on Tianzhou-6 |
| **GaN 基底 SoC/射频**（西电广州） / **GaN-based SoC / RF** (Xidian Guangzhou) | 抗辐射计算、通信前端、高功率密度电源 / Rad-hard compute, comms front end, high-power-density power supply | 郝跃团队明确 GaN 具**抗辐射、耐高温、耐高压、大功率**特性，适合宇航边缘推理 / Hao Yue's team states GaN is **radiation-resistant, high-temperature, high-voltage and high-power**, suited to space edge inference |

→ CMR 主板 = **GaN 抗辐射计算 SoC（西电广州设计/中试） + SiC 功率级（西电主校器件） + 不锈钢导热骨架（散热+被动屏蔽）**，详见 `hardware_mod.md` §3.3。

→ CMR mainboard = **GaN rad-hard compute SoC (designed/piloted at Xidian Guangzhou) + SiC power stage (Xidian main-campus devices) + stainless-steel thermal frame (cooling + passive shielding)**; see `hardware_mod.md` §3.3.

---

## 3. CMR "编程—编译"工具链（落到广州的具体操作） / 3. CMR "Programming — Compilation" Toolchain (Concrete Steps in Guangzhou)

把"用广州第三代半导体进行编程编译"落成可执行步骤：

Turning "programming and compiling with Guangzhou third-generation semiconductors" into executable steps:

1. **电路与 RTL 设计**：在西电广州创新中心的 GaN 设计平台完成抗辐射 SoC / 电源管理芯片的电路图与 FPGA RTL（参考该中心已建成的 GaN 微波毫米波与电力电子设计平台）。
   **Circuit and RTL design**: complete the schematics and FPGA RTL for the rad-hard SoC / power-management chips on the GaN design platform of the Xidian Guangzhou Innovation Center (building on its existing GaN microwave/mm-wave and power-electronics design platforms).
2. **交叉编译 / 固件构建**：针对抗辐射 SoC 目标（如 Xilinx Zynq UltraScale+ MPSoC 宇航级、Microchip RTG4/PolarFire，或国产 GaN 基抗辐照 MCU）做**交叉编译**，生成可在辐射环境运行的位流与固件；工具链容器化，CI 跑在本地（参考本项目 `simulation/` 的纯本地作风）。
   **Cross-compilation / firmware build**: **cross-compile** for rad-hard SoC targets (e.g. space-grade Xilinx Zynq UltraScale+ MPSoC, Microchip RTG4/PolarFire, or domestic GaN-based radiation-tolerant MCUs) to produce bitstreams and firmware that run in radiation environments; containerize the toolchain and run CI locally (in the purely local style of this project's `simulation/`).
3. **中试流片**：在西电广州创新中心中试线做小批量工艺验证（6–8 英寸 GaN 全流程能力）。
   **Pilot tape-out**: small-batch process validation on the Xidian Guangzhou Innovation Center pilot line (6–8-inch GaN full-process capability).
4. **量产制造**：放量走南沙供应链——南砂晶圆衬底 → 芯粤能芯片 → 芯聚能功率模块，由南沙产业园做封测与系统集成。
   **Volume manufacturing**: scale up through the Nansha supply chain — Nansha Wafer substrates → Xinyueneng chips → Xinjuneng power modules, with packaging/testing and system integration in the Nansha industrial park.
5. **辐照试验**：送西电/院所辐照平台做总剂量/单粒子试验，形成飞行件数据（接入本项目 `blockchain_ledger.py` 做数据溯源，见 `docs/blockchain.md`）。
   **Irradiation testing**: send to Xidian/institute irradiation facilities for total-dose / single-event tests, producing flight-hardware data (fed into this project's `blockchain_ledger.py` for provenance; see `docs/blockchain.md`).

> 注：西电广州创新中心面向企业提供**合作代工、技术培训、成果转化、产业孵化**服务[³]，CMR 团队可走"合作研发 + 中试代工"而非自建产线，大幅降低启动成本。
>
> Note: the Xidian Guangzhou Innovation Center offers companies **contract foundry, technical training, technology transfer and industrial incubation** services[³]; the CMR team can take the "joint R&D + pilot foundry" route instead of building its own line, greatly lowering start-up costs.

---

## 4. 与既有文档的衔接 / 4. Links to Existing Documents

- `docs/hardware_mod.md` §3.3「抗辐射算力与电源（西电三代半）」：补充广州分支（GaN 设计/中试）与南沙（量产）的分工。
  `docs/hardware_mod.md` §3.3 "Rad-hard compute and power (Xidian 3rd-gen semiconductors)": adds the division of labour between the Guangzhou branch (GaN design/pilot) and Nansha (volume production).
- `docs/launch_plan.md`：发射成本账不变；但"抗辐射化"阶段现在有了明确的**本地（广州）设计与制造入口**。
  `docs/launch_plan.md`: launch costs are unchanged, but the "radiation hardening" stage now has a clear **local (Guangzhou) design and manufacturing entry point**.
- 火星场景（`docs/mars_rover.md`）与区块链审计（`docs/blockchain.md`）产生的遥测/样品哈希，可回灌到西电广州平台做在轨数据闭环验证。
  Telemetry/sample hashes from the Mars scenario (`docs/mars_rover.md`) and blockchain audit (`docs/blockchain.md`) can be fed back to the Xidian Guangzhou platform for closed-loop in-orbit data validation.

---

## 5. 诚实边界 / 5. Honest Limits

- 西电公开的是**功率器件/中试平台**，不是现成的"整板飞行计算机"；CMR 仍需自研主板并把商用抗辐射 SoC 与西电器件集成。
  What Xidian has published are **power devices / a pilot platform**, not a ready-made "complete flight computer board"; CMR still needs its own mainboard integrating a commercial rad-hard SoC with Xidian devices.
- 南沙量产以**车规级 SiC** 为主，宇航级筛选需额外试验；GaN 中试线面向研发与技术服务，**宇航批量**仍需工程化爬坡。
  Nansha's volume production is mainly **automotive-grade SiC**; space-grade screening needs extra testing. The GaN pilot line serves R&D and technical services; **space-grade volume** still needs an engineering ramp-up.
- 上述产业事实来自 2026-10-29 公开报道（南方+、澎湃、中国贸易报、西电官网、黄埔/广州科技局），落地前建议与西电广州研究院、南沙产业园做正式对接核实。
  The industry facts above come from public reports as of 2026-10-29 (Nanfang+, The Paper, China Trade News, Xidian's official site, Huangpu/Guangzhou S&T bureaus); before implementation, formally verify with the Xidian Guangzhou Institute and the Nansha industrial park.
