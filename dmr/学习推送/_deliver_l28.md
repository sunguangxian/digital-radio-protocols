# 第 28 课 · 短数据与头压缩

> DMR 深入学习 · **阶段 D 语音与数据第 4 课**（接第 27 课「PDP：确认与非确认数据」）  
> 适合：已经分得清「确认 = 挂号信 / 非确认 = 塞邮筒」，也知道 Data Header → Rate 块列车，但仍会把「状态码」当成 IP、把「短数据」和「UDP 头压缩」搅成一种东西、或以为集群控制信道短数据也全在 Part3 里的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**短数据三姐妹（SP_HEAD / R_HEAD / DD_HEAD）是乘客证件；UDP/IPv4 头压缩是另一类乘客的登机牌；二者仍坐第 27 课那两条确认/非确认列车；TCP HC 与 UDT 控制信道只留诚实指针**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。短数据与头压缩**不换频、不改调制、不另开带宽**——差别在 Data Header 上的 **DPF / SAP** 与后续块里装什么。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是 **短数据三头 + A/SARQ + UDP/IPv4 HC + 现场分诊**。

---

## 1. 为什么本课重要（动机）

第 27 课把「车次」钉死了：确认要回执，非确认发完就走。机房下一句要命的话往往是：

- 产品说「发个到位状态」——你去配 IP over PDP，还是找 **Status/Precoded** 短数据？  
- 分析仪看见 Data Header，DPF=`1110`，后面**没有** Rate 块——是丢包了，还是本就是 **SP_HEAD**（状态码就在头里）？  
- 同事把「短报文」和「UDP 5016 文本」当成同一种东西——一个走 **SAP=Short Data**，一个走 **SAP=UDP/IP HC**，证件完全不同。  
- 写频开了头压缩，却解不出对端定位——是 SPID/DPID 指错端口，还是 Extended Header 规则没对齐？  
- 培训台若只背「DMR 能发短数据」七个字，后面会卡在同一处：

> **短数据 ≠ IP。** Status/Precoded、Raw、Defined 是 Part3 短数据承载上的三种证件（三姐妹头）；IP 包常再配 **UDP/IPv4 头压缩**，把 20+8 字节的 IP/UDP 头压进第一个续块里的紧凑登机牌，好省 Rate 块字节。它们都还坐在第 27 课的确认/非确认列车上——先认证件（DPF/SAP），再谈车次（A/确认），最后才骂射频。

本课目标：能画出「乘客证件」总图；对照 SP/R/DD 三头字段；说清 A+SARQ 与 stop-and-wait；展开 UDP/IPv4 HC 的 SAID/DAID/SPID/DPID 与 Extended Header 规则；诚实标出 TCP HC / UDT / Tier III 边界；做现场分诊、六则例子与自测；并为第 29 课「字段文怎么查」留好接口。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不 dump Idle 96-bit、不贴完整 SDL、不发明 ETSI 条款号（字段锚点以资料库 `03-数据协议/数据协议字段速览.md` **§1 / §4.3–§5 / §7–§9** 与 Part1 Table **9.17A–C / 9.30–9.31**、Part3 Table **6.5 / 6.6 / 7.14** 等已摘录者为准）、**不重讲第 27 课确认/非确认全时间线**（只简短回唤）、**不编造 TCP HC 八位组表**（SAP=`0010` 有预留即可）、**不展开 Part4 UDT Opcode / 控制信道字节布局**（仅指针，留给第 39 课一带）。

---

## 2. 总图 / 故事：「乘客证件」

先把整课装进一个故事，再落到资料库 `03-数据协议/数据协议字段速览.md` **§5 / §7 / §8**、第 13 课 **§7.3–7.5**、第 27 课承载回唤。

### 2.1 一句话故事：三姐妹证件 + 压缩登机牌

第 27 课是邮局窗口（确认 / 非确认）。本课是**检票口看证件**：

