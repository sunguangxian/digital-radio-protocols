# 第 27 课 · PDP：确认与非确认数据

> DMR 深入学习 · **阶段 D 语音与数据第 3 课**（接第 26 课「补充业务 / 迟后进入」）  
> 适合：已能背出「语音 = Header → 超帧 A–F → Terminator → Hangtime」，也知道数据主战场在 **Part 3**，但仍会把「发了个 IP 包」当成自动确认、把 **TD_LC** 当成语音 Terminator、或以为短数据/头压缩就是本课全部的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**PDP 有两条 DLL 投递：确认（挂号信+回执）vs 非确认（塞邮筒就走）；空口都是 Data Header → Rate ½/¾/1 块列车；（确认才）等响应 / 可选选择重传；IP 与短数据坐在这两条承载之上，细讲留给第 28 课**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。确认/非确认数据**不换频、不改调制、不另开带宽**——差别在「要不要回执、块里有没有 DBSN、末尾要不要等响应窗」。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是 **PDP 两条投递时间线 + 头字段对照 + 现场分诊**。

---

## 1. 为什么本课重要（动机）

第 25–26 课把语音主菜与补充加料讲完了。机房下一句要命的话往往是：

- 产品写「数据必到」——你该配确认 PDP，还是非确认再靠应用层重发？  
- 分析仪看见 **Data Header**，后面一串 Rate 块，却**永远等不到 Response**——是对端死了，还是你发的其实是 **U_HEAD（A=0）**、根本不该有 ACK？  
- 同事把语音 **Terminator with LC** 和数据 hangtime 里的 **TD_LC** 当成同一种「结束铃」——排障会指错车厢。  
- 培训台若只背「DMR 也能传数据」七个字，后面会卡在同一处：

> **PDP（Packet Data Protocol）在空口 DLL 层先选两条投递之一：确认 = 请求响应、块可带序号、可 ACK/NACK/SACK 重试；非确认 = 发完就走、无 ACK 窗。IP 包与短数据都是「坐在这两条承载上的乘客」——先认清车次（确认/非确认），再谈第 28 课的短数据头与头压缩。**

本课目标：能画出非确认与确认两条时间线；对照 C_HEAD / U_HEAD 关键字段；说清 Rate ½/¾/1 的载荷与保护权衡；认得 ACK/NACK/SACK 与 TD_LC 的岗位含义；做现场分诊与自测；并为第 28 课短数据与头压缩留好接口。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不 dump Idle 96-bit、不贴完整 SDL、不发明 ETSI 条款号（字段锚点以资料库 `03-数据协议/数据协议字段速览.md` 与 Part1 Table **9.10/9.15**、Part3 Table **6.6** 等已摘录者为准）、不把短数据三姐妹/UDP HC 字段表当成本课主菜（指针到第 28 课）、不编造 TCP HC 八位组表（SAP 有预留即可）。

---

## 2. 总图 / 故事：挂号信 vs 塞邮筒

先把整课装进两个故事，再落到资料库 `03-数据协议/数据协议字段速览.md` **§1–§4 / §6 / §8**、第 13 课 **§7** PDP 地图。

### 2.1 一句话故事：邮局两条窗口

回想第 13 课：确认像「**挂号信 + 回执**」；非确认像「**塞进邮筒就走**」。

```text
  你要寄的「信」= 用户数据（IP 包、短报文、厂商载荷…）
  邮局柜台问你：要不要回执？

  ┌─ 非确认窗口（Unconfirmed / U_HEAD）──────────────┐
  │  贴邮票（Data Header）→ 扔进邮筒（Rate 块列车）  │
  │  → 末块盖 MsgCRC → 走人，不站在窗口等回执       │
  └──────────────────────────────────────────────────┘

  ┌─ 确认窗口（Confirmed / C_HEAD）──────────────────┐
  │  贴挂号条（A=1，带 N(S)/可重同步）                │
  │  → 分装块（块内可带 DBSN）→ 末块 MsgCRC           │
  │  → 站在窗口等：ACK / NACK / SACK（可选再跟位图） │
  │  → 中继侧常留一小段数据 Hangtime（TD_LC）给回执道 │
  └──────────────────────────────────────────────────┘
```

