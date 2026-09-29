# 第 23 课 · CSBK 控制信令块

> DMR 深入学习 · **阶段 C 空口深入第 9 课**  
> 适合：已吃透第 14 课「FID/CSBKO 门牌」、第 21 课「SLOT / Data Type」、第 22 课「Full LC / Short LC」，但仍会把「控制信令」和「呼叫门牌」混为一谈、或分不清 **CSBKO ≠ FLCO ≠ SLCO**、或看见 Data Type=CSBK 却去语音超帧里找嵌入、或把 **LB（Last Block）** 当成「最后一通电话」口语的人  
> 阅读量：约 **30–40 分钟** · 几乎不推公式 · 要把「**CSBK = 另一只控制外壳（Table 9.9）：LB|PF|CSBKO|FID|Data64|CRC-16；走数据突发 + Slot Type Data Type=CSBK（0011），典型 BPTC(196,96)；单块 LB=1，MBC 可 LB=0…末块=1；CSBK ≠ Full LC ≠ Short LC ≠ EMB/SLOT；FLCO≠CSBKO≠SLCO；Full LC 管话务门牌，CSBK 管请求/应答/唤醒/前导等控制事务；Tier III 大量复用此外壳（本课只预告）**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**，符号率约 **4800 baud**，总比特率约 **9.6 kbps**。CSBK **不换频、不改调制、不另开带宽**——它只是「控制事务」写在数据壳里的一块 **96 bit 信息外壳**。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是**CSBK 外壳怎么长、怎么运、和 LC 怎么分工、现场怎么对症**。

---

## 1. 为什么本课重要（动机）

第 14 课把门牌钉死了：先看 **FID**，再看 Opcode——那时已经提过 **CSBKO** 和 **FLCO** 是两张表。  
第 21 课把小报头拆开了：**SLOT** 里的 **Data Type** 决定「196 信息比特按哪张单据解」——其中就有 **CSBK / MBC Header / MBC Continuation**。  
第 22 课把链路控制正文拆开了：**Full LC** = 呼叫门牌；**Short LC** = CACH 缝里短广播；并预告「下一课打开 CSBK 外壳」。

同事接下来会盯着分析仪问：

- 屏幕上出现 **CSBK**、**Voice LC Header**、**Embedded LC**、**CACH Short LC**——这四样是不是「都叫控制」就可以互相替代？  
- 为什么个呼有时先看到 **UU_V_Req / UU_Ans_Rsp**，再才看到 Voice LC Header？那前两步是 LC 还是 CSBK？  
- 中继「睡醒」前有一条 **BS_Dwn_Act**——它走语音壳还是数据壳？有没有 Slot Type？  
- 培训台上若只背「CSBK = 控制信令」六个字，后面会卡在同一处：

> **CSBK 与 Full LC / Short LC 是不同 PDU、不同 Opcode 表、不同运载路径。CSBK 外壳（Part1 Table 9.9）是 LB|PF|CSBKO|FID|Data64 + CRC-CCITT 16，约 96 bit 信息 PDU，装进数据突发（Data SYNC + Slot Type，Data Type=CSBK），典型再经 BPTC(196,96)。它负责请求、应答、唤醒、前导、定时等控制事务；Full LC 负责话务「谁找谁」的门牌正文；Short LC 只住在出站 CACH。EMB/SLOT 仍只是小报头。**

本课目标是让你能自己讲清十件事：

1. **为什么** CSBK ≠ Full LC ≠ Short LC ≠ EMB/SLOT；  
2. 一张总图：控制事务车 vs 话务门牌车 vs 缝里短广播；  
3. 白话术语：CSBK、CSBKO、LB、PF、FID、CSBK Data、CRC-16、MBC、Data Type；  
4. 机制：Part1 Table **9.9** / clause **9.1.8** / figure **7.8** 精神，少公式；  
5. **FLCO ≠ CSBKO ≠ SLCO** 与 Data Type **0011/0100/0101** 对照；  
6. 现场：唤醒、个呼存在性检查、前导、拒答、误把 CSBK 当 LC；  
7. 完整例子：BS_Dwn_Act；UU_V_Req→Ans/NACK；Pre_CSBK；LB/MBC 草图；误读「CSBK=短 LC」；  
8. 数字账本；误区 + 自测 + 资料库 + 核验外链；  
9. 下一课预告：FEC 原则（不贴矩阵）。

---

## 2. 总图 / 故事：控制事务车 vs 话务门牌车

先把整课装进一个故事，再落到 Part1 clauses **7.2、9.1.8、9.3.6、9.3.31–9.3.32**、figure **7.8**、Table **9.9 / 9.22** 与资料库 `01-空中接口/CSBK与LC字段详表.md` **§6**、`帧结构与字段定义.md` **§7.5**、`02-语音业务/语音业务字段速览.md` **§1.2 / §4**。

### 2.1 一句话故事：门牌 vs 办手续窗口

把一次通话想成进商场办事：

