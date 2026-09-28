
## 10. 资料库加深

按这个顺序读，避免一上来背厂商写频手册里的「色码传说」：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `00-入门/DMR术语与帧结构速查卡.md` | Colour Code 行：区分同频、降低误听 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§2–§3** | CC 出现在嵌入与数据突发；108+48+108；Slot Type / EMB 解剖图 |
| 3 | 同上 **§7.1 / §7.2** | EMB PDU、SLOT PDU 字段表（含 CC） |
| 4 | 同上 **§8** | IE：CC 4 bit；DM 中 `1111`=All site；条款 9.3.1 |
| 5 | `学习推送/第16课.md` | 数据壳为何有 Slot Type；别把 48 当色码 |
| 6 | `学习推送/第17课.md` | 嵌入窗与 EMB 出场 |
| 7 | `学习推送/第18课.md` | CACH 与 CC 划界 |
| 8 | `学习推送/第19课.md` | SYNC ≠ CC；同步成功≠色码对 |
| 9 | 官方 **TS 102 361-1 V2.7.1** clause **4.2.1、9.1.2、9.1.3、9.3.1**；Tables **9.3–9.4** | 原文；冲突以 PDF 为准 |
| 10 | **TR 102 398** 对应导读 | 概念对照，**不是**替代 TS |
| 11 | `01-空中接口/跳过项原则说明.md` | Slot Type Golay / EMB QR 记名不贴矩阵 |
| 12 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍怀疑「改 CC 会换频」 |

官方版本锚点：**Part1 V2.7.1**；**TR V1.5.1**。冲突规则：**TS > TR > 手册/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 11. 下一课预告

**第 21 课 · EMB / SLOT 字段**

本课站住了 **4 bit Colour Code**：它住在 Slot Type / EMB，用来给同频系统刷色，并且 **SYNC ≠ CC ≠ CACH**。下一课把 **EMB PDU** 与 **SLOT PDU** 整包拆开：PI、LCSS、Data Type、两段 parity 各管什么，语音嵌入与数据壳如何从「有个 CC」进到「能读完整小报头」。仍少公式，多对照字段表与分析仪。

---

## 12. 推荐阅读与视频

本课外链为 **2026-09-28**（上午推送）检索核验；**不编造地址**。策略 = **Part1 CC 原文 + TR 导读 + GopherTrunk 色码词条/突发解码文 + 入门写频向英文博文 + qdmr 技术背景 + Guido 常规 Tier II 培训 PDF**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **4.2.1** 写明 CC 出现在嵌入信令与一般数据突发、用于区分重叠站点并检测同频干扰，且 **CC 不做个呼/组呼寻址**；clause **9.3.1** 与 Tables **9.3–9.4** 给 EMB/SLOT 中的 CC 位宽——请在 PDF 内核对 All site 等细则。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)。  
   - **适合哪一段**：第 2、4、7、10 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读用「同频区分 / 色码」叙事，比纯条款好读；可与突发长度账本对账。  
   - **适合哪一段**：第 2、7、10 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[GopherTrunk｜Color code (DMR) 词条](https://gophertrunk.org/reference/color-code/)**  
   - **为什么值得看**：把 CC 说成「每突发携带的 4 bit 系统色 / 同频过滤」，并明确 **CC 是接入过滤不是地址、不是加密**——与本课钉子同向。  
   - **适合哪一段**：第 1–3、5、8 节后对照。  
   - **注意**：实现/监测向表述；若文中提到 CACH 等扩展位置，**以 Part1「嵌入 + 一般数据突发」与资料库 Slot Type/EMB 为准**做主记忆。  
   - **基础**：入门～中级；英文网页。

4. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：把 Slot Type（CC+Data Type）与 EMB 在突发里的位置画进解码叙事，适合从本课滑向第 21 课。  
   - **适合哪一段**：第 4、6、11 节。  
   - **注意**：实现向；个别 FEC 俗称若与资料库「Golay(20,8)」表述不一致，**以 ETSI Annex B / 资料库为准**。  
   - **基础**：中级～进阶；英文网页。

5. **[Buy Two Way Radios｜Understanding Color Codes on DMR](https://www.buytwowayradios.com/blog/2026/02/understanding-color-codes-on-dmr-digital-two-way-radios.html)**  
   - **为什么值得看**：写频向白话：CC0–15、须与频率/时隙/组一起匹配、「有信号没声音先查 CC」——适合现场对照热身。  
   - **适合哪一段**：第 1、5、6 节。  
   - **注意**：零售科普；「CC 像亚音」只可作类比；硬条款与 All site 语义以 ETSI 为准。  
   - **基础**：入门；英文网页。

6. **[qdmr 手册｜Technical background（Time Slot & Color Code）](https://static.dm3mat.de/qdmr/manual/ch01s09.html)**  
   - **为什么值得看**：从「频率不够、多中继同频覆盖重叠 → 靠色码决定中继是否响应」讲清**工程动机**，和本课例子 A 同向。  
   - **适合哪一段**：第 2、5、6 节。  
   - **注意**：开源写频项目文档，偏业余/工具向；**不是** ETSI 原文。  
   - **基础**：入门～中级；英文网页。

7. **[Alessandro Guido｜How DMR Works — Conventional Tier 2（PDF）](https://www.qsl.net/kb9mwr/projects/dv/dmr/How%20DMR%20Works%20Conventional%20Tier%202.pdf)**  
   - **为什么值得看**：常规 Tier II 培训口吻重申「4 bit Colour Code 区分重叠站点」；并可见礼貌接入与 FEC 名表，便于和本课账本对读。  
   - **适合哪一段**：第 4、7、10 节后复盘。  
   - **注意**：培训文年代可能早于现行 Part1 V2.7.1；**硬条款以 V2.7.1 为准**。  
   - **基础**：入门～中级；英文 PDF。

8. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：突发与帧结构图便于回看 Slot Type / 嵌入位置，把「CC 藏在哪」钉回总图。  
   - **适合哪一段**：第 2、4 节。  
   - **注意**：厂商/分析仪向综述；**以 ETSI 为准**。  
   - **基础**：中级；英文 PDF。

**说明（视频）**：公开检索未找到专门把 **「CC 4 bit 位于 Slot Type/EMB；SYNC 成功 ≠ CC 匹配；同频异色降低误听但消不掉 RF 叠扰；DM 中 1111=All site；CC ≠ Talkgroup ≠ CACH」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只口播「色码像亚音、0–15」或产品写频演示）。本课**未找到合适公开专题视频**。建议用：**Part1 4.2.1 + 9.3.1 + GopherTrunk 色码词条 + 写频向博文 + 资料库 §7–§8** 对照自学。

---

*推送说明：本课为阶段 C「Colour Code 与同频系统」。频谱/调制仅保留短提醒（CC 不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、同频色标总图、术语、Slot Type/EMB 机制、All site 慎讲、SYNC≠CC≠CACH、现场对照、五则工作例子、数字账本、十则误区、八题自测、资料库路径与八条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「为何同频要靠色码、色码住在哪、为何有 SYNC 仍可能没声、写频 CC 与 Talkgroup/时隙如何分诊」，并进入第 21 课 EMB / SLOT 字段。*
