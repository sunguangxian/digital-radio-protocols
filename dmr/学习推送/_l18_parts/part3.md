## 8. 数字账本（建议钉在速查卡旁）

| 项 | 值 | 备注 |
|----|-----|------|
| Timeslot | **30 ms** | 第 15 课 |
| TDMA frame | **60 ms** | 两时隙 |
| Traffic 内容窗 | **≈ 27.5 ms** | 264 bit |
| **Guard / CACH 缝** | **≈ 2.5 ms** | 入站 Guard；出站 CACH |
| Traffic 总比特 | **264 = 108+48+108** | 第 16 课 |
| **CACH** | **24 bit** | **仅出站**；约每 **30 ms** 一次 |
| CACH 字段切分 | 1+1+2+3+17 | AT\|TC\|LCSS\|FEC\|Signalling |
| TACT | **7 bit** | AT+TC+LCSS+parity；Hamming (7,4) |
| Signalling 载荷率（约） | **17 bit / 30 ms ≈ 566.67 bit/s** | 资料库 §5；TACT 另计 |
| CACH 毛比特率（约） | **24 / 0.030 ≈ 800 bit/s** | 教学口算；勿与 9.6 kbps 混加 |
| Standalone RC | **96 bit** | 与 CACH 不同物种 |
| Voice superframe | **360 ms** | 只占用 Traffic 窗（第 17） |
| 入/出站编号 | 常见 **30 ms** 偏移 | 便于 CACH 同信道号 |
| CACH 指示延迟 | 约 **一个时隙** | figure 4.8/4.9 精神 |
| 符号率 / 比特率 | **≈ 4800 baud / 9.6 kbps** | 4FSK；缝不改调制 |
| 信道形态 | Traffic+CACH / Traffic+Guard / … | clause 4.6 |

口算口诀：

> **三十窗、二七五货箱、二五缝；出站缝塞二十四，入站缝留空气囊；忙闲看 AT，槽号看 TC，慢信走 Short LC。**

---

## 9. 常见误区

1. **「CACH 的 24 bit 算在 Traffic 的 264 里面。」**  
   错。CACH 在出站 **≈2.5 ms 缝**，与 108+48+108 **首尾相接但分账**（第 16 课已判错，本课再钉死）。

2. **「Guard 和 CACH 是同一个东西的两个名字。」**  
   错。同一条时间缝，**出站塞 CACH、入站留 Guard**——用途相反。

3. **「入站也有 CACH。」**  
   错。典型入站是 Traffic + **Guard**。CACH **仅出站**（连续发模式等场景按 Part1）。

4. **「AT=busy 表示我的 Talkgroup 忙。」**  
   错。AT 指示的是**对应入站时隙**忙闲，服务随机接入/礼貌接入，不是组号本身。

5. **「TC 就是超帧字母 A–F。」**  
   错。TC 只标 **信道 1/2**；A–F 是语音超帧车厢号（第 17 课）。

6. **「DM 直通也有基站那种 CACH 报站。」**  
   错。Talkaround / TDMA DM 通常**没有** BS 出站 CACH；同步压力更大。

7. **「CACH 换了一套调制或另开了 6.25 kHz。」**  
   错。仍是 **12.5 kHz + 4FSK**；只是时间缝里的比特。

8. **「Null Short LC 等于 Idle 突发。」**  
   错。Idle 填的是 **Traffic** 窗；Null Short LC 填的是 **CACH** 载荷空窗。两层都「空」，但不是同一个 PDU。

9. **「CACH 里的 LCSS 和嵌入 EMB 里的 LCSS 是同一个寄存器。」**  
   错。名字相同、职责类似（分片起止），但分属 **CACH TACT** 与 **EMB** 两处；解码时看你在解哪一层。

10. **「缝只有 2.5 ms，所以可以忽略定时误差。」**  
    错。正因为它短，PA 爬升、传播、晶振漂才更要守时——Guard 存在的理由就是这些「小误差」。

---

## 10. 自测（请先自己答，再展开）

**题 1.** 一个 30 ms 时隙，业务内容窗与缝大约各多长？出站缝与入站缝分别叫什么？

<details><summary>简答</summary>

内容窗约 **27.5 ms**（264 bit）；缝约 **2.5 ms**。出站缝 = **CACH**；入站缝 = **Guard**。

</details>

**题 2.** CACH 有多少 bit？是否包含在 Traffic 的 264 bit 内？它出现在入站还是出站？

<details><summary>简答</summary>