- **Full LC** = 店门口大海报 / 火车上的门牌正文：「这趟车是谁找哪一组」（第 22 课）。  
- **Short LC** = 出站缝里（CACH）的慢速小广播：活动看板、空消息（第 18/22 课）。  
- **CSBK** = **办手续窗口**递过来的单页表格：唤醒基站、个呼「人在不在」、礼貌拒绝、扫描前导、直通定时……——Opcode 叫 **CSBKO**，外壳带 **LB**（是否本块已是最后一块）。

口诀：**话务门牌看 Full LC；缝里短广播看 Short LC；办手续看 CSBK；小报头看 EMB/SLOT。**

### 2.2 总图：CSBK 外壳与运载

```text
                    ┌──────────────────────────────────────┐
                    │  CSBK PDU 信息外壳 ≈ 96 bit            │
                    │  Octet0: LB(1) | PF(1) | CSBKO(6)     │
                    │  Octet1: FID(8)                       │
                    │  Octet2–9: CSBK Data (64)             │
                    │  + CSBK CRC-16 (CRC-CCITT, B.3.8)     │
                    └──────────────────┬───────────────────┘
                                       │
                                       ▼
                    【运载：数据 / 控制突发】
                    Data SYNC（认「数据壳」）
                    + Slot Type：CC(4) + Data Type(4) + Golay
                      Data Type = CSBK          → 0011
                                 MBC Header     → 0100
                                 MBC Continuation → 0101
                    196 Info 典型经 BPTC(196,96) 托起上述 96 bit PDU
                                       │
          ┌────────────────────────────┼────────────────────────────┐
          ▼                            ▼                            ▼
   单块 CSBK                      MBC 多块控制                 Tier III 预告
   LB = 1                         头可为 LB=0；末块 LB=1      大量控制 PDU
   Part2：唤醒/个呼请求…          同家族外壳，分片续传         复用此外壳（Part4）
```

### 2.3 和第 14–22 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 14 | FID 门牌；CSBKO 与 FLCO 是不同 Opcode 表 |
| 第 17–18 | 语音超帧与 CACH；Short LC 不住数据壳 |
| 第 19–20 | SYNC 认壳；CC 在 EMB/SLOT |
| 第 21 | SLOT + Data Type 路由单据（含 CSBK/MBC） |
| 第 22 | Full LC / Short LC 正文与三路径 |
| **本课** | 打开 **CSBK 外壳**：LB、CSBKO、Data64、CRC16、与 LC 分工 |

四句话串起来：

1. **门牌号**在第 14 课（FID + Opcode 表）；  
2. **小报头**在第 21 课（SLOT 告诉你 Data Type=CSBK）；  
3. **第 22 课**读话务门牌正文（Full/Short LC）；  
4. **本课**读控制事务外壳（CSBK），并钉死「办手续 ≠ 贴门牌」。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；CSBK 不另开频。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps**。  
4. **解调直觉**：先对齐 **Data SYNC** → 读 **SLOT**（CC + Data Type）→ 若类型是 CSBK/MBC，再解 96 bit 外壳里的 CSBKO/FID/Data；解错 CSBK ≠「没解调出射频」，而是「控制单据读歪了」。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **CSBK** | Control Signalling Block，控制信令块；Part1 Table **9.9** 外壳 | ≠ Full LC；≠ Short LC |
| **CSBKO** | CSBK Opcode，**6 bit**（Part1 **9.3.32**；业务表 Part2） | ≠ FLCO；≠ SLCO |
| **LB** | Last Block，**1 bit**；单块 CSBK 置 `1`；MBC 头可为 `0`，末块 `1` | ≠「最后一通电话」口语 |
| **PF** | Protect Flag，**1 bit**；与 Full LC 同名位（现行常置 0） | ≠ 加密开关口语 |
| **FID** | Feature set ID，**8 bit**；标准业务 SFID=`0x00`（第 14 课） | ≠ 24-bit 地址 |
| **CSBK Data** | 跟在 FID 后的 **64 bit** 业务体 | 随 CSBKO 变；见 Part2 §4 |
| **CSBK CRC** | **16 bit** CRC-CCITT（Annex **B.3.8**） | ≠ Full LC 的 RS24 / CS5；≠ Short 的 CRC8 |
| **MBC** | Multi Block Control；多块控制，同家族外壳 | Data Type 头/续块不同 |
| **Data Type** | SLOT 内 **4 bit**；CSBK=`0011`，MBC H=`0100`，MBC C=`0101` | 第 21 课；语音无 SLOT |
| **BPTC(196,96)** | 多数数据/控制 196→96 信息块的块码名 | 本课只记名称；矩阵见原文 |
| **FLCO / SLCO** | Full / Short LC 的 Opcode | **不是** CSBKO |
| **EMB / SLOT** | 小报头 16 / 20 bit | **不是** CSBK 正文 |

---

## 4. 机制拆解：外壳 → 运载 → Opcode → 分工

### 4.1 CSBK PDU（Table 9.9）— 八位组直觉

