
## 8. 自测（请先自己答，再展开）

**题 1.** 语音超帧由几个业务突发组成？标号是什么？总时长多少？它是不是 TDMA frame？

<details><summary>简答</summary>

**6** 个，标号 **A–F**，共 **360 ms**。它**不是** TDMA frame（TDMA frame = 60 ms）。

</details>

**题 2.** Burst A 的中心 48 bit 通常是什么？它对迟后进入有何意义？

<details><summary>简答</summary>

通常是 **Voice SYNC**。它标记超帧边界，并作为迟后进入接收机「跳上火车」的同步点。

</details>

**题 3.** 一条 Full LC 典型由超帧里哪几节的嵌入场拼成？大约几个碎片？

<details><summary>简答</summary>

典型由 **Burst B–E** 的嵌入场拼成，共 **4** 个碎片（经 BPTC 等 FEC 回到 Full LC）。

</details>

**题 4.** 同事说：「语音通话时每个 30 ms 都有 Voice SYNC。」请纠正，并给出正确的疏密直觉。

<details><summary>简答</summary>

纠正：Voice SYNC 通常在每个超帧的 **Burst A**，每逻辑信道大约 **360 ms** 一次，不是每 30 ms。B–F 中心多为嵌入。

</details>

**题 5.** 画出（或默写）常规组呼从发车到到站的顺序：Header、超帧、Terminator。并标明谁用 Data SYNC、谁用 Voice SYNC。

<details><summary>简答</summary>

**Voice LC Header**（可选 **PI Header**）→ **A B C D E F**（可多列）→ **Terminator with LC**。  
Header / Terminator：数据壳，中心 **Data SYNC**。  
Burst A：语音壳，中心 **Voice SYNC**。B–F：语音壳，中心多为嵌入。

</details>

**题 6.** 用户中途开机进组，先安静再突然有声。用本课两步解释。

<details><summary>简答</summary>

① 等待下一次 **Burst A 的 Voice SYNC** 对齐超帧（上车）；② 从嵌入碎片（及/或 Header）拼出 **Full LC** 确认地址/组号（认门牌）。拼齐前可能「有载波/有能量但无完整组显示」。

</details>

**题 7.** 出站两路同时语音且超帧错开 30 ms 时，Part1 给出的 Voice SYNC 最坏等待大约多少？这和「每信道 360 ms」如何同时成立？

<details><summary>简答</summary>

最坏约 **330 ms**。因为接收机出站可看两个时隙：两路超帧错开时，最近的一次 Voice SYNC 可能来自另一路，间隔被缩短到约 330 ms；**每一路自己**仍是约每 360 ms 一个 A。

</details>

**题 8.** （巩固调制弱项）超帧 A–F 有没有改用别的调制或劈开 12.5 kHz？264 bit 货箱验算应用 30 ms 还是 ≈27.5 ms 做分母？

<details><summary>简答</summary>

没有改调制，也不劈频；仍是 **12.5 kHz + 4FSK**。验算用 **≈27.5 ms**：264/0.0275≈9600 bit/s。

</details>

---

## 9. 资料库加深

按这个顺序读，避免一上来背 SYNC 比特图案表或 BPTC 矩阵：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `00-入门/DMR术语与帧结构速查卡.md`「语音超帧」 | 墙上三行：A–F、360 ms、SYNC 疏密 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§4** | 超帧总图 + Burst 分工 + SYNC 对照表 |
| 3 | 同上 §3 | 回看 264 / 语音壳 vs 数据壳（接第 16 课） |
| 4 | `02-语音业务/语音业务字段速览.md` §2–3 | 呼叫阶段表；Late entry 一句；Full LC 业务 PDU |
| 5 | `学习推送/第15课.md`、`第16课.md` | 时隙/突发复习 |
| 6 | `01-空中接口/CSBK与LC字段详表.md` | 需要 FLCO/FID 字段名时再查 |
| 7 | 官方 **TS 102 361-1 V2.7.1** clause **5.1.2.1–5.1.2.3**、**4.3**、**7.1.3** | 超帧/发起/终止/嵌入原文；**冲突以 PDF 为准** |
| 8 | **TR 102 398** 对应导读图 | 概念对照，**不是**替代 TS |
| 9 | `学习推送/加餐_频率带宽与调制解调.md` | 若 12.5 kHz / 4FSK 仍糊 |

官方版本锚点：**Part1 V2.7.1**；**TR V1.5.1**。冲突规则：**TS > TR > 手册/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 10. 下一课预告

**第 18 课 · CACH 与 Guard**

本课站住了语音列车：A–F = 360 ms，A 亮 Voice SYNC，B–E 拼 Full LC，迟后进入半路上车。下一课回到第 15 课埋下的那条 **≈2.5 ms 缝**：出站缝里的 **CACH（24 bit）** 到底广播什么，入站缝里的 **Guard** 在防什么。仍少公式，多对照「缝不是 264 货箱的一部分」。

