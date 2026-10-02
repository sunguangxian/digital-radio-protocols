# 第 29 课 · Part2/Part3 字段文怎么查

> DMR 深入学习 · **阶段 D 语音与数据第 5 课**（接第 28 课「短数据与头压缩」）  
> 适合：已经跟过语音补充业务、确认/非确认 PDP、短数据三姐妹与 UDP HC，但一打开 ETSI PDF 或资料库字段文就迷路——分不清该翻 FLCO 还是 CSBKO、该查 DPF 还是 SAP、总索引关键词表到底怎么用——的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**三层书架（总索引 → 字段速览 → 官方 PDF）+ 查表路径（现象→关键词→打开哪篇→哪一节→何时回 PDF）**」练成肌肉记忆  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。**查字段文不会改频、改调制、改带宽**——翻错书（Part4 当 Part3、Part2 当 Part1）也不等于射频坏了。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是 **图书馆技能：怎么进 Part2/Part3 字段速览与总索引**。

---

## 1. 为什么本课重要（动机）

第 25–28 课把「语音补充、确认车次、短数据证件、HC 登机牌」都讲过了。机房下一句要命的话往往是：

- 同事问：「个呼没应答，是看 UU_V_Req 还是看 NACK？」——你记得课里讲过，但**打开哪一节**？  
- 分析仪吐出 FLCO=`000100`——Talker Alias header？还是去翻 CSBKO 表？  
- 确认数据没 ACK——该开 Part3 §2/§4，还是先骂天线？  
- DPF=`1110` 且后面没有 Rate 块——你记得第 28 课是 SP_HEAD，但**资料库哪一行**能一秒钉死？  
- 新人把 Tier II 业务信道短数据翻到 Part4 UDT——整晚对不上字段。

培训台若只背「去看 Part2 / Part3」六个字，后面会卡在同一处：

> **会背字段名 ≠ 会查字段文。** Part2 管语音业务 PDU 与 Opcode；Part3 管数据业务字段与短数据/HC；外壳（EMB/SLOT/Data Type）仍在 Part1。总索引是「我想查什么」的门牌；字段速览是结构化货架；官方 PDF 是硬出处。本课练的是**路径**，不是把第 25–28 课字段再 dump 一遍。

本课目标：能画出三层书架与决策树；会按 FLCO/CSBKO/DPF/SAP/现象三种入口进速览；分清 Part2≠Part1 壳、Part3≠Part4 UDT、TCP HC 仅预留、缺口节不可发明；用总索引 §2/§4 做 6–8 道查表操练；做现场分诊、七则例子与自测；并为第 30 课「跟一次语音呼叫空口」留好翻书肌肉。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不 dump Idle 96-bit、不贴完整 SDL、不发明 ETSI 条款号（入口锚点以资料库 `02-语音业务/语音业务字段速览.md` **§1–§9**、`03-数据协议/数据协议字段速览.md` **§1–§9**、`总索引.md` **§0–§5** 已有编号为准）、**不重讲第 27 课确认/非确认全时间线**、**不重讲第 28 课三姐妹字段全表**（只短提醒）、**不从缺口节编造缺失表**、**不把 Part4 当 Part3 日常入口**。

---

## 2. 总图 / 故事：「三层书架」

先把整课装进一个故事，再落到 `总索引.md`、`语音业务字段速览.md`、`数据协议字段速览.md`。

### 2.1 一句话故事：门牌 → 货架 → 库房

把资料库想成一间小图书馆：

```text
  ╔══════════════════════════════════════════════════════╗
  ║  第一层 · 总索引.md（门牌 / 检索台）                 ║
  ║   「我想查什么」→ 关键词表 §2 → 打开哪篇文件         ║
  ║   角色最小打开集 §4 → 新人/语音/数据各开哪几本       ║
  ╠══════════════════════════════════════════════════════╣
  ║  第二层 · 字段速览（结构化货架）                     ║
  ║   Part2：02-语音业务/语音业务字段速览.md §1–§9       ║
  ║   Part3：03-数据协议/数据协议字段速览.md §1–§9       ║
  ║   （外壳详表仍在 01-空中接口/ …）                    ║
  ╠══════════════════════════════════════════════════════╣
  ║  第三层 · 官方 PDF（库房硬出处）                     ║
  ║   Part2 V2.5.1 · Part3 V1.3.1 · Part1 V2.7.1         ║
  ║   实现 / 认证 / 争议 → 回 PDF；笔记冲突以 TS 为准    ║
  ╚══════════════════════════════════════════════════════╝
```

口诀：**先问门牌（总索引），再上货架（速览），最后进库房（PDF）。别一上来把 Part2 全文 PDF 从头读到尾。**

### 2.2 决策树：现象 → 关键词 → 打开哪篇 → 哪一节 → 何时回 PDF