引用：Part1 clause **9.1.8**；figure **7.8**；资料库 `CSBK与LC字段详表.md` **§6**；`帧结构与字段定义.md` **§7.5**。

```text
  Octet0:  LB(1) | PF(1) | CSBKO(6)
  Octet1:  FID(8)
  Octet2–9: CSBK Data (64)     ← 业务字段，Part 2 / Part 4 定义
  + CSBK CRC 16 (CRC-CCITT, B.3.8)
  → 信息 PDU 直觉 96 bit；装进数据突发的 196 Info（典型 BPTC(196,96)）
```

| IE | Len | 备注 | 条款 |
|----|-----|------|------|
| **Last Block (LB)** | 1 | 单块 CSBK 置 `1`；MBC 头可为 `0` | 9.3.31 |
| **PF** | 1 | 与 Full LC 同名位 | 9.3.10 |
| **CSBKO** | 6 | 业务 Opcode → **Part 2 / Part 4** | 9.3.32 |
| **FID** | 8 | SFID=`0x00` / MFID | 9.3.5 |
| **CSBK Data** | 64 | 地址、选项、Reason 等 | Part 2/4 |
| **CSBK CRC** | 16 | CRC-CCITT | B.3.8 |

**不要背错的一点**：96 bit 是**信息 PDU 叙事**（外壳+CRC）；空口上还要经 Slot Type 标签与 BPTC 保护。具体 CRC 初值/掩码、BPTC 矩阵以 ETSI Annex B 为准——本课记**名称、字段顺序、运载路径**即可（矩阵留给第 24 课原则课，且永不贴生成矩阵）。

### 4.2 LB（Last Block）：单块 vs 多块

| 场景 | LB | Data Type（学习摘要） | 直觉 |
|------|----|----------------------|------|
| 普通单块 CSBK（Part2 常见） | **`1`** | CSBK `0011` | 「这一页表格写完了」 |
| MBC Header（后面还有续块） | 可为 **`0`** | MBC Header `0100` | 「封面，后面还有页」 |
| MBC 末块 | **`1`** | MBC Continuation `0101`（末片） | 「最后一页」 |
| MBC 中间续块 | **`0`** | MBC Continuation `0101` | 「翻页中」 |

口诀：**单块 CSBK → LB 必须当「本块即末块」理解（置 1）；看见 LB=0，先想「这是多块家族（MBC），别当单页读完」。**

### 4.3 运载路径：数据突发，不是语音壳，也不是 CACH

| 项 | CSBK 路径 | 对照 |
|----|-----------|------|
| 突发壳 | **数据 / 控制突发** | 语音突发中心是 Voice SYNC 或 EMB+嵌入 |
| 中心 SYNC | 常见 **Data SYNC** | ≠ Voice SYNC；≠ 独立 RC SYNC 故事 |
| 小报头 | **Slot Type 20**（CC+Data Type+Golay） | 语音**没有** Slot Type（第 21 课） |
| Data Type | **CSBK / MBC H / MBC C** | ≠ Voice LC Header / Terminator |
| 载荷 FEC 名 | 典型 **BPTC(196,96)** | 嵌入 LC 是另一条可变长 BPTC |
| 与 CACH | **不走** CACH Signalling 缝 | Short LC 才走 CACH |

```text
数据突发直觉（第 21 课回顾）：
  Info(98) | SLOT(20) | Data SYNC 或嵌入窗(48) | Info(98)
              │
              └─ Data Type = 0011 → 按 CSBK 解 96 bit PDU
                 Data Type = 0100/0101 → 按 MBC 头/续解
```

### 4.4 FID 门牌再钉一次（回指第 14 课）

CSBK 与 Full LC **同样**在 Octet1 带 **FID**：

1. 标准馆业务：先确认 **SFID=`0x00`**，再查 **CSBKO** 表（Part2 Table B.2 / clause 7.1.2）。  
2. **MFID** 下同数值 CSBKO **不可**当标准功能翻译。  
3. 口诀仍是：**先 FID，后 Opcode**——只是本课 Opcode 换成了 **CSBKO**，不是 FLCO。

### 4.5 Part2 常见 CSBKO（学习摘要，不背全库）

引用：`02-语音业务/语音业务字段速览.md` **§1.2 / §4**；冲突以 Part2 PDF 为准。

| CSBKO | 别名 | 一句话直觉 | 典型何时看见 |
|-------|------|------------|--------------|
| `111000` | **BS_Dwn_Act** | 唤醒 / 激活 BS 出站 | 中继「睡醒」前 |
| `000100` | **UU_V_Req** | 个呼语音服务请求（存在性检查） | 个呼 OACSU 前半 |
| `000101` | **UU_Ans_Rsp** | 个呼应答（Proceed / Deny） | 对 UU_V_Req 的回答 |
| `100110` | **NACK_Rsp** | 否定应答 / 礼貌拒绝 | 不支持、拒服务等 |
| `111101` | **Pre_CSBK** | 前导：叫醒扫描/睡眠台 | 非语音投递前「敲窗户」 |
| `000111` | **CT_CSBK** | 信道定时（直通广域时隙） | TDMA DM 定时传播 |