**24 bit**。**不包含**在 264 内。出现在**出站**缝；入站同位置通常是 Guard。

</details>

**题 3.** 默画（或默写）CACH 字段切分：AT、TC、LCSS、FEC、Signalling 的比特数，并指出 TACT 是哪一段。

<details><summary>简答</summary>

**1 + 1 + 2 + 3 + 17 = 24**。TACT = 前 **7** bit（AT+TC+LCSS+parity），由 Hamming (7,4) 保护。

</details>

**题 4.** AT 与 TC 各回答现场哪句话？同事说「AT=busy 就是我的组忙了」如何纠正？

<details><summary>简答</summary>

AT → 对应**入站时隙** idle/busy（接入用）。TC → 随后 outbound 是 ch1 还是 ch2。纠正：AT 不是 Talkgroup 忙闲标志。

</details>

**题 5.** 为什么规范常让 CACH 的忙闲/信道指示相对 outbound **延迟约一个时隙**？缺这拍延迟会伤到谁？

<details><summary>简答</summary>

给 MS 留出 **收 CACH → 解码 → 决策 → Tx/Rx 切换** 的时间（figure 4.8/4.9 精神）。没有延迟，手机来不及礼貌接入或选对槽。

</details>

**题 6.** 对比 Tier II 中继出站与 DM Talkaround：谁更常看到 CACH？上行缝通常是什么？

<details><summary>简答</summary>

中继出站常有 **CACH**；DM / Talkaround **通常没有** BS CACH。上行（及 DM）缝多为 **Guard**。

</details>

**题 7.** 写出突发长度三兄弟：Traffic / CACH / standalone RC 各多少 bit？哪一个住在 ≈2.5 ms 出站缝？

<details><summary>简答</summary>

**264 / 24 / 96**。住在出站缝的是 **CACH（24）**。

</details>

**题 8.** （巩固调制弱项）CACH / Guard 有没有改用别的调制或劈开 12.5 kHz？Signalling 约 17 bit/30 ms 的速率大约多少？能否把它和 9.6 kbps 直接相加当「空口总速率」对外乱讲？

<details><summary>简答</summary>

没有改调制，也不劈频；仍是 **12.5 kHz + 4FSK**。约 **566.67 bit/s**。**不能**随便和 Traffic 的 9.6 kbps 混加成对外口径——那是不同水管。

</details>

---

## 11. 资料库加深

按这个顺序读，避免一上来背 Short LC 全表或 BPTC 矩阵：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `00-入门/DMR术语与帧结构速查卡.md` | Guard / CACH 行 + 四种信道形态 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§2** | 时序数字；入站 Guard / 出站 CACH 总图 |
| 3 | 同上 **§5** | CACH 24 bit、TACT、AT/TC/LCSS、延迟一拍、Null Short LC |
| 4 | 同上 **§10** | Traffic+CACH / Traffic+Guard / Bi-directional / DM |
| 5 | `学习推送/第15课.md` | 缝的第一次预告与双时隙例子 |
| 6 | `学习推送/第16课.md` §5.8 | 264 vs 24 vs 96 划界 |
| 7 | `学习推送/第17课.md` | 确认 A–F 只住 Traffic 窗 |
| 8 | 官方 **TS 102 361-1 V2.7.1** clause **4.2、4.5、4.6、6.3、9.1.4**；figure **4.8 / 4.9** | CACH/Guard 原文；**冲突以 PDF 为准** |
| 9 | **TR 102 398** 对应导读 | 概念对照，**不是**替代 TS |
| 10 | `学习推送/加餐_频率带宽与调制解调.md` | 若 12.5 kHz / 4FSK 仍糊 |

官方版本锚点：**Part1 V2.7.1**；**TR V1.5.1**。冲突规则：**TS > TR > 手册/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 12. 下一课预告

**第 19 课 · SYNC：语音/数据如何区分**