```text
  现场现象 / 分析仪字段
           │
           ▼
  ┌─ 我能说出关键词吗？（个呼 / FLCO / DPF / 无ACK / Late entry …）
  │         是 → 总索引 §2 关键词表 → 得到「去哪」
  │         否 → 总索引 §4 角色最小打开集 → 先摸岗位书架
  ▼
  打开字段速览（Part2 或 Part3）
           │
           ▼
  ┌─ 入口怎么选？
  │   · 有 Opcode 值？→ Part2 §1（FLCO/CSBKO/SLCO）
  │   · 有 DPF/SAP？→ Part3 §1（+ 需要时 Part1 Table 9.30–9.31）
  │   · 只有现象？→ Part2 §2 过程对照 / Part3 §8 Data Type 速查
  │   · 知道 PDU 名？→ Part2 §3–§5 / Part3 §2–§7 按名跳节
  ▼
  速览表里字段够不够？
           │
    够 → 现场结论 / 写笔记
    不够 / 有争议 / 要认证 → 第三层官方 PDF（同目录）
    速览写了「缺口」→ 诚实停住；回 PDF 或后课，不编造
```

### 2.3 和第 11 / 13 / 25–28 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 11 | 语音过程粗地图（组呼/个呼时间线）——本课教**去哪翻**对应字段 |
| 第 13 | PDP 地图与短数据门口——本课教 Part3 速览入口 |
| 第 25–26 | 补充业务 / Late Entry / Talker Alias——本课教 Part2 §7 + §1 Opcode 入口 |
| 第 27 | 确认/非确认车次——本课教 Part3 §2/§4 查 ACK/NACK/SACK，不重画时间线 |
| 第 28 | 三姐妹 + UDP HC——本课教 Part3 §5/§7 怎么进，不 dump 全字段 |
| **本课** | **三层书架 + 查表路径 + 操练** |
| 第 30（预告） | 小综合：跟一次语音呼叫空口——用本课肌肉当场翻表 |

四句话串起来：

1. **总索引**回答「打开哪篇」；**速览**回答「打开哪一节」；**PDF**回答「硬字段与争议」。  
2. **Part2** 是语音业务货架；**Part3** 是数据业务货架；**Part1** 是突发外壳与 Data Type/DPF/SAP 硬表。  
3. **缺口节**是诚实边界，不是「自己补全」的邀请函。  
4. **翻错书 ≠ 射频坏了**——先纠路径，再谈 12.5 kHz / 4FSK。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；查表本身不占频谱。  
2. **多址**：仍是 **2-slot TDMA**；一个时隙查语音字段时，另一时隙可能在跑数据——别把「查 Part2」和「查 Part3」当成同一时隙互斥故事。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps** 毛速率——字段文写的是**比特语义**，不是另开一条「文档信道」。  
4. **解调直觉**：空口先认 **Data Type / SYNC / EMB**（Part1）→ 再决定上 Part2 还是 Part3 货架。  
   **翻错书 ≠ 弱场**，也可能是：把 EMB 当 FLCO、把 Part4 UDT 当 Part3 短数据、把 Service Options 当 CSBKO。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **总索引** | `dmr/总索引.md`：门牌 + 关键词表 + 角色最小打开集 | ≠ 字段速览本身；≠ 手册全文 |
| **字段速览** | Part2/Part3 结构化字段笔记（§1–§9） | ≠ 官方 PDF 全文；冲突以 TS 为准 |
| **三层书架** | 总索引 → 速览 → PDF | ≠ 「只读 PDF」或「只读笔记」二选一 |
| **FLCO** | Full LC Opcode（Part2 Annex B / 速览 §1.1） | ≠ CSBKO；≠ DPF |
| **CSBKO** | CSBK Opcode（速览 §1.2） | ≠ FLCO；≠ SLCO |
| **SLCO** | Short LC Opcode（CACH；速览 §1.3） | ≠ Full LC |
| **DPF** | Data Packet Format（Part1 Table 9.30；Part3 速览 §1） | ≠ SAP；≠ FLCO |
| **SAP** | Service Access Point（Part1 Table 9.31） | ≠ DPF；决定上层/压缩类型 |
| **Service Options** | 语音 LC/CSBK 里 8-bit 业务选项（Part2 速览 §6） | ≠ Answer Response；≠ Reason Code |
| **缺口节** | 速览 §9：诚实标明未展开项 | ≠ 「可以自己发明表」 |
| **硬出处** | ETSI PDF 同目录副本 | 笔记是学习整理；实现/认证以 PDF 为准 |
| **角色最小打开集** | 总索引 §4：按新人/空口/语音/数据/集群各开几本 | ≠ 「把仓库全读完」 |

---

## 4. 机制拆解：查表路径

### 4.1 总索引怎么进（30 秒 + 关键词 + 角色）

打开 `dmr/总索引.md`，先看三块（编号以库内为准）：

| 节 | 用途 | 本课怎么用 |
|----|------|------------|
| **§0** 30 秒怎么用 | 新人/墙上速查/附录覆盖/关键词入口 | 迷路时先回这里 |
| **§1** 文档目录 | 按文件夹列 md + PDF | 确认「语音速览在 02/」「数据速览在 03/」 |
| **§2** 关键词 → 文档 | 物理/语音/数据/集群/TR 五张检索表 | **日常主入口** |
| **§3** 官方 PDF 版本 | Part1 V2.7.1、Part2 V2.5.1、Part3 V1.3.1… | 报版本号、对争议 |
| **§4** 角色最小打开集 | 新人 / 空口 / 语音 / 数据 / 集群 | 岗位培训起点 |
| **§5** 刻意不收入 | FEC 矩阵、Idle 转储等 | 提醒本课硬禁令 |