字段级八位组（Service Options、Answer Response、Reason Code、CBF…）→ 打开资料库 **§4**，本课建立「壳 + 分工」即可。

### 4.6 分工：Full LC 贴门牌，CSBK 办手续

引用：语音业务速览 **§2** 呼叫过程对照表精神。

| 阶段（学习摘要） | 典型单据 | Opcode 家族 |
|------------------|----------|-------------|
| 可选唤醒 BS | **CSBK** BS_Dwn_Act | CSBKO |
| 个呼存在性检查 | **CSBK** UU_V_Req → UU_Ans_Rsp / NACK | CSBKO |
| 扫描/节电前导 | **CSBK** Pre_CSBK | CSBKO |
| 语音开始 | **Voice LC Header**（Full LC） | FLCO |
| 超帧语音 | Voice + 嵌入 Full LC | FLCO |
| 语音结束 | **Terminator with LC** | FLCO |
| 出站活动看板 | **Short LC** Act_Updt / Nul_Msg | SLCO |

口诀：**先办手续（CSBK），再贴门牌开车（Full LC）；缝里看板（Short LC）另算一路。**

### 4.7 MBC 与 Tier III：同家族外壳，本课只预告

- **MBC**：多块控制共用「控制块外壳」叙事；靠 Data Type 区分头/续，靠 **LB** 标末块。细节字段随具体 MBC 类型变——本课只要会分诊「单块 CSBK vs 多块 MBC」。  
- **Tier III（Part4）**：集群控制信道上大量 grant / 注册 / 系统状态等 **复用 CSBK/MBC 外壳**。外链博客常把「CSBK」几乎等同于「集群控制信道」——那是 **Tier III 使用场景**，**不是**「常规（Tier II）没有 CSBK」。常规侧 Part2 已明确使用 BS_Dwn_Act、UU_V_Req、Pre_CSBK 等。  
- 本课**不**深挖 Part4 Opcode；记住「壳是同一家族，业务表另开 Part4」即可。

---

## 5. 对照表：CSBK vs Full LC vs Short LC vs EMB/SLOT

| 维度 | **CSBK** | Full LC | Short LC | EMB / SLOT |
|------|----------|---------|----------|------------|
| 角色 | 控制事务**外壳** | 呼叫门牌**正文** | 缝里**短广播** | **小报头** |
| 表 | Table **9.9** | Table **9.7** | Table **9.8** | Table **9.3 / 9.4** |
| Opcode | **CSBKO 6** | **FLCO 6** | **SLCO 4** | 无（PI/LCSS 或 Data Type） |
| 门牌 FID | 有（8） | 有（8） | 无此八位组布局 | 无 |
| 首八位组差异 | **LB\|PF\|CSBKO** | **PF\|R\|FLCO** | （无 LB/PF/FID 布局） | — |
| 业务数据 | **64** bit | **56** bit | **24** bit | — |
| 校验名 | **CRC-CCITT 16** | RS(12,9) 24 或 5-bit CS | CRC-8 | QR / Golay |
| 运载 | 数据壳 **Data Type=CSBK/MBC** | Header/Terminator/嵌入 B–E | **仅 CACH** | 嵌在突发结构里 |
| 和 CC 关系 | 正文不含 CC；CC 在 SLOT | 同左（嵌入路径 CC 在 EMB） | 不替代 CC | **携带 CC** |

分柜口诀：

```text
看见「CSBKO / LB / Data Type=CSBK」→ 控制事务外壳（本课）
看见「FLCO / 组地址 / 源台号」→ Full LC 门牌正文（第 22 课）
看见「CACH / SLCO / Act_Updt」→ Short LC
看见「CC + Data Type」或「CC + LCSS」→ 还在小报头，没进正文
看见「FLCO 数值拿去当 CSBKO」→ 嘴瓢，打回两张表
```

### 5.1 Opcode 三表对照（再钉一次）

| 名称 | 宽度 | 住在谁里面 | 典型例子（学习摘要） |
|------|------|------------|----------------------|
| **FLCO** | 6 | Full LC | Grp_V_Ch_Usr `000000` |
| **CSBKO** | 6 | CSBK | UU_V_Req `000100`；BS_Dwn_Act `111000` |
| **SLCO** | 4 | Short LC | Act_Updt `0001`；Nul_Msg `0000` |

注意：`000100` 在 FLCO 表里是 **Talker Alias header**，在 CSBKO 表里是 **UU_V_Req**——**同数值、不同表、不同语义**。这是现场最高频的「数字撞车」陷阱之一。

---

## 6. 现场岗位对照

