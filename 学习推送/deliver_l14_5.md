## 16. 推荐阅读与视频

本课外链为 2026-09-25 检索核验；**不编造地址**。策略 = **协会 IOP 说明 + Part2 互操作正文 + Part1 Annex H 入口 + 中文协议字段文 + 开源解码库**。

1. **[DMR Association｜DMR Interoperability（PDF）](https://www.dmrassociation.org/public-downloads/documents/DMR_Interoperability.pdf)**  
   - **为什么值得看**：用产业语言说明「为什么要有多厂家互通、IOP 测什么」；强制/可选特性清单有 Tier II/III 直觉。  
   - **适合哪一段**：第 8 节；招投标/售前对照。  
   - **注意**：文档内引用的 TS 版本可能偏旧；**字段与硬规则以你资料库当前 TS 为准**。  
   - **基础**：入门～进阶；英文 PDF。

2. **[DMR Association｜IOP Certification Process](https://dmrassociation.org/dmr-iop-certification.html)**  
   - **为什么值得看**：讲清认证是厂间对测、要抓空口日志、证书绑定软硬件版本。  
   - **适合哪一段**：第 8 节；理解「证书上有的才是承诺互通的」。  
   - **基础**：入门；英文网页。

3. **[ETSI TS 102 361-2 V2.5.1｜Part 2（DMR Association 镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：clause **4.3 Feature interoperability** 是本课硬规则原文；默认特性集=SFID、私有走 MFID、FNS 等均在此语境。  
   - **适合哪一段**：第 5–6 节后精读 4.3，再翻 Annex B Opcode。  
   - **基础**：进阶；英文 PDF；与本地 `02-语音业务/TS102361-2_V2.5.1.pdf` 同系列。

4. **[DMR 对讲机数字协议详解（含 Full LC / FLCO / FID 字段表）](http://www.cqkexun.com/products/292_2.html)**  
   - **为什么值得看**：中文图文把 Full LC 里 FLCO、FID、组呼/个呼地址摆出来，适合建立「外壳长什么样」的第一印象。  
   - **适合哪一段**：第 5–6 节。  
   - **注意**：厂商/集成商科普，版本与用词可能不新；**冲突以 ETSI TS 为准**。  
   - **基础**：入门；中文。

5. **[OK-DMR/ok-dmrlib（GitHub）](https://github.com/OK-DMR/ok-dmrlib)**  
   - **为什么值得看**：开源库显式支持 Full LC / CSBK 等 PDU，信息元素列表含 **FID、FLCO、CSBKO**，适合开发同学对照「字段名在实现里叫什么」。  
   - **适合哪一段**：第 5 节后；有代码阅读习惯时。  
   - **基础**：进阶；英文仓库。

6. **[Open source DMR modem（qradiolink）｜FID 与声码器/私有特性讨论](https://www.qradiolink.org/open-source-DMR-transceiver-implementation.html)**  
   - **为什么值得看**：用「不同 FID 区分特性集（文中讨论 Codec2 与 AMBE FEC）」说明 **FID 会改变对端如何解释载荷**——是 MFID/非默认 FID 思维的好例子。  
   - **适合哪一段**：第 2、7 节；理解「门牌一变，处理规则就变」。  
   - **注意**：这是研究/业余实现讨论，**不是**让你在商用标准语音里随意改 FID；商用标准语音仍应走 SFID。  
   - **基础**：进阶；英文。

**说明（视频）**：公开检索未找到专门把 **SFID / MFID / FLCO** 讲透的高质量中文长视频或 B 站专课；本课**未找到合适公开视频**。请以协会 IOP 文档 + Part2 clause 4.3 + 中文字段文 + 开源库补充。若你通勤只想听课，可复习第 13 课外链中的 [Tait Radio Academy｜Introduction to DMR](https://www.taitradioacademy.com/courses/introduction-to-digital-mobile-radio/)（呼叫类型与特性，英文），再回到本课看门牌模型。

---

## 17. 下一课预告

**第 15 课 · 时隙 30 ms 与 TDMA frame**

阶段 B 到此收官：你已经能从「DMR 是什么」走到「业务种类」再到「互操作门牌」。下一阶段进入空口肌肉记忆——**为什么是 30 ms 时隙、60 ms 一帧两时隙、和 12.5 kHz「地皮」如何一起养活两路业务**。仍然少公式，多对照：听得见比特之后，时间轴上到底发生了什么。

---

*推送说明：本课为阶段 B「互操作：SFID / MFID / FLCO」收官课。不加长篇频率加餐，只保留分流提醒（L1 差 vs 门牌错）。主文加厚覆盖动机、商场门牌总图、术语、现场对照、Full LC/CSBK 外壳、Annex H 分区、FLCO/CSBKO 地图、PDU 对照表、与 Service Options 分工、四则排障剧本、五则正反例、IOP 语感、误区、自测与六条核验外链（并诚实标明本课未找到合适公开专题视频）。读完应能向同事讲清「标准业务挂 SFID、私有走 MFID、同频同色码仍可能各说各话」，并进入阶段 C 时隙课。*