**语音侧**关键词（总索引 §2「语音 / 补充业务」摘要）：个呼、组呼、迟后进入、主叫识别、FLCO、CSBKO、Service Options → **语音业务字段速览**。  
**数据侧**关键词：PDP、确认/非确认、C_HEAD、U_HEAD、DPF、SAP、短数据、UDP/IPv4 头压缩 → **数据协议字段速览**。

### 4.2 Part2 字段文怎么查（走一遍 TOC）

文件：`02-语音业务/语音业务字段速览.md`  
源声明：ETSI **TS 102 361-2 V2.5.1 (2023-05)**；公共外壳见 Part1 与 `01-空中接口/CSBK与LC字段详表.md`。

| 速览节 | 标题（库内） | 什么时候进 |
|--------|--------------|------------|
| **§1** | Opcode 速查（Annex B） | 手里有 FLCO/CSBKO/SLCO **数值** |
| **§1.1** | FLCO Table B.1 | Grp/UU Voice User、Talker Alias、GPS、TD_LC 指针 |
| **§1.2** | CSBKO Table B.2 | UU_V_Req/Ans、NACK、BS_Dwn_Act、Pre_CSBK、CT_CSBK |
| **§1.3** | SLCO Table B.3 | Nul_Msg / Act_Updt |
| **§2** | 语音呼叫过程与空口 PDU 对照 | **只有现象**（个呼检查、语音开始/结束、扫描前导） |
| **§3** | Full LC 业务 PDU | 已知 PDU 名：Grp_V_Ch_Usr / UU_V_Ch_Usr / GPS / Talker Alias |
| **§4** | CSBK 业务 PDU | 已知 CSBK 名：UU_V_Req、NACK_Rsp… |
| **§5** | Short LC（CACH） | 时隙活动、哈希地址、紧急活动 ID |
| **§6** | Service Options 与相关 IE | Emergency / Broadcast / Priority / Answer / Reason |
| **§7** | 补充业务相关字段 | Late Entry、Talker Alias、Emergency…概念→字段落点 |
| **§8** | 语音 Terminator 要点 | Data Type=`0010`；与 TD_LC 分家 |
| **§9** | 缺口 | CT_CSBK 全状态机、Privacy、Tier III 建链等——**停** |

**三种入口（必背）**：

```text
  A. 按 Opcode 值
     分析仪：FLCO=000100 → §1.1 → Talker_Alias_hdr → 需要字段细节再 §3.4
     分析仪：CSBKO=000100 → §1.2 → UU_V_Req → §4.2

  B. 按现象 / 过程阶段
     「个呼存在性检查没应答」→ §2 表「个呼存在性检查」行
       → UU_V_Req / UU_Ans_Rsp / NACK → 再进 §4.2–§4.4

  C. 按 PDU 名
     同事说「看一下 Pre_CSBK」→ §4.5；「Service Options Emergency」→ §6.1
```

**Part2 边界提醒（写进纪律）**：

- EMB / SLOT / Data Type / 突发壳 → **Part1**（`帧结构与字段定义.md`、`CSBK与LC字段详表.md`），不是 Part2 速览主战场。  
- FLCO=`110000` **TD_LC** 在 Part2 §1.1 只是对照指针——数据终止细节在 **Part3 §6**。  
- Tier III 控制信道语音建立（C_GRANT 等）→ **Part4** 集群速览；Part2 §9 已写缺口。

### 4.3 Part3 字段文怎么查（走一遍 TOC）

文件：`03-数据协议/数据协议字段速览.md`  
源声明：ETSI **TS 102 361-3 V1.3.1 (2017-10)**；头/块位宽硬表多在 **Part1 clause 8–9**。

| 速览节 | 标题（库内） | 什么时候进 |
|--------|--------------|------------|
| **§1** | 与 Part1 的衔接 | 手里有 **DPF / SAP**；或要确认 Data Type 角色 |
| **§2** | C_HEAD / U_HEAD 逐比特 | 确认 vs 非确认头字段差（A/FMF/S/N(S)…） |
| **§3** | 续块 / 末块载荷 | Rate ½·¾·1；DBSN / MsgCRC 差别 |
| **§4** | 确认响应（C_RHEAD / C_RDATA） | 无 ACK、NACK、SACK、Class/Type/Status |
| **§5** | 短数据头 | SP / R / DD_HEAD（+ UDT/P 指针）——第 28 课货架 |
| **§6** | TD_LC | 数据 hangtime Terminator |
| **§7** | UDP/IPv4 压缩头 | SAID/DAID/SPID/DPID / EH——第 28 课货架 |
| **§8** | 数据呼叫与 Data Type 速查 | **只有现象**时的总表入口 |
| **§9** | 缺口 | TCP HC 无完整表、UDT Opcode→Part4、ARP 未展开——**停** |

**三种入口（必背）**：