口诀：**同一条 12.5 kHz / 双时隙铁路，两种投递条款；先问「要不要回执」，再问「车上坐的是 IP 还是短数据」。**

### 2.2 数据列车总图（两条时间线并排）

```text
  时间 →

  非确认：
  [U_HEAD] → [Rate ½/¾/1 DATA]… → [末块 + MsgCRC]
       DPF=0010 · A=0 · FMF=1
       （通常无响应窗；发完结束）

  确认：
  [C_HEAD] → [Rate 块 + DBSN+CRC-9]… → [末块 + MsgCRC]
       DPF=0011 · A=1 · 有 N(S)/FSN…
            → （等）[C_RHEAD] （可选 + [C_RDATA 重传位图]）
            → 中继模式常见 [TD_LC…] 留数据 Hangtime 给响应道
```

和语音时间线对照（防混）：

| | 语音（第 25–26 课） | 数据 PDP（本课） |
|--|-------------------|-----------------|
| 开头壳 | Voice LC Header（DT≈`0001`） | **Data Header**（DT=`0110`） |
| 中间 | 超帧 A–F 语音壳 | **Rate ½ / ¾ / 1** 数据块 |
| 结束/保留 | Terminator（组/个 FLCO）+ Hangtime | 末块 MsgCRC；确认还可等 **Response**；保留窗用 **TD_LC**（FLCO=`110000`） |
| 「迟后进入」故事 | Voice SYNC@A + 嵌入门牌 | **不适用同一套**——数据靠整段 Header+块收齐；别把 late entry 话术硬套过来 |

### 2.3 和第 13 / 25 / 26 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 13 §7 | Bearer 上确认/非确认 PDP；DPF 地图；短数据/IP 指针；Tier I/II vs III |
| 第 25–26 | 语音时间线与补充加料——本课把「语音主菜」留在身后 |
| **本课** | 两条 DLL 投递细讲 + C_HEAD/U_HEAD 对照 + 响应与 TD_LC |
| 第 28（预告） | 短数据三头 + 头压缩（UDP/IPv4）细讲 |

四句话串起来：

1. **Part2** 管语音过程；**Part3** 管 PDP / 短数据 / IP 承载过程；  
2. **确认 vs 非确认** 是 DLL 投递条款，不是「上了 IP 就自动确认」；  
3. **短数据 / HC** 是头上的 DPF/SAP 乘客类型——本课只认门口，细讲第 28 课；  
4. **Tier III** 控制信道短数据是 Part4——业务信道上的 PDP 仍是本课 Part3 故事。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；数据呼叫不另开频。  
2. **多址**：仍是 **2-slot TDMA**；一个时隙跑数据列车时，另一时隙可另有语音/数据。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps** 毛速率。  
4. **解调直觉**：先认 **Data SYNC / Data Type**（Header 壳 vs Rate 块壳）→ 再解 DPF/A/BF → 再决定「要不要等响应」。  
   **没收到 ACK ≠ 射频一定坏了**，也可能是：你发的是非确认、对端不支持确认、ID/色码不对、或数据 Hangtime（TD_LC 窗）不够。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **PDP** | Packet Data Protocol：Part3 分组数据协议 | ≠ 语音过程（Part2）；≠ 仅「IP」一词 |