```text
  同一条铁路（12.5 kHz · 4FSK · 2-slot · 30 ms）
  同一类列车（确认 / 非确认 —— 第 27 课已钉）
                    │
                    ▼  检票：看 Data Header 上的 DPF + SAP
  ┌─────────────────────────────────────────────────────┐
  │  短数据三姐妹（SAP 常 = 1010 Short Data）            │
  │   · SP_HEAD  状态/预编码 —— 10-bit 码就在头里       │
  │   · R_HEAD   原始短载荷 —— 后面跟 AB 块             │
  │   · DD_HEAD  已定义字符集 —— DD 说 Binary/BCD/UTF… │
  └─────────────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────────────┐
  │  IP 乘客 + 压缩登机牌（SAP = 0011 UDP/IP HC）        │
  │   · 第一个续块里放 UDP/IPv4 压缩头                   │
  │   · SAID/DAID + LLID 推导 IP；SPID/DPID 指端口      │
  │   · 真端口不够用时再挂 Extended Header              │
  └─────────────────────────────────────────────────────┘
  （另：SAP=0100 未压缩 IP based；SAP=0010 TCP HC 仅预留）
```

口诀：**先认证件（短数据三姐妹 vs IP/HC），再认车次（确认要不要回执）；别把「状态码」和「UDP 文本」当成一张票。**

### 2.2 总图：证件怎么上车

```text
  时间 →（仍坐第 27 课列车壳）

  状态 ping（常无续块）：
  [SP_HEAD]  DPF=1110 · SAP=1010 · Status/Precoded 10 bit 在头内
       （A=0 → 发完就走；A=1 → 等短数据响应子集）

  原始/已定义短报文：
  [R_HEAD 或 DD_HEAD] → [Rate 块]…（AB=后续块数）
       DPF=1110（Raw）或 1101（Defined）
       可带 SARQ；短数据侧强调 stop-and-wait

  UDP/IPv4 头压缩 IP：
  [C_HEAD 或 U_HEAD] SAP=0011
       → [第一个续块：压缩头 + 应用数据起头…]
       → [更多 Rate 块…] → [末块 + MsgCRC]
```

和「普通 IP / 短数据」对照（防混）：

| | 短数据三姐妹 | UDP/IPv4 HC | 未压缩 IP（门口） |
|--|-------------|-------------|------------------|
| 典型 DPF | `1110` / `1101` | 仍是确认 `0011` 或非确认 `0010` | 同左 |
| 典型 SAP | `1010` Short Data | `0011` UDP/IP HC | `0100` IP based |
| 头家族 | SP / R / DD_HEAD | C_HEAD / U_HEAD | C_HEAD / U_HEAD |
| 载荷直觉 | 状态在头内；或短续块 | 第一续块先放压缩头 | 续块直接装 IP/UDP |

### 2.3 和第 13 / 27 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 13 §7 | PDP 地图；短数据三姐妹门口；IP/HC 指针；Tier I/II vs III |
| 第 27 | **DLL 两条车次**（确认/非确认、ACK/NACK/SACK、TD_LC）——本课乘客坐在上面 |
| **本课** | 三头字段表 + A/SARQ + UDP HC 字段与解压常量 + 分诊 |
| 第 29（预告） | Part2/Part3 **字段文怎么查**——学会自己翻表 |

四句话串起来：

1. **车次**（确认/非确认）第 27 课已钉；本课不重画整条时间线。  
2. **证件**（DPF/SAP + 短数据头 / HC）是本课主菜。  
3. **TCP HC** 只有 SAP 预留，Part3 V1.3.1 **没有**与 UDP 对等的完整八位组表——不编造。  
4. **UDT / Tier III 控制信道短数据** → Part4 / 后课指针；业务信道 PDP 短数据仍是本课 Part3 故事。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；短数据/HC 不另开频。  
2. **多址**：仍是 **2-slot TDMA**；一个时隙跑短数据时，另一时隙可另有语音/数据。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps** 毛速率——所以 **HC 省的是 Rate 块里的宝贵字节**，不是另开一条「压缩信道」。  
4. **解调直觉**：先认 **Data Type=Data Header** → 读 **DPF / SAP** → 再决定是「头内状态码」还是「续块里压缩头/短载荷」。  
   **解不出 IP ≠ 射频一定坏了**，也可能是：SAP 不是 HC、SPID/DPID 指错、Extended Header 规则不对、或把短数据头当成了 C_HEAD。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **Short Data / 短数据** | Part3 短数据承载：状态/原始/已定义 | ≠ 「任意短一点的 IP 包」；≠ 语音 LC |
