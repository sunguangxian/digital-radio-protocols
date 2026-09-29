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
