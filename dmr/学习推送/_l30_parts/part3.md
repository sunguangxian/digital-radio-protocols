## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| 时隙 | **30 ms** | 跟读尺子 |
| 超帧 | **A–F ≈ 360 ms** | CP2 一列 |
| Voice LC Header Data Type | **`0001`** | CP1 |
| Terminator with LC Data Type | **`0010`** | CP4 |
| FLCO 组呼 / 个呼 | **`000000` / `000011`** | CP1/嵌入/终止门牌 |
| CSBKO 唤醒 / 前导 | **`111000` / `111101`** | CP0 |
| CSBKO 个呼 Req/Ans/NACK | **`000100` / `000101` / `100110`** | CP0 OACSU |
| Talker Alias FLCO | **`000100`–`000111`** | CP2 加料 |
| GPS_Info FLCO | **`001000`** | CP2 加料 |
| TD_LC FLCO（对照） | **`110000`** | **不是**本课语音终止 |
| Part2 官方版本 | **TS 102 361-2 V2.5.1 (2023-05)** | 语音过程硬出处 |
| Part1 官方版本 | **TS 102 361-1 V2.7.1 (2026-05)** | 外壳 / SYNC / EMB |
| 速览主节 | **§1–§2 / §3–§4 / §7–§8** | 本课跟读入口 |
| 详表主节 | **§2 EMB / §4 FULL LC / §6 CSBK / §8 SYNC** | 认壳 |
| 总索引 | **§2 语音关键词 / §4 语音最小打开集** | 门牌 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 跟读不改射频 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |

---

## 9. 十则误区（看见就打回）

1. **「跟读 = 把第 25 课总图再背一遍。」** → 跟读 = 每个 CP 认壳 + 翻表。  
2. **「看见 CSBK 就等于通话开始。」** → CP0 是手续；语音开闸看 Header（或 Late Entry 拼门牌）。  
3. **「错过 Header = 这通呼叫对你永久不可见。」** → CP3 Late Entry：SYNC@A + 嵌入。  
4. **「FLCO 和 CSBKO 混用一张嘴。」** → 两张 Opcode 表；外壳还在 Part1。  
5. **「Hangtime = 射频卡死 / = Late Entry / = TxHang。」** → 三者分家；先翻 §8。  
6. **「Terminator Data Type=`0010` 就一定是语音结束。」** → 再看 FLCO；`110000` 是数据 TD_LC。  
7. **「UU_V_Req 已经在说话。」** → 先问在不在；Proceed 后才 Header(UU)。  
8. **「嵌入里换了 FLCO = 换了一趟呼叫。」** → 可能是 Alias/GPS 加料乘客。  
9. **「Tier III Grant 可以画进本课常规轴。」** → 控制信道故事留给第 31+；别硬对齐。  
10. **「听不见说明 4FSK/12.5 kHz 坏了。」** → 先定 CP、认壳、对组/CC/时隙；调制账本最后背锅。

---

## 10. 自测题（含答案）

**题 1.** 用三句话说明本课「跟读」和第 25 课「直觉总图」差在哪。

<details><summary>答案</summary>

第 25 课给故事形状（门牌→火车→下车→留灯）。本课在每个检查点要求：认壳（SYNC/Data Type/EMB）→ 读 Opcode（FLCO/CSBKO）→ 打开速览/总索引哪一节（第 29 课肌肉）。跟读是可演示的操作清单，不是再背一遍上下车比喻。

</details>

**题 2.** 分析仪显示 Data Type=`0001`，FLCO=`000011`。写出跟读路径（CP + 文件节）。

<details><summary>答案</summary>

CP1。总索引「个呼」→ `语音业务字段速览.md` **§2** 确认「语音开始」→ **§1.1** FLCO=`000011` → **§3.2** UU_V_Ch_Usr；外壳争议回详表 §4 / Part1 PDF。

</details>

**题 3.** 为何「只看见 Burst A 的 Voice SYNC、没有 Header」不能直接判「没有呼叫」？

<details><summary>答案</summary>

可能处于 CP3 Late Entry：错过 Header 后，靠 Voice SYNC@A 对齐超帧，再拼 B–E 嵌入门牌；组/CC/时隙匹配仍可开声。翻总索引「迟后进入」与速览 §2/§7。