| 现场现象 | 先看什么 | 本课解释 |
|----------|----------|----------|
| 个呼前先闪 **UU_V_Req / Ans** | Data Type 是否 CSBK；CSBKO/FID | 办手续阶段；还不是 Voice LC Header |
| 中继久闲后首包像「控制」 | 是否 BS_Dwn_Act（CSBKO `111000`） | 唤醒出站；别当成组呼门牌 |
| 扫描台漏收短数据/控制 | 是否有 **Pre_CSBK**；CBF 是否合理 | 前导在「敲窗户」；壳对了再查后续块 |
| 对端礼貌拒绝 | NACK_Rsp：Reason / Service Type | 控制面拒绝 ≠ 射频解调失败 |
| 分析仪显示 CSBK 但解不出业务 | FID 是否 SFID？CRC16 是否过？ | 先门牌与校验，再查 CSBKO 表 |
| 在语音超帧里找 CSBK | — | CSBK 走**数据壳**；别在 B–E 嵌入里找 CSBKO |
| 把 CACH Act_Updt 叫成 CSBK | Short LC 的 SLCO | 活动看板 ≠ 控制块外壳 |
| 色码不对整网静音 | SLOT 的 **CC**（第 20–21 课） | 先过色码门，再谈 CSBK 正文 |
| 博客说「只有集群才有 CSBK」 | Part2 常规 CSBKO 表 | Tier III **大量用**外壳；常规**也有**控制 CSBK |

**分诊三步（建议贴显示器旁）**：

1. **壳对不对？** Data SYNC + Slot Type？（第 19/21 课）  
2. **色码与类型？** CC 过了吗？Data Type 是 CSBK 还是 Voice LC Header？  
3. **FID → CSBKO → Data64？** 标准馆吗？是唤醒/请求/应答/前导哪一种？

---

## 7. 工作例子（5 则）

### 例子 A · BS_Dwn_Act：叫醒中继出站

场景：中继入站侧有台要发起业务，出站可能处于省电/未激活（教学叙事）。

1. 空口先见**数据突发**：Data SYNC + SLOT（CC + Data Type=**CSBK**）。  
2. 解 CSBK：`LB=1`，`PF=0`，`FID=0x00`，`CSBKO=111000`（BS_Dwn_Act）。  
3. Data64 直觉（Part2 §4.1）：保留位 + **BS 地址 24** + **源地址 24**（数字教学用即可）。  
4. 之后才可能进入语音门牌（Voice LC Header / 超帧）——**先手续，后门牌**。

### 例子 B · 个呼：UU_V_Req → UU_Ans_Rsp / NACK

场景：源台 `1001` 呼叫个号 `1002`（OACSU 存在性检查精神）。

```text
1001 → UU_V_Req  (CSBKO=000100)  「你在吗？要语音个呼」
1002 → UU_Ans_Rsp (CSBKO=000101)  Proceed / Deny
  或 → NACK_Rsp   (CSBKO=100110)  礼貌拒绝 / 不支持
（通过后）→ Voice LC Header（FLCO=UU_V_Ch_Usr）→ 超帧语音…
```

要点：

- 前半段 Opcode 读 **CSBKO**；后半段门牌读 **FLCO**——**不要混表**。  
- `UU_V_Req` 的 CSBKO=`000100` **不是** Full LC 的 Talker Alias header。  
- Answer Response / Reason Code 细比特 → 资料库 §4.3–4.4，本课记流程骨架。

### 例子 C · Pre_CSBK：给扫描台「敲窗户」

场景：要投递非语音控制/数据，目标台可能在扫描或睡眠。

1. 先发 **Pre_CSBK**（CSBKO=`111101`），`LB=1`（单块前导常见）。  
2. Data 直觉：Data/CSBK 标志、组/个标志、**CBF**（后续块数，**不含**当前 preamble）、目标/源地址。  
3. 现场：若只有业务块、从不发前导，扫描台「偶发漏收」——先查产品是否启用 Pre_CSBK，再查射频。

### 例子 D · LB 与 MBC 草图（不深挖业务体）

```text
单块 CSBK：
  [Data Type=CSBK]  LB=1 | PF | CSBKO | FID | Data64 | CRC16
  → 一页读完

MBC（精神图）：
  [Data Type=MBC Header]       LB=0 | … | （封面，后面还有）
  [Data Type=MBC Continuation] LB=0 | … | （续页）
  [Data Type=MBC Continuation] LB=1 | … | （末页，读完）
```

分诊：看见 **LB=0** 却按「单块 CSBK 业务」强行解释完整故事——会半截读歪。

### 例子 E · 误读「CSBK = 短一点的 LC」

同事说：「CSBK 不就是控制用的 LC 吗？截短版。」  
你纠正：

| | Full LC | CSBK |
|--|---------|------|
| 首字段 | PF\|R\|**FLCO** | **LB**\|PF\|**CSBKO** |
| 数据 | 56 bit | **64** bit |
| CRC | RS24 或 CS5 | **CRC-16** |
| 典型 Data Type | Voice LC Header / Terminator | **CSBK / MBC** |
| 角色 | 话务门牌 | 控制事务 |

