## 7. 工作例子（6 则）

### 例子 A · 状态 ping（SP_HEAD，幸福路径）

```text
  应用：车台按键「到位」→ 预编码状态值 S
  空口：[SP_HEAD]
        DPF=1110  SAP=1010  AB=0
        SP/DP=约定端口  Status/Precoded=S
        A=0  → 发完结束（调度席靠周期/下一次刷新）
  分诊要点：不要找 Rate 块；不要找 IP。
```

### 例子 B · 原始短报文 + SARQ（R_HEAD）

```text
  [R_HEAD] DPF=1110 SAP=1010 A=1 SARQ=1 F=1 AB=2
        SP/DP=应用端口  Bit Padding=…
    → [Rate 块 0][Rate 块 1]
  （等）← ACK  → 收工
  若 ← SACK + 位图：只补缺块，F=0 再发 → 再等 ACK
  节奏：stop-and-wait，不连发下一封短报文抢窗口。
```

### 例子 C · Defined UTF 短文本（DD_HEAD）

```text
  [DD_HEAD] DPF=1101 SAP=1010
        DD=约定 UTF 类字符集（见 Part1 9.3.38 表，此处不抄全表）
        A=1 SARQ=0  → 整消息确认即可
    → 续块：UTF 字节…
  对端按 DD 约定解码；若误当成 Raw，会「有字节但读成乱码」。
```

### 例子 D · UDP HC：LIP 定位 / 文本（5017 / 5016）

```text
  [C_HEAD] DPF=0011 A=1 SAP=0011  LLID Dest/Src=…
    → [第一续块]
         IPv4 ID | SAID=0000 | DAID=0000
         HC Opcode=00 | SPID=0000010 | DPID=0000010   ← 5017 LIP
         （SPID/DPID 均 ≠0 → 无 EH，后面直接 LIP 载荷）
    → …更多块… → 末块 + MsgCRC
  （等）← ACK

  文本变体：SPID/DPID=0000001 → UDP 5016 UTF-16BE Text
  （RMHAM 课堂幻灯有「文本=UDP 5016」语感；硬字段仍以 ETSI / 资料库为准）
```

### 例子 E · SAP 不匹配（短数据当成 HC 解）

```text
  空口：SP_HEAD  SAP=1010  DPF=1110  AB=0
  解码脚本：按 UDP HC 去解析「第一续块」——但根本没有续块
  现象：脚本报「压缩头长度错 / 端口 0」
  正解：先读 SAP。1010=短数据证件；0011 才是 HC 登机牌。
```

### 例子 F · Tier III 路径混淆

```text
  集群同事：「控制信道天天短状态，怎么你们课里大讲 SP_HEAD？」
  常规同事：「短数据必须走 PDP。」
  仲裁：两边都对。
    · Tier III 控制信道自有短数据 → Part4（本课不展开 UDTO）
    · 业务信道 / Tier I·II → Part3 三姐妹或 IP/HC（本课）
  先问 Tier 与信道种类，再选书。
```

---

## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| Data Header Data Type | `0110` | 头壳（与第 27 课同） |
| DPF Status·Raw / Defined | `1110` / `1101` | 短数据三姐妹 |
| DPF Confirmed / Unconfirmed | `0011` / `0010` | IP/HC 车次 |
| DPF Response / UDT | `0001` / `0000` | 响应；UDT 指针 |
| SAP Short Data | `1010` | 三姐妹 |
| SAP UDP/IP HC | `0011` | 压缩登机牌 |
| SAP IP based | `0100` | 未压缩 IP |
| SAP TCP HC | `0010` | **仅预留** |
| Status/Precoded 场 | 10 bit | 在 SP_HEAD 内 |
| SP / DP（短数据） | 3+3 bit | R/SP 头端口 |
| DD 字符集 | 6 bit | DD_HEAD |
| AB | 2+4 | SP 时常 0；R/DD=后续块数 |
| SARQ / F | 1+1 | 选择重传与首试/重试 |
| Bit Padding | 8 bit | R/DD 头 |
| HC Opcode | `00` | UDP/IPv4 HC |
| SAID Radio / USB | `0000` / `0001` | 网段索引 |
| DAID Group Network | `0010` | 组网段 |
| SPID/DPID Text / LIP | `0000001`→5016 / `0000010`→5017 | 端口索引 |
| SPID/DPID = 0 | 真端口在 EH | Extended Header 规则 |
| Header 长度 | 96 bit | 各 Data Header 家族 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 不换频不改调 |

---

