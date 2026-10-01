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