再补一句：Short LC 更是第三条路（CACH），更不是 CSBK。

---

## 8. 数字账本

| 量 | 值 / 关系 | 别和谁混 |
|----|-----------|----------|
| CSBK 信息 PDU | **96** bit（外壳+CRC 叙事） | ≠ 264 突发；≠ 196 Info 码字 |
| Octet0 | LB**1** + PF**1** + CSBKO**6** | ≠ Full 的 PF\|R\|FLCO |
| FID | **8** bit | ≠ 地址 24 |
| CSBK Data | **64** bit（Octet2–9） | ≠ Full Data 56；≠ Short Data 24 |
| CSBK CRC | **16** bit，CRC-CCITT | B.3.8；≠ RS24 / CRC8 / CS5 |
| Data Type CSBK | **`0011`** | MBC H **`0100`**；MBC C **`0101`** |
| SLOT | **20** = CC4+DT4+Golay12 | 语音无 SLOT |
| 典型载荷 FEC | **BPTC(196,96)** | 名称；矩阵见原文 / 第 24 课原则 |
| CSBKO / FLCO / SLCO | 6 / 6 / **4** | 三张表 |
| 时隙 / 超帧 | 30 ms / 360 ms | CSBK 不改 TDMA 节拍 |
| 带宽/调制 | 12.5 kHz + 4FSK≈4800 baud / 9.6 kbps | CSBK **不改变**二者 |

分柜口诀：

```text
办手续外壳 …… CSBK（LB|PF|CSBKO|FID|64|CRC16）→ Data Type 0011
话务门牌 ……… Full LC（第 22 课）
缝里短广播 … Short LC → CACH
运货标签 ……… EMB 16 / SLOT 20
多块亲戚 ……… MBC（0100/0101 + LB）
下一课 ……… FEC 原则（不贴矩阵）
```

---

## 9. 常见误区（10 则）

1. **「CSBK 就是控制用的 Full LC / 短 LC。」** → 否。不同 PDU、不同 Opcode 表、不同 CRC、不同运载。  
2. **「FLCO 和 CSBKO 都是 6 bit，数值能通用。」** → 否。例如 `000100` 在两表语义不同。  
3. **「CSBK 嵌在语音超帧 B–E 里。」** → 否。CSBK 走数据壳 + Slot Type；B–E 嵌的是 Full LC 类碎片。  
4. **「CACH 上的 Act_Updt 就是 CSBK。」** → 否。那是 Short LC（SLCO）。  
5. **「LB=1 表示通话结束。」** → 否。LB=Last **Block**（本控制块是否末块）。  
6. **「只有 Tier III 才有 CSBK。」** → 片面。Tier III 大量用；Part2 常规同样定义唤醒/个呼请求/前导等 CSBK。  
7. **「看见 Data Type=CSBK 就可以不管 FID。」** → 否。仍先 FID 后 CSBKO（第 14 课）。  
8. **「CRC 失败一定是天线坏了。」** → 先分：色码门、SYNC 壳、BPTC/CRC 哪一层；也可能是类型解错。  
9. **「改 CSBK 会换 12.5 kHz 或 4FSK。」** → 否。  
10. **「EMB/SLOT 里已经有控制信息，等于读完 CSBK。」** → 否。小报头只告诉你「有哪种单据 / 哪色码」；正文在 96 bit PDU 里。

---

## 10. 自测（8 题）

**题 1.** 用一句话说明 CSBK 与 Full LC 的分工。为什么说「不是同一种控制」？

<details><summary>简答</summary>

Full LC 是话务呼叫门牌正文（谁找谁）；CSBK 是控制事务外壳（请求/应答/唤醒/前导等）。PDU 布局、Opcode 表、CRC、典型 Data Type 均不同——不能互相替代。

</details>

**题 2.** 写出 CSBK 八位组外壳（含 CRC 名称），并写出单块时 LB 应取何值。

<details><summary>简答</summary>

`[LB|PF|CSBKO][FID][Data 64][+CRC-16 CRC-CCITT]`。单块 CSBK → **LB=1**。

</details>

**题 3.** CSBK 走语音壳还是数据壳？依赖什么小报头？Data Type 学习编码是什么？

<details><summary>简答</summary>

走**数据/控制突发**；依赖 **Slot Type**；Data Type CSBK=`0011`（MBC Header=`0100`，Continuation=`0101`）。语音突发无 Slot Type。

</details>

**题 4.** 对照解释：FLCO ≠ CSBKO ≠ SLCO。各举一个学习用别名。

<details><summary>简答</summary>

FLCO（Full LC）如 Grp_V_Ch_Usr；CSBKO（CSBK）如 UU_V_Req / BS_Dwn_Act；SLCO（Short LC）如 Act_Updt。宽度 6/6/4，表不同；同数值不可跨表翻译。

</details>

**题 5.** 个呼存在性检查的典型 CSBK 顺序是什么？之后才出现哪类 Full LC？

<details><summary>简答</summary>

