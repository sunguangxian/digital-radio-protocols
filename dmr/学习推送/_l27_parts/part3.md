## 7. 工作例子（6 则）

### 例子 A · 非确认 GPS 周期上报（幸福路径）

```text
  [U_HEAD] DPF=0010 A=0 FMF=1 BF=2  Dest=组/网关  Src=车台
    → [Rate ¾ DATA] 定位载荷…
    → [Rate ¾ LDATA] … + MsgCRC
  结束。无 C_RHEAD。偶发丢包由下一周期覆盖。
```

### 例子 B · 确认配置下发（整消息 ACK）

```text
  [C_HEAD] DPF=0011 A=1 FMF=1 N(S)=3 BF=3 …
    → 三块 Rate ½（含 DBSN）+ 末块 MsgCRC
  （BS 侧 TD_LC 留窗）
  ← [C_RHEAD] Class/Type/Status = ACK
  发送方收工。
```

### 例子 C · SACK 选择重传

```text
  首试：C_HEAD FMF=1 + 块 0..4
  ← SACK + C_RDATA 位图：块 2、4 坏了
  重试：C_HEAD FMF=0 + 只重发块 2、4
  ← ACK
```

### 例子 D · 模式不匹配：发确认、对端当非确认听

```text
  空口：C_HEAD A=1 …
  对端配置/能力：只收 unconfirmed 或 ID 不匹配 → 无响应
  发送方：T_RspnsWait 超时 → 重试 → 最终失败
  分诊：先对齐「两边是否都开确认、地址/色码/时隙」——不是先换天线
```

### 例子 E · 误把 TD_LC 当语音结束铃

```text
  同事：「Terminator 又来了，语音 Hangtime。」
  抓包：Data Type=Terminator with LC，但 FLCO=110000（TD_LC）
  正解：数据呼叫留窗等 ACK，不是组呼礼貌说话窗
```

### 例子 F · 「数据必到」却配了非确认 + 应用层不重试

```text
  写频：Unconfirmed
  应用：发一次定位/工单，失败无重发
  现场：弱场丢包 → 「DMR 数据不可靠」
  正解：要么改 Confirmed，要么应用层做确认/重试——两层别甩锅
```

---

## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| Data Header Data Type | `0110` | 数据头壳 |
| DPF 非确认 | `0010` | U_HEAD |
| DPF 确认 | `0011` | C_HEAD |
| DPF Response | `0001` | C_RHEAD |
| DPF 短数据 Defined / Raw·Status | `1101` / `1110` | 第 28 课门口 |
| SAP Short Data / IP / UDP HC | `1010` / `0100` / `0011` | 乘客类型 |
| U_HEAD 固定 | A=`0`，FMF=`1` | 无响应窗 |
| TD_LC FLCO | `110000` | 数据 hangtime |
| Header 长度 | 96 bit | C_HEAD/U_HEAD/C_RHEAD |
| MsgCRC | 32 bit | 整消息末块 |
| 块内 CRC-9 | 确认续块 | 盖 DBSN+User |
| T_RspnsWait（建议） | ~180 ms（同播可更长） | 等响应 |
| T_DataHngtime（建议） | ~180 ms | TD_LC 留窗 |
| N_RtryLmt（建议 max） | 8 | 确认重试上限量级 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 不换频不改调 |

---

## 9. 十则误区（看见就打回）