```text
  A. 按 DPF / SAP
     DPF=0011 → 确认数据 → §2 C_HEAD + §3 续块 +（要回执）§4
     DPF=1110 + 无续块 → §5.1 SP_HEAD（别先骂丢包）
     SAP=0011 → §7 UDP HC；SAP=0010 → §9 诚实：仅预留，不编造 TCP 表

  B. 按现象
     丢包 / 无 ACK / 解不出 IP / 状态码
       → §8 总表定 PDU 家族 → 再进 §2/§4/§5/§7

  C. 硬出处何时回 Part1
     三头位宽、DPF/SAP 枚举争议 → Part1 Tables **9.17A–C** / **9.30–9.31**
     （速览 §1/§5 已指向；实现认证以 PDF 为准）
```

**Part3 边界提醒（写进纪律）**：

- 业务信道短数据（三姐妹）≠ **Part4 UDT/控制信道**短数据过程。  
- TCP HC：SAP 有编码，Part3 V1.3.1 **无**与 UDP 对等完整八位组表 → **不编造**（§9）。  
- C_HEAD/U_HEAD 外壳 Data Type=`0110` 的定义在 Part1；Part3 讲业务语义与过程字段。

### 4.4 边界对照一张表（防串架）

| 问题 | 正确书架 | 常见错架 |
|------|----------|----------|
| EMB / Colour Code / Data Type 枚举 | Part1 帧结构 / CSBK详表 | 在 Part2 里找「突发壳」 |
| FLCO / 语音 Service Options / UU_V_Req | Part2 速览 | 在 Part3 里找个呼 CSBK |
| C_HEAD / DPF / 短数据三姐妹 / UDP HC | Part3 速览（+ Part1 硬表） | 在 Part2 里找 Data Header |
| Tier III 控制信道 UDT Opcode | Part4 | 在 Part3 §5.4 指针处硬编 UDTO 表 |
| TD_LC（数据终止） | Part3 §6（Part2 §1 仅对照） | 当成 Grp_V_Ch_Usr Terminator |
| 缺口节写「未展开」 | 回 PDF / 后课 | 自己补一张「看起来合理」的表 |

### 4.5 总索引实操：查表操练（8 题，含答案）

做题时请真的打开文件路径；答案只作对拍。

**操练 1.** 关键词「迟后进入」——总索引 §2 指向哪？再进 Part2 哪一节概念落点？

<details><summary>答案</summary>

总索引 §2「语音 / 补充业务」→ **语音业务字段速览**。概念落点在 Part2 速览 **§7**（Late Entry → Voice SYNC + 地址 LC）；过程对照见 **§2**；空口细节回 Part1（速览已注 Part1 5.1.2）。

</details>

**操练 2.** 手里 CSBKO=`100110`，第一步开 Part2 哪一小节？PDU 别名是什么？

<details><summary>答案</summary>

Part2 速览 **§1.2** → **NACK_Rsp**；字段细节再进 **§4.4**。

</details>

**操练 3.** 现象「确认数据发出后对端无响应」——Part3 先看哪两节？

<details><summary>答案</summary>

先 **§2**（C_HEAD 上 A/FMF/S/N(S) 是否像确认头）+ **§4**（C_RHEAD Class/Type/Status、有无 C_RDATA/SACK）；§8 可作总表入口。不要一上来只查 §7 HC。

</details>

**操练 4.** DPF=`1110` 且 AB/后续块迹象为无——进 Part3 哪一小节？和「丢了 Rate 块」怎么分？

<details><summary>答案</summary>

**§5.1 SP_HEAD**：Status/Precoded 在头内，AB 常置 0。先认证件再谈丢包——这是第 28 课纪律，本课练的是**进 §5.1 的路径**。

</details>

**操练 5.** 新人岗位「只做语音业务」——总索引 §4 最小打开集是什么？

<details><summary>答案</summary>

**语音字段速览 → Part2 PDF**（总索引 §4「语音业务」行）。需要外壳时再补 Part1 帧结构/CSBK详表。

</details>

**操练 6.** 要查「UDP/IPv4 头压缩」——总索引关键词去哪？Part3 哪一节？TCP HC 呢？

<details><summary>答案</summary>

总索引 §2「数据 / PDP / IP」→ 数据协议字段速览；细表在 Part3 **§7**。TCP HC：SAP=`0010` 仅预留 → 看 **§9 缺口**，**不编造**表。

</details>

**操练 7.** Service Options 的 Emergency 比特——Part2 哪一节？和 Act_Updt 紧急活动 ID 是否同一张表？

<details><summary>答案</summary>

Emergency 比特在 Part2 **§6.1 Service Options**。Act_Updt 的紧急活动编码在 **§5.2** Activity ID 表——相关但**不是同一张表**；§7 补充业务表把两者都挂到「Emergency」概念下。

</details>

**操练 8.** 同事在 Part4 里找 Tier II 业务信道 SP_HEAD——错在哪一层书架？应回哪？

<details><summary>答案</summary>

错在**第一层选书**：业务信道 / Tier I·II 短数据 → Part3 速览 §5；Part4 是集群/控制信道 UDT 主战场。总索引 §2 已把「短数据、UDT（常规数据面）」指向数据速览，并注明集群 UDT 见 Stun_DGNA_UDT。

</details>

---

## 5. 对照表：先前各课 → 本课查表角色