## 9. 十则误区（看见就打回）

1. **「短数据就是短一点的 IP。」** → 证件不同：DPF/SAP/头家族都不同。  
2. **「SP_HEAD 后面一定还有 Rate 块。」** → Status 时常 AB=0，码在头里。  
3. **「开了 UDP HC 就一定是确认 PDP。」** → HC 是 SAP；车次仍看 DPF/A。  
4. **「TCP HC 可以按 UDP 表改两个字段来用。」** → Part3 V1.3.1 **无**对等完整表；禁止编造。  
5. **「SP/DP（3 bit）和 SPID/DPID（7 bit）是同一个端口。」** → 短数据端口 vs UDP 端口索引，两套语义。  
6. **「Defined 就是厂商随便定义。」** → DD 指向 Part1 **9.3.38** 字符集约定；厂商私有另看 P_HEAD/MFID。  
7. **「集群没有 SP/R/DD，只有控制信道短数据。」** → 控制信道有自有路径；业务信道仍可走 Part3 PDP。  
8. **「UDT 和三姐妹每天一起背全表。」** → UDT Opcode / 控制信道布局 → Part4；本课只留指针。  
9. **「头压缩失败先换天线。」** → 先查 SAP、SPID/DPID、EH 规则、SAID/DAID+LLID。  
10. **「A=1 就可以连发多封短数据不等 ACK。」** → 短数据侧强调 **stop-and-wait**；别按无限窗口想。

---

## 10. 自测题（含答案）

**题 1.** 用两句话区分：短数据三姐妹 vs UDP/IPv4 头压缩（从 DPF/SAP/头家族说）。

<details><summary>答案</summary>

短数据三姐妹用 SP/R/DD_HEAD，DPF 多为 `1110`/`1101`，SAP 常为 Short Data `1010`；状态甚至可只在头内。UDP/IPv4 HC 仍用 C_HEAD/U_HEAD 作车次壳，SAP=`0011`，压缩头在**第一个续块**，服务的是 IP/UDP 乘客。

</details>

**题 2.** SP_HEAD 里 Status/Precoded 多宽？AB 在 Status/Precoded 时通常怎么置？这意味着空口上通常看不看得到续块？

<details><summary>答案</summary>

**10 bit**；AB **置 0**；通常**没有** Rate 续块——别把「没续块」当成丢包。

</details>

**题 3.** 写出 A+SARQ 四种组合的含义；短数据侧推荐的确认节奏叫什么？

<details><summary>答案</summary>

00 非确认；01 保留；10 整消息确认；11 确认+按块 SARQ。节奏：**stop-and-wait**（发一趟、等回执、再发下一趟）。

</details>

**题 4.** R_HEAD 与 DD_HEAD 最关键的字段级差别是什么？

<details><summary>答案</summary>

骨架类似（都有 A、AB、SARQ、F、Bit Padding 等），但 DD_HEAD 用 **DD（6 bit）字符集**替代 R_HEAD 的 **SP/DP（3+3）端口**——一个靠端口找应用，一个靠字符集约定如何解码字节。

</details>

**题 5.** UDP HC 中 SPID=DPID=`0000010` 表示什么端口？此时 Extended Header 要不要出现？为什么？

<details><summary>答案</summary>

表示 UDP **5017（LIP）**。SPID、DPID 均 ≠0 → 按表 **不用** EH1/EH2，后面直接放应用数据。

</details>

**题 6.** 判断：SAP=`0010`（TCP/IP header compression）意味着你可以在 Part3 V1.3.1 里找到与 UDP 对等的逐字段压缩八位组表。（对 / 错）并说明纪律。

<details><summary>答案</summary>

**错。** SAP 仅预留；Part3 V1.3.1 正文展开的是 UDP/IPv4 HC。资料库明确缺口 → **不编造 TCP HC 表**；产品宣称以厂商文档为准。

</details>

**题 7.** 现场：「分析仪有 Data Header，同事按 HC 解第一块失败」——请给出至少四步分诊顺序。

<details><summary>答案</summary>

示例：① 读 DPF/SAP——是不是根本是 SP/R/DD（`1010`）而不是 HC（`0011`）；② 若是 HC，核对第一续块是否存在、HC Opcode 是否为 `00`；③ 查 SPID/DPID 与 EH 规则是否匹配（索引为 0 才挂真端口）；④ 查 SAID/DAID+LLID 推导与应用端口（5016/5017/厂商）；⑤ 再查确认车次/A/CRC；⑥ 最后才是弱场与天线。

