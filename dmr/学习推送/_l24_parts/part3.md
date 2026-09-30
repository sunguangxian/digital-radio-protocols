（第24课 · 推送 part 3/3）

## 9. 常见误区（10 则）

1. **「CRC fail = 天线坏了。」** → 否。先分层：SYNC/CC/短码/块 FEC/Mask/CRC，最后才是 RF。  
2. **「FEC 和 CRC 是同一种东西。」** → FEC 侧重纠错冗余；CRC 侧重检错。DMR 里两者常叠用。  
3. **「所有数据都走 BPTC(196,96)。」** → ¾ 走 Trellis；Rate1 几乎不编；嵌入/CACH 走变长 BPTC。  
4. **「EMB 和 SLOT 用同一种短码。」** → EMB=QR，SLOT=Golay，TACT=Hamming。  
5. **「Header 与嵌入 Full LC 校验长度一样。」** → Header/Term 是 RS24；嵌入是 CS5。  
6. **「Idle 也应有 CRC。」** → Table B.1：Idle **无** checksum、无 Mask。  
7. **「分析仪 BPTC fail 就要去背矩阵。」** → 先查 Data Type 是否选错解码档案。  
8. **「Rate1 = 完全没有校验。」** → 无**块 FEC**；确认路径仍可有 CRC-9 / CRC-32。  
9. **「Data Type CRC Mask 改的是 PDU 业务字段。」** → 掩的是 **CRC 场**；且收发必须同一掩码。  
10. **「本课应把 Annex B 矩阵抄进笔记。」** → **禁止**。原则 + 名称 + 挂点即可；矩阵回 PDF。

---

## 10. 自测（8 题）

**题 1.** 用一句话讲清本课核心口诀（寄包裹）。

<details><summary>参考答案</summary>
FEC/CRC 是「寄包裹先贴胶带、再按规则打散装箱」：组 PDU → 算校验 →（部分）Mask → 块 FEC → 交织入突发 → 中心场另加短码；永不背生成矩阵。
</details>

**题 2.** 写出 B.0 处理链的 6 步顺序（不含调制）。

<details><summary>参考答案</summary>
① 组 PDU ② 算校验(CRC/RS/CS) ③ Data Type CRC Mask（若适用）④ 块 FEC ⑤ 交织入突发 ⑥ 中心场另加 Golay/QR/Hamming。
</details>

**题 3.** BPTC(196,96)、Trellis ¾、Rate 1 各主要护哪类载荷？

<details><summary>参考答案</summary>
BPTC：多数控制/头/Idle/½ 数据；Trellis：Rate ¾ 数据；Rate1：几乎无块 FEC 的高吞吐数据（仍可能有 CRC-9/32）。
</details>

**题 4.** EMB、SLOT、TACT 各用什么短码？信息比特大约多少？

<details><summary>参考答案</summary>
EMB：QR(16,7,6)，7 信息；SLOT：Golay(20,8)，8 信息；TACT：Hamming(7,4)，4 信息。
</details>

**题 5.** Voice LC Header 与嵌入 Full LC 的校验名有何不同？为什么？

<details><summary>参考答案</summary>
Header/Terminator：RS(12,9)→24 bit；嵌入：5-bit CS。运载路径与比特预算不同——整包走数据壳 BPTC，嵌入拆四片走变长 BPTC。
</details>

**题 6.** Idle 有没有 CRC？有没有 BPTC？

<details><summary>参考答案</summary>
无 CRC、无 Mask；有 BPTC(196,96)。用于占空/保活，不是用户数据。
</details>

**题 7.** 现场看到「BPTC fail」，第一步应查什么？

<details><summary>参考答案</summary>
先核对 SLOT 的 Data Type 是否本应按 BPTC 解（会不会其实是 ¾ Trellis / Rate1）；同时确认 SYNC 壳与 CC。不要先背矩阵或先拆天线。
</details>

**题 8.** CSBK 的校验与块 FEC 顺序是什么？