本课站住了那条 ≈2.5 ms 缝：出站 CACH 报忙闲与槽号，入站 Guard 护邻槽与功放。下一课钻进 Traffic 货箱正中间那 **48 bit**：为什么语音与数据用**不同 SYNC 图案**，入站与出站图案又为何不同，接收机怎样「一听」就知道这是语音壳还是数据壳。仍少公式，多对照「SYNC ≠ Colour Code ≠ CACH」。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-27** 检索核验；**不编造地址**。策略 = **Part1 CACH/Guard 原文 + TR 导读 + Wavecom 出站 CACH/入站 Guard 图 + Guido Tier II 帧文 + VK4PK 时间参数 + 中文科普（带冲突声明）**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **4.5** 专节 CACH；**4.2** 讲入站 Guard / 出站 CACH 不对称；**4.6** 四种信道形态；**6.3 / 9.1.4** 给 24 bit 与 TACT；figure **4.8 / 4.9** 即「延迟约一个时隙」的硬出处。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)（部分网络可能拦截，可用协会镜像）。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读用同样的「入站 guard / 出站 CACH」叙事，比纯条款好读；突发长度定义（264 / 24 / 96）也常在 TR 术语里一眼能对上。  
   - **适合哪一段**：第 2、7、8 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：明确写出站含 CACH、入站留 guard；并有 BS/MS 突发与帧结构图（文中 fig.3–5 一带），和本课总图可对照。  
   - **适合哪一段**：第 2、6、7 节。  
   - **注意**：厂商/分析仪向综述；个别术语口误勿盲从；**以 ETSI 为准**。  
   - **基础**：中级；英文 PDF。

4. **[Alessandro Guido｜How DMR Works — Conventional Tier 2（PDF）](https://www.qsl.net/kb9mwr/projects/dv/dmr/How%20DMR%20Works%20Conventional%20Tier%202.pdf)**  
   - **为什么值得看**：用常规 Tier II 口吻写清：入站 2.5 ms 给 PA/传播，出站 2.5 ms 给 CACH（帧编号、接入指示、低速信令）；并列出 CACH TACT 用 Hamming (7,4)、Short LC in CACH 等 FEC 名称表，和本课账本同向。  
   - **适合哪一段**：第 4、5、8 节后对照。  
   - **注意**：培训文年代可能早于现行 Part1 V2.7.1；**硬条款以 V2.7.1 为准**。  
   - **基础**：入门～中级；英文 PDF。

5. **[VK4PK｜DMR Signal Processing Notes](https://lyonscomputer.com.au/MMDVM/DMR-Signal-Processing-Notes/DMR-Signal-Processing-Notes.html)**  
   - **为什么值得看**：一页把 264 / 108+48+108 / 2.5 ms Guard / 4FSK / 4800 baud 写在一起，方便和「缝 vs 货箱」两本账对账。  
   - **适合哪一段**：第 2.5、8 节；巩固调制弱项。  
   - **基础**：入门～中级；英文网页；业余/MMDVM 笔记，**规范数字仍以 ETSI 为准**。

6. **[科讯｜DMR 对讲机数字协议详解](http://www.cqkexun.com/service/problem/hand/292.html)**  
   - **为什么值得看**：中文专段写明：每时隙 30 ms、27.5 ms 有效信息、另 2.5 ms 在上行作保护间隔（传播+功放）、在下行作 **CACH**（业务信道管理与低速信令）——适合建立中文第一印象。  
   - **适合哪一段**：第 2–3 节。  
   - **注意**：科普文版本偏旧；文中把 2.5 ms 叙述成「左右各 1.25 ms」等细节属教学简化，**间隙总账与用途划分以 ETSI TS 为准**。  
   - **基础**：入门；中文。

7. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：协会培训向总图；可与第 17 课嵌入/迟入材料连读，帮助把「Traffic 窗里的事」和「缝里的 CACH」在头脑里分柜。  
   - **适合哪一段**：读完本课想回看超帧与嵌入边界时。  
   - **注意**：不是 CACH 专章；幻灯版本锚点可能早于现行 Part1。  
   - **基础**：入门～中级；英文 PDF。

**说明（视频）**：公开检索未找到专门把 **「≈2.5 ms 缝：出站 CACH 24 bit（AT/TC/LCSS/Short LC）vs 入站 Guard（PA/传播/护邻槽）；CACH 指示延迟约一个时隙」** 讲透的独立高质量中文/英文短片（多数入门视频只口播「有两个时隙」或厂商产品介绍）。本课**未找到合适公开视频**。建议用：**Part1 clause 4.5 + figure 4.8/4.9 + Wavecom 出站/入站图 + Guido Tier II 文 + 资料库 §5** 对照自学。

---

*推送说明：本课为阶段 C「CACH 与 Guard」。频谱/调制仅保留短提醒（缝不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、缝总图、术语、24 bit 字段、忙闲/槽号/Short LC、延迟一拍时序、现场对照、中继 vs DM 例子、数字账本、十则误区、八题自测、资料库路径与七条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「为何出站缝塞 CACH、入站缝留 Guard、AT/TC 各管什么、为何指示常晚一拍、264/24/96 如何分柜」，并进入第 19 课 SYNC。*