---

## 11. 推荐阅读与视频

本课外链为 **2026-09-26** 检索核验；**不编造地址**。策略 = **Part1 超帧原文 + 协会「嵌入支持迟入」图 + 解码文 EMB/B–E→FLC + 厂商帧图 + 中文超帧科普**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **5.1.2.1** figure 5.3 即语音超帧 A–F；**5.1.2.2 / 5.1.2.3** 讲发起与终止；**4.3** 讲 SYNC 疏密与迟后进入动机；**7.1.3** 讲嵌入。硬出处。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)（部分网络可能拦截，可用协会镜像）。  
   - **适合哪一段**：第 2、5、6、9 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：「Embedding Data within Voice」一页直接画出 **A = Voice SYNC、B–E = Embedded、超帧 = 360 ms**，并写明嵌入 initially 用于 **Late Entry**（呼叫类型、源/目的 ID、业务选项）。协会培训口吻，和图与本课总图同向。  
   - **适合哪一段**：第 2.2、4.3、5.3 节后对照。  
   - **注意**：幻灯年代/版本锚点可能早于现行 Part1；**硬条款以 V2.7.1 为准**。  
   - **基础**：入门～中级；英文 PDF。

3. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读用同样的超帧 / SYNC 疏密叙事，比纯条款好读。  
   - **适合哪一段**：第 2.4、6 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

4. **[GopherTrunk｜Protocol Decoders Part 5: DMR Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：清楚写出 Full LC 的两条到达路径——Voice LC Header **或** 语音突发 **B–E** 四个 32-bit 碎片经 EMB/BPTC 拼回；正好把本课「门牌怎么来」钉死。  
   - **适合哪一段**：第 5.1–5.3、7、9 节后深挖。  
   - **基础**：中级～进阶；英文长文；实现向，字段以 Part1 为准。

5. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：Fig.7 Voice format 标出语音突发 **A–F**；并有出站 CACH / 入站 Guard 对照，衔接下课。  
   - **适合哪一段**：第 2、4 节；预习第 18 课缝。  
   - **注意**：文中个别「frame/superframe」口误勿盲从；**以 ETSI 定义为准**（超帧 = 6 **bursts**，不是 6 个 TDMA frame）。  
   - **基础**：中级；英文 PDF。

6. **[VK4PK｜DMR Signal Processing Notes](https://lyonscomputer.com.au/MMDVM/DMR-Signal-Processing-Notes/DMR-Signal-Processing-Notes.html)**  
   - **为什么值得看**：把 264 / 108+48+108 / 4FSK / 4800 baud 与时间参数写在一页，方便和超帧时间轴对账。  
   - **适合哪一段**：第 2.5、6 节；巩固调制弱项。  
   - **基础**：入门～中级；英文网页；业余/MMDVM 笔记，**规范数字仍以 ETSI 为准**。

7. **[科讯｜DMR 对讲机数字协议详解](http://www.cqkexun.com/service/problem/hand/292.html)**  
   - **为什么值得看**：中文专节写「语音超帧：6 突发、360 ms、A 含 SYNC、B–F 可嵌嵌入式信令」，适合建立中文第一印象。  
   - **适合哪一段**：第 2–3 节。  
   - **注意**：科普文版本偏旧；文中个别「语音头中间是语音同步码」等表述与现行 Part1 **不符**（Header 应为 Data SYNC）——**冲突以 ETSI TS 为准**。  
   - **基础**：入门；中文。

8. **[Electronics Notes｜How does DMR Mobile Radio Work](https://www.electronics-notes.com/articles/connectivity/private-land-mobile-radio-pmr-lmr/how-does-dmr-mobile-radio-work.php)**  
   - **为什么值得看**：英文通俗总览 TDMA/双时隙与数字对讲直觉，适合当「休息页」回看大图。  
   - **适合哪一段**：读完本课想换口气时。  
   - **基础**：入门；英文网页；不替代 Part1 超帧条款。

**说明（视频）**：公开检索未找到专门把 **「语音超帧 A–F = 360 ms、Burst A = Voice SYNC、B–E 四碎片拼 Full LC、迟后进入两步上车」** 讲透的独立高质量中文/英文短片（多数入门视频只口播「有两个时隙」或厂商产品介绍）。本课**未找到合适公开视频**。建议用：**Part1 figure 5.3 + 协会 Feature Evolution 嵌入图 + GopherTrunk Part5 EMB/FLC 段 + 资料库 §4** 对照自学。

---

*推送说明：本课为阶段 C「语音超帧 A–F」。频谱/调制仅保留短提醒（超帧不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、六车厢总图、术语、现场对照、Header→A–F→Terminator 例子、数字账本、十则误区、八题自测、资料库路径与八条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「A–F 为何是 360 ms、为何 SYNC 不按 30 ms 贴、B–E 如何拼门牌、迟后进入在等什么」，并进入第 18 课 CACH 与 Guard。*