| **SP_HEAD** | Status/Precoded 头；10-bit 状态/预编码在头内；AB 常置 0 | ≠ R_HEAD；≠ 语音嵌入 GPS |
| **R_HEAD** | Raw 原始短数据头；AB=后续块数；有 SP/DP、SARQ、Bit Padding | ≠ DD_HEAD |
| **DD_HEAD** | Defined 已定义短数据头；用 **DD（6 bit）字符集**替代 SP/DP | ≠ 「随便定义的私有头」——字符集见 Part1 **9.3.38** |
| **UDT_HEAD** | Unified Data Transport 头；DPF=`0000`；控制信道故事多在 Part4 | **本课只认门口**，不展开 UDTO |
| **P_HEAD** | Proprietary 专有头；带 MFID | ≠ 标准三姐妹 |
| **Status / Precoded** | 预约定状态码（到位、告警…） | ≠ 自由文本短信 |
| **Raw** | 原始比特/字节短载荷 | ≠ 已带字符集约定的 Defined |
| **Defined** | 带字符集（Binary/BCD/UTF…）的短数据 | ≠ Raw「自己猜编码」 |
| **DPF `1101` / `1110`** | Defined / Raw·Status 短数据包格式 | ≠ 确认 `0011`、非确认 `0010` |
| **SAP `1010`** | Short Data 上层指示 | ≠ SAP `0011` UDP HC；≠ SAP `0100` IP |
| **SP / DP（短数据端口）** | 短数据头上 3+3 bit 源/目的端口 | ≠ UDP 的 SPID/DPID 索引 |
| **AB（Appended Blocks）** | 短数据后续块数；SP 时常 0；R/DD 表示跟几块 | ≠ C_HEAD 的 BF（7 bit）——家族不同，别混名硬套宽度 |
| **SARQ** | Selective ARQ：是否按块选择重传 | 与 A 组合见 Table **6.5** |
| **A + SARQ** | 00 非确认；10 整消息确认；11 确认+按块 SARQ；01 保留 | 短数据侧更常显式出现 |
| **stop-and-wait** | 短数据确认：发一趟、等回执、再发下一趟 | ≠ 复杂滑窗（本课不展开） |
| **Bit Padding** | R/DD 头上 8 bit：末块有效比特对齐/填充相关 | ≠ POC（确认/非确认头上的 Pad Octet Count） |
| **DD（charset）** | Defined Data 6-bit 字符集选择 | ≠ UDT Format（4 bit，另一张表） |
| **UDP/IPv4 HC** | 把头压缩进**第一个续块**；SAP=`0011` | ≠ 短数据；≠ 未压缩 IP |
| **SAID / DAID** | 源/目的网段索引（4 bit）；配合 LLID 推导 IPv4 | ≠ LLID 本身 |
| **SPID / DPID** | 源/目的 **UDP 端口索引**（7 bit）；`0` 表示真端口在 Extended Header | ≠ 短数据 SP/DP（3 bit） |
| **HC Opcode** | 2 bit；`00` = UDP/IPv4 Header Compression；其它保留 | 拆在两处各 1 bit（资料库 §7.1） |
| **Extended Header 1/2** | 可选 16+16：真 UDP 端口；是否出现看 SPID/DPID | ≠ 再来一个 Data Header |
| **DLL derived IP** | 解压侧用 SAID/DAID + Data Header LLID 推出 IPv4 地址 | ≠ 头里原样塞 32+32 |
| **TCP HC** | SAP=`0010` 已预留；Part3 V1.3.1 **无**对等完整字段表 | **禁止编造八位组表** |
| **LIP / 5017** | Location Information Protocol；SPID/DPID=`0000010` → UDP 5017 | 产品常叫「定位」 |
| **UTF-16BE Text / 5016** | SPID/DPID=`0000001` → UDP 5016 文本 | ≠ 短数据 Defined 的 UTF 字符集路径 |