</details>

**题 4.** 写出 CP0 三种常见 CSBKO 及「还没进语音」的判断句。

<details><summary>答案</summary>

`111000` BS_Dwn_Act（唤醒）、`111101` Pre_CSBK（前导）、`000100` UU_V_Req（个呼先问）。判断句：壳是 CSBK 数据壳，不是 Voice LC Header；个呼还需 Ans Proceed 才进 CP1。

</details>

**题 5.** Hangtime 与 EOC、TxHang 如何用空口现象一眼分诊？

<details><summary>答案</summary>

Hangtime：EOT 后 BS 仍可发 Terminator with LC，本组优先。EOC/Idle：保留结束，信道放空。TxHang：实现层「再挂载波多久」，名称不是规范条款。先翻速览 §8，再对配置名。

</details>

**题 6.** 判断：Data Type=`0010` 且 FLCO=`110000`，应按本课语音 Terminator Hangtime 处理。（对 / 错）

<details><summary>答案</summary>

**错。** FLCO=`110000` 是 Part3 TD_LC（数据挂起指针）；语音终止通常是 Grp/UU_V_Ch_Usr。跟读轴不要串到数据车次。

</details>

**题 7.** 组呼跟读时，Broadcast 位应在哪一步读？为何「仅组呼」？

<details><summary>答案</summary>

CP1（及嵌入拼门牌后）先认 FLCO=`000000`，再读 Service Options 里的 Broadcast。资料库标明 Broadcast **仅组呼**侧用于广播/全呼类语义；个呼 FLCO 路径不走这套贴纸故事。

</details>

**题 8.** 现场：「同事把 Grant 时间戳和 Voice LC Header 画在同一条常规中继轴上」——你如何纠偏？再补一句调制提醒。

<details><summary>答案</summary>

用 §4.8：本课是 Tier II 常规 Header/嵌入/Terminator；Grant 属 Tier III 控制信道，留给第 31 课。调制提醒：选错时间线故事不改变 12.5 kHz/4FSK/双时隙——先纠跟读轴，再查射频。

</details>

**题 9.（加分）** 从「中继留灯」现象列出完整翻表路径（含与 Late Entry 的一句话区别）。

<details><summary>答案</summary>

现象 → 总索引/速览 §8 Terminator 与 Hangtime → 看是否仍在下发 Terminator with LC → 对实现 CallHang/TxHang 语义。区别：Late Entry 是半路拼门牌上车（CP3）；Hangtime 是 EOT 后保留本组优先（CP5）——不是同一件事。

</details>

**题 10.（加分）** 一列超帧里 A 与 B–E 的「先认什么」分别是什么？各翻详表哪一节？

<details><summary>答案</summary>

A：先认 **Voice SYNC**（详表 §8）。B–E：先认 **EMB + 嵌入碎片**（详表 §2），再拼回与 Header 同类的 Full LC（速览 §2/§3）。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `02-语音业务/语音业务字段速览.md` **§2 / §8** | 过程对照表 + Terminator/Hangtime（本课 canonical 时间线） |
| 2 | 同上 **§1 / §3–§4 / §7** | Opcode 入口、Full LC/CSBK PDU、补充/Late Entry 指针 |
| 3 | `01-空中接口/CSBK与LC字段详表.md` **§2 / §4 / §6 / §8** | EMB、FULL LC、CSBK 壳、SYNC 类型名 |
| 4 | `总索引.md` **§2 语音关键词 / §4 语音最小打开集** | 门牌：个呼组呼迟后进入 → 速览 → Part2 PDF |
| 5 | `学习推送/第25课.md` | 呼叫直觉总图（故事回唤，不重读全文也行） |
| 6 | `学习推送/第26课.md` | Late Entry 两步与加料（CP3 回唤） |
| 7 | `学习推送/第29课.md` | 三层书架与查表路径（每个 CP 的肌肉） |
| 8 | `学习推送/第17课.md` / `第21课.md` / `第22课.md` | 超帧、Data Type、Full LC 三处运载 |
| 9 | `00-入门/DMR术语与帧结构速查卡.md` | 墙上 30 ms / 超帧 / Data Type |
| 10 | `DMR整合学习手册.md` | 全貌与 Tier 边界 |
| 11 | 官方 **TS 102 361-2 V2.5.1**（`02-语音业务/TS102361-2_V2.5.1.pdf`） | 组/个呼过程与 PDU 原文 |
| 12 | 官方 **TS 102 361-1 V2.7.1** | Voice LC Header / Terminator / 嵌入 / SYNC 硬出处 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「跟错检查点」当成调制故障 |