UU_V_Req → UU_Ans_Rsp（或 NACK_Rsp）；通过后再见 Voice LC Header 等，FLCO 为 UU_V_Ch_Usr 类门牌。

</details>

**题 6.** Pre_CSBK 解决什么现场问题？CBF 计数含不含当前 preamble 块？

<details><summary>简答</summary>

给扫描/睡眠台「敲窗户」，提高后续非语音投递成功率。CBF = 后续块数，**不含**当前 preamble 块（Part2 精神）。

</details>

**题 7.** 现场「博客说只有集群才有 CSBK，但抓包在常规中继上也看到 CSBK」——如何用本课回答？

<details><summary>简答</summary>

外壳家族在常规与集群都会用：Part2 已定义 BS_Dwn_Act、UU_V_Req、Pre_CSBK 等；Tier III（Part4）是更大规模地复用该外壳做 grant/注册等。博客常把「CSBK」口语绑定到控制信道场景，不能否定常规 CSBK。

</details>

**题 8.** 为什么说「解错 CSBK ≠ 没解调出 4FSK」？分诊应先看哪三层？

<details><summary>简答</summary>

射频/调制仍是 12.5 kHz + 4FSK；CSBK 是数据壳上的单据。分诊：① SYNC/壳；② SLOT 的 CC+Data Type；③ FID→CSBKO→CRC16/Data64。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `01-空中接口/CSBK与LC字段详表.md` **§6** | Table 9.9 外壳；LB/CSBKO；MBC 一句；CRC 名 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§3 Data Type、§7.5 CSBK、§8 Table 9.22** | 数据突发；CSBK/MBC 编码；与语音壳对照 |
| 3 | `02-语音业务/语音业务字段速览.md` **§1.2、§2、§4** | CSBKO 表；呼叫阶段对照；六种常见 CSBK PDU 字段 |
| 4 | `学习推送/第14课.md` | FID 门牌；FLCO/CSBKO 分表 |
| 5 | `学习推送/第21课.md` | EMB/SLOT；Data Type 路由 |
| 6 | `学习推送/第22课.md` | Full/Short LC；与本课对照入口 |
| 7 | `01-空中接口/跳过项原则说明.md` + 本课数字账本 | FEC **名称**级；不贴矩阵 |
| 8 | 官方 **TS 102 361-1 V2.7.1** clause **7.2、9.1.8、9.3.31–9.3.32**；Table **9.9、9.22**；Annex **B.3.8、B.1.1** | 原文；冲突以 PDF 为准 |
| 9 | 官方 **TS 102 361-2**（本库 `02-语音业务/TS102361-2_V2.5.1.pdf`）clause **7.1.2**、Annex **B.2** | CSBKO 业务体；勿用 Part1 冒充 |
| 10 | **TR 102 398** | 概念导读，**不是**替代 TS |
| 11 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍怀疑「CSBK 会换调制」 |

官方版本锚点：**Part1 V2.7.1**；语音/控制业务体以本库 **Part2** PDF 为准；集群控制体例见 **Part4**（本课仅预告）。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 12. 下一课预告

**第 24 课 · FEC 原则（不贴矩阵）**

本课站住了控制外壳：**CSBK**（LB|PF|CSBKO|FID|Data64|CRC16）与 **MBC** 家族、和 Full/Short LC 的分工，并钉死 Data Type 路由与「常规也有 CSBK」。下一课把一路上反复出现的名字——**BPTC(196,96)、Golay、QR、RS、CRC-CCITT、5-bit CS…**——收成「原则课」：各自保护谁、失败时现场怎么分诊；**不粘贴生成矩阵**，只建立正确的纠错/检错地图。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-29**（晚间推送）检索核验；真实打开过内容页/PDF（HTTP 200 或协会镜像可用）；**不编造地址**。策略 = **Part1 CSBK 原文 + Part2 业务体 + TR 导读 + GopherTrunk CSBK/解码器深文 + Tier II/III 对照（并纠正「仅集群才有 CSBK」的口语简化）+ Wavecom/培训 PDF 帧图**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **7.2** 讲 CSBK / MBC 消息结构；**9.1.8** 与 Table **9.9** / figure **7.8** 定义外壳；**9.3.31–9.3.32** 钉 LB/CSBKO；Table **9.22** 钉 Data Type。  
   - **备链**（部分网络对 etsi.org 直链可能 403，以协会镜像为准）：`https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf`。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TS 102 361-2 V2.5.1｜Voice services（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：Annex **B.2** CSBKO 表；clause **7.1.2** 展开 BS_Dwn_Act / UU_V_Req / UU_Ans_Rsp / NACK / Pre_CSBK / CT_CSBK 字段——本课 §4.5–4.6 的原文。  
   - **备链**：`https://dmrassociation.org/downloads/standards/ts_10236102v020501p.pdf`。  
   - **适合哪一段**：第 4、6、7、11 节。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读里对控制/链路信令的叙事比纯条款好读，便于和本课「办手续 vs 贴门牌」对账。  
   - **适合哪一段**：第 2、7、11 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