---

## 4. 机制拆解：三姐妹 + SARQ + UDP HC

Canonical 来源：`03-数据协议/数据协议字段速览.md` **§1、§4.3–§5、§7–§9**；第 13 课 **§7**；第 27 课承载回唤；手册 **§5.3**。下列**故意不画完整 SDL**，也**不重讲**确认/非确认全时间线。

### 4.1 短数据 ≠ IP：先分家

| 问题 | 短数据路径 | IP / HC 路径 |
|------|-----------|--------------|
| 用户要什么 | 状态码、短报文、约定字符集载荷 | IP 包（定位 LIP、文本 UDP、厂商应用…） |
| 头长什么样 | SP / R / DD_HEAD | C_HEAD 或 U_HEAD（+ 可选压缩头在续块） |
| DPF 家族 | `1110` / `1101`（另：UDT=`0000` 指针） | `0011` / `0010`（确认/非确认） |
| SAP | 常 `1010` Short Data | `0011` HC 或 `0100` IP based |
| 省字节手法 | 状态直接塞进头；载荷本来就短 | **HC** 去掉重复的 IP/UDP 常量与可推导地址 |

现场仲裁句：

> 「状态码先找 SP_HEAD；自由短字节找 R/DD；说『上网传定位』才进 IP/HC——三张票，别撕成一张。」

### 4.2 短数据三姐妹字段表（必背）

引用：Part1 Tables **9.17A–C**；资料库速览 **§5.1–§5.3**。

#### 4.2.1 SP_HEAD — Status/Precoded（Table 9.17A）

| IE | Len | 岗位备注 |
|----|-----|----------|
| G/I, A | 1+1 | 目的组/个；是否请求响应 |
| AB | 2+4 | **Status/Precoded 时置 `0`**（状态在头内，通常无续块） |
| DPF / SAP | 4+4 | DPF 常为 `1110`；SAP Short Data `1010` |
| LLID Dest/Src | 24+24 | |
| Source Port (SP) | 3 | 短数据源端口 |
| Destination Port (DP) | 3 | 短数据目的端口 |
| Status/Precoded | **10** | **状态码本体** |
| Header CRC | 16 | |

```text
  幸福路径（状态 ping）：
  [SP_HEAD] 里面已经带着 10-bit 状态
       → 若 A=0：发完即结束（像非确认）
       → 若 A=1：等短数据响应（Table 6.6 子集）
```

#### 4.2.2 R_HEAD — Raw（Table 9.17B）

| IE | Len | 岗位备注 |
|----|-----|----------|
| G/I, A | 1+1 | |
| AB MSBs/LSBs | 2+4 | **后续块数** |
| DPF / SAP | 4+4 | 常 DPF=`1110`；SAP Short Data |
| LLID Dest/Src | 24+24 | |
| SP / DP | 3+3 | |
| SARQ | 1 | 是否按块选择重传 |
| Full Message Flag (F) | 1 | 有 SARQ：首次 `1`、重试 `0`；无 SARQ 置约定值 |
| Bit Padding | 8 | |
| Header CRC | 16 | |

#### 4.2.3 DD_HEAD — Defined Data（Table 9.17C）

与 R_HEAD **类似骨架**，但用 **Defined Data（DD）6 bit** 字符集选择（Binary / BCD / UTF…，Part1 **9.3.38**）**替代** SP/DP 那一对端口字段；同样含 SARQ、F、Bit Padding。

口诀：

- **SP**：码在头里，AB=0。  
- **R**：原始字节跟在后面，靠 SP/DP 找应用。  
- **DD**：跟在后面，但先靠 **DD 字符集**约定「怎么读这些字节」。