| **Confirmed / 确认数据** | 请求响应；可整消息或按块重传 | ≠ 「应用层自己重发」自动等于 DLL 确认 |
| **Unconfirmed / 非确认数据** | 发完就走，无 ACK 窗 | ≠ 「一定不可靠到不能用」——适合容许丢包的周期流量 |
| **C_HEAD** | 确认数据头；DPF=`0011` | ≠ U_HEAD；≠ 短数据头 |
| **U_HEAD** | 非确认数据头；DPF=`0010`；A 固定 `0`，FMF 固定 `1` | ≠ 「没填完的确认头」 |
| **DPF** | Data Packet Format（4 bit）：包类型 | ≠ SAP；≠ CSBKO / FLCO |
| **SAP** | 上层处理/压缩类型（IP、HC、短数据…） | ≠ DPF；告诉「车上坐谁」 |
| **BF（Blocks to Follow）** | 头后面还跟几块（不含本头） | ≠ 语音超帧 A–F 的「6」 |
| **FMF** | Full Message Flag：完整首试 / 选择重传语义 | 非确认固定 `1`；确认重试时可 `0` |
| **A 位（Response Requested）** | 是否请求响应 | 非确认固定 `0`；确认常为 `1` |
| **N(S)** | 发送序号（确认头，mod 8） | 非确认头该位置为 Reserved |
| **FSN** | Fragment Sequence Number（分片，含末片语义） | ≠ DBSN（块序号） |
| **DBSN** | 确认续块里的数据块序号 + 块内 CRC-9 | 非确认续块通常整段 User，无 DBSN |
| **MsgCRC** | 整消息 32-bit CRC，落在末块 | ≠ Header CRC-16；≠ 块内 CRC-9 |
| **C_RHEAD** | 确认响应头；DPF 常为 Response=`0001`；带 Class/Type/Status | ≠ 语音 Terminator |
| **C_RDATA** | 选择重传位图（Retry Flags）+ Response CRC | 常跟在 SACK 类响应后 |
| **ACK / NACK / SACK** | 全成功 / 失败原因 / 按位图选择重传 | 见 Part3 Table **6.6** 子集 |
| **SARQ** | Selective ARQ：按块选择重传（短数据头上更常见 A+SARQ 组合） | ≠ 「只要确认就一定按块」 |
| **stop-and-wait** | 发完一趟再等回执再发下一趟（短数据侧明确） | ≠ 无限窗口滑窗（本课不展开复杂滑窗） |
| **TD_LC** | 数据 Terminator LC；FLCO=`110000`；数据 hangtime / 预留响应窗 | ≠ 语音 Terminator 的组/个 FLCO |
| **Rate ½ / ¾ / 1** | 数据块编码速率：保护多↔载荷多 | Header 在用 ¾/1 时仍常按 rate-½ 思路保护头 |
| **T_RspnsWait / T_DataHngtime** | 等响应 / BS 用 TD_LC 留窗的量级定时器（Annex A） | 本课只记岗位量级，不背全表 |
| **IP over PDP** | IP 包坐在确认或非确认承载上 | 确认与否是产品选择，不是「IP⇒确认」 |
| **Short Data** | 状态/原始/已定义短数据（DPF `1101`/`1110` 家族） | **第 28 课主菜**；本课只认门口 |

---

## 4. 机制拆解：两条投递 + 头对照 + 响应

Canonical 来源：`03-数据协议/数据协议字段速览.md` **§1–§4、§6、§8**；第 13 课 **§7**；定时器量级见 `03-数据协议/AnnexA定时器与AnnexC_IPv6.md` **Annex A**（本课只作指针）。下列**故意不画完整 SDL**。

### 4.1 PDP 是什么？和语音 Part2 差在哪？

| | Part2 语音 | Part3 PDP |
|--|-----------|-----------|
| 用户感知 | 组呼/个呼「说话」 | 传报文/IP/短状态 |
| 空口壳家族 | Voice Header / 超帧 / Terminator | **Data Header** / **Rate 块** /（数据）**TD_LC** |
| 主过程书 | TS 102 361-2 | **TS 102 361-3**（头布局多与 Part1 clause 8–9 衔接） |
| 「确认」一词 | 个呼可有 OACSU「先问在不在」 | **DLL 数据确认**：要不要 ACK/重传 |

分层直觉（第 12–13 课眼镜）：

```text
  应用 / 短数据语义 / IP 包
           │
           ▼
  Layer-3 业务（Part3 过程叙述）
           │
           ▼
  DLL 承载两条：Confirmed 或 Unconfirmed   ← 本课主线
           │
           ▼
  同一条 L1：12.5 kHz · 4FSK · 2-slot · 30 ms burst
```

### 4.2 非确认时间线：U_HEAD → 块 → MsgCRC（无 ACK 窗）

典型空口故事：