4. **[GopherTrunk｜CSBK（词条）](https://gophertrunk.org/reference/csbk/)**  
   - **为什么值得看**：用一页把「96-bit 控制块 + CSBKO + FID + BPTC/CRC + Preamble CSBK + Tier III grant 场景」串起来——本课总图的英文对照。  
   - **适合哪一段**：第 2、4、7 节。  
   - **注意**：词条叙述偏 **Tier III 控制信道**；**不要**读成「常规没有 CSBK」——以 Part2 为准（本课 §4.7、误区 6）。  
   - **基础**：入门～中级；英文网页。

5. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：明确 Data Type 分支点包含 **CSBK**；BPTC(196,96) 保护控制/LC；语音突发无 Slot Type——和第 21 课、本课运载钉子同向。  
   - **适合哪一段**：第 4、5、8 节。  
   - **注意**：校验命名以 ETSI Annex B 为准。  
   - **基础**：中级～进阶；英文网页。

6. **[GopherTrunk｜DMR Tier II & Tier III（对照页）](https://gophertrunk.org/learn/digital-trunking/dmr-tier-2-3/)**  
   - **为什么值得看**：帮助建立「集群控制信道上 CSBK 流」的直觉；同时用本课纠正：Tier II 常规仍有 Part2 控制 CSBK。  
   - **适合哪一段**：第 4.7、6、7、9 节。  
   - **注意**：监测产品叙事 ≠ 规范穷尽表；**互操作与字段以 ETSI 为准**。  
   - **基础**：入门～中级；英文网页。

7. **[GopherTrunk｜Control-channel signaling（概念）](https://gophertrunk.org/learn/digital-trunking/control-channel-signaling/)**  
   - **为什么值得看**：把 P25 TSBK 与 DMR CSBK 对照成「短而带类型的控制块流」——方便向同事打比方（仍须回到 DMR 自己的 Data Type/CSBKO）。  
   - **适合哪一段**：第 2、12 节热身。  
   - **注意**：跨体制类比，细节以 DMR TS 为准。  
   - **基础**：入门；英文网页。

8. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：帧/突发/超帧图，便于把「数据壳 + Slot Type」钉回 264 结构，避免在语音壳里找 CSBK。  
   - **适合哪一段**：第 2、4、7 节。  
   - **注意**：厂商综述，版本锚点可能早于 V2.7.1；**硬条款以现行 Part1 为准**。  
   - **基础**：中级；英文 PDF。

9. **[Alessandro Guido｜How DMR Works — primer PDF（hamgear）](https://hamgear.files.wordpress.com/2014/02/dmr-primer.pdf)**  
   - **为什么值得看**：培训幻灯式回顾控制/LC/FEC/CRC 名称——和本课数字账本、下一课 FEC 原则同向。  
   - **适合哪一段**：第 8、11、12 节后复盘。  
   - **注意**：年代偏早、版本号旧；**以 V2.7.1 / 本库 Part2 为准**。  
   - **基础**：入门～中级；英文 PDF。

10. **[GopherTrunk｜DMR End to End Part 5：Link Control & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
    - **为什么值得看**：用「门牌/嵌入」故事反衬本课：读完 CSBK 手续后，话务仍要回到 Full LC 路径——和 §4.6 分工表对读。  
    - **适合哪一段**：第 4.6、5、7 节。  
    - **注意**：实现向细节是工程选择；规范语义以 ETSI 为准。  
    - **基础**：中级～进阶；英文网页。

**说明（视频）**：公开检索未找到专门把 **「CSBK 外壳 LB|PF|CSBKO|FID|Data64|CRC16；Data Type 0011 vs MBC；CSBKO≠FLCO≠SLCO；常规 Part2 CSBK vs Tier III 复用；与 Full/Short LC 分工」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只演示写频、集群跟控界面或产品抓包，不拆 PDU 外壳）。本课**未找到合适公开专题视频**。建议用：**Part1 Table 9.9 + Part2 §7.1.2 + GopherTrunk CSBK 词条 + 资料库 §6 / 语音业务速览 §4** 对照自学。

---

*推送说明：本课为阶段 C「CSBK 控制信令块」。频谱/调制仅保留短提醒（CSBK 不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、办手续总图、术语、Table 9.9 外壳与 LB/MBC、数据壳运载与 Data Type、FID/CSBKO 门牌、Part2 常见 CSBKO 摘要、与 Full/Short LC 分工与对照、现场分诊、五则工作例子、数字账本、十则误区、八题自测、资料库路径与十条核验外链（并诚实标明未找到合适公开专题视频；纠正「仅集群才有 CSBK」的口语简化）。读完应能向同事讲清「CSBK 为何不是 LC、单块 LB 怎么读、个呼前手续与话务门牌如何衔接、为何不能在语音嵌入里找 CSBKO」，并进入第 24 课 FEC 原则（不贴矩阵）。*