### 4.3 A + SARQ + stop-and-wait + 响应子集（回唤第 27 课）

短数据确认响应 Class/Type/Status 见 Part3 Table **6.6**（资料库 §4.3）——与第 27 课同一张实用子集：

| Class | Type | Status | Message | 含义摘要 |
|-------|------|--------|---------|----------|
| 00 | 001 | 000 | ACK | 全部块成功 |
| 01 | 000 | 000 | NACK | Illegal format |
| 01 | 001 | 000 | NACK | Packet CRC failed |
| 01 | 010 | 000 | NACK | Memory full |
| 01 | 100 | 000 | NACK | Undeliverable |
| 10 | 000 | 000 | SACK | 按 C_RDATA 位图选择重传 |

**A + SARQ**（Table **6.5**）：

| A | SARQ | 含义 |
|---|------|------|
| 0 | 0 | 非确认（无响应） |
| 0 | 1 | 保留 |
| 1 | 0 | 确认（整消息） |
| 1 | 1 | 确认 + 按块 SARQ |

岗位节奏（短数据侧规范强调）：

```text
  stop-and-wait：
  发完本趟短数据（头 ± 续块）→ 若 A=1 则站岗等 ACK/NACK/SACK
       → 若 SACK：按位图补块（F 置重试语义）→ 再等
       → 成功或失败后再考虑发下一趟
  （不要幻想无限大窗口滑窗——本课记节奏即可）
```

R_HEAD / DD_HEAD：**无 SARQ** 时 F 置约定值；**有 SARQ** 时首次 F=`1`、重试 F=`0`（Part3 正文，资料库 §4.4）。

> 回唤一句第 27 课：C_RHEAD / C_RDATA、TD_LC 留窗、T_RspnsWait 量级——机制相同家族；本课不重画列车时刻表。

### 4.4 DPF 与 SAP 速查（短数据/HC 相关）

**DPF**（Part1 Table **9.30**，摘与本课相关行）：

| Value | Meaning | 本课角色 |
|-------|---------|----------|
| 0000 | UDT | 仅指针 → Part4 / 后课 |
| 0001 | Response | 短数据确认时的响应壳 |
| 0010 / 0011 | Unconfirmed / Confirmed | IP/HC 乘客的车次 |
| **1101** | Short Data: **Defined** | DD_HEAD |
| **1110** | Short Data: **Raw or Status/Precoded** | R_HEAD / SP_HEAD |
| 1111 | Proprietary | P_HEAD 门口 |

**SAP**（Part1 Table **9.31**，摘与本课相关行）：

| Value | Meaning | 本课角色 |
|-------|---------|----------|
| 0000 | UDT | 指针 |
| **0010** | TCP/IP header compression | **仅预留；无完整表** |
| **0011** | UDP/IP header compression | **本课 HC 主菜** |
| 0100 | IP based Packet data | 未压缩 IP 门口 |
| **1010** | Short Data | **三姐妹** |

### 4.5 UDP/IPv4 头压缩（Part3 clause 7.2 / Table 7.14）

压缩头位于**第一个数据续块**；Data Header 上 **SAP = `0011`**。

为什么值得压？IPv4 头 20 字节 + UDP 头 8 字节 = 28 字节常量/半常量——在 Rate ½/¾ 块里非常贵。HC 留下真正会变的 Identification 与端口索引，地址用 **SAID/DAID + LLID** 推导，长度/校验和在接收侧重算。

#### 4.5.1 压缩头字段（资料库 §7.1）

| IE | Len | 备注 |
|----|-----|------|
| IPv4 Identification | 16 | 原样传送 |
| SAID | 4 | 源网段索引 |
| DAID | 4 | 目的网段索引 |
| HC Opcode bit1 | 1 | Opcode MSB |
| SPID | 7 | 源端口索引；`0000000` → 扩展头带真端口 |
| HC Opcode bit2 | 1 | Opcode LSB |
| DPID | 7 | 目的端口索引 |
| Extended Header 1 | 16 | 可选 UDP 端口 |
| Extended Header 2 | 16 | 可选 UDP 端口 |

