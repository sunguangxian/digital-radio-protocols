## 10. 自测（8 题）

**题 1.** 用一句话区分 Full LC 与 Short LC。为什么说「不是截短关系」？

<details><summary>简答</summary>

Full LC 是约 72 bit 信息的呼叫门牌正文，走 Header/Terminator/嵌入；Short LC 是 SLCO+24+CRC8，只经 CACH。Opcode 宽度、有无 FID、校验、运载缝全不同——不是同一 PDU 截短。

</details>

**题 2.** 画出 Full LC 八位组外壳（PF/R/FLCO/FID/Data），并写出头/终止与嵌入两条 CRC 名称差异。

<details><summary>简答</summary>

`[PF|R|FLCO][FID][Data 56][+CRC]`。头/终止：RS**(12,9)** 24-bit；嵌入：5-bit checksum。

</details>

**题 3.** Full LC 有哪两条主要运载路径？各依赖什么小报头/单据类型？

<details><summary>简答</summary>

① Voice LC Header / Terminator with LC：数据壳 **SLOT** + Data Type。② 超帧 B–E 嵌入：语音壳 **EMB+LCSS**，无 Slot Type。

</details>

**题 4.** 标准组呼 Full LC 在 SFID 下，FLCO 学习值是什么？Data 里通常有哪三类字段直觉？

<details><summary>简答</summary>

FLCO=`000000`（Grp_V_Ch_Usr）。直觉：Service Options + 组地址 24 + 源地址 24（细则 Part2）。

</details>

**题 5.** Short LC 三个字段长度？经哪条物理缝？CACH 分片有何特殊提醒？

<details><summary>简答</summary>

SLCO**4** + Data**24** + CRC**8**；经出站 **CACH**。提醒：无「单片 LC」用法，须按 LCSS 拼装。

</details>

**题 6.** 对照表各用一句话区分：Full LC、Short LC、EMB/SLOT、CSBK。

<details><summary>简答</summary>

Full=门牌正文；Short=缝里短广播；EMB/SLOT=小报头；CSBK=控制块外壳（FLCO≠CSBKO）。

</details>

**题 7.** 现场「色码对、有语音超帧，但扬声器不响」——如何用本课做下一步？

<details><summary>简答</summary>

查是否拼出/解出 Full LC 地址与组匹配；FLCO/FID 是否标准馆；是否落在错误时隙。区分「CC 已过」与「门牌正文未匹配」。

</details>

**题 8.** 为什么说 late entry 证明「嵌入 LC 不是装饰」？它替代 Header 了吗？

<details><summary>简答</summary>

嵌入重复广播同一类门牌，让中途加入者仍能识别组/源——这是设计能力。它不消灭 Header 的发起角色；常规系统发起仍常用 Header，嵌入是并行的重复与补救路径。

</details>

---

## 11. 资料库加深

按这个顺序读，避免一上来背厂商解码树黑话：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `01-空中接口/CSBK与LC字段详表.md` **§4–§5** | Full LC Table 9.7；Short LC Table 9.8 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§4、§5、§7.3–7.4** | 超帧嵌入；CACH；FULL/SHORT 外壳 |
| 3 | `02-语音业务/语音业务字段速览.md` **§1、§3、§5、§6** | FLCO 业务体；Short LC Act_Updt；Service Options |
| 4 | `学习推送/第14课.md` | FID/FLCO 门牌（本课前门） |
| 5 | `学习推送/第17课.md` | B–E 嵌入与 late entry 故事 |
| 6 | `学习推送/第18课.md` | CACH / Short LC / LCSS |
| 7 | `学习推送/第21课.md` | EMB/SLOT；Data Type=Header/Terminator |
| 8 | 官方 **TS 102 361-1 V2.7.1** clause **7.1、9.1.6–9.1.7、9.3.10–9.3.12**；Tables **9.7、9.8**；Annex **B.2.1、B.2.3、B.3.6、B.3.7、B.3.11** | 原文；冲突以 PDF 为准 |
| 9 | 官方 **TS 102 361-2**（本库 `02-语音业务/TS102361-2_V2.5.1.pdf`）clause **7.1.x** | FLCO/SLCO **业务体**；勿用 Part1 冒充 |
| 10 | **TR 102 398** | 概念导读，**不是**替代 TS |
| 11 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍怀疑「LC 会换调制」 |

官方版本锚点：**Part1 V2.7.1**；语音业务体以本库 **Part2** PDF 为准。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 12. 下一课预告

**第 23 课 · CSBK 控制信令块**