</details>

**题 8.** 为什么本课把 UDT Opcode / 控制信道短数据字节布局划走，只留指针？

<details><summary>答案</summary>

因为 UDT 控制信道过程主战场在 **Part4**（Tier III），与业务信道上 Part3 三姐妹/IP-HC 容易搅成一锅；大纲把细讲留给后课。本课纪律：认 UDT_HEAD 门口与 DPF=`0000` 即可，**不展开 UDTO 取值表**。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `03-数据协议/数据协议字段速览.md` **§5** | **SP/R/DD/UDT/P 头**（本课 canonical） |
| 2 | 同上 **§7** | **UDP/IPv4 HC** 字段、索引、EH、解压常量 |
| 3 | 同上 **§1 / §8** | DPF/SAP；Data Type/DPF 速查 |
| 4 | 同上 **§4.3–§4.4** | Table 6.6 子集；A+SARQ |
| 5 | 同上 **§9** | TCP HC / UDT / 缺口声明（诚实边界） |
| 6 | `学习推送/第13课.md` **§7.3–7.5** | 三姐妹门口、IP、Tier 一行 |
| 7 | `学习推送/第27课.md` | 确认/非确认车次、响应、TD_LC（回唤） |
| 8 | `DMR整合学习手册.md` **§5.3** | 数据能力 Tier 对照 |
| 9 | `01-空中接口/帧结构与字段定义.md` §8 一带 | DD/SP/DP/SARQ/AB 位宽索引 |
| 10 | `00-入门/DMR术语与帧结构速查卡.md` | Data Type 一页墙 |
| 11 | 官方 **TS 102 361-3 V1.3.1**（库内：`03-数据协议/TS102361-3_V1.3.1.pdf`） | §5.6 / §6 短数据 / §7.2 HC 原文 |
| 12 | 官方 **TS 102 361-1** Tables **9.17A–C、9.30–9.31** | 三头与 DPF/SAP 硬出处 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把 HC 失败一律怪调制 |

官方版本锚点：**Part3 V1.3.1**、**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。FEC 矩阵、Idle 比特、完整 SDL、TCP HC 臆造表、Part4 UDTO 全表：**永远回 PDF / 后课**，本课不补第二份。

---

## 12. 下一课预告

**第 29 课 · Part2/Part3 字段文怎么查**

本课把乘客证件（短数据三姐妹）与压缩登机牌（UDP/IPv4 HC）钉进现场眼镜。下一课练「图书馆技能」：面对 Part2 语音过程字段与 Part3 数据字段速览，怎么按岗位检索、怎么避免条款号迷路、怎么用总索引/手册/速览三层书架快速定位——仍然少公式，多查表路径；为阶段 D 小综合（跟一次语音呼叫空口）做好翻书肌肉。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-02**（晨间推送）检索核验；真实打开过内容页/PDF（协会镜像 / GitHub / RMHAM 等 HTTP 200；ETSI 官方链可能对部分抓取返回 403，浏览器/协会镜像仍可用）；**不编造地址**。策略 = **Part3 协会镜像（短数据 §6 + HC §5.6/7.2）+ ETSI 官方链 + Part1 三头/DPF/SAP 表 + Benefits 白皮书 + RMHAM IP DATA 幻灯（5016 文本语感）+ go-dmr 头解析代码 + Tier III 特性综述 + TR 设计导读**。另检索公开「DMR short data / UDP header compression」专题视频与长文：**未找到**达到本课深度的独立优质短片（多为产品写频演示或「DMR 能传 IP 吗」科普）。**已弃用**易触发浏览器挑战的第三方 wiki 页。

1. **[ETSI TS 102 361-3 V1.3.1｜Packet Data Protocol（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236103v010301p.pdf)**  
   - **为什么值得看**：短数据承载 §6（Defined/Raw/Status）与 UDP/IPv4 头压缩 §5.6 / §7.2——本课硬出处。  
   - **库内副本**：`dmr/03-数据协议/TS102361-3_V1.3.1.pdf`。  
   - **适合哪一段**：第 4、6、8、11 节。  
   - **基础**：进阶；英文 PDF。

2. **[ETSI TS 102 361-3 V1.3.1｜ETSI 官方投递链](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236103/01.03.01_60/ts_10236103v010301p.pdf)**  
   - **为什么值得看**：与协会镜像同文的官方入口；部分环境对自动抓取返回 403 时改用镜像或浏览器。  
   - **适合哪一段**：同上。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：Tables **9.17A–C**（SP/R/DD_HEAD）、**9.30–9.31**（DPF/SAP）——三头与枚举硬出处。  
   - **适合哪一段**：第 4.2、4.4、8、11 节。  
   - **基础**：进阶；英文 PDF。