**HC Opcode（2 bit）**：`00` = UDP/IPv4 Header Compression；其它保留。

#### 4.5.2 SAID / DAID / SPID / DPID 取值摘要（§7.2）

| IE | 关键值 |
|----|--------|
| SAID | `0000` Radio Network；`0001` USB(Ethernet)；`1100–1111` 厂商；其它保留 |
| DAID | 同上，另 `0010` Group Network |
| SPID/DPID | `0000000` → 真端口在 Extended Header；`0000001` → **5016** UTF-16BE Text；`0000010` → **5017** LIP；高值厂商可配 |

#### 4.5.3 Extended Header 选用（Tables 7.20 / 7.21）

| SPID | DPID | EH1 | EH2 |
|------|------|-----|-----|
| 0 | 任意 | 源 UDP 端口 | （若 DPID 也 0 → EH2=目的端口） |
| ≠0 | 0 | 目的 UDP 端口 | 不用 → 改放应用数据 |
| ≠0 | ≠0 | 不用 → 应用数据 | 不用 → 应用数据 |
| 0 | 0 | 源端口 | 目的端口 |

口诀：**索引能说清端口就别占 EH；两边都是 0 才双挂真端口。**

#### 4.5.4 解压侧常量 / 推导（§7.4 摘要）

| 字段 | 处理 |
|------|------|
| UDP Length | = 8 + User − 压缩头字节 |
| UDP Checksum | 接收侧重算（RFC 768） |
| IPv4 Version / IHL | 常量 `0100` / `0101`（IHL=5） |
| IPv4 TOS / Flags / FragOff | 规范默认（常 0） |
| IPv4 Total Length | = 20 + UDP Length |
| IPv4 TTL / Protocol | 默认；Protocol=UDP |
| IPv4 Header Checksum | 接收侧重算 |
| IPv4 Src/Dst Addr | **SAID/DAID + Data Header LLID** 推导（DLL derived IP） |

```text
  [C_HEAD/U_HEAD] SAP=0011 · LLID Dest/Src …
        │
        ▼
  [第一续块]  [IPv4 ID|SAID|DAID|Opcode/SPID|Opcode/DPID|(EH…)|应用数据…]
        │
        ▼ 接收侧拼回「像模像样的 UDP/IPv4 包」
  应用：LIP / 文本 / 厂商 UDP …
```

### 4.6 诚实边界三块（写进纪律）

**（1）TCP HC**  
SAP=`0010` 已预留；Part3 V1.3.1 **clause 7.2** 正文展开的是 **UDP/IPv4** 压缩头字段表。资料库 §9 写明：未见与 UDP 对等的完整 TCP 压缩八位组表 → **本课与资料库都不编造**。现场若产品声称 TCP HC，去问厂商实现说明书，别假装 ETSI 有一张你「记得」的表。

**（2）UDT**  
UDT_HEAD（Table 9.17D）本课**只做指针**：DPF=`0000`；含 UDT Format、Pad Nibble、AB/SF/PF、**UDT Opcode（UDTO）** 等；续/末块 UDT_LDATA。**控制信道 UDT 短数据过程 → Part4**；UDTO 取值**不在本课展开**（大纲后段 / 约第 39 课一带）。别把 UDT 和 SP/R/DD 三姐妹背成四种平行「日常短数据」。

**（3）Tier I/II vs Tier III（一行提醒，手册 §5.3 / 第 13 §7.5）**

| 能力 | Tier I / II | Tier III |
|------|-------------|----------|
| 短数据 | 多经 **业务信道 PDP（Part3）** 三姐妹 | **控制信道有自有短数据**（Part4）；业务信道仍可走 PDP |
| IP / HC | 业务信道 PDP | 业务信道 PDP（HC 故事同族） |