| 主题 | 先前课（会什么） | 本课查表入口（怎么找） |
|------|------------------|------------------------|
| 组呼/个呼 Voice LC | 第 11 | Part2 §1.1 + §3.1/§3.2；过程 §2 |
| 个呼 OACSU / NACK | 第 11 / 25 | Part2 §2 + §4.2–§4.4 |
| Late Entry | 第 26 | Part2 §7 + §2；外壳 Part1 Voice SYNC |
| Talker Alias / GPS | 第 26 | Part2 §1.1 FLCO 000100–001000 → §3.3–§3.5 |
| Service Options | 第 11/26 | Part2 §6 |
| Pre_CSBK / BS_Dwn_Act / Act_Updt | 第 26 | Part2 §4.1/§4.5、§5 |
| 确认/非确认 PDP | 第 27 | Part3 §2/§3/§4/§8（不重画时间线） |
| 短数据三姐妹 | 第 28 | Part3 §5（路径课，不 dump 全字段） |
| UDP/IPv4 HC | 第 28 | Part3 §7；TCP→§9 |
| 「打开哪篇」 | （新） | **总索引 §2 / §4** |

咬合原则：**内容课负责「是什么」；本课负责「去哪翻」。** 两者都要，缺一不可。

---

## 6. 现场岗位对照 / 分诊

| 岗位 / 现象 | 先问 | 打开 | 别急着 |
|-------------|------|------|--------|
| 写频 / 产品 | 语音还是数据？Tier II 还是 III？ | 总索引 §4 → 对应速览 | 把白皮书当字段表 |
| 空口分析 | Data Type / SYNC 认出来了吗？ | Part1 帧结构 → 再分流 Part2/3 | 直接在 Part2 找 EMB |
| 个呼无应答 | 有没有 UU_V_Req？Ans 还是 NACK？ | Part2 §2 → §4.2–§4.4 | 先换天线 |
| 听半截才进组 | Late entry？有无 Voice SYNC@A + LC？ | Part2 §7 + Part1 | 当成 hangtime 配错唯一原因 |
| 屏上无主叫名 | Talker Alias FLCO 段有没有？ | Part2 §1.1 → §3.4–§3.5 | 怪显示驱动之前不查 Opcode |
| 确认数据无 ACK | C_HEAD.A？对端 C_RHEAD？ | Part3 §2 + §4 | 先查 §7 HC |
| 「短消息」失败 | 状态码 / Raw / Defined / UDP 文本？ | Part3 §5 vs §7（证件分家） | 三种证件当一种 |
| 解不出 IP | SAP 是不是 `0011`？SPID/DPID/EH？ | Part3 §7；对照第 28 课 | 当射频故障 |
| 集群台短状态 | 控制信道还是业务信道？ | 控制→Part4；业务→Part3 §5 | 两套书搅一锅 |
| 争议字段位宽 | 速览不够 | 同目录 PDF；Part1 9.17A–C / 9.30–9.31 | 用博客/代码覆盖 TS |

**分诊口诀**：证件/Opcode → 速览节 →（不够）PDF →（仍像射频）再测场强与天线。

---

## 7. 工作例子（7 则）

### 例子 A · 个呼无应答

```text
  现象：主叫按了个呼，对端不响；分析仪偶发 CSBK
  路径：总索引「个呼」→ Part2 速览
        §2「个呼存在性检查」→ UU_V_Req / UU_Ans_Rsp / NACK
        → §4.2–§4.4 看 Target、Answer Response、Reason Code
  结论线索：
    · 有 Req 无 Ans → 对端未听清/未开机/未在网
    · 有 NACK_Rsp → 读 Reason / Service Type（=被拒 CSBKO）
  别做：在 Part3 里找「语音应答码」
```

### 例子 B · Late entry

```text
  现象：组呼已打一会儿，后开机的人能听进后半段
  路径：总索引「迟后进入」→ Part2 §7
        提醒：靠超帧 A 的 Voice SYNC + 嵌入/头中地址 LC
        外壳细节 → Part1（速览已注）
  别做：只在 Part2 §3 找一个叫「Late_Entry_PDU」的独立表（没有这种单独 PDU 名当日常入口）
```

### 例子 C · Talker Alias

```text
  现象：屏上要显示主叫别名；抓到 FLCO=000100
  路径：Part2 §1.1 → Talker_Alias_hdr
        → §3.4 头字段；块 1/2/3 → §3.5（FLCO 000101–000111）
  别做：把 FLCO 表和 CSBKO 表对着找「Alias」
```

### 例子 D · 确认数据无 ACK

```text
  现象：确认 PDP 发出，对端无 ACK
  路径：Part3 §8 定家族 → §2 核对 C_HEAD（A、FMF、BF、N(S)…）
        → §4 看是否该出现 C_RHEAD；Class/Type/Status 是否 NACK/SACK
  短提醒（不重讲第 27 课）：确认要回执；SACK 才带 C_RDATA 位图
  别做：先打开 §7 怀疑头压缩
```

### 例子 E · SP 状态 vs UDP 文本

```text
  现象：产品说「发个短消息」
  路径：先问证件——
        状态/预编码 → Part3 §5.1 SP_HEAD（常无续块）
        UDP 5016 文本 → Part3 §7（SAP=0011，SPID/DPID 索引）
  这是第 28 课内容课 + 本课路径课的叠乘
  别做：在 Part2 Service Options 里找「短信 bit」
```