官方版本锚点：**Part2 V2.5.1**、**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。FEC 矩阵、Idle 比特、完整 SDL、Tier III Grant 全表、PDP 车次细节：**永远回 PDF / 对应课**，本课不补第二份。

---

## 12. 下一课预告

**第 31 课 · 控制信道 vs 业务信道**

本课把阶段 D 收在「一条语音呼叫空口跟读 + 检查点翻表」。下一课进入 **阶段 E · 集群 Tier III**：先分清**控制信道**和**业务信道**各干什么——谁负责叫号/授权（Grant），谁承载真正的语音超帧；为什么常规中继的 Header 故事不能直接套到集群控制信道。仍然少公式；把「Tier II 常规 ≠ Tier III Grant」从本课的边界警告，展开成可跟读的集群地图第一课。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-03**（上午推送）检索核验；真实打开过内容页/PDF（协会镜像 / ETSI deliver / Tait Academy / GopherTrunk 等 HTTP 200）。**不编造地址**。策略 = **Part1 协会镜像 + Part2 协会镜像 + Part2 ETSI 官方链 + DMRA 标准目录 + Benefits 白皮书 + Feature Evolution + TR 系统总览 + Tait Intro Study Guide + Tait 课程页 + GopherTrunk E2E Part5（Link Control / Embedded LC / Late Entry，最贴「跟读时间线」）+ GopherTrunk Operator Cookbook Part3（常规双时隙语感）+ GopherTrunk Decoders Part5（Bursts/EMB/FLC）**。另检索公开「walk a DMR voice call air-interface timeline / 跟读语音呼叫空口」专题视频与长文：**未找到**达到本课「CP0–CP6 检查点 + 当场翻表」深度的独立优质短片（Tait Academy 有入门视频课，但是 **DMR 概论**；产品写频/双时隙口播亦不适用）。**已弃用**易触发浏览器挑战的第三方 wiki 页。