> 「集群控制信道短数据是 Part4；常规模式下短数据走 Part3 PDP。两边都对，路径不同。」——第 13 课原句，本课继续有效。

### 4.7 和确认/非确认列车如何叠乘（只回唤）

```text
  短数据：
    A=0 → 像「非确认」节奏（无响应）
    A=1 → 像「确认」节奏（等 Table 6.6 子集；可 SARQ）

  IP + HC：
    外层仍是 C_HEAD（DPF=0011）或 U_HEAD（DPF=0010）
    SAP=0011 只说明「第一续块有压缩登机牌」
    要不要 ACK，仍看确认/非确认车次 —— 不是「开了 HC 就自动确认」
```

---

## 5. 对照表：先前各课 → 本课角色

| 来源 | 本课用它做什么 |
|------|----------------|
| 第 13 §7.3–7.5 | 三姐妹门口、IP/HC 指针、Tier 分家 |
| 第 27 全文 | 车次（确认/非确认）、响应、TD_LC——乘客往上坐 |
| 速览 §1 | DPF/SAP 总表 |
| 速览 §4.3–4.4 | Table 6.6 子集；A+SARQ |
| 速览 §5 | SP/R/DD/UDT/P 头字段 |
| 速览 §7 | UDP/IPv4 HC 全表与解压常量 |
| 速览 §8–§9 | Data Type/DPF 速查；TCP HC / UDT 缺口声明 |
| 手册 §5.3 | Tier 数据能力一览 |
| 第 24 课 | Rate 保护权衡直觉（HC 省字节的背景） |
| 加餐 | 12.5 kHz / 4FSK / 双时隙提醒 |

---

## 6. 现场岗位对照 / 分诊

| 现场现象 | 本课解释 | 先查什么 |
|----------|----------|----------|
| 「发个到位」却去配 IP 通道 | 应用要的是 **Status/Precoded** | 写频/API 是否走 SP_HEAD；DPF 是否 `1110` 且头内 10-bit |
| 抓到 SP_HEAD 却抱怨「后面 Rate 块丢了」 | Status 常 **AB=0、无续块** | 先读 AB 与 Status 字段，再骂丢包 |
| 短报文对端乱码 | Raw vs Defined 路径混用；或 DD 字符集不一致 | DPF `1110` vs `1101`；DD 值；应用是否按约定解码 |
| 要回执的短报文却永无 ACK | A=0；或对端不支持；或 ID/CC 错 | 先读 **A / SARQ**，再查射频 |
| 开了 SARQ 仍整包重传 | 对端只回 NACK 不回 SACK；或实现未走选择重传 | 看响应 Class/Type；F 重试语义 |
| 「UDP 文本/定位失败」 | 可能 SAP 不是 `0011`；或 SPID/DPID≠5016/5017；或 EH 规则错 | Data Header SAP → 第一续块压缩头 → 端口索引 |
| 解压后 IP 地址怪异 | SAID/DAID / LLID 推导链断 | 对照 Radio Network / USB / Group Network 索引 |
| 产品说支持 TCP HC，规范里找不到表 | SAP 仅预留 | **不要编造**；问厂商说明书 |
| 集群网优与常规网优吵「短数据走哪」 | Tier 路径不同 | 问清 Tier；控制信道 → Part4；业务信道 PDP → 本课 |
| 把短数据 SP/DP（3 bit）当成 UDP SPID/DPID（7 bit） | 两套端口语义 | 先看 SAP：Short Data vs UDP HC |

写频 / 网优 30 秒话术：

> 「短数据先问要状态码还是短字节：状态码看 SP_HEAD，码在头里；短字节看 R 或 DD，DD 还多一个字符集约定。要回执就置 A，需要按块补洞再加 SARQ，短数据侧是发一趟等一趟。传 IP 定位/文本才进 UDP 头压缩：SAP=0011，第一块里是压缩登机牌，5017 是 LIP、5016 是 UTF-16BE 文本。车次还是第 27 课那两班——确认或非确认。集群控制信道短数据另翻 Part4。」

---

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