1. **「发了 IP 就一定是确认 PDP。」** → IP 可坐确认或非确认；看 A/DPF，不看「IP」三个字母。  
2. **「非确认=绝对不能用。」** → 周期遥测/组播洪泛常用；条款是「无 ACK」，不是「禁止使用」。  
3. **「看见 Data Header 却无 ACK，一定是射频坏了。」** → 先查是否 U_HEAD（A=0）。  
4. **「TD_LC 就是语音 Terminator。」** → FLCO=`110000` 的数据留窗，不是组/个语音结束 LC。  
5. **「确认模式会无限重传直到成功。」** → 有重试上限量级（如 N_RtryLmt）；还有 NACK 失败语义。  
6. **「Rate 1 一定比 Rate ½ 更好。」** → 载荷更多、保护更少；信道差时可能更惨。  
7. **「短数据 / 头压缩就是本课要背的全表。」** → 本课钉承载；短数据与 HC 是第 28 课主菜。  
8. **「Tier III 没有 PDP，只有控制信道短数据。」** → 控制信道有自有短数据；业务信道仍可 PDP。  
9. **「SACK 和 NACK 是一回事。」** → NACK 常表整消息失败原因；SACK 带位图要你补缺块。  
10. **「FMF 在非确认里也可以随便置 0 表示重试。」** → 非确认 FMF **固定为 1**；选择重传语义属于确认世界。

---

## 10. 自测题（含答案）

**题 1.** 用一句话区分：Confirmed PDP vs Unconfirmed PDP（站在 DLL 投递条款上说）。

<details><summary>答案</summary>

确认：请求响应（A=1 一类语义），块可带序号，对端可 ACK/NACK/SACK，允许重试。非确认：A=0、通常无 ACK 窗，发完带 MsgCRC 即结束。二者都是 PDP 承载，不是「另一种无线制式」。

</details>

**题 2.** U_HEAD 的 DPF 是什么？A 与 FMF 的固定值各是什么？这意味着空口上通常看不看得到 C_RHEAD？

<details><summary>答案</summary>

DPF=`0010`；**A=0**；**FMF=1**。通常**不应该**期待 C_RHEAD——没有响应窗是设计如此。

</details>

**题 3.** 画出确认数据的最短幸福路径（从 C_HEAD 到 ACK），并指出中继侧谁可能用 TD_LC。

<details><summary>答案</summary>

`C_HEAD → Rate 块（含 DBSN）… → 末块+MsgCRC →（等）C_RHEAD=ACK`。中继（BS）侧常用 **TD_LC**（FLCO=`110000`）留数据 Hangtime，给响应突发腾道。

</details>

**题 4.** 判断：只要 SAP 指明 IP based Packet data，空口就必定出现 Response 包。（对 / 错）并说明为什么。

<details><summary>答案</summary>

**错。** SAP 说明乘客是 IP；车次仍由 DPF/A（确认/非确认）决定。IP 可以坐非确认列车，此时无 Response。

</details>

**题 5.** SACK 之后空口上还可能紧跟什么 PDU？发送方接下来做什么？FMF 在选择重传时常见怎么置？

<details><summary>答案</summary>

常跟 **C_RDATA**（Retry Flags 位图）。发送方按位图重发缺块；选择重传时头上 **FMF 常置 0**（相对首试 FMF=1）。

</details>

**题 6.** 现场：「分析仪有 Data Header，对端无任何响应」——请给出至少三条分诊顺序（先协议后射频）。

<details><summary>答案</summary>

示例顺序：① 读 DPF/A——是否本就是 U_HEAD；② 确认模式下检查 Dest/Src LLID、色码、时隙、双方是否都开确认；③ 看有无 TD_LC 留窗 / 是否被抢占；④ 再查弱场、MsgCRC/NACK 原因。最后才是「换天线撞大运」。

</details>

**题 7.** Rate ½ 与 Rate 1 的岗位权衡各用一句话；为什么说「Header 和续块要分开看」？

<details><summary>答案</summary>

Rate ½：保护多、载荷少；Rate 1：载荷多、保护少、差信道更脆。Header 在 ¾/1 场景下仍常按更强的头保护（rate-½ 思路）编码——头失败与单块失败的重救策略不同（确认可 SACK 补块，头坏了整趟可能起不来）。

</details>

**题 8.** 为什么本课要把「短数据三头 + UDP 头压缩字段表」划到第 28 课，而不是在这里一次背完？

<details><summary>答案</summary>