<details><summary>参考答案</summary>
先算 CRC-CCITT 16 →（按规则 Mask）→ 再 BPTC(196,96) 入数据突发；SLOT 另用 Golay 护 CC+Data Type。
</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `01-空中接口/跳过项原则说明.md` **§1** | **本课 canonical**：Annex B 挂法；故意不抄矩阵 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§11** | FEC/CRC 名称索引 |
| 3 | `01-空中接口/CSBK与LC字段详表.md` **§9** | FEC 名称速查；与外壳对照 |
| 4 | `学习推送/第21课.md` | EMB QR / SLOT Golay / Data Type |
| 5 | `学习推送/第22课.md` | RS24 vs CS5；Short CRC8 + 变长 BPTC |
| 6 | `学习推送/第23课.md` | CSBK CRC16 + BPTC；与本课例子 A 对读 |
| 7 | `01-空中接口/AnnexCDE_时序Idle比特序.md` | Idle/Null 原则短注（不 dump 比特） |
| 8 | 官方 **TS 102 361-1 V2.7.1** Annex **B**（尤其 B.0、B.1.1、B.2、B.3.1–B.3.13、B.4.1） | 原文；矩阵/多项式只在实现时查 PDF |
| 9 | **TR 102 398** | 系统设计导读，**不是**替代 TS |
| 10 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把 CRC fail 当成「调制坏了」 |

官方版本锚点：**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。矩阵、多项式系数、Idle 96-bit、E.1–E.12：**永远回 PDF**，本库不补第二份。

---

## 12. 下一课预告

**第 25 课 · 语音呼叫过程直觉**（阶段 D · 语音与数据 开篇）

本课收官了阶段 C：把空口上反复出现的保护名字收成一张**原则地图**——谁护中缝、谁护单据、谁护整舱；并钉死「失败要分层、矩阵永不背」。下一课离开「字段积木」，进入**一次语音呼叫怎么从请求走到语音超帧再走到 Terminator** 的过程直觉：把第 17（超帧）、21（EMB/SLOT）、22（Full LC）、23（CSBK 手续）串成一条时间线。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-30**（早间推送）检索核验；真实打开过内容页/PDF（HTTP 200 或协会镜像可用）；**不编造地址**。策略 = **Part1 Annex B 原文（协会镜像）+ TR 导读 + Wavecom/hamgear 帧与名称回顾 + GopherTrunk 突发/解码器深文 + 原则级 FEC/CRC/Hamming 优质通识（含一条已核验的优秀公开视频）**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：Annex **B** 是本课一切名称的原文锚点——B.0 总序、B.1.1 BPTC、B.2 变长/Trellis/Rate1、B.3 短码与 CRC 族、B.3.12 Mask、B.4.1 CACH 交织。学习时**只读条款标题与叙述顺序**，矩阵表留给实现。  
   - **备链**（部分网络对 etsi.org 直链可能 403，以协会镜像为准）：`https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf`。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读里对信道编码/链路保护的叙事比纯 Annex 好读，便于和本课「胶带+打散装箱」对账。  
   - **适合哪一段**：第 2、6、11 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：帧/突发/超帧图，帮助把「196 Info + 中心短场」钉回 264 结构，避免把 FEC 想像成另开一条射频。  
   - **适合哪一段**：第 2、5、7 节。  
   - **注意**：厂商综述，版本锚点可能早于 V2.7.1；**硬条款以现行 Part1 为准**。  
   - **基础**：中级；英文 PDF。

