## 8. 数字账本

| 量 | 值 / 关系 | 别和谁混 |
|----|-----------|----------|
| CSBK 信息 PDU | **96** bit（外壳+CRC 叙事） | ≠ 264 突发；≠ 196 Info 码字 |
| Octet0 | LB**1** + PF**1** + CSBKO**6** | ≠ Full 的 PF\|R\|FLCO |
| FID | **8** bit | ≠ 地址 24 |
| CSBK Data | **64** bit（Octet2–9） | ≠ Full Data 56；≠ Short Data 24 |
| CSBK CRC | **16** bit，CRC-CCITT | B.3.8；≠ RS24 / CRC8 / CS5 |
| Data Type CSBK | **`0011`** | MBC H **`0100`**；MBC C **`0101`** |
| SLOT | **20** = CC4+DT4+Golay12 | 语音无 SLOT |
| 典型载荷 FEC | **BPTC(196,96)** | 名称；矩阵见原文 / 第 24 课原则 |
| CSBKO / FLCO / SLCO | 6 / 6 / **4** | 三张表 |
| 时隙 / 超帧 | 30 ms / 360 ms | CSBK 不改 TDMA 节拍 |
| 带宽/调制 | 12.5 kHz + 4FSK≈4800 baud / 9.6 kbps | CSBK **不改变**二者 |

分柜口诀：

```text
办手续外壳 …… CSBK（LB|PF|CSBKO|FID|64|CRC16）→ Data Type 0011
话务门牌 ……… Full LC（第 22 课）
缝里短广播 … Short LC → CACH
运货标签 ……… EMB 16 / SLOT 20
多块亲戚 ……… MBC（0100/0101 + LB）
下一课 ……… FEC 原则（不贴矩阵）
```

---

## 9. 常见误区（10 则）

1. **「CSBK 就是控制用的 Full LC / 短 LC。」** → 否。不同 PDU、不同 Opcode 表、不同 CRC、不同运载。  
2. **「FLCO 和 CSBKO 都是 6 bit，数值能通用。」** → 否。例如 `000100` 在两表语义不同。  
3. **「CSBK 嵌在语音超帧 B–E 里。」** → 否。CSBK 走数据壳 + Slot Type；B–E 嵌的是 Full LC 类碎片。  
4. **「CACH 上的 Act_Updt 就是 CSBK。」** → 否。那是 Short LC（SLCO）。  
5. **「LB=1 表示通话结束。」** → 否。LB=Last **Block**（本控制块是否末块）。  
6. **「只有 Tier III 才有 CSBK。」** → 片面。Tier III 大量用；Part2 常规同样定义唤醒/个呼请求/前导等 CSBK。  
7. **「看见 Data Type=CSBK 就可以不管 FID。」** → 否。仍先 FID 后 CSBKO（第 14 课）。  
8. **「CRC 失败一定是天线坏了。」** → 先分：色码门、SYNC 壳、BPTC/CRC 哪一层；也可能是类型解错。  
9. **「改 CSBK 会换 12.5 kHz 或 4FSK。」** → 否。  
10. **「EMB/SLOT 里已经有控制信息，等于读完 CSBK。」** → 否。小报头只告诉你「有哪种单据 / 哪色码」；正文在 96 bit PDU 里。

---

## 10. 自测（8 题）

**题 1.** 用一句话说明 CSBK 与 Full LC 的分工。为什么说「不是同一种控制」？

<details><summary>简答</summary>

Full LC 是话务呼叫门牌正文（谁找谁）；CSBK 是控制事务外壳（请求/应答/唤醒/前导等）。PDU 布局、Opcode 表、CRC、典型 Data Type 均不同——不能互相替代。

</details>

**题 2.** 写出 CSBK 八位组外壳（含 CRC 名称），并写出单块时 LB 应取何值。

<details><summary>简答</summary>

`[LB|PF|CSBKO][FID][Data 64][+CRC-16 CRC-CCITT]`。单块 CSBK → **LB=1**。

</details>

**题 3.** CSBK 走语音壳还是数据壳？依赖什么小报头？Data Type 学习编码是什么？

<details><summary>简答</summary>

走**数据/控制突发**；依赖 **Slot Type**；Data Type CSBK=`0011`（MBC Header=`0100`，Continuation=`0101`）。语音突发无 Slot Type。

</details>

**题 4.** 对照解释：FLCO ≠ CSBKO ≠ SLCO。各举一个学习用别名。

<details><summary>简答</summary>

FLCO（Full LC）如 Grp_V_Ch_Usr；CSBKO（CSBK）如 UU_V_Req / BS_Dwn_Act；SLCO（Short LC）如 Act_Updt。宽度 6/6/4，表不同；同数值不可跨表翻译。

</details>

**题 5.** 个呼存在性检查的典型 CSBK 顺序是什么？之后才出现哪类 Full LC？

<details><summary>简答</summary>

