## 11. 自测（闭卷先想，再对答案）

1. **填空**：电信习惯下，业务分 ______（承载）、______（电信业务）、______（补充业务）；互操作门牌预告是 ______ / ______ / ______（第 14 课）。  
2. **选择**：Service Options 中 Broadcast=1 适用于？  
   - A. 仅个呼  
   - B. 仅组呼  
   - C. 个呼与组呼都行  
   - D. 仅数据 PDP  
3. **判断**：Tier III 短数据只能走业务信道 PDP。（对 / 错）  
4. **连线**：  
   - Grp_V_Ch_Usr FLCO → ?  
   - UU_V_Ch_Usr FLCO → ?  
   - Talker Alias FLCO 范围 → ?  
   - GPS_Info FLCO → ?  
5. **排序**：把语音过程排成时间线：Voice LC Header；Terminator with LC；可选 BS_Dwn_Act；语音超帧 A–F；可选 UU_V_Req/Ans。  
6. **简答**：为什么说「短数据状态码不应到 Service Options 里找」？请用两句话说明该翻哪本书、DPF 家族大概是什么。

### 参考答案

1. **Bearer；Tele-service；Supplementary；SFID；MFID；FLCO。**  
2. **B。**  
3. **错。** Tier III 控制信道有自有短数据业务；业务信道亦可走 PDP。  
4. **000000；000011；000100–000111；001000。**  
5. **可选 BS_Dwn_Act → 可选 UU_V_Req/Ans → Voice LC Header → 超帧 A–F → Terminator with LC。**  
6. **状态/预编码短数据属 Part3（短数据头，DPF 常为 1110 家族）；Service Options（Part2 Table 7.11）管紧急/广播/OVCM/优先级等语音加料，不管预编码状态表。**

---

## 12. 资料库加深阅读

按「先手册分类、再语音速览、再数据速览、再官方 PDF」：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `DMR整合学习手册.md` **§5** | Bearer / Tele / Supplementary + Tier 数据对照（本课骨架） |
| 2 | `02-语音业务/语音业务字段速览.md` | FLCO/CSBK、过程阶段、Service Options Table 7.11 |
| 3 | `03-数据协议/数据协议字段速览.md` | DPF/SAP、确认/非确认头、短数据三头 |
| 4 | `00-入门/DMR术语与帧结构速查卡.md` | 突发、超帧、墙上词热身 |
| 5 | `学习推送/第07课.md` | 寻址直觉：个呼/组呼（本课语音前置） |
| 6 | `学习推送/第12课.md` | 分层 L1/L2/L3（本课「种类之上还要分层」） |
| 7 | `学习推送/加餐_频率带宽与调制解调.md` | 弱项加餐；业务症状背后的 L1 |
| 8 | `总索引.md` | 关键词→文档 |
| 9 | `02-语音业务/TS102361-2_V2.5.1.pdf` | 官方 Part2；对照 clause 5–6、Service Options |
| 10 | `03-数据协议/TS102361-3_V1.3.1.pdf` | 官方 Part3；先读目录与概述再下钻 |
| 11 | `DMR协议学习导航.md` | 版本表与官方链接入口 |

官方版本锚点：**TR V1.5.1**；**Part1 V2.7.1**；**Part2 V2.5.1**；**Part3 V1.3.1**；**Part4 V1.12.1**。冲突：**TS > TR > 手册笔记**。

---

## 13. 推荐阅读与视频

本课外链为指定核验清单（2026-09-24）；**不编造地址**。策略 = **中文业务综述 + TR clause 6 + Part2/Part3 正文 + Tait 呼叫类型课 + 产业白皮书**。

1. **[什么是数字对讲机？DMR 数字无线通信原理（海川通）](https://www.hacton.com/newsinfo/1174391.html)**  
   - **为什么值得看**：中文业务综述，覆盖单呼/组呼/全呼、迟后进入、短数据/IP 等直觉。  
   - **适合哪一段**：第 2–7 节。  
   - **注意**：厂商科普；**冲突以 ETSI TS 为准**。  
   - **基础**：入门；中文。

2. **[ETSI TR 102 398 V1.5.1｜DMR General System Design](https://www.etsi.org/deliver/etsi_tr/102300_102399/102398/01.05.01_60/tr_102398v010501p.pdf)**  
   - **为什么值得看**：clause **6 Services Overview** 权威导读（语音/数据分类总览）。  
   - **适合哪一段**：第 2、8 节后作对照。  
   - **基础**：进阶；英文 PDF；本课先读 clause 6，不必一次读完全文。

3. **[ETSI TS 102 361-2 V2.5.1｜Part 2 语音与通用业务](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/02.05.01_60/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：语音过程与补充业务规范正文；Service Options 终审文本。  
   - **适合哪一段**：第 5–6 节后精读 clause 5–6 / Table 7.11。  
   - **基础**：进阶；收藏。

4. **[ETSI TS 102 361-3 V1.3.1｜Part 3 数据协议](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236103/01.03.01_60/ts_10236103v010301p.pdf)**  
   - **为什么值得看**：PDP / 短数据 / IP 权威定义。  
   - **适合哪一段**：第 7 节后先读目录与概述，再下钻确认/非确认与短数据。  
   - **基础**：进阶；英文 PDF。

5. **[Introduction to DMR｜Tait Radio Academy（Call Types and Features）](https://www.taitradioacademy.com/courses/introduction-to-digital-mobile-radio/)**  
   - **为什么值得看**：英文结构化课；Lesson 4 专讲呼叫类型与特性，和本课语音/补充地图同频。  
   - **适合哪一段**：第 5–6 节；通勤复习。  
   - **基础**：入门；英文课程/视频。

6. **[DMR Association｜Benefits and Features of DMR White Paper](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：产业白皮书列举 Late Entry、Talking Party ID、数据应用等，适合建立「特性清单」语感。  
   - **适合哪一段**：第 6–7 节；与 TS 对照着看。  
   - **注意**：版本可能偏旧；**细节以最新 TS 为准**。  
   - **基础**：入门～进阶；英文 PDF。

**说明**：专门只讲「DMR 业务分类」的优质长篇中文视频不好找；本课用 **中文综述 + TR/TS + Tait 课程** 补充。业务边界、Service Options 与 DPF 以本课与语音/数据字段速览、ETSI TS 为准。

---

## 14. 下一课预告

**第 14 课 · 互操作：SFID / MFID / FLCO**

你已经能说出：业务按 Bearer / Tele-service / Supplementary 分类；语音个呼/组呼等走 Part2，补充加料看 Service Options 与 Late Entry/别名等；数据看 Part3 的 PDP/短数据/IP，集群控制信道短数据还要看 Part4。下一课会把「特性怎么在空口上被认出、标准与厂商如何共存」钉死——**SFID、MFID、FLCO** 是互操作的门牌与功能码，仍然少公式，多现场对照：为什么同频同色码仍可能「各说各话」。

---

*推送说明：本课为阶段 B「业务全景：语音 / 数据 / 补充业务」专课。不加长篇频率加餐，只保留一句指向加餐文的提醒，并点明坏射频常表现为语音/数据失败。主文加厚覆盖动机、餐厅/快递总图、术语、现场对照、语音过程与 OACSU、补充业务与 Service Options 8 bit 表、数据 PDP/短数据/Tier 差异、书架映射、正反例、误区、自测与六条核验外链。读完应能向同事讲清「用户要的是哪类业务、该翻 Part2 还是 Part3/4」，并为第 14 课 SFID/MFID/FLCO 打好业务全景地基。*