本课站住了链路控制正文：**Full LC**（门牌 72 + 头终止/嵌入两路径）与 **Short LC**（CACH 慢广播），并钉死「Short ≠ 截短 Full、EMB/SLOT 只是标签」。下一课打开另一只控制外壳：**CSBK**——`LB|PF|CSBKO|FID|Data64|CRC-16`，单块与 MBC、和 Full LC 的分工（谁管呼叫门牌、谁管请求/应答/唤醒等控制事务），仍少公式，多对照字段表与现场抓包。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-29**（上午推送）检索核验；真实打开过内容页/PDF；**不编造地址**。策略 = **Part1 Full/Short LC 原文 + Part2 业务体指针 + TR 导读 + GopherTrunk Link Control/Late Entry 深文 + CACH 词条 + Wavecom/培训 PDF 帧图**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **7.1** 讲 Voice LC Header / Terminator / Embedded / Short LC in CACH；**9.1.6 / 9.1.7** 与 Tables **9.7 / 9.8** 定义两套 PDU；**9.3.11–9.3.12** 钉 FLCO/SLCO。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读里对链路控制/突发/嵌入的叙事比纯条款好读，便于和本课总图对账。  
   - **适合哪一段**：第 2、7、11 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
   - **为什么值得看**：把 72-bit Full LC、Header/Terminator/嵌入三条运载、B–E 拼装与 late entry 写成同一条故事线——本课例子 A/C 的加厚版。  
   - **适合哪一段**：第 4、6、7、12 节。  
   - **注意**：实现向（如「确认两次」）是工程选择；规范语义以 ETSI 为准。文中若把 EMB 的 PI 写成 privacy 口语，**以 Part1「Pre-emption and power control Indicator」为准**（业务 Privacy 在 Service Options / Part2）。  
   - **基础**：中级～进阶；英文网页。

4. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：Slot Type 与 EMB+嵌入 LC 拼装同框，便于回看第 21 课小报头如何托起本课正文。  
   - **适合哪一段**：第 2、4、5 节。  
   - **注意**：校验命名以 ETSI Annex B 为准。  
   - **基础**：中级～进阶；英文网页。

5. **[GopherTrunk｜DMR CACH（词条）](https://gophertrunk.org/reference/dmr-cach/)**  
   - **为什么值得看**：巩固「Short LC 住在出站缝」；并诚实标明实现可能只拿 CACH 当节拍——对照第 18 课与本课 §4.4。  
   - **适合哪一段**：第 4、7 节例子 D。  
   - **注意**：词条偏 SDR 节拍；**Short LC 业务体仍以 Part2 为准**。  
   - **基础**：入门～中级；英文网页。

6. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：帧/突发/超帧 A–F 图，便于把 Header→A–F→Terminator 钉回 264 与缝。  
   - **适合哪一段**：第 2、7 节。  
   - **注意**：厂商综述，版本锚点可能早于 V2.7.1；**硬条款以现行 Part1 为准**。  
   - **基础**：中级；英文 PDF。

7. **[Alessandro Guido｜How DMR Works — primer PDF（hamgear）](https://hamgear.files.wordpress.com/2014/02/dmr-primer.pdf)**  
   - **为什么值得看**：培训幻灯式回顾 Voice LC Header/Terminator、嵌入 LC、Short LC in CACH、FEC/CRC 名称表——和本课数字账本同向。  
   - **适合哪一段**：第 4、8、11 节后复盘。  
   - **注意**：年代偏早、版本号旧；**以 V2.7.1 / 本库 Part2 为准**。  
   - **基础**：入门～中级；英文 PDF。

8. **[GopherTrunk｜DMR End to End Part 2：Bursts, Sync Words & Polarity](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-02-bursts-sync-polarity/)**  
   - **为什么值得看**：再次钉死「语音突发没有 Slot Type」——避免把嵌入路径误读成「也有 Data Type」。  
   - **适合哪一段**：第 4、5、9 节。  
   - **注意**：偏扫描器/实现；极性故事超纲可略读。  
   - **基础**：中级；英文网页。

9. **[qdmr 手册｜Technical background（Time Slot & Color Code）](https://static.dm3mat.de/qdmr/manual/ch01s09.html)**  
   - **为什么值得看**：从工程动机复习色码门——读 LC 正文前先过 CC（第 20–21 课保活）。  
   - **适合哪一段**：第 1、6 节热身。  
   - **注意**：开源写频文档，**不是** Full/Short LC 字段专论。  
   - **基础**：入门；英文网页。

**说明（视频）**：公开检索未找到专门把 **「Full LC 72 信息 + 头终止 RS24 / 嵌入 CS5；Short LC 4+24+8 经 CACH；FLCO≠SLCO；三路径对照；late entry」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只演示写频组呼或产品抓包界面，不拆 PDU）。本课**未找到合适公开专题视频**。建议用：**Part1 Tables 9.7/9.8 + GopherTrunk E2E Part5 + 资料库 §4–§5 / 语音业务速览** 对照自学。

---

*推送说明：本课为阶段 C「FULL LC / SHORT LC」。频谱/调制仅保留短提醒（LC 不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、三路径总图、术语、Full LC 八位组与两 CRC 路径、Short LC/CACH、FLCO 门牌回指、四柜对照、现场分诊、五则工作例子、数字账本、十则误区、八题自测、资料库路径与九条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「Full LC 与 Short LC 为何不是截短关系、门牌正文如何经 Header/嵌入两路到达、CACH 短广播怎么拼、为何不能把 EMB/SLOT 叫成 LC」，并进入第 23 课 CSBK 控制信令块。*