UU_V_Req → UU_Ans_Rsp（或 NACK_Rsp）；通过后再见 Voice LC Header 等，FLCO 为 UU_V_Ch_Usr 类门牌。

</details>

**题 6.** Pre_CSBK 解决什么现场问题？CBF 计数含不含当前 preamble 块？

<details><summary>简答</summary>

给扫描/睡眠台「敲窗户」，提高后续非语音投递成功率。CBF = 后续块数，**不含**当前 preamble 块（Part2 精神）。

</details>

**题 7.** 现场「博客说只有集群才有 CSBK，但抓包在常规中继上也看到 CSBK」——如何用本课回答？

<details><summary>简答</summary>

外壳家族在常规与集群都会用：Part2 已定义 BS_Dwn_Act、UU_V_Req、Pre_CSBK 等；Tier III（Part4）是更大规模地复用该外壳做 grant/注册等。博客常把「CSBK」口语绑定到控制信道场景，不能否定常规 CSBK。

</details>

**题 8.** 为什么说「解错 CSBK ≠ 没解调出 4FSK」？分诊应先看哪三层？

<details><summary>简答</summary>

射频/调制仍是 12.5 kHz + 4FSK；CSBK 是数据壳上的单据。分诊：① SYNC/壳；② SLOT 的 CC+Data Type；③ FID→CSBKO→CRC16/Data64。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `01-空中接口/CSBK与LC字段详表.md` **§6** | Table 9.9 外壳；LB/CSBKO；MBC 一句；CRC 名 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§3 Data Type、§7.5 CSBK、§8 Table 9.22** | 数据突发；CSBK/MBC 编码；与语音壳对照 |
| 3 | `02-语音业务/语音业务字段速览.md` **§1.2、§2、§4** | CSBKO 表；呼叫阶段对照；六种常见 CSBK PDU 字段 |
| 4 | `学习推送/第14课.md` | FID 门牌；FLCO/CSBKO 分表 |
| 5 | `学习推送/第21课.md` | EMB/SLOT；Data Type 路由 |
| 6 | `学习推送/第22课.md` | Full/Short LC；与本课对照入口 |
| 7 | `01-空中接口/跳过项原则说明.md` + 本课数字账本 | FEC **名称**级；不贴矩阵 |
| 8 | 官方 **TS 102 361-1 V2.7.1** clause **7.2、9.1.8、9.3.31–9.3.32**；Table **9.9、9.22**；Annex **B.3.8、B.1.1** | 原文；冲突以 PDF 为准 |
| 9 | 官方 **TS 102 361-2**（本库 `02-语音业务/TS102361-2_V2.5.1.pdf`）clause **7.1.2**、Annex **B.2** | CSBKO 业务体；勿用 Part1 冒充 |
| 10 | **TR 102 398** | 概念导读，**不是**替代 TS |
| 11 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍怀疑「CSBK 会换调制」 |

官方版本锚点：**Part1 V2.7.1**；语音/控制业务体以本库 **Part2** PDF 为准；集群控制体例见 **Part4**（本课仅预告）。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 12. 下一课预告

**第 24 课 · FEC 原则（不贴矩阵）**

本课站住了控制外壳：**CSBK**（LB|PF|CSBKO|FID|Data64|CRC16）与 **MBC** 家族、和 Full/Short LC 的分工，并钉死 Data Type 路由与「常规也有 CSBK」。下一课把一路上反复出现的名字——**BPTC(196,96)、Golay、QR、RS、CRC-CCITT、5-bit CS…**——收成「原则课」：各自保护谁、失败时现场怎么分诊；**不粘贴生成矩阵**，只建立正确的纠错/检错地图。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-29**（晚间推送）检索核验；真实打开过内容页/PDF（HTTP 200 或协会镜像可用）；**不编造地址**。策略 = **Part1 CSBK 原文 + Part2 业务体 + TR 导读 + GopherTrunk CSBK/解码器深文 + Tier II/III 对照（并纠正「仅集群才有 CSBK」的口语简化）+ Wavecom/培训 PDF 帧图**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **7.2** 讲 CSBK / MBC 消息结构；**9.1.8** 与 Table **9.9** / figure **7.8** 定义外壳；**9.3.31–9.3.32** 钉 LB/CSBKO；Table **9.22** 钉 Data Type。  
   - **备链**（部分网络对 etsi.org 直链可能 403，以协会镜像为准）：`https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf`。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TS 102 361-2 V2.5.1｜Voice services（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：Annex **B.2** CSBKO 表；clause **7.1.2** 展开 BS_Dwn_Act / UU_V_Req / UU_Ans_Rsp / NACK / Pre_CSBK / CT_CSBK 字段——本课 §4.5–4.6 的原文。  
   - **备链**：`https://dmrassociation.org/downloads/standards/ts_10236102v020501p.pdf`。  
   - **适合哪一段**：第 4、6、7、11 节。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读里对控制/链路信令的叙事比纯条款好读，便于和本课「办手续 vs 贴门牌」对账。  
   - **适合哪一段**：第 2、7、11 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

