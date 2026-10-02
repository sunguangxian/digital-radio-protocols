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