### 例子 F · Service Options Emergency

```text
  现象：紧急组呼；要确认 Emergency 比特位置
  路径：Part2 §6.1 Service Options 表 → Emergency 1 bit
        若还看 CACH 活动宣布 → §5.2 Act_Updt Activity ID（11xx 紧急类）
  别做：在 Part3 DPF 表里找 Emergency
```

### 例子 G · 错书：Part4 里找 Tier II 短数据

```text
  现象：Tier II 中继业务信道发状态，同事翻 Part4 UDT Opcode
  路径纠偏：总索引 §2 短数据 → 数据协议字段速览 §5
        Part3 §5.4 UDT_HEAD 只是指针；控制信道过程 → Part4
  口诀：先问 Tier 与信道种类，再选书（第 28 课例子 F 的书架版）
```

---

## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| Part2 官方版本 | **TS 102 361-2 V2.5.1 (2023-05)** | 语音业务硬出处 |
| Part3 官方版本 | **TS 102 361-3 V1.3.1 (2017-10)** | 数据协议硬出处 |
| Part1 官方版本 | **TS 102 361-1 V2.7.1 (2026-05)** | 外壳 / DPF/SAP / 三头位宽 |
| 总索引关键节 | §0–§5 | 门牌；本课用 §2/§4 最多 |
| Part2 速览节 | §1–§9 | Opcode→过程→LC→CSBK→Short LC→SO→补充→Terminator→缺口 |
| Part3 速览节 | §1–§9 | 衔接→C/U头→续块→响应→短数据→TD_LC→HC→Data Type→缺口 |
| FLCO 例 | `000000` Grp · `000011` UU · `000100–000111` Alias · `001000` GPS · `110000` TD_LC 指针 | §1.1 入口 |
| CSBKO 例 | `000100` UU_V_Req · `000101` UU_Ans · `100110` NACK · `111000` BS_Dwn_Act · `111101` Pre_CSBK | §1.2 入口 |
| SLCO 例 | `0000` Nul · `0001` Act_Updt | §1.3 |
| DPF 例 | `0010`/`0011` U/C 数据 · `1110`/`1101` 短数据 · `0001` 响应 · `0000` UDT | Part3 §1 |
| SAP 例 | `1010` Short Data · `0011` UDP HC · `0100` IP · `0010` TCP HC 预留 | Part3 §1 |
| Voice Terminator Data Type | `0010` | Part2 §8 |
| Data Header Data Type | `0110` | Part3 §1 / §8 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 查表不改射频 |

---

## 9. 十则误区（看见就打回）

1. **「字段文 = 把 PDF 从头读到尾。」** → 先总索引门牌，再速览货架，最后 PDF 库房。  
2. **「FLCO 和 CSBKO 是一张 Opcode 表。」** → Part2 §1.1 / §1.2 分家；外壳还在 Part1。  
3. **「Part2 里找得到 EMB/SLOT 详解。」** → 外壳回 Part1；Part2 是业务 PDU。  
4. **「Part3 短数据 = Part4 UDT。」** → 信道与 Tier 不同；§5.4 只是指针。  
5. **「缺口节可以自行补表。」** → 缺口 = 停；回 PDF 或后课。  
6. **「DPF 和 SAP 哪个都能当唯一入口。」** → 常要两个一起看；再分流 §2/§5/§7。  
7. **「确认无 ACK 先查头压缩。」** → 先 §2/§4 车次与响应，再 §7。  
8. **「总索引 §4 最小打开集 = 只需那几页永远够。」** → 起步集；争议与认证仍回 PDF。  
9. **「代码仓库/幻灯条款号可覆盖速览。」** → 实现≠规范；TS 优先。  
10. **「翻错书说明射频一定有问题。」** → 错架是文档路径问题；12.5 kHz/4FSK 先别背锅。

---

## 10. 自测题（含答案）

**题 1.** 用三句话说明「三层书架」各层做什么。

<details><summary>答案</summary>

第一层总索引：按「我想查什么」给出打开哪篇。第二层 Part2/Part3 字段速览：结构化 Opcode/PDU/字段表，按节跳转。第三层官方 PDF：硬出处与认证；与笔记冲突时以 TS 为准。

</details>

**题 2.** 分析仪显示 CSBKO=`000101`。写出查表路径（文件 + 节）。

<details><summary>答案</summary>

打开 `02-语音业务/语音业务字段速览.md` **§1.2** → UU_Ans_Rsp；需要 Answer Response 等字段再进 **§4.3**（及 §6.2）。

</details>

**题 3.** 为什么说 Part2 ≠ Part1 shell？举两个仍应回 Part1 的例子。

<details><summary>答案</summary>

Part2 展开语音业务 PDU/Opcode/Service Options；突发壳、EMB/SLOT、Data Type 枚举、许多 IE 位宽在 Part1。例子：Voice SYNC 与 Late Entry 外壳；Data Type=`0010` Terminator with LC 的空口定义。

</details>

**题 4.** DPF=`0011` 的包「无 ACK」——Part3 建议的两步入口是什么？何时才进 §7？

<details><summary>答案</summary>

先 **§2** 核对 C_HEAD 是否像确认头 + **§4** 查响应；仅当 SAP 指向 UDP HC、或解 IP/端口失败时再进 **§7**。