4. **[Alessandro Guido｜How DMR Works — primer PDF（hamgear）](https://hamgear.files.wordpress.com/2014/02/dmr-primer.pdf)**  
   - **为什么值得看**：培训幻灯式回顾控制/LC/FEC/CRC **名称**——和本课术语表、数字账本同向。  
   - **适合哪一段**：第 3、8、11 节后复盘。  
   - **注意**：年代偏早；**以 V2.7.1 / 本库原则说明为准**。  
   - **基础**：入门～中级；英文 PDF。

5. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：明确 Data Type 分支、BPTC 保护控制/LC、语音突发无 Slot Type——和第 21 课及本课「选错解码档案 → 假 BPTC fail」同向。  
   - **适合哪一段**：第 5、6、7 节。  
   - **注意**：校验命名以 ETSI Annex B 为准。  
   - **基础**：中级～进阶；英文网页。

6. **[EcrioniX｜Forward Error Correction（Hamming / RS 等原则）](https://ecrionix.org/digital-electronics/fec/)**  
   - **为什么值得看**：用通识语言讲清「FEC 为何加冗余、距离与可纠个数」——帮助弱基础同事建立「胶带厚度」直觉，而不陷入 DMR 矩阵。  
   - **适合哪一段**：第 1、3、9 节热身。  
   - **注意**：通识文 **不是** DMR 规范；落到场名仍回 Annex B / 本课 §4。  
   - **基础**：入门；英文网页。

7. **[KnowledgeGate｜DLL Error Control：CRC and Hamming](https://www.knowledgegate.ai/blog/dll-error-control-computer-networks-complete-guide)**  
   - **为什么值得看**：把「CRC 偏检错、Hamming 偏纠错、ARQ vs FEC」对照讲清——正好支撑本课「CRC fail ≠ 没 FEC」。  
   - **适合哪一段**：第 3、6、9 节。  
   - **注意**：计算机网络教材语境；DMR 叠用方式以本课为准。  
   - **基础**：入门～中级；英文网页。

8. **[solderic｜CRC vs Hamming Code](https://solderic.com/communication/hamming-code-vs-crc)**  
   - **为什么值得看**：短文对照「检错胶带 vs 纠错格子」——给同事做 3 分钟口头解释时好用。  
   - **适合哪一段**：第 3、9 节。  
   - **注意**：通识；不替代 Annex B 挂点表。  
   - **基础**：入门；英文网页。

9. **[Wikipedia｜Hamming code](https://en.wikipedia.org/wiki/Hamming_code)**  
   - **为什么值得看**：权威通识入口，帮助理解 BPTC 行列为何反复出现 Hamming 积木名。  
   - **适合哪一段**：第 4.1、4.3 节旁证。  
   - **注意**：不讲 DMR 交织；**实现以 ETSI 为准**。  
   - **基础**：入门；英文。

10. **[Wikipedia｜Cyclic redundancy check](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)**  
    - **为什么值得看**：CRC 检错直觉与多项式故事的标准入口——本课**不抄 G(x)**，需要系数时用百科建立语感后回 PDF。  
    - **适合哪一段**：第 4.5、6 节。  
    - **注意**：通用 CRC ≠ 某一 DMR 初值/掩码；掩码表回 Annex B.3.12。  
    - **基础**：入门；英文。

11. **[3Blue1Brown｜But what are Hamming codes?（YouTube）](https://www.youtube.com/watch?v=X8jsijhllIA)**  
    - **为什么值得看**：目前公开检索到的、讲解质量最高的 **Hamming / 纠错码起源** 可视化视频之一；帮助建立「冗余如何换可纠能力」的几何直觉，与本课「永不背矩阵、先懂原则」完全同向。  
    - **适合哪一段**：第 1、3、4.1、4.3 节前后。  
    - **注意**：**不是** DMR 专题——不会讲 BPTC/Trellis/Data Type Mask；看完必须回到本课 §4 挂点表。  
    - **基础**：入门；英语视频（可开字幕）。

**说明（视频）**：公开检索**未找到**专门把 **「DMR Annex B：BPTC(196,96)/变长 BPTC/Trellis/Rate1 + Golay/QR/Hamming 挂场 + Data Type CRC Mask 收发顺序」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只演示写频、声码或产品抓包）。本课采用折中：收录一条已核验的优秀通识视频（3Blue1Brown · Hamming），并诚实标明 **DMR 专题 FEC 视频未找到**（`video_found=true` 指「有优质可用视频」，但是通识而非 DMR Annex B 专题）。建议用：**原则说明 §1 + Part1 Annex B 目录 + 本课对照表 + GopherTrunk 解码器文** 对照自学。

---

*推送说明：本课为阶段 C「FEC 原则（不贴矩阵）」收官课。频谱/调制仅保留短提醒（FEC 不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、寄包裹总图与 B.0 处理链、术语、BPTC/变长 BPTC/中心短码/Trellis/Rate1/CRC 族挂点、第 16–23 课映射表、现场分层分诊、六则工作例子、数字账本、十则误区、八题自测、资料库路径与核验外链（含一条优秀通识 Hamming 视频；诚实标明无 DMR Annex B 专题视频）。硬禁令贯穿全文：不贴生成矩阵、不写 G(x)、不 dump Idle/符号表。读完应能向同事讲清「CRC fail 为何不等于天线坏、BPTC/Trellis/Rate1 如何分工、Header RS24 与嵌入 CS5 为何不同、Idle 为何无 CRC」，并进入第 25 课语音呼叫过程直觉。*
