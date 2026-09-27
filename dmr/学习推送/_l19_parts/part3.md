## 10. 资料库加深

按这个顺序读，避免一上来背 Table 9.2 全表 hex：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `00-入门/DMR术语与帧结构速查卡.md` | SYNC 行；语音/数据不同图案；疏密一句 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§3** | 108+48+108；中心 SYNC 或嵌入；~5 ms |
| 3 | 同上 **§4** | 超帧 A = Voice SYNC；SYNC 疏密对照表 |
| 4 | 同上 **§6** | SYNC 类型摘要；类别表；互补直觉；首突发规则 |
| 5 | `学习推送/第16课.md` | 中心座位总览；264 vs 48 |
| 6 | `学习推送/第17课.md` | A = Voice SYNC；B–F 嵌入；迟后进入 |
| 7 | `学习推送/第18课.md` | CACH/Guard 与中心 48 划界 |
| 8 | 官方 **TS 102 361-1 V2.7.1** clause **4.2.2、4.3、9.1.1**；Tables **9.1–9.2** | SYNC 原文与图案表；**hex 只在 PDF 查**；冲突以 PDF 为准 |
| 9 | **TR 102 398** 对应导读 | 概念对照，**不是**替代 TS |
| 10 | `01-空中接口/跳过项原则说明.md` | 为何资料库不全文抄 SYNC hex |
| 11 | `学习推送/加餐_频率带宽与调制解调.md` | 若 12.5 kHz / 4FSK 仍糊 |

官方版本锚点：**Part1 V2.7.1**；**TR V1.5.1**。冲突规则：**TS > TR > 手册/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 11. 下一课预告

**第 20 课 · Colour Code 与同频系统**

本课站住了 Traffic 中心那 48 bit：Voice / Data 图案分壳，BS / MS / DM 分册，首突发与疏密有数。下一课钻进「同频怎么不搅成一锅」：**Colour Code（色码）** 出现在哪里（Slot Type / EMB 等）、和 SYNC 成功有何不同、写频与现场串台如何对照。仍少公式，多对照「SYNC ≠ Colour Code ≠ CACH」。

---

## 12. 推荐阅读与视频

本课外链为 **2026-09-27**（晚间推送）检索核验；**不编造地址**。策略 = **Part1 SYNC 原文 + TR 导读 + Wavecom/Guido 帧文 + VK4PK 时间参数 + GopherTrunk SYNC 专文 + 中文科普（带冲突声明）**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **4.3** 专讲 SYNC 用途、语音/数据不同图案、入/出站不同图案、疏密与**首突发必须 SYNC**；clause **9.1.1** 与 Tables **9.1–9.2** 给类别与（PDF 内）比特图案——**请在 PDF 内查 hex，不要从课文抄全表**。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)（部分网络可能间歇拦截，可用协会镜像）。  
   - **适合哪一段**：第 2、4、5、7、10 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读用同样的「中心同步场 / 语音与数据不同 SYNC」叙事，比纯条款好读；突发长度 264/24/96 也便于和本课账本对账。  
   - **适合哪一段**：第 2、7、10 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[GopherTrunk｜DMR End to End, Part 2: Bursts, Sync Words & Polarity](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-02-bursts-sync-polarity/)**  
   - **为什么值得看**：少见的 **SYNC 专篇**：九类 48-bit 图案、相关检测、语音/数据在极性翻转下的「孪生」关系、以及为何 SYNC 匹配后还要靠 Slot Type / FEC 仲裁——和本课「互补直觉 + 分壳」同向，并可作进阶阅读。  
   - **适合哪一段**：第 4.2、4.3、6、8 节后对照。  
   - **注意**：实现/开源解码向深潜；术语与极性细节以帮助理解为限，**硬图案与条款以 Part1 V2.7.1 为准**；文中若出现具体 hex，请回到官方 Table 9.2 核对，勿当唯一真源。  
   - **基础**：中级～进阶；英文网页。

4. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：突发与帧结构图把中心 SYNC/嵌入位置画清楚，便于和本课总图、语音/数据壳对照。  
   - **适合哪一段**：第 2、6 节。  
   - **注意**：厂商/分析仪向综述；个别术语口误勿盲从；**以 ETSI 为准**。  
   - **基础**：中级；英文 PDF。

5. **[Alessandro Guido｜How DMR Works — Conventional Tier 2（PDF）](https://www.qsl.net/kb9mwr/projects/dv/dmr/How%20DMR%20Works%20Conventional%20Tier%202.pdf)**  
   - **为什么值得看**：常规 Tier II 口吻串起突发、同步与帧结构，适合在学完类别表后做「整页复盘」。  
   - **适合哪一段**：第 4、6、7 节后对照。  
   - **注意**：培训文年代可能早于现行 Part1 V2.7.1；**硬条款以 V2.7.1 为准**。  
   - **基础**：入门～中级；英文 PDF。

6. **[VK4PK｜DMR Signal Processing Notes](https://lyonscomputer.com.au/MMDVM/DMR-Signal-Processing-Notes/DMR-Signal-Processing-Notes.html)**  
   - **为什么值得看**：一页把 264 / 108+48+108 / 4FSK / 4800 baud 写在一起，方便确认「SYNC 仍在同一物理水管里」。  
   - **适合哪一段**：第 2.4、7 节；巩固调制弱项。  
   - **基础**：入门～中级；英文网页；业余/MMDVM 笔记，**规范数字仍以 ETSI 为准**。

7. **[科讯｜DMR 对讲机数字协议详解](http://www.cqkexun.com/service/problem/hand/292.html)**  
   - **为什么值得看**：中文建立「时隙 / 突发 / 同步」第一印象；可读作本课之前的语感热身。  
   - **适合哪一段**：第 2–3 节。  
   - **注意**：科普文版本偏旧；SYNC 类别与疏密细节**以 ETSI TS 为准**。  
   - **基础**：入门；中文。

8. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：协会培训向总图；可与第 17 课嵌入/迟后进入连读，帮助把「Voice SYNC 上车点」嵌回业务全景。  
   - **适合哪一段**：读完本课想回看超帧与嵌入边界时。  
   - **注意**：不是 SYNC 专章；幻灯版本锚点可能早于现行 Part1。  
   - **基础**：入门～中级；英文 PDF。

**说明（视频）**：公开检索未找到专门把 **「Traffic 中心 48 bit：Voice/Data SYNC 图案分壳；BS/MS/DM 分册；逐符号互补与相关峰；首突发必须 SYNC；语音 ~360 ms / 数据更密；SYNC ≠ CC ≠ CACH」** 讲透的独立高质量中文/英文短片（多数入门视频只口播「有同步字」或厂商产品介绍；实现向材料多为源码/博客而非课堂视频）。本课**未找到合适公开视频**。建议用：**Part1 clause 4.3 + 9.1.1（Table 9.2 只在 PDF 查）+ GopherTrunk SYNC 专文 + Wavecom/Guido 帧图 + 资料库 §6** 对照自学。

---

*推送说明：本课为阶段 C「SYNC：语音/数据如何区分」。频谱/调制仅保留短提醒（SYNC 不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、中心 48 总图、术语、图案类别（无 Table 9.2 hex 全文）、互补直觉、首突发与疏密、现场对照、五则工作例子、数字账本、十则误区、八题自测、资料库路径与八条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「为何分析仪有 Voice/Data SYNC、Header 为何挂 Data SYNC、同步不上如何与 CC/CACH 分诊、264/48/24/96 如何分柜」，并进入第 20 课 Colour Code。*