</details>

**题 5.** 总索引 §4「数据业务」最小打开集是什么？若还要 DPF 枚举硬表呢？

<details><summary>答案</summary>

**数据字段速览 → Part3 PDF**。DPF/SAP 硬枚举争议再加 **Part1** Tables 9.30–9.31（速览 §1 已桥接）。

</details>

**题 6.** 判断：Part3 速览 §9 写了 TCP HC 无完整表，因此可以根据 UDP 表「改两个字段」自造 TCP 表。（对 / 错）

<details><summary>答案</summary>

**错。** 缺口纪律：不编造；SAP=`0010` 仅预留；产品宣称以厂商文档为准，规范侧停在诚实边界。

</details>

**题 7.** 写出从「屏上无 Talker Alias」到字段表的完整路径（含 Opcode）。

<details><summary>答案</summary>

总索引「主叫识别」→ Part2 速览 → §1.1 FLCO `000100`–`000111` → §3.4/§3.5 头与块字段；并确认嵌入在语音超帧（§2/§7）。

</details>

**题 8.** 现场：「同事用 Part4 查 Tier II 中继上的 SP 状态」——你如何用总索引 + Part3 纠偏？再补一句调制提醒。

<details><summary>答案</summary>

总索引 §2「短数据」→ 数据协议字段速览 §5（SP_HEAD）；Part4 留给控制信道/UDT。调制提醒：选错书不改变 12.5 kHz/4FSK/双时隙——先纠路径，再查射频。

</details>

**题 9.（加分）** Part2 §8 语音 Terminator 与 Part3 §6 TD_LC 如何用 FLCO/Data Type 一眼分开？

<details><summary>答案</summary>

两者都可以走 Data Type = Terminator with LC（`0010`），但语音终止 LC 通常是 Grp/UU_V_Ch_Usr 的 FLCO；数据 hangtime 用 **TD_LC，FLCO=`110000`**（Part3 §6；Part2 §1.1 仅对照指针）。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `总索引.md` **§0 / §2 / §4** | 门牌、关键词、角色最小打开集（本课 canonical） |
| 2 | `02-语音业务/语音业务字段速览.md` **§1–§9** | Part2 全 TOC 入口（本课主书架） |
| 3 | `03-数据协议/数据协议字段速览.md` **§1–§9** | Part3 全 TOC 入口（本课主书架） |
| 4 | `01-空中接口/帧结构与字段定义.md` | 外壳 / Data Type；Late Entry SYNC |
| 5 | `01-空中接口/CSBK与LC字段详表.md` | EMB/SLOT/LC/CSBK 公共外壳 |
| 6 | `学习推送/第25课.md` / `第26课.md` | 补充业务与 Late Entry 内容回唤 |
| 7 | `学习推送/第27课.md` | 确认/非确认车次（查 §2/§4 时回唤） |
| 8 | `学习推送/第28课.md` | 三姐妹与 HC（查 §5/§7 时回唤） |
| 9 | `00-入门/DMR术语与帧结构速查卡.md` | 墙上 Data Type / 时隙 |
| 10 | `DMR整合学习手册.md` | 全貌；版本与能力 Tier |
| 11 | 官方 **TS 102 361-2 V2.5.1**（`02-语音业务/TS102361-2_V2.5.1.pdf`） | 语音过程与 PDU 原文 |
| 12 | 官方 **TS 102 361-3 V1.3.1**（`03-数据协议/TS102361-3_V1.3.1.pdf`） | PDP / 短数据 / HC 原文 |
| 13 | 官方 **TS 102 361-1 V2.7.1** | Tables 9.17A–C、9.30–9.31 等硬表 |
| 14 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「翻错书」当成调制故障 |

官方版本锚点：**Part2 V2.5.1**、**Part3 V1.3.1**、**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。FEC 矩阵、Idle 比特、完整 SDL、缺口臆造表、Part4 UDTO 全表：**永远回 PDF / 后课**，本课不补第二份。

---

## 12. 下一课预告

**第 30 课 · 小综合：跟一次语音呼叫空口**

本课把「三层书架 + Part2/Part3 查表路径」钉进手指肌肉。下一课做阶段 D 小综合：跟着一次语音呼叫的空口时间线（从可选 BS 激活、Voice LC Header、超帧、嵌入补充、到 Terminator/hangtime），在关键节点**当场翻表**——仍然少公式；把第 11/25/26/29 课叠成一条可演示的跟读路径，为后续数据小综合留接口。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-02**（晚间推送）检索核验；真实打开过内容页/PDF（协会镜像 / ETSI deliver / Tait Academy / GitHub 等 HTTP 200；`www.dmrassociation.org/dmr-standards.html` 本环境失败时以 **`https://dmrassociation.org/dmr-standards.html`** 为准）。**不编造地址**。策略 = **Part2 协会镜像 + Part2 ETSI 官方链 + Part3 协会镜像 + Part1 协会镜像 + DMRA 标准目录页 + Benefits 白皮书（产品语感）+ Tait Intro to DMR 学习指南 PDF + Tait Radio Academy 课程页 + go-dmr（实现≠规范对照）**。另检索公开「如何查阅 DMR Part2/Part3 字段文档 / navigate ETSI TS 102 361 field tables」专题视频与长文：**未找到**达到本课「三层书架 + 速览 TOC 入口」深度的独立优质短片（Tait Academy 有入门视频课，但是 **DMR 概论**，不是字段文导航课；产品写频演示亦不适用）。**已弃用**易触发浏览器挑战的第三方 wiki 页。