因为本课主线是 **DLL 两条投递条款**（确认/非确认时间线、响应、TD_LC）。短数据与 HC 是 **DPF/SAP 乘客与头格式** 的加厚课；混进本课会把「车次」和「乘客身份证」搅成一锅，现场分诊时反而不会先问 A/DPF。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `03-数据协议/数据协议字段速览.md` **§2** | **C_HEAD / U_HEAD 逐比特对照**（本课 canonical） |
| 2 | 同上 **§3** | 确认/非确认续块与 MsgCRC / DBSN |
| 3 | 同上 **§4** | C_RHEAD / C_RDATA；Table 6.6 子集；A+SARQ |
| 4 | 同上 **§6 / §8** | TD_LC；Data Type / DPF 速查 |
| 5 | `学习推送/第13课.md` **§7** | PDP 地图、短数据门口、Tier 一行 |
| 6 | `03-数据协议/AnnexA定时器与AnnexC_IPv6.md` | T_RspnsWait / T_DataHngtime / N_RtryLmt 量级 |
| 7 | `学习推送/第25课.md` / `第26课.md` | 语音时间线对照；为何数据不用 late entry 话术硬套 |
| 8 | `学习推送/第24课.md` | FEC 原则（不贴矩阵）——理解 Rate 权衡 |
| 9 | `00-入门/DMR术语与帧结构速查卡.md` | Data Type / 264 burst 一页墙 |
| 10 | `DMR整合学习手册.md` §5 | 数据业务总述 |
| 11 | 官方 **TS 102 361-3 V1.3.1**（库内：`03-数据协议/TS102361-3_V1.3.1.pdf`） | PDP 过程原文 |
| 12 | 官方 **TS 102 361-1**（Data Header / DPF / SAP / Rate 块表） | 空口头与块布局硬出处 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「无 ACK」一律怪调制 |

官方版本锚点：**Part3 V1.3.1**、**Part1 V2.7.1**（头/DPF 表）。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。FEC 矩阵、Idle 比特、完整 SDL：**永远回 PDF**，本课不补第二份。

---

## 12. 下一课预告

**第 28 课 · 短数据与头压缩**

本课钉死了 DLL 两条车次（确认 / 非确认）。下一课上车看乘客证件：短数据三姐妹（Status/Precoded、Raw、Defined）、端口与 SARQ 在短数据头上怎么露面，以及 **UDP/IPv4 头压缩**（SAP、SAID/DAID、端口索引）如何把 IP 塞进宝贵的 Rate 块——仍少公式，多现场对照；TCP HC 仅保留「SAP 有预留、无对等完整字段表」的诚实边界。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-01**（晚间推送）检索核验；真实打开过内容页/PDF（协会镜像 HTTP 200；ETSI 官方链可能对部分抓取返回 403，浏览器/协会镜像仍可用）；**不编造地址**。策略 = **Part3 协会镜像 + ETSI 官方链 + Benefits 白皮书（Confirmed PDP / IP over PDP）+ Part1 头/DPF + RMHAM IP DATA 课堂幻灯（确认 vs 非确认）+ go-dmr 头解析代码对照 + Tier III 特性综述 + TR 设计导读**。**已弃用**易触发浏览器挑战的第三方 wiki 页。

1. **[ETSI TS 102 361-3 V1.3.1｜Packet Data Protocol（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236103v010301p.pdf)**  
   - **为什么值得看**：确认/非确认过程、响应、数据 hangtime / TD_LC 叙事——本课硬出处。  
   - **库内副本**：`dmr/03-数据协议/TS102361-3_V1.3.1.pdf`。  
   - **适合哪一段**：第 4、6、8、11 节。  
   - **基础**：进阶；英文 PDF。

2. **[ETSI TS 102 361-3 V1.3.1｜ETSI 官方投递链](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236103/01.03.01_60/ts_10236103v010301p.pdf)**  
   - **为什么值得看**：与协会镜像同文的官方入口；部分环境对自动抓取返回 403 时改用镜像或浏览器。  
   - **适合哪一段**：同上。  
   - **基础**：进阶；英文 PDF。