1. **[ETSI TS 102 361-2 V2.5.1｜Voice and generic services（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：组呼/个呼过程、Voice Channel User LC、Call hangtime 与 EOC 语义的硬出处；与速览 §2/§8 对照跟读。  
   - **库内副本**：`dmr/02-语音业务/TS102361-2_V2.5.1.pdf`。  
   - **适合哪一段**：第 2、4.1–4.6、8、11 节。  
   - **基础**：进阶；英文 PDF。

2. **[ETSI TS 102 361-2 V2.5.1｜ETSI 官方投递链](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/02.05.01_60/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：与协会镜像同文的官方入口；部分环境抓取异常时改用镜像或浏览器。  
   - **适合哪一段**：同上。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：Voice LC Header / Terminator with LC / 嵌入信令 / Voice SYNC 与 late entry 超帧叙述——跟读时「认壳」第三层。  
   - **适合哪一段**：第 4.2–4.4、8、11 节。  
   - **基础**：进阶；英文 PDF。

4. **[DMR Association｜DMR Standards 目录页](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：协会标准下载门牌——给新人「官方书架在哪」；跟读争议时知道回哪本 PDF。  
   - **注意**：目录页≠时间线课文；版本以 PDF 封面与总索引 §3 为准。  
   - **适合哪一段**：第 2、11 节。  
   - **基础**：入门；英文网页。

5. **[DMR Association｜Benefits and Features of DMR（白皮书 PDF）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：产品语言里的语音能力与迟后进入语感——适合向领导解释「为什么要会跟读空口」。  
   - **注意**：白皮书不是 TS；冲突以 Part1/2 为准。  
   - **基础**：入门；英文 PDF。

6. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：嵌入 LC / late entry 等能力演进图示——补 CP2/CP3 产品侧直觉。  
   - **注意**：演进叙述≠字段表；Opcode 仍回速览/Part2。  
   - **适合哪一段**：第 4.3–4.4、7 节例 4/6。  
   - **基础**：入门～中级；英文 PDF。

7. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统总览——把本课「常规语音跟读」放回 Tier 与业务全景；为第 31 课控制/业务信道铺垫。  
   - **注意**：TR 非 TS；冲突以 Part1/2 为准。  
   - **适合哪一段**：第 2.3、4.8、12 节。  
   - **基础**：中级；英文 PDF。

8. **[Tait Radio Academy｜Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：厂商学院指南，巩固「时隙 / 语音超帧 / 中继」语感，降低跟读门坎。  
   - **注意**：导读≠速览；版本较旧时以现行 ETSI / 总索引 §3 为准。  
   - **适合哪一段**：第 1、2、6 节。  
   - **基础**：入门；英文 PDF。

9. **[Tait Radio Academy｜Introduction to DMR 课程页](https://www.taitradioacademy.com/courses/introduction-to-digital-mobile-radio/)**  
   - **为什么值得看**：有入门视频课与评估——弱基础补「DMR 是什么」；**不是**「跟读语音呼叫空口检查点」专题课。  
   - **适合哪一段**：课前预习 / 第 1 节动机。  
   - **基础**：入门；英文网页/视频。

10. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
    - **为什么值得看**：把 Full LC、Header/Terminator、嵌入碎片与 late entry 串成一条实现侧故事——**最贴近本课「跟读时间线」**的公开长文。  
    - **注意**：**实现≠规范**；确认次数等策略是实现选择，冲突以 ETSI PDF 为准。  
    - **适合哪一段**：第 4.2–4.4、7、9 节。  
    - **基础**：中级～进阶；英文网页。

11. **[GopherTrunk｜Operator Cookbook Part 3：Conventional DMR Two Slots](https://gophertrunk.org/blog/tutorials/operator-cookbook-03-conventional-dmr-two-slots/)**  
    - **为什么值得看**：常规双时隙操作语感——提醒跟读时 TS1/TS2 各有各的呼叫与 Hangtime。  
    - **注意**：操作菜谱≠ Part2 过程条文。  
    - **适合哪一段**：第 2.4、6、7 节。  
    - **基础**：入门～中级；英文网页。

12. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
    - **为什么值得看**：从解码器视角看 Burst / EMB / FLC——练「先认壳再读门牌」。  
    - **注意**：解码器字段名可能简称；以速览/TS 为准。  
    - **适合哪一段**：第 4.2–4.3、8、10 题。  
    - **基础**：中级～进阶；英文网页。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 语音呼叫空口跟读：可选 CSBK → Voice LC Header → 超帧 A–F（嵌入 LC）→ Late Entry 窗口 → Terminator → Hangtime → EOC，并在每个检查点翻 Part2 速览/总索引」** 按课堂深度讲透的独立高质量中文/英文短片。Tait Radio Academy 的 Introduction to DMR 是**概论视频课**，可作弱基础补课，但不能替代本课检查点操练。本课 **`video_found=false`**。建议用：**语音业务字段速览 §2/§8 + Part2 V2.5.1 + 本课 CP 速查卡 + GopherTrunk E2E Part5** 对照自学。

---

*推送说明：本课为阶段 D 收官小综合「跟一次语音呼叫空口」。频谱/调制仅保留短提醒（跟读不换频、不改 4FSK/双时隙；跟错检查点≠射频故障），不复述加餐全文。主文加厚覆盖动机、跟读总图与 CP0–CP6 翻表挂钩、术语、各检查点机制（可选手续/Header/超帧嵌入/Late Entry 窗口/Terminator/Hangtime–EOC/组个呼 OACSU/Tier II≠Tier III Grant）、与第 11/15–26/29 课对照、现场分诊、七则例子、账本、十则误区、十题自测、资料库路径与核验外链（含 Part1/Part2、DMRA 目录与白皮书/Feature Evolution、TR、Tait 指南与课程页、GopherTrunk 三条；诚实标明无合适公开「跟读空口检查点」专题视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle、不发明条款号、不重讲第 25/26/29 课全文、不展开 Grant/PDP。读完应能向同事演示「从录波跟读一通组呼/个呼：每个站认壳并翻到速览对应节」，并带着「常规 ≠ 集群控制信道」边界进入第 31 课。*