1. **[ETSI TS 102 361-2 V2.5.1｜Voice and generic services（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：Part2 官方正文——Opcode / 语音过程 / Full LC / CSBK 硬出处；与资料库语音速览对照。  
   - **库内副本**：`dmr/02-语音业务/TS102361-2_V2.5.1.pdf`。  
   - **适合哪一段**：第 4.2、7、8、11 节。  
   - **基础**：进阶；英文 PDF。

2. **[ETSI TS 102 361-2 V2.5.1｜ETSI 官方投递链](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/02.05.01_60/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：与协会镜像同文的官方入口；部分环境抓取异常时改用镜像或浏览器。  
   - **适合哪一段**：同上。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TS 102 361-3 V1.3.1｜Packet Data Protocol（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236103v010301p.pdf)**  
   - **为什么值得看**：Part3 硬出处——C/U_HEAD、响应、短数据、UDP HC；与数据速览 §1–§9 对照。  
   - **库内副本**：`dmr/03-数据协议/TS102361-3_V1.3.1.pdf`。  
   - **适合哪一段**：第 4.3、7、11 节。  
   - **基础**：进阶；英文 PDF。

4. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：外壳与 Tables **9.17A–C / 9.30–9.31**——当速览不够时的第三层。  
   - **适合哪一段**：第 4.3、4.4、8、11 节。  
   - **基础**：进阶；英文 PDF。

5. **[DMR Association｜DMR Standards 目录页](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：协会标准下载门牌——Part1–4 / TR 入口一览，适合给新人「官方书架在哪」。  
   - **注意**：目录页≠字段表；版本以 PDF 封面与总索引 §3 为准。  
   - **适合哪一段**：第 2、4.1、11 节。  
   - **基础**：入门；英文网页。

6. **[DMR Association｜Benefits and Features of DMR（白皮书 PDF）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：产品语言里的语音/数据能力量级——适合向领导解释「我们为什么要会查 Part2/Part3」。  
   - **注意**：白皮书不是 TS；冲突以 Part1/2/3 为准。  
   - **基础**：入门；英文 PDF。

7. **[Tait Radio Academy｜Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：厂商学院学习指南，帮助建立「标准分 Part、语音/数据/集群分家」的直觉——为本课选书铺垫。  
   - **注意**：导读≠字段速览；版本较旧时以现行 ETSI / 总索引 §3 为准。  
   - **适合哪一段**：第 1、2、4.1 节。  
   - **基础**：入门；英文 PDF。

8. **[Tait Radio Academy｜Introduction to DMR 课程页](https://www.taitradioacademy.com/courses/introduction-to-digital-mobile-radio/)**  
   - **为什么值得看**：有入门视频课与评估——适合弱基础同事补「DMR 是什么」；**不是**「字段文怎么查」专题课。  
   - **适合哪一段**：课前预习 / 第 1 节动机。  
   - **基础**：入门；英文网页/视频。

9. **[pd0mz/go-dmr｜dataheader.go（头字段解析代码）](https://github.com/pd0mz/go-dmr/blob/master/dataheader.go)**  
   - **为什么值得看**：实现侧可见 DPF/SAP/短数据头拆解——用来练习「代码枚举 vs 速览表 vs PDF」三层对照。  
   - **注意**：**代码不是规范**；冲突以 ETSI PDF 为准。  
   - **适合哪一段**：第 4.3、4.4、9 节误区。  
   - **基础**：中级～进阶；Go 源码。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 资料库三层书架 + Part2/Part3 字段速览 TOC 入口（FLCO/CSBKO/DPF/SAP/现象分流）」** 按课堂深度讲透的独立高质量中文/英文短片。Tait Radio Academy 的 Introduction to DMR 是**概论视频课**，可作弱基础补课，但不能替代本课查表操练。本课 **`video_found=false`**。建议用：**总索引 §2/§4 + 语音速览 §1–§9 + 数据速览 §1–§9 + Part2/Part3 PDF + 本课决策树与 8 道操练** 对照自学。

---

*推送说明：本课为阶段 D「Part2/Part3 字段文怎么查」图书馆技能专课。频谱/调制仅保留短提醒（查表不换频、不改 4FSK/双时隙；翻错书≠射频故障），不复述加餐全文。主文加厚覆盖动机、三层书架与决策树、术语、总索引/Part2 TOC/Part3 TOC 入口、边界表、8 道查表操练、与第 11/13/25–28 课对照、现场分诊、七则例子、账本、十则误区、九题自测、资料库路径与核验外链（含 Part2 双链、DMRA 目录、Tait 指南与课程页；诚实标明无合适公开「字段文导航」专题视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle、不发明条款号、不重讲第 27/28 课全文、不从缺口编造表、不把 Part4 当 Part3 日常入口。读完应能向同事演示「现象→总索引→速览节→（必要时）PDF」，并进入第 30 课语音呼叫空口小综合。*