4. **[GopherTrunk｜CSBK（词条）](https://gophertrunk.org/reference/csbk/)**  
   - **为什么值得看**：用一页把「96-bit 控制块 + CSBKO + FID + BPTC/CRC + Preamble CSBK + Tier III grant 场景」串起来——本课总图的英文对照。  
   - **适合哪一段**：第 2、4、7 节。  
   - **注意**：词条叙述偏 **Tier III 控制信道**；**不要**读成「常规没有 CSBK」——以 Part2 为准（本课 §4.7、误区 6）。  
   - **基础**：入门～中级；英文网页。

5. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：明确 Data Type 分支点包含 **CSBK**；BPTC(196,96) 保护控制/LC；语音突发无 Slot Type——和第 21 课、本课运载钉子同向。  
   - **适合哪一段**：第 4、5、8 节。  
   - **注意**：校验命名以 ETSI Annex B 为准。  
   - **基础**：中级～进阶；英文网页。

6. **[GopherTrunk｜DMR Tier II & Tier III（对照页）](https://gophertrunk.org/learn/digital-trunking/dmr-tier-2-3/)**  
   - **为什么值得看**：帮助建立「集群控制信道上 CSBK 流」的直觉；同时用本课纠正：Tier II 常规仍有 Part2 控制 CSBK。  
   - **适合哪一段**：第 4.7、6、7、9 节。  
   - **注意**：监测产品叙事 ≠ 规范穷尽表；**互操作与字段以 ETSI 为准**。  
   - **基础**：入门～中级；英文网页。

7. **[GopherTrunk｜Control-channel signaling（概念）](https://gophertrunk.org/learn/digital-trunking/control-channel-signaling/)**  
   - **为什么值得看**：把 P25 TSBK 与 DMR CSBK 对照成「短而带类型的控制块流」——方便向同事打比方（仍须回到 DMR 自己的 Data Type/CSBKO）。  
   - **适合哪一段**：第 2、12 节热身。  
   - **注意**：跨体制类比，细节以 DMR TS 为准。  
   - **基础**：入门；英文网页。

8. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：帧/突发/超帧图，便于把「数据壳 + Slot Type」钉回 264 结构，避免在语音壳里找 CSBK。  
   - **适合哪一段**：第 2、4、7 节。  
   - **注意**：厂商综述，版本锚点可能早于 V2.7.1；**硬条款以现行 Part1 为准**。  
   - **基础**：中级；英文 PDF。

9. **[Alessandro Guido｜How DMR Works — primer PDF（hamgear）](https://hamgear.files.wordpress.com/2014/02/dmr-primer.pdf)**  
   - **为什么值得看**：培训幻灯式回顾控制/LC/FEC/CRC 名称——和本课数字账本、下一课 FEC 原则同向。  
   - **适合哪一段**：第 8、11、12 节后复盘。  
   - **注意**：年代偏早、版本号旧；**以 V2.7.1 / 本库 Part2 为准**。  
   - **基础**：入门～中级；英文 PDF。

10. **[GopherTrunk｜DMR End to End Part 5：Link Control & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
    - **为什么值得看**：用「门牌/嵌入」故事反衬本课：读完 CSBK 手续后，话务仍要回到 Full LC 路径——和 §4.6 分工表对读。  
    - **适合哪一段**：第 4.6、5、7 节。  
    - **注意**：实现向细节是工程选择；规范语义以 ETSI 为准。  
    - **基础**：中级～进阶；英文网页。

**说明（视频）**：公开检索未找到专门把 **「CSBK 外壳 LB|PF|CSBKO|FID|Data64|CRC16；Data Type 0011 vs MBC；CSBKO≠FLCO≠SLCO；常规 Part2 CSBK vs Tier III 复用；与 Full/Short LC 分工」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只演示写频、集群跟控界面或产品抓包，不拆 PDU 外壳）。本课**未找到合适公开专题视频**。建议用：**Part1 Table 9.9 + Part2 §7.1.2 + GopherTrunk CSBK 词条 + 资料库 §6 / 语音业务速览 §4** 对照自学。

---

*推送说明：本课为阶段 C「CSBK 控制信令块」。频谱/调制仅保留短提醒（CSBK 不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、办手续总图、术语、Table 9.9 外壳与 LB/MBC、数据壳运载与 Data Type、FID/CSBKO 门牌、Part2 常见 CSBKO 摘要、与 Full/Short LC 分工与对照、现场分诊、五则工作例子、数字账本、十则误区、八题自测、资料库路径与十条核验外链（并诚实标明未找到合适公开专题视频；纠正「仅集群才有 CSBK」的口语简化）。读完应能向同事讲清「CSBK 为何不是 LC、单块 LB 怎么读、个呼前手续与话务门牌如何衔接、为何不能在语音嵌入里找 CSBKO」，并进入第 24 课 FEC 原则（不贴矩阵）。*
