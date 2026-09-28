
## 11. 资料库加深

按这个顺序读，避免一上来背厂商解码树黑话：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `00-入门/DMR术语与帧结构速查卡.md` | 264 / 超帧 / SYNC / CACH 总尺 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§3** | 语音 108+48+108；数据 98+SLOT+48；嵌入 8+32+8 |
| 3 | 同上 **§7.1 / §7.2** | EMB PDU、SLOT PDU |
| 4 | 同上 **§8** | LCSS、Data Type、Table 9.22 速查 |
| 5 | `01-空中接口/CSBK与LC字段详表.md` **§1–§3** | 嵌入位置、EMB、SLOT、LCSS 表 |
| 6 | `01-空中接口/跳过项原则说明.md` §1.4 | Golay/QR **记名不贴矩阵** |
| 7 | `学习推送/第16课.md`–`第17课.md` | 货箱与超帧；EMB 出场 |
| 8 | `学习推送/第18课.md`–`第19课.md` | CACH LCSS vs SYNC 分壳 |
| 9 | `学习推送/第20课.md` | CC 与同频；本课的前门 |
| 10 | 官方 **TS 102 361-1 V2.7.1** clause **6.1–6.2、9.1.2–9.1.3、9.3.2–9.3.3、9.3.6**；Tables **9.3、9.4、9.19、9.22** | 原文；冲突以 PDF 为准 |
| 11 | **TR 102 398** | 概念导读，**不是**替代 TS |
| 12 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍怀疑「小报头会换调制」 |

官方版本锚点：**Part1 V2.7.1**；**TR V1.5.1**。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 12. 下一课预告

**第 22 课 · FULL LC / SHORT LC**

本课站住了两套小报头：**EMB 16**（CC+PI+LCSS+QR）与 **SLOT 20**（CC+Data Type+Golay），并钉死「语音无 Slot Type、Data Type 路由 196、LCSS 管分片」。下一课进入报头背后的**链路控制正文**：Full LC 八位组（PF/FLCO/FID/地址…）、头/终止与嵌入两条路径、以及 CACH 上的 Short LC（SLCO+数据）——仍少公式，多对照字段表与呼叫「门牌」。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-28**（傍晚推送）检索核验；真实打开过内容页/PDF；**不编造地址**。策略 = **Part1 EMB/SLOT 原文 + TR 导读 + GopherTrunk 突发/EMB/Slot Type 深文 + Late Entry 嵌入文 + Wavecom 帧图 + 协会/ETSI 镜像**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **6.1 / 6.2** 给语音嵌入与数据壳布局；**9.1.2 / 9.1.3** 与 Tables **9.3 / 9.4** 定义 EMB、SLOT；**9.3.2–9.3.3、9.3.6** 与 Tables **9.19 / 9.22** 钉 PI、LCSS、Data Type。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读里对突发/嵌入/控制块的叙事比纯条款好读，便于和本课总图对账。  
   - **适合哪一段**：第 2、7、11 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：把 Slot Type（CC+Data Type）与 EMB+嵌入 LC 拼装画进同一套解码叙事；明确数据壳两侧 10+10、语音走另一套读法——与本课钉子同向。  
   - **适合哪一段**：第 2、4、5、7、12 节。  
   - **注意**：实现向；文中 Slot Type 或称 Hamming(20,8)，资料库/ETSI Annex B 学习记名用 **Golay(20,8)**——**以 ETSI 为准**。  
   - **基础**：中级～进阶；英文网页。

4. **[GopherTrunk｜DMR End to End Part 2：Bursts, Sync Words & Polarity](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-02-bursts-sync-polarity/)**  
   - **为什么值得看**：FAQ 级钉子「Do voice bursts have a slot type? **No.**」；并把 Data Type 写成「payload 之前的路由」。适合巩固 §4–§6。  
   - **适合哪一段**：第 4、5、6、9 节。  
   - **注意**：偏扫描器/实现；极性故事超纲可略读。  
   - **基础**：中级；英文网页。

5. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
   - **为什么值得看**：EMB+LCSS 如何服务 late entry；Header / Terminator / 嵌入三条运 LC 的车——本课例子 D 的加厚版，并自然滑向第 22 课。  
   - **适合哪一段**：第 4、7、12 节。  
   - **注意**：实现细节（确认两次等）是工程选择；规范语义以 ETSI 为准。文中若把 PI 写成 privacy 口语，**以 Part1「Pre-emption and power control Indicator」为准**。  
   - **基础**：中级～进阶；英文网页。

6. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：帧/突发/超帧 A–F / RC 位置图，便于回看「中心场与缝」总图，把 EMB/SLOT 钉回 264。  
   - **适合哪一段**：第 2、5 节。  
   - **注意**：厂商综述，版本锚点可能早于 V2.7.1；**硬条款以现行 Part1 为准**。  
   - **基础**：中级；英文 PDF。

7. **[Alessandro Guido｜How DMR Works — Conventional Tier 2（PDF）](https://www.qsl.net/kb9mwr/projects/dv/dmr/How%20DMR%20Works%20Conventional%20Tier%202.pdf)**  
   - **为什么值得看**：常规 Tier II 培训口吻回顾超帧与控制/语音分壳，便于和 Data Type / 嵌入叙事对读。  
   - **适合哪一段**：第 2、7、11 节后复盘。  
   - **注意**：培训文年代可能偏早；**以 V2.7.1 为准**。  
   - **基础**：入门～中级；英文 PDF。

8. **[qdmr 手册｜Technical background（Time Slot & Color Code）](https://static.dm3mat.de/qdmr/manual/ch01s09.html)**  
   - **为什么值得看**：从工程动机复习「同频靠色码」——本课 SLOT/EMB 都携带 CC，读完第 20 课后用来保活上下文。  
   - **适合哪一段**：第 1、6 节热身。  
   - **注意**：开源写频文档，**不是** EMB/SLOT 字段专论。  
   - **基础**：入门；英文网页。

**说明（视频）**：公开检索未找到专门把 **「EMB 16 = CC+PI+LCSS+QR；SLOT 20 = CC+Data Type+Golay；语音无 Slot Type；LCSS 分片；Data Type 路由 196；SYNC≠EMB≠SLOT≠CACH」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只演示写频色码或产品抓包界面，不拆 PDU）。本课**未找到合适公开专题视频**。建议用：**Part1 Tables 9.3/9.4/9.19/9.22 + GopherTrunk Part5 / E2E Part2&5 + 资料库 §3/§7/§8** 对照自学。

---

*推送说明：本课为阶段 C「EMB / SLOT 字段」。频谱/调制仅保留短提醒（小报头不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、两套小报头总图、术语、EMB（PI/LCSS/QR）与 SLOT（Data Type/Golay）机制、四柜对照、现场分诊、五则工作例子、数字账本、十则误区、八题自测、资料库路径与八条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「语音嵌入小报头与数据 Slot Type 各长什么样、Data Type 与 CC 如何分诊、LCSS 如何服务晚入网、为何不能把中心 48 整段叫作 EMB」，并进入第 22 课 FULL LC / SHORT LC。*