3. **[DMR Association｜Benefits and Features of DMR（白皮书 PDF）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：用产品语言提到 **Confirmed packet data**、**IP over PDP**、短数据尺寸量级——适合给领导/新同事的一句话语感。  
   - **注意**：白皮书不是 TS；冲突以 Part1/3 为准。  
   - **基础**：入门；英文 PDF。

4. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：Data Header / DPF / SAP / Rate ½·¾·1 块表——C_HEAD/U_HEAD 位宽硬出处。  
   - **适合哪一段**：第 4.4–4.5、8、11 节。  
   - **基础**：进阶；英文 PDF。

5. **[RMHAM｜IP DATA OVER DMR（课堂幻灯 PDF）](https://www.rmham.org/wp-content/uploads/2023/02/IP-DATA-Slides.pdf)**  
   - **为什么值得看**：用教学幻灯把 **Confirmed vs Unconfirmed** 画成「ACK+retry / 多一对一」vs「no retries / 可 talkgroup」——本课 §2 / §4.2–4.3 的课堂友好对照。  
   - **注意**：业余/培训幻灯，**不以幻灯条款号替代 ETSI**；IP 细节与 HC 仍回 Part3 + 第 28 课。  
   - **适合哪一段**：第 2、4.2–4.3、6 节。  
   - **基础**：入门～中级；英文幻灯。

6. **[pd0mz/go-dmr｜dataheader.go（头字段解析代码）](https://github.com/pd0mz/go-dmr/blob/master/dataheader.go)**  
   - **为什么值得看**：从实现侧对照 Confirmed / Unconfirmed 头字段拆解——便于和资料库 §2 表互证。  
   - **注意**：**代码不是规范**；冲突以 ETSI PDF 为准。  
   - **适合哪一段**：第 4.4、8 节。  
   - **基础**：中级～进阶；Go 源码。

7. **[DMR Association｜State of the art of ETSI DMR Tier III（PDF）](https://dmrassociation.org/public-downloads/documents/State-of-the-art-of-ETSI-DMR-Tier-III-Standard-Critical-Comms-Russia-18Apr-2019.pdf)**  
   - **为什么值得看**：把 packet data / IP+HC 放进 Tier III 特性清单语境——帮助记住「控制信道短数据 vs 业务信道 PDP」分家。  
   - **适合哪一段**：第 4.8、11 节。  
   - **基础**：中级；英文 PDF。

8. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读，把数据能力放回整网叙事。  
   - **注意**：TR **不是**规范。  
   - **基础**：入门～中级；英文 PDF。

**说明（视频）**：公开检索**未找到**专门把 **「DMR PDP：确认 vs 非确认空口时间线（C_HEAD/U_HEAD、DBSN、ACK/NACK/SACK、TD_LC 数据 hangtime）」** 按课堂深度讲透的独立高质量中文/英文短片（多数是产品写频演示、业余 packet 玩法或「DMR 能传 IP 吗」科普，深度不够当本课视频教材）。本课 **`video_found=false`**。建议用：**数据协议字段速览 §2–§4 + RMHAM IP DATA 幻灯 + Part3 PDF 目录/概述 + 本课总图** 对照自学。

---

*推送说明：本课为阶段 D「PDP：确认与非确认数据」专课。频谱/调制仅保留短提醒（数据不换频、不改 4FSK/双时隙），不复述加餐全文。主文加厚覆盖动机、挂号信/邮筒总图与双时间线、术语、非确认/确认过程、C_HEAD↔U_HEAD 对照、Rate 权衡、ACK/NACK/SACK、TD_LC、IP/短数据门口与 Tier 一行、现场分诊、六则例子、账本、十则误区、八题自测、资料库路径与核验外链（含 RMHAM 幻灯；诚实标明无合适公开专题视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle、不发明条款号、不展开短数据/HC 全表、不编造 TCP HC。读完应能向同事讲清「确认与非确认两条车次、头上哪些位是分水岭、没 ACK 时先查是不是根本不该有 ACK、TD_LC 不是语音结束铃」，并进入第 28 课短数据与头压缩。*