```text
  [U_HEAD]  DPF=0010 · A=0 · FMF=1 · BF=后续块数
      │
      ├─→ [Rate ½/¾/1 DATA]  …用户八位组…
      ├─→ …
      └─→ [末块 LDATA] … + MsgCRC(32)
           （通常到此结束；不站岗等 C_RHEAD）
```

岗位要点：

1. **A=0、FMF=1** 是资料库对照表里的固定语义——别指望对端「好心回一个 ACK」。  
2. 续块多为整段 **User**（无 DBSN）；末块带 **MsgCRC** 做整消息校验。  
3. 适合：周期 GPS/遥测洪泛、容许偶发丢失、组播「能收到最好」类流量（产品文档常写 unconfirmed / no retries）。  
4. RMHAM《IP DATA OVER DMR》课堂幻灯的对照语感：**Unconfirmed = no retries**；可对 talkgroup；**Confirmed = ACK + retries**，更常一对一——幻灯是教具，**硬字段仍以 ETSI / 资料库为准**。

### 4.3 确认时间线：C_HEAD → 带号块 → 等响应（可选选择重传）

```text
  [C_HEAD]  DPF=0011 · A=1 · FMF（首试常 1）· BF · S · N(S) · FSN …
      │
      ├─→ [Rate DATA]  DBSN + CRC-9 + User …
      ├─→ …
      └─→ [末块] … + MsgCRC
           │
           ▼  等响应（量级：T_RspnsWait 建议约 180 ms；同播可更长）
      [C_RHEAD]  Class / Type / Status
           │
           ├─ ACK  → 整消息成功，结束本趟
           ├─ NACK → 格式/CRC/内存/不可达等失败语义
           └─ SACK → 常再跟 [C_RDATA] 64-bit Retry Flags 位图
                      发送方按位图重发缺块；选择重传时 FMF 可置 0
```

中继模式下，BS 常用 **TD_LC**（Data Type = Terminator with LC，FLCO=`110000`）在数据后留一小段 **T_DataHngtime**（建议约 **180 ms**，约 3 个业务突发量级）——给对端回 **C_RHEAD** 腾道。  
这不是语音 Hangtime 的「同组礼貌说话窗」翻版口号，但**岗位直觉相近**：灯还亮着，是为了让回执有路可走。

重试上限量级：**N_RtryLmt** 建议 max **8**（Annex A）——记「不是无限重试」，精确配置看实现与产品。

### 4.4 C_HEAD vs U_HEAD 字段对照（必背表）

两端头均为 **96 bits**（Part1 Tables **9.10 / 9.15**；资料库 §2）。

| IE | 确认 C_HEAD | 非确认 U_HEAD |
|----|-------------|---------------|
| G/I | 目的是否组 | 同左 |
| **A（Response Requested）** | 是否请求响应（确认语义） | **固定 `0`** |
| DPF | **`0011` Confirmed** | **`0010` Unconfirmed** |
| SAP | 上层（IP/HC/短数据…） | 同左 |
| LLID Dest / Src | 24+24 | 同左 |
| **FMF** | 首试/重试语义 | **固定 `1`** |
| BF | 后续块数 | 同左 |
| **S + N(S)** | 有（重同步 + 发送序号） | **无 → Reserved 4 bit=0** |
| FSN | 分片序号 | 同左 |
| Header CRC | 16-bit | 同左 |

八位组直觉（确认头，资料库 §2.2）：

```text
  [G/I|A|0|POC_msb| DPF ][ SAP | POC_lsb ][ Dest LLID 24 ][ Src LLID 24 ]
  [FMF| BF 7 ][ S | N(S) 3 | FSN 4 ][ Header CRC 16 ]
```

非确认：把 **A 钉死 0、FMF 钉死 1、S/N(S) 换成 Reserved**——分析仪上「长得很像却差这几位」，就是两条车次的分水岭。

### 4.5 Rate ½ / ¾ / 1：载荷 vs 保护（直觉即可）

同一条毛速率管道上，编码速率越高，**每块用户比特越多、保护越少**（原则课第 24 课；本课不贴矩阵）。