4. **[DMR Association｜Benefits and Features of DMR（白皮书 PDF）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：产品语言提到短数据/IP over PDP 等能力量级——适合给领导/新同事的一句话语感。  
   - **注意**：白皮书不是 TS；冲突以 Part1/3 为准。  
   - **基础**：入门；英文 PDF。

5. **[RMHAM｜IP DATA OVER DMR（课堂幻灯 PDF）](https://www.rmham.org/wp-content/uploads/2023/02/IP-DATA-Slides.pdf)**  
   - **为什么值得看**：用教学幻灯点明 **UDP 5016 UTF-16BE 文本**、Confirmed vs Unconfirmed 语感——对本课例子 D / HC 端口索引极友好。  
   - **注意**：业余/培训幻灯，**不以幻灯条款号替代 ETSI**；短数据三头仍回 Part1/3 + 资料库 §5。  
   - **适合哪一段**：第 4.5、6、7 节。  
   - **基础**：入门～中级；英文幻灯。

6. **[RMHAM｜IP Over DMR Slides（2023-12 另一份课堂 PDF）](https://www.rmham.org/wp-content/uploads/2023/12/IP-Over-DMR-Slides.pdf)**  
   - **为什么值得看**：与上条同系列课堂材料，便于对照「文本/自定义 UDP」演示路径。  
   - **注意**：同上，幻灯≠规范。  
   - **适合哪一段**：第 4.5、7 节。  
   - **基础**：入门～中级；英文幻灯。

7. **[pd0mz/go-dmr｜dataheader.go（头字段解析代码）](https://github.com/pd0mz/go-dmr/blob/master/dataheader.go)**  
   - **为什么值得看**：实现侧可见 Short Data Defined/Raw、UDP/TCP HC 的 SAP 枚举与头拆解——便于和资料库 §5/§7 互证。  
   - **注意**：**代码不是规范**；冲突以 ETSI PDF 为准。  
   - **适合哪一段**：第 4.2、4.5、8 节。  
   - **基础**：中级～进阶；Go 源码。

8. **[DMR Association｜State of the art of ETSI DMR Tier III（PDF）](https://dmrassociation.org/public-downloads/documents/State-of-the-art-of-ETSI-DMR-Tier-III-Standard-Critical-Comms-Russia-18Apr-2019.pdf)**  
   - **为什么值得看**：把 packet data / IP+HC 放进 Tier III 特性清单——帮助记住「控制信道短数据 vs 业务信道 PDP」分家。  
   - **适合哪一段**：第 4.6、6、11 节。  
   - **基础**：中级；英文 PDF。

9. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读，把短数据/IP 能力放回整网叙事。  
   - **注意**：TR **不是**规范。  
   - **基础**：入门～中级；英文 PDF。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 短数据三姐妹（SP/R/DD_HEAD）+ UDP/IPv4 头压缩（SAID/DAID/SPID/DPID/Extended Header）」** 按课堂深度讲透的独立高质量中文/英文短片（多数是产品写频演示、业余 packet 玩法或「DMR 能传 IP/短信吗」科普，深度不够当本课视频教材）。本课 **`video_found=false`**。建议用：**数据协议字段速览 §5+§7 + RMHAM IP DATA 幻灯 + Part3 PDF §6/§7.2 + 本课总图** 对照自学。

---

*推送说明：本课为阶段 D「短数据与头压缩」专课。频谱/调制仅保留短提醒（短数据/HC 不换频、不改 4FSK/双时隙），不复述加餐全文。主文加厚覆盖动机、乘客证件总图、术语、三姐妹字段表、A+SARQ 与 stop-and-wait、DPF/SAP 速查、UDP/IPv4 HC 全链路与解压常量、TCP HC/UDT/Tier 诚实边界、现场分诊、六则例子、账本、十则误区、八题自测、资料库路径与核验外链（含两份 RMHAM 幻灯；诚实标明无合适公开专题视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle、不发明条款号、不重讲第 27 课全时间线、不编造 TCP HC、不展开 Part4 UDTO。读完应能向同事讲清「状态码看 SP_HEAD、短字节看 R/DD、IP 文本/定位看 UDP HC、车次仍是确认/非确认、集群控制信道短数据另翻 Part4」，并进入第 29 课字段文检索。*
