# 制造与技术背书 / Manufacturing and Technical Credentials

> 语言说明 / Language note：本文中英双语，先中文后英文。 / This document is bilingual: Chinese first, then English.

本项目团队在工业识别、5G 终端硬件、多模态感知与数据安全方面已有实际专利、软件著作权与工程经验积累，可直接支撑 Cosmic Mining Rover（CMR）地面原型的传感器、样品识别、数据采集与加密回传链路。抗辐射化与轨道发射将与国内高校第三代半导体研究机构及商业发射服务商按计划推进合作，地面原型的核心识别与数据硬件可由团队自主设计与制造。

The project team already has real patents, software copyrights and engineering experience in industrial identification, 5G terminal hardware, multimodal sensing and data security, which directly support the sensors, sample identification, data acquisition and encrypted downlink chain of the Cosmic Mining Rover (CMR) ground prototype. For radiation hardening and orbital launch, cooperation with a domestic university third-generation semiconductor research institute and a commercial launch provider is being advanced as planned; the core identification and data hardware of the ground prototype can be designed and manufactured by the team in-house.

## 核心知识产权清单 / Core Intellectual Property

| 类型 / Type | 名称 / Title | 编号 / 登记号 (No. / Reg. No.) | 授权 / 登记日期 (Grant / Reg. date) | 与 CMR 的对应关系 / Relevance to CMR |
|------|------|---------------|-----------------|-------------------|
| 发明专利 / Invention patent | 一种基于5G网络的工业产品识别与溯源实现方法 / A 5G-network-based method for industrial product identification and traceability | ZL 2021 1 1029128.7 | 2024-05-31 | 样品材质识别后的身份确认与全流程溯源，支撑集尘盒内容物上链前的可信确认 / Identity confirmation and end-to-end traceability after sample-material identification, supporting trusted confirmation of dust-box contents before they go on-chain |
| 实用新型 / Utility model | 一种基于5G网络的工业产品识别装置 / A 5G-network-based industrial product identification device | ZL 2021 2 1583908.1 | 2021-12-21 | 机载多光谱 / 近红外识别终端、工具头数据采集模块的硬件基础 / Hardware basis for the onboard multispectral / NIR identification terminal and the tool-head data acquisition module |
| 实用新型 / Utility model | 一种用于工业产品自动识别的数据采集头盔 / A data acquisition helmet for automatic industrial product identification | ZL 2021 2 1584209.9 | 2021-11-30 | 可改造为便携式样品采集与现场识别单元，用于地面原型测试 / Can be adapted into a portable sample-collection and on-site identification unit for ground-prototype testing |
| 软件著作权 / Software copyright | 基于5G网络加密的微信小程序人脸识别认证系统 / 5G-network-encrypted WeChat mini-program face recognition authentication system | 2020SR0196023 | 2020-03-02 | 多模态识别算法与加密传输机制，可迁移至样品视觉分类与机载数据回传 / Multimodal recognition algorithms and encrypted transmission, transferable to sample visual classification and onboard data downlink |
| 论文 / Paper | 基于5G网络的人脸识别系统模型与加密机制 / A 5G-network-based face recognition system model and encryption mechanism | 《计算机技术与发展》2020年增刊 / *Computer Technology and Development*, 2020 supplement | 2020-10 | 5G 架构下设备端-网络-云端模型与 PKG/AES 加密流程，支撑机载加密与高速回传设计 / Device–network–cloud model and PKG/AES encryption flow under 5G, supporting onboard encryption and high-speed downlink design |

## 工程经验补充 / Additional Engineering Experience

- 广东省科技计划项目“面向大规模流动人群的健康码防疫智能管理系统的研发”（2022 年省科技创新战略专项），由本项目负责人担任技术第一负责人。项目涉及多模态生物识别、戴口罩人脸识别、大数据 AI 算法与数据安全加固，具备面向大规模场景的系统级设计与落地经验。
  Guangdong Provincial Science and Technology Programme project "R&D of a health-code intelligent epidemic-prevention management system for large mobile populations" (2022 Provincial Special Fund for S&T Innovation Strategy), with the project lead serving as the first technical lead. The project involved multimodal biometrics, masked-face recognition, big-data AI algorithms and data-security hardening, providing system-level design and deployment experience for large-scale scenarios.
- 相关识别与加密技术已在工业与公共场景验证，可直接复用至 CMR 的样品视觉识别（集尘盒内容物分类）、机载数据加密存储与星链回传链路。
  The related identification and encryption technologies have been validated in industrial and public settings and can be reused directly for CMR's sample visual recognition (dust-box content classification), onboard encrypted data storage and the Starlink downlink.

## 迁移说明 / Transfer Notes

1. **传感器与识别终端**：现有工业产品识别装置与数据采集头盔的硬件架构，可进行轻量化、抗辐射化改造后用于 CMR 工具头与样品仓。
   **Sensors and identification terminals**: the hardware architecture of the existing industrial product identification device and data acquisition helmet can be made lighter and radiation-hardened for use in the CMR tool head and sample bay.
2. **识别算法**：多模态识别与加密机制可直接应用于 `simulation/` 中的视觉分类模块，并扩展至真实硬件。
   **Recognition algorithms**: the multimodal recognition and encryption mechanisms can be applied directly to the visual classification module in `simulation/` and extended to real hardware.
3. **溯源与上链**：发明专利中的识别与溯源流程可与仓库现有区块链账本（`ledger.json`）对接，形成“采集 → 识别 → 确认 → 铸造资产”的完整可信链路。
   **Traceability and on-chain recording**: the identification and traceability flow in the invention patent can connect to the repository's existing blockchain ledger (`ledger.json`), forming a complete trusted chain of "collect → identify → confirm → mint asset".

> 注：以上材料均已公开授权或登记。具体证书与论文全文可在需要时补充至本目录或通过官方渠道查询验证。
>
> Note: all the above materials have been publicly granted or registered. Certificates and full paper texts can be added to this directory when needed, or verified through official channels.