| 速率 | 岗位语感 | 确认续块里常见「多出来」的东西 |
|------|----------|--------------------------------|
| **Rate ½** | 保护更狠，载荷更省 | DBSN+CRC-9 占掉一部分；User 更短 |
| **Rate ¾** | 折中 | 同上结构，User 更长 |
| **Rate 1** | 载荷更猛，信道差时更脆 | User 最长一档 |

资料库 §3 对照摘要（记结构，不背每个 bit）：

| PDU | 确认 | 非确认 |
|-----|------|--------|
| Rate ¾ DATA | DBSN+CRC-9+User(128) | User 144 |
| Rate ½ DATA | DBSN+CRC-9+User(80) | User 96 |
| Rate 1 DATA | DBSN+CRC-9+User(176) | User 192 |
| 各档 LDATA（末块） | 再加 **MsgCRC(32)**（User 再短一截） | 末块 User+MsgCRC |

**头保护提醒**：即便后续块跑 Rate ¾/1，**Data Header 仍常按 rate-½ 编码保护**（工程/规范同向的常见说法）——排障时「头比身子脆还是身子比头脆」要分开看：头 CRC 失败整趟可能起不来；身子单块坏了，确认模式才有机会 SACK 补洞。

### 4.6 响应表：ACK / NACK / SACK（实用子集）

C_RHEAD 带 **Class(2) / Type(3) / Status(3)**。短数据响应集见 Part3 Table **6.6**（亦为更广响应集的子集；完整叙述见 Part1 **8.2.2.3** 一带指针）。岗位先认这几行：

| Class | Type | Status | Message | 白话 |
|-------|------|--------|---------|------|
| 00 | 001 | 000 | **ACK** | 全部块成功 |
| 01 | 000 | 000 | **NACK** | Illegal format |
| 01 | 001 | 000 | **NACK** | Packet CRC failed（MsgCRC 等） |
| 01 | 010 | 000 | **NACK** | Memory full |
| 01 | 100 | 000 | **NACK** | Undeliverable |
| 10 | 000 | 000 | **SACK** | 按 **C_RDATA** 位图选择重传 |

**A + SARQ**（Table **6.5** 语感，短数据头上更常显式出现）：

| A | SARQ | 含义 |
|---|------|------|
| 0 | 0 | 非确认（无响应） |
| 1 | 0 | 确认（整消息） |
| 1 | 1 | 确认 + 按块 SARQ |

短数据侧规范强调 **stop-and-wait**——发一趟、等回执、再发下一趟。本课记岗位节奏即可；短数据三头字段表进第 28 课。

### 4.7 IP / 短数据坐在承载之上（只认门口）

```text
  ┌─ SAP / DPF 告诉「乘客类型」─────────────────────┐
  │  SAP=0100 IP based · 0011 UDP/IP HC · 1010 Short │
  │  DPF=0010/0011 仍是「确认/非确认车次」            │
  │  DPF=1101/1110 短数据头家族 → 第 28 课            │
  └──────────────────────────────────────────────────┘
           坐在
  Confirmed 或 Unconfirmed  DLL 承载上
```

硬规矩：

- **不要**背「上了 IP 就一定是确认」——确认/非确认是产品与可靠性选择。  
- **不要**在本课展开 UDP HC 的 SAID/DAID/SPID 全表（资料库 §7 有，第 28 课加厚）。  
- **TCP HC**：SAP=`0010` 已预留；Part3 V1.3.1 **未见**与 UDP 对等的完整 TCP 压缩八位组表 → **不编造**。

### 4.8 Tier I/II vs III：一行提醒

| | Tier I/II（常规） | Tier III（集群） |
|--|------------------|------------------|
| 短数据 / IP | 多经 **业务信道 PDP（Part3）** | **控制信道**可有自有短数据（**Part4**）；业务信道仍可走 PDP |
| 本课主线 | **业务信道上的确认/非确认 PDP** | 同上（业务信道）；控制信道故事不抢戏 |

口诀（第 13 课原句加厚）：**常规事事问 Part3；集群控制信道短数据还要翻 Part4——两边都对，路径不同。**

### 4.9 TD_LC：数据的「留灯」，不是语音 Terminator 翻版

| IE 要点 | 值 / 语义 |
|---------|-----------|
| Data Type | Terminator with LC |
| FLCO | **`110000`**（TD_LC） |
| 还带 | Dest/Src LLID、G/I、A、FMF、S、N(S) 等与数据呼叫相关的影子字段 |

对比：

| | 语音 Terminator | TD_LC |
|--|-----------------|-------|
| FLCO | 组呼/个呼等 Voice Channel User | **固定 `110000`** |
| 岗位用途 | EOT、语音 Hangtime 礼貌窗 | **数据 hangtime / 预留确认响应道** |
| 误判 | 「通话结束」 | 「数据结束且可能还在等 ACK」 |

---

## 5. 对照表：先前各课 → 本课角色

| 角色 | 空口形态 | 你用哪一课的眼镜看 |
|------|----------|-------------------|
| 业务地图 | Bearer 上确认/非确认 | 第 13 §7 |
| 语音时间线（对照用） | Header→超帧→Term→Hangtime | 第 25–26 |
| 数据头类型 | Data Header DT=`0110`；DPF | 资料库 §1 / §8；本课 §4.4 |
| 续块家族 | Rate ½/¾/1 + 末块 MsgCRC | 资料库 §3；本课 §4.5 |
| 响应 | C_RHEAD / C_RDATA | 资料库 §4；本课 §4.6 |
| 数据留窗 | TD_LC | 资料库 §6；本课 §4.9 |
| 定时器量级 | T_RspnsWait / T_DataHngtime / N_RtryLmt | Annex A 指针 |
| 短数据 / HC | DPF/SAP 门口 | **第 28 课** |
| 保护原则 | 不贴矩阵 | 第 24 课原则 |

---

## 6. 现场岗位对照 / 分诊

| 现场现象 | PDP 解释 | 先查什么 |
|----------|----------|----------|
| 产品说「数据必到 / 必须有回执」 | 应走 **Confirmed（C_HEAD，A=1）** | 写频/API 是否真开确认；空口 DPF 是否 `0011` |
| 周期 GPS 洪泛、丢一两个点可接受 | 常走 **Unconfirmed（U_HEAD）** | 别强行开确认把信道打满重传 |
| 分析仪有 Data Header + Rate 块，**永远无 Response** | 可能本就是 **U_HEAD（A=0）**；或对端不支持确认；或 ID/CC 错 | 先读 **DPF 与 A 位**，再骂射频 |
| 确认呼叫发出后对端偶发 SACK | 正常：按位图补洞 | 看 C_RDATA Retry Flags；弱场/干扰 |
| 确认呼叫反复 NACK「Packet CRC failed」 | MsgCRC/整包校验失败 | 载荷长度/POC、末块是否截断、干扰 |
| 中继上确认数据发出后立刻被别的业务抢走 | 可能 **TD_LC / T_DataHngtime** 窗不够或未留 | 抓有没有 Terminator with LC 且 FLCO=`110000` |
| 把语音 Terminator 当成数据结束 | FLCO 家族不同 | 语音组/个 FLCO vs **TD_LC=`110000`** |
| 「IP 传定位失败」就去改语音 Hangtime | 改错旋钮 | 先分语音 Hangtime vs **数据 Hangtime（TD_LC）** |
| 集群同事说「控制信道天天短数据」 | Tier III Part4 路径 | 问清 Tier；业务信道 PDP 仍可用本课眼镜 |
| 解码器显示 Rate ¾ 但头解不出 | 头/身编码速率策略不同 | Header 与续块分开看 CRC |

写频 / 网优 30 秒话术：

> 「数据先问要不要回执。不要回执：贴 U_HEAD，块发完带 MsgCRC 就走。要回执：贴 C_HEAD，块上带序号，对端回 ACK/NACK，缺块就 SACK 补洞；中继还会用 TD_LC 留一小段灯给回执。IP 和短数据都是坐车的乘客——车次（确认/非确认）选错了，乘客再高级也到不了。」

---

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
