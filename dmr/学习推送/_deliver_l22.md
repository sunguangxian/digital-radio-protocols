# 第 22 课 · FULL LC / SHORT LC

> DMR 深入学习 · **阶段 C 空口深入第 8 课**  
> 适合：已吃透第 14 课「FID/FLCO」、第 17 课「超帧 B–E 嵌入」、第 18 课「CACH Short LC / LCSS」、第 21 课「EMB / SLOT」，但仍会把「Short LC 当成 Full LC 截短版」、或分不清「头/终止整包 LC」与「嵌入拼出来的 LC」、或把 EMB/SLOT 小报头误叫成「链路控制正文」的人  
> 阅读量：约 **30–40 分钟** · 几乎不推公式 · 要把「**Full LC 与 Short LC 是两套不同 PDU / 不同运载路径，不是同一张 LC 截短；Full LC ≈72 bit 信息（PF|R|FLCO|FID|Data56）走头/终止（RS 24）与嵌入 B–E（5-bit CS）两条路；Short LC = SLCO4+Data24+CRC8 经 CACH 分片拼装，无单片 LC；FLCO/FID 门牌回指第 14 课；Full LC ≠ Short LC ≠ CSBK ≠ EMB/SLOT**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**，符号率约 **4800 baud**，总比特率约 **9.6 kbps**。Link Control **不换频、不改调制、不另开带宽**——它只是「这次呼叫写在谁门牌上」的正文。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是**两套 LC PDU 怎么长、怎么运、现场怎么对症**。

---

## 1. 为什么本课重要（动机）

第 14 课把门牌钉死了：先看 **FID**，再看 **FLCO**。  
第 17 课把火车排齐了：A = Voice SYNC，**B–E 嵌入 Full LC 碎片**，晚入网靠拼出来的地址。  
第 18 课把缝拆开了：出站 **CACH** 用 LCSS 拼 **Short LC**——且 CACH **没有**「单片 LC」用法。  
第 21 课把两套小报头拆开了：**EMB 16** 管嵌入碎片标签；**SLOT 20** 管数据单据类型（含 Voice LC Header / Terminator with LC）。

同事接下来会盯着分析仪问：

- 屏幕上同时出现 **Voice LC Header**、**Embedded LC**、**Terminator with LC**、**CACH Short LC**——这四样是不是「同一张 LC」的四种写法？  
- 为什么错过 Header 还能进组听？拼出来的那串比特和 Header 里的是不是同一类 PDU？  
- Short LC 的 **SLCO** 和 Full LC 的 **FLCO** 看起来都像 Opcode，能互相替代吗？  
- 培训台上若只背「LC = 链路控制」六个字，后面会卡在同一处：

> **Full LC 与 Short LC 是两套不同的 PDU，走两条不同的运载路径。Full LC 是呼叫「门牌正文」（约 72 bit 信息：PF|Reserved|FLCO|FID|Data56），可整包塞进 Voice LC Header / Terminator with LC（数据壳 + Slot Type），也可拆成碎片嵌进超帧 B–E（EMB+LCSS）。Short LC 更短（SLCO4+Data24+CRC8），只经出站 CACH 慢信道分片拼装——不是 Full LC 的截短版。EMB/SLOT 只是小报头/运货标签；CSBK 是下一课的控制块外壳。**

本课目标是让你能自己讲清十件事：

1. **为什么** Full LC ≠ Short LC（PDU 不同、路径不同、Opcode 表不同）；  
2. 一张总图：头/终止整包、嵌入拼装、CACH 短信令三条路；  
3. 白话术语：Full LC、Short LC、FLCO、SLCO、PF、FID、Service Options、地址门牌；  
4. 机制：Part1 Table **9.7 / 9.8**、clause **7.1 / 9.1.6 / 9.1.7** 精神，少公式；  
5. **Full LC vs Short LC vs CSBK vs EMB/SLOT** 对照表；  
6. 现场：分析仪读 FLCO/地址 vs 只见 EMB；晚入网；CACH 活动更新 vs 话务 LC；错 FID/FLCO vs 错 CC；  
7. 完整例子：组呼 Header+嵌入；Terminator；晚入网；CACH Short LC 拼装草图；误读「Short=截短 Full」；  
8. 数字账本；误区 + 自测 + 资料库 + 核验外链；  
9. 下一课预告：CSBK 控制信令块。

---

## 2. 总图 / 故事：三辆「运门牌」的车

先把整课装进一个故事，再落到 Part1 clauses **5.1.2、7.1、9.1.6、9.1.7、9.3.10–9.3.12** 与资料库 `01-空中接口/CSBK与LC字段详表.md` **§4–§5**、`帧结构与字段定义.md` **§4、§5、§7.3–7.4**、`02-语音业务/语音业务字段速览.md`（业务体指针）。

### 2.1 一句话故事：门牌正文 vs 缝里小广播

把一次组呼想成商场广播：

- **Full LC** = 完整「谁找谁、什么业务」的**门牌正文**（约 72 bit 信息）。可以贴在店门口的大海报上（**Voice LC Header / Terminator with LC**），也可以撕成四条贴纸贴在火车车厢 B–E 上（**嵌入 LC**），方便中途上车的人（**late entry**）仍能认出「这趟车开往哪一组」。  
- **Short LC** = 出站缝里（**CACH**）的**慢速小广播**：活动更新、空消息等——Opcode 叫 **SLCO**，体量更小，**不是**把 Full LC 砍一半。

口诀：**话务门牌看 Full LC；缝里短广播看 Short LC；小报头看 EMB/SLOT；控制块看 CSBK（下一课）。**

### 2.2 总图：三条运载路径

```text
                    ┌─────────────────────────────────────┐
                    │  Full LC 信息场 ≈ 72 bit              │
                    │  Octet0: PF(1)|R(1)|FLCO(6)         │
                    │  Octet1: FID(8)                      │
                    │  Octet2–8: Full LC Data (56)         │
                    │  （组呼直觉：Service Options + 目的24 │
                    │   + 源24 —— 见 Part2 / 资料库）      │
                    └───────────────┬─────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
 【路径① 头/终止整包】      【路径② 嵌入拼装】         【路径③ 与 Full 无关】
 Data Type =                 超帧 B–E：                 Short LC PDU
 Voice LC Header             EMB(8)|碎片(32)|EMB(8)     SLCO(4)+Data(24)+CRC(8)
 或 Terminator with LC       LCSS 标首/续/末            经 CACH 17-bit 载荷分片
 SLOT 小报头 + Data SYNC     拼完 → 同一类 Full LC      （无「单片 LC」）
 CRC：RS(12,9) 24 bit        CRC：5-bit checksum        CRC：8-bit
 PDU 直觉 ≈ 96 bit 壳        嵌入信息场直觉 77 bit      再经 CACH 侧 BPTC
```

### 2.3 和第 14–21 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 14 | FID/SFID/MFID、FLCO 门牌直觉 |
| 第 17 | A=SYNC；B–E 嵌 Full LC；late entry |
| 第 18 | CACH；Short LC；CACH LCSS 无单片 LC |
| 第 19–20 | SYNC 认壳；CC 在 EMB/SLOT |
| 第 21 | EMB/SLOT 小报头；Data Type 路由 Header/Terminator |
| **本课** | 打开 **Full LC / Short LC 正文**：八位组、两条 CRC、三路径对照 |

四句话串起来：

1. **门牌号**在第 14 课（FID+FLCO）；  
2. **小报头**在第 21 课（EMB/SLOT 告诉你「有碎片 / 是哪种单据」）；  
3. **本课**读单据**里面**写了什么、以及 Short LC 另走哪条缝；  
4. **下一课** CSBK 是另一只控制外壳（LB|PF|CSBKO|FID|Data64|CRC16）。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；LC 不另开频。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**；超帧仍 **360 ms**。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps**。  
4. **解调直觉**：先对齐 SYNC / 壳类型 → 读 EMB 或 SLOT → 再解 LC 正文或拼碎片；解错 LC ≠「没解调出射频」，而是「门牌读歪了」。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **Full LC** | 完整链路控制 PDU；信息场约 **72 bit**（Table **9.7**） | ≠ Short LC；≠ EMB；≠ CSBK |
| **Short LC** | 经 **CACH** 的短链路控制；SLCO+Data24+CRC8（Table **9.8**） | ≠「截短的 Full LC」 |
| **FLCO** | Full Link Control Opcode，**6 bit**（Part1 **9.3.11**） | ≠ SLCO；≠ CSBKO（下一课） |
| **SLCO** | Short Link Control Opcode，**4 bit**（Part1 **9.3.12**） | 业务语义见 Part2 |
| **PF** | Protect Flag，Full LC 内 **1 bit**；现行规范置 `0` | ≠ 加密开关口语 |
| **FID** | Feature set ID，**8 bit**；SFID=`0x00` / MFID（第 14 课） | ≠ 24-bit 源/目的地址 |
| **Full LC Data** | 跟在 FID 后的 **56 bit** 业务体 | 随 FLCO 变；组呼常见 Service Options+地址 |
| **Service Options** | 组/个呼 LC 里常见的 **8 bit** 业务选项（紧急/优先级等） | 细则 Part2；本课只建立直觉 |
| **源/目的地址** | 常见各 **24 bit**「谁 ↔ 哪一组/哪个台」 | ≠ Colour Code；≠ FID |
| **Voice LC Header** | Data Type 单据：语音开始，整包带 Full LC | 数据壳 + Slot Type；有 RS 路径 |
| **Terminator with LC** | Data Type 单据：语音结束，整包带 Full LC | 同上；别和「只有 Data SYNC 也能停」混谈细节 |
| **Embedded LC** | 超帧 B–E 四个 32-bit 碎片拼出的 Full LC | 同一类 PDU；CRC 变短（5-bit） |
| **LCSS** | 分片起止（EMB 与 CACH 都有） | CACH **无**单片 LC 用法（第 18/21 课） |
| **EMB / SLOT** | 小报头（16 / 20 bit） | **不是** LC 正文 |
| **CSBK** | 控制信令块外壳（下一课） | Opcode 叫 CSBKO，不是 FLCO |

---

## 4. 机制拆解：先 Full LC，再 Short LC

### 4.1 Full LC PDU（Table 9.7）— 八位组直觉

引用：Part1 clause **9.1.6**；figure **7.1**；资料库 `CSBK与LC字段详表.md` **§4**。

```text
头/终止突发路径（信息场 72 + CRC 相关 → 总 PDU 直觉 96 bit）：
  Octet0:  PF(1) | Reserved(1) | FLCO(6)
  Octet1:  FID(8)
  Octet2–8: Full LC Data (56)
  + Full LC CRC：头/终止 24 bit（Reed-Solomon (12,9)）
嵌入路径：同一信息叙事 + 5-bit checksum；嵌入信息场总长直觉 77 bits（CRC 变短）
```

| IE | Len | 备注 | 条款 |
|----|-----|------|------|
| Protect Flag (PF) | 1 | 现行置 `0` | 9.3.10 |
| Reserved | 1 | | |
| **FLCO** | 6 | 业务 Opcode → **Part 2** | 9.3.11 |
| **FID** | 8 | SFID=`0x00` / MFID | 9.3.5 |
| Full LC Data | 56 | 地址、Service Options 等 | Part 2 |
| Full LC CRC | 24 或 5 | RS(12,9) 或 5-bit CS | B.3.6 / B.3.11 |

**不要背错的一点**：72 bit 是**信息场叙事**（九个八位组的门牌+数据）；头/终止再加 RS 校验进 BPTC(196,96) 壳；嵌入路径校验变短。具体比特级掩码 / RS seed 以 ETSI Annex B 与实现文为准——本课记**名称与路径差异**即可。

### 4.2 Full LC Data 里常见「门牌正文」（组呼直觉）

标准馆（**SFID**）下最常见的语音 LC（第 14 课已见）：

| FLCO（学习摘要） | 别名 | Full LC Data 直觉（Part2） |
|------------------|------|---------------------------|
| `000000` | Grp_V_Ch_Usr | Service Options(8) + **组地址(24)** + **源地址(24)** |
| `000011` | UU_V_Ch_Usr | Service Options(8) + **目的台(24)** + **源地址(24)** |
| `000100`…`000111` | Talker Alias 头/块 | 主叫显示名碎片（嵌入常见） |
| `001000` | GPS_Info | 位置类嵌入（细则 Part2） |

Service Options（Part2 Table 7.11 精神）：紧急、优先级、广播/OVCM 等开关位——本课把它记成「门牌上的业务贴纸」，逐 bit 表回 `02-语音业务/语音业务字段速览.md` **§6**。

> **口诀**：FID 选馆 → FLCO 选服务 → Data 写「谁找谁 + 选项」。

### 4.3 Full LC 的两条（其实是「整包 + 嵌入」）运载路径

#### 路径 A · Voice LC Header / Terminator with LC（整包）

- 走**数据/控制壳**：有 **Slot Type**；Data Type = **Voice LC Header** 或 **Terminator with LC**（Table **9.22** 名，第 21 课）。  
- 中心常是 **Data SYNC**（认「数据壳」）。  
- 196 Info 经 BPTC(196,96) 托起 Full LC + **RS(12,9) 24-bit** 路径。  
- **常规发起**（常规系统）：Header（可选再 PI Header）→ 再进超帧 A…（Part1 **5.1.2.2**）。  
- **结束**：末语音后可跟 Terminator with LC（**5.1.2.3 / 7.1.2**）。

#### 路径 B · 嵌入 B–E（晚入网的主力）

- 走**语音壳**：中心 = **EMB(8)+Embedded(32)+EMB(8)**；**没有 Slot Type**。  
- 一条 Full LC 经可变长 BPTC（Annex **B.2.1**）拆进超帧 **B–E** 四个 32-bit 场；EMB 内 **LCSS** 标首/续/末（Table **9.19**）。  
- 校验用 **5-bit checksum**（B.3.11）——与头/终止的 RS 24 **不是同一条校验故事**。  
- **late entry**：错过 Header 的台，仍可在后续超帧里拼出「组/源」——这是 DMR 设计意图（Part1 **5.1.2**；Part2 组呼叙述）。实现上有的接收机要求「两次一致」才放行，那是工程稳健性，不是另发明一种 PDU。

```text
时间线（常规组呼精神图）：

  [Voice LC Header] → A(SYNC) B C D E F → A B C D E F → … → [Terminator with LC]
       │整包 Full LC│    └──── 每超帧 B–E 再广播同一类 Full LC ────┘      │整包 Full LC│
       │  RS 24    │         （拼装 + 5-bit CS）                          │  RS 24    │
```

### 4.4 Short LC PDU（Table 9.8）— 经 CACH

引用：Part1 clause **9.1.7**；figure **7.2**；`CSBK与LC字段详表.md` **§5**；CACH 结构见第 18 课。

| IE | Len | 备注 | 条款 |
|----|-----|------|------|
| **SLCO** | 4 | 短 Opcode → Part 2 | 9.3.12 |
| Short LC Data | 24 | 随 SLCO 变 | Part 2 |
| Short LC CRC | 8 | 8-bit CRC | B.3.7 |

```text
Short LC：28 bit 信息（SLCO+Data）+ CRC8
        → CACH 侧再经 Variable length BPTC for CACH（Annex B.2.3）
        → 拆进多个 CACH 的 Signalling(17) 载荷，用 TACT 内 LCSS 标分片
```

**硬钉子（再念一遍）**：

1. Short LC **不是** Full LC 砍掉一半地址；八位组布局、Opcode 宽度、运载缝全部不同。  
2. CACH 上 Short LC **无「单片 LC」用法**（clause **9.3.3** / 第 18、21 课）——要等 LCSS 拼完。  
3. 无载荷时发 **Null Short LC**（Part2 `Nul_Msg`，SLCO=`0000`）。

#### Short LC 业务体指针（建立语感，不背全表）

资料库 `语音业务字段速览.md` **§5**：

| SLCO（学习摘要） | 别名 | 直觉 |
|------------------|------|------|
| `0000` | Nul_Msg | 填空 / 无其它 Short LC 可发 |
| `0001` | Act_Updt | 两时隙活动类型 + hashed 地址摘要（出站「谁在忙」小广播） |

Activity ID / hashed address 细则见 Part2 Table **7.10**——本课记住：**Act_Updt 是缝里的活动看板，不是话务 Full LC 的替身**。

### 4.5 FLCO / FID / SFID / MFID —— 回指第 14 课

本课不再重开「商场门牌」长故事，只钉三句：

1. Full LC 里 **FID** 仍是特性集门牌；标准语音业务应走 **SFID=`0x00`**。  
2. **FLCO** 只在选定 FID 下有意义；MFID 下同数值**不可**当标准功能。  
3. Short LC 的 **SLCO** 是另一张 Opcode 表——**不要**拿 FLCO 数值去「翻译」SLCO。

---

## 5. 对照表：Full LC vs Short LC vs CSBK vs EMB/SLOT

| 维度 | Full LC | Short LC | CSBK（预告） | EMB / SLOT |
|------|---------|----------|--------------|------------|
| 角色 | 呼叫门牌**正文** | 缝里**短广播** | 控制块**外壳** | **小报头**（运货标签） |
| 表 | Table **9.7** | Table **9.8** | Table **9.9** | Table **9.3 / 9.4** |
| Opcode | **FLCO 6** | **SLCO 4** | **CSBKO 6** | 无（有 PI/LCSS 或 Data Type） |
| 门牌 FID | 有（8） | 无此八位组布局 | 有（8） | 无 |
| 典型长度叙事 | 信息 72；头终止≈96；嵌入+CS | 信息 28+CRC8 | 信息+CRC16≈96 壳 | 16 / 20 |
| 运载 | Header / Terminator / 嵌入 B–E | **仅 CACH** | 数据壳 Data Type=CSBK | 嵌在突发结构里 |
| 校验名 | RS(12,9) 或 5-bit CS | CRC-8 | CRC-CCITT 16 | QR / Golay |
| 和 CC 关系 | 正文不含 CC；CC 在 EMB/SLOT | 不替代 CC | 同左 | **携带 CC** |

分柜口诀：

```text
看见「组地址 / FLCO / 源台号」→ 你在读 Full LC 正文（或拼出来的同一类）
看见「CACH / SLCO / Act_Updt」→ Short LC
看见「CSBKO / LB」→ 下一课 CSBK
看见「CC + LCSS」或「CC + Data Type」→ 还在小报头（EMB/SLOT），没进正文
```

---

## 6. 现场岗位对照

| 现场现象 | 先看什么 | 本课解释 |
|----------|----------|----------|
| 分析仪已解出 **FLCO / 组 / 源** | Full LC 是否完整（Header 或拼装成功） | 门牌正文已在；再查组配、权限、加密选项 |
| 只有 **EMB / LCSS**，地址栏空 | 碎片是否收齐 B–E？校验是否过？ | 小报头在，正文还没拼出来或 CS 失败 |
| 错过 Header 仍进组 | 后续超帧嵌入 LC | **late entry** 设计如此；不是「神秘补包」 |
| 出站缝里刷 **Act_Updt** | CACH Short LC | 活动看板；**不能**当成话务 Full LC |
| 同频同色仍「各说各话」 | **FID/FLCO** 是否标准馆 | 第 14 课：门牌错 ≠ CC 错 |
| 色码不对整网静音 | EMB/SLOT 的 **CC**（第 20/21 课） | 先过色码门，再谈 LC 正文 |
| 语音壳上硬找 Slot Type | — | 语音无 SLOT；Header/Terminator 才是数据壳 |

**分诊三步（建议贴显示器旁）**：

1. **壳对不对？** SYNC / 语音还是数据（第 19 课）。  
2. **色码过没过？** EMB/SLOT 的 CC（第 20–21 课）。  
3. **门牌正文在哪？** Header/Terminator 整包，或 B–E 拼装；缝里另看 Short LC。

---

## 7. 工作例子（5 则）

### 例子 A · 组呼：Header + 嵌入 Full LC

场景：台源 `1001` 向组 `200` 发起标准组呼（数字仅为教学用）。

1. 空口先见 **Voice LC Header**（Data Type 名，SLOT 里 CC+类型）。  
2. 解 Full LC：`PF=0`，`FID=0x00`，`FLCO=000000`（Grp_V_Ch_Usr），Data 含 Service Options + 组 `200` + 源 `1001`。  
3. 进入超帧：A=Voice SYNC；**B–E** 再嵌入**同一类** Full LC 碎片（LCSS 走首→续→末）。  
4. 同组台即使扫描晚到，也可在下一两个超帧拼出门牌（late entry）。

### 例子 B · Terminator with LC

场景：讲话结束。

1. 末语音超帧后出现 **Terminator with LC**（数据壳 + Data SYNC）。  
2. 其中仍可携带与通话相关的 Full LC（便于对端确认「谁的呼叫结束」）。  
3. 现场：别把「有 Data SYNC」只理解成「同步图案变了」——同时要看 Data Type 是否 Terminator、LC 是否仍可读。

### 例子 C · 晚入网：中途插入超帧

场景：同事打开监听时，Header 已过，正落在某超帧的 **C** 突发。

1. 先靠后续 **A** 的 Voice SYNC 对齐超帧相位（第 17 课）。  
2. 收集 **B–E**（可能跨到下一超帧）拼 Full LC；看 EMB.LCSS 是否完整。  
3. 拼出 `FLCO + 组 + 源` 后，才谈得上「该不该打开扬声器」。  
4. 提醒：实现若要求「两次一致」，属于稳健策略；规范语义仍是「嵌入携带地址 LC」。

### 例子 D · CACH Short LC 拼装草图

场景：中继出站空闲/半忙，缝里在刷短信令。

```text
CACH#n:   LCSS=首片  +  Signalling 碎片…
CACH#n+1: LCSS=续片  +  …
CACH#n+k: LCSS=末片  +  …  → 拼出 Short LC
              SLCO | Short LC Data(24) | CRC8
例：SLCO=0000 → Nul_Msg（填空）
    SLCO=0001 → Act_Updt（两槽活动 + hashed 地址）
```

要点：**没有**「一个 CACH 直接等于一条完整 Short LC 且 LCSS=单片 LC」的用法（与 EMB 路径不同）。

### 例子 E · 误读「Short LC = 截短的 Full LC」

同事指着文档说：「Short 就是 Full 去掉地址。」  
你纠正：

- Full：FLCO**6** + FID**8** + Data**56** +（RS24 或 CS5），走 Header/嵌入；  
- Short：SLCO**4** + Data**24** + CRC**8**，走 **CACH**；  
- Opcode 表不同、有无 FID 不同、CRC 不同、缝不同。  

这是本课最高频的嘴瓢——用 §5 对照表打回去。

---

## 8. 数字账本

| 量 | 值 / 关系 | 别和谁混 |
|----|-----------|----------|
| Full LC 信息场 | **72** bit（9 octets 叙事） | ≠ 264 突发；≠ 196 Info |
| Full LC Data | **56** bit（Octet2–8） | 随 FLCO 变 |
| FLCO | **6** bit | ≠ SLCO 4；≠ CSBKO |
| FID | **8** bit | ≠ 地址 24 |
| 头/终止 CRC | **24** bit，RS**(12,9)** | 嵌入不是这条 |
| 嵌入 checksum | **5** bit | B.3.11 |
| 嵌入碎片 | **4 × 32** bit（B–E） | 加 EMB 标签 |
| Short 信息 | SLCO**4** + Data**24** = **28** | + CRC8 → 再进 CACH BPTC |
| Short CRC | **8** bit | ≠ Full 的 24/5 |
| CACH | **24** bit 缝；载荷约 17 | 第 18 课 |
| EMB / SLOT | **16** / **20** | 小报头，非 LC 正文 |
| 超帧 | **360** ms = 6×30 | A SYNC；B–E 嵌 LC |
| 带宽/调制 | 12.5 kHz + 4FSK | LC **不改变**二者 |

分柜口诀：

```text
门牌正文 …… Full LC（72 信息；头终止 RS24 / 嵌入 CS5）
缝里短广播 … Short LC（4+24+8 → CACH）
运货标签 …… EMB 16 / SLOT 20
下一课外壳 … CSBK（LB|PF|CSBKO|FID|64|CRC16）
```

---

## 9. 常见误区（10 则）

1. **「Short LC 就是截短的 Full LC。」** → 否。不同 PDU、不同 Opcode 宽、不同路径。  
2. **「EMB 就是 Link Control。」** → 否。EMB 是小报头；中间 32 才是碎片载荷。  
3. **「有 Voice SYNC 就等于读到了组地址。」** → 否。A 对齐超帧；地址在 Header 或 B–E 拼装。  
4. **「嵌入 LC 和 Header LC 是两种业务。」** → 通常是**同一类 Full LC** 的不同运载；CRC 路径不同。  
5. **「CACH 上可以像 EMB 那样发单片 LC。」** → 否。CACH Short LC 无单片 LC 用法。  
6. **「FLCO 数值拿到 Short LC 当 SLCO 用。」** → 否。两张表。  
7. **「错 FLCO 和错 CC 是一回事。」** → 否。CC 是同频色；FLCO/FID 是门牌服务。  
8. **「FID 就是源地址。」** → 否。FID 8 bit 特性集；地址常见 24 bit。  
9. **「改 LC 会换 12.5 kHz 或 4FSK。」** → 否。  
10. **「分析仪只显示 EMB 就说明没有 LC。」** → 可能只是还没拼完或 CS 失败——先查 B–E 完整性。

---

## 10. 自测（8 题）

**题 1.** 用一句话区分 Full LC 与 Short LC。为什么说「不是截短关系」？

<details><summary>简答</summary>

Full LC 是约 72 bit 信息的呼叫门牌正文，走 Header/Terminator/嵌入；Short LC 是 SLCO+24+CRC8，只经 CACH。Opcode 宽度、有无 FID、校验、运载缝全不同——不是同一 PDU 截短。

</details>

**题 2.** 画出 Full LC 八位组外壳（PF/R/FLCO/FID/Data），并写出头/终止与嵌入两条 CRC 名称差异。

<details><summary>简答</summary>

`[PF|R|FLCO][FID][Data 56][+CRC]`。头/终止：RS**(12,9)** 24-bit；嵌入：5-bit checksum。

</details>

**题 3.** Full LC 有哪两条主要运载路径？各依赖什么小报头/单据类型？

<details><summary>简答</summary>

① Voice LC Header / Terminator with LC：数据壳 **SLOT** + Data Type。② 超帧 B–E 嵌入：语音壳 **EMB+LCSS**，无 Slot Type。

</details>

**题 4.** 标准组呼 Full LC 在 SFID 下，FLCO 学习值是什么？Data 里通常有哪三类字段直觉？

<details><summary>简答</summary>

FLCO=`000000`（Grp_V_Ch_Usr）。直觉：Service Options + 组地址 24 + 源地址 24（细则 Part2）。

</details>

**题 5.** Short LC 三个字段长度？经哪条物理缝？CACH 分片有何特殊提醒？

<details><summary>简答</summary>

SLCO**4** + Data**24** + CRC**8**；经出站 **CACH**。提醒：无「单片 LC」用法，须按 LCSS 拼装。

</details>

**题 6.** 对照表各用一句话区分：Full LC、Short LC、EMB/SLOT、CSBK。

<details><summary>简答</summary>

Full=门牌正文；Short=缝里短广播；EMB/SLOT=小报头；CSBK=控制块外壳（FLCO≠CSBKO）。

</details>

**题 7.** 现场「色码对、有语音超帧，但扬声器不响」——如何用本课做下一步？

<details><summary>简答</summary>

查是否拼出/解出 Full LC 地址与组匹配；FLCO/FID 是否标准馆；是否落在错误时隙。区分「CC 已过」与「门牌正文未匹配」。

</details>

**题 8.** 为什么说 late entry 证明「嵌入 LC 不是装饰」？它替代 Header 了吗？

<details><summary>简答</summary>

嵌入重复广播同一类门牌，让中途加入者仍能识别组/源——这是设计能力。它不消灭 Header 的发起角色；常规系统发起仍常用 Header，嵌入是并行的重复与补救路径。

</details>

---

## 11. 资料库加深

按这个顺序读，避免一上来背厂商解码树黑话：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `01-空中接口/CSBK与LC字段详表.md` **§4–§5** | Full LC Table 9.7；Short LC Table 9.8 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§4、§5、§7.3–7.4** | 超帧嵌入；CACH；FULL/SHORT 外壳 |
| 3 | `02-语音业务/语音业务字段速览.md` **§1、§3、§5、§6** | FLCO 业务体；Short LC Act_Updt；Service Options |
| 4 | `学习推送/第14课.md` | FID/FLCO 门牌（本课前门） |
| 5 | `学习推送/第17课.md` | B–E 嵌入与 late entry 故事 |
| 6 | `学习推送/第18课.md` | CACH / Short LC / LCSS |
| 7 | `学习推送/第21课.md` | EMB/SLOT；Data Type=Header/Terminator |
| 8 | 官方 **TS 102 361-1 V2.7.1** clause **7.1、9.1.6–9.1.7、9.3.10–9.3.12**；Tables **9.7、9.8**；Annex **B.2.1、B.2.3、B.3.6、B.3.7、B.3.11** | 原文；冲突以 PDF 为准 |
| 9 | 官方 **TS 102 361-2**（本库 `02-语音业务/TS102361-2_V2.5.1.pdf`）clause **7.1.x** | FLCO/SLCO **业务体**；勿用 Part1 冒充 |
| 10 | **TR 102 398** | 概念导读，**不是**替代 TS |
| 11 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍怀疑「LC 会换调制」 |

官方版本锚点：**Part1 V2.7.1**；语音业务体以本库 **Part2** PDF 为准。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 12. 下一课预告

**第 23 课 · CSBK 控制信令块**

本课站住了链路控制正文：**Full LC**（门牌 72 + 头终止/嵌入两路径）与 **Short LC**（CACH 慢广播），并钉死「Short ≠ 截短 Full、EMB/SLOT 只是标签」。下一课打开另一只控制外壳：**CSBK**——`LB|PF|CSBKO|FID|Data64|CRC-16`，单块与 MBC、和 Full LC 的分工（谁管呼叫门牌、谁管请求/应答/唤醒等控制事务），仍少公式，多对照字段表与现场抓包。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-29**（上午推送）检索核验；真实打开过内容页/PDF；**不编造地址**。策略 = **Part1 Full/Short LC 原文 + Part2 业务体指针 + TR 导读 + GopherTrunk Link Control/Late Entry 深文 + CACH 词条 + Wavecom/培训 PDF 帧图**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **7.1** 讲 Voice LC Header / Terminator / Embedded / Short LC in CACH；**9.1.6 / 9.1.7** 与 Tables **9.7 / 9.8** 定义两套 PDU；**9.3.11–9.3.12** 钉 FLCO/SLCO。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读里对链路控制/突发/嵌入的叙事比纯条款好读，便于和本课总图对账。  
   - **适合哪一段**：第 2、7、11 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
   - **为什么值得看**：把 72-bit Full LC、Header/Terminator/嵌入三条运载、B–E 拼装与 late entry 写成同一条故事线——本课例子 A/C 的加厚版。  
   - **适合哪一段**：第 4、6、7、12 节。  
   - **注意**：实现向（如「确认两次」）是工程选择；规范语义以 ETSI 为准。文中若把 EMB 的 PI 写成 privacy 口语，**以 Part1「Pre-emption and power control Indicator」为准**（业务 Privacy 在 Service Options / Part2）。  
   - **基础**：中级～进阶；英文网页。

4. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：Slot Type 与 EMB+嵌入 LC 拼装同框，便于回看第 21 课小报头如何托起本课正文。  
   - **适合哪一段**：第 2、4、5 节。  
   - **注意**：校验命名以 ETSI Annex B 为准。  
   - **基础**：中级～进阶；英文网页。

5. **[GopherTrunk｜DMR CACH（词条）](https://gophertrunk.org/reference/dmr-cach/)**  
   - **为什么值得看**：巩固「Short LC 住在出站缝」；并诚实标明实现可能只拿 CACH 当节拍——对照第 18 课与本课 §4.4。  
   - **适合哪一段**：第 4、7 节例子 D。  
   - **注意**：词条偏 SDR 节拍；**Short LC 业务体仍以 Part2 为准**。  
   - **基础**：入门～中级；英文网页。

6. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：帧/突发/超帧 A–F 图，便于把 Header→A–F→Terminator 钉回 264 与缝。  
   - **适合哪一段**：第 2、7 节。  
   - **注意**：厂商综述，版本锚点可能早于 V2.7.1；**硬条款以现行 Part1 为准**。  
   - **基础**：中级；英文 PDF。

7. **[Alessandro Guido｜How DMR Works — primer PDF（hamgear）](https://hamgear.files.wordpress.com/2014/02/dmr-primer.pdf)**  
   - **为什么值得看**：培训幻灯式回顾 Voice LC Header/Terminator、嵌入 LC、Short LC in CACH、FEC/CRC 名称表——和本课数字账本同向。  
   - **适合哪一段**：第 4、8、11 节后复盘。  
   - **注意**：年代偏早、版本号旧；**以 V2.7.1 / 本库 Part2 为准**。  
   - **基础**：入门～中级；英文 PDF。

8. **[GopherTrunk｜DMR End to End Part 2：Bursts, Sync Words & Polarity](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-02-bursts-sync-polarity/)**  
   - **为什么值得看**：再次钉死「语音突发没有 Slot Type」——避免把嵌入路径误读成「也有 Data Type」。  
   - **适合哪一段**：第 4、5、9 节。  
   - **注意**：偏扫描器/实现；极性故事超纲可略读。  
   - **基础**：中级；英文网页。

9. **[qdmr 手册｜Technical background（Time Slot & Color Code）](https://static.dm3mat.de/qdmr/manual/ch01s09.html)**  
   - **为什么值得看**：从工程动机复习色码门——读 LC 正文前先过 CC（第 20–21 课保活）。  
   - **适合哪一段**：第 1、6 节热身。  
   - **注意**：开源写频文档，**不是** Full/Short LC 字段专论。  
   - **基础**：入门；英文网页。

**说明（视频）**：公开检索未找到专门把 **「Full LC 72 信息 + 头终止 RS24 / 嵌入 CS5；Short LC 4+24+8 经 CACH；FLCO≠SLCO；三路径对照；late entry」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只演示写频组呼或产品抓包界面，不拆 PDU）。本课**未找到合适公开专题视频**。建议用：**Part1 Tables 9.7/9.8 + GopherTrunk E2E Part5 + 资料库 §4–§5 / 语音业务速览** 对照自学。

---

*推送说明：本课为阶段 C「FULL LC / SHORT LC」。频谱/调制仅保留短提醒（LC 不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、三路径总图、术语、Full LC 八位组与两 CRC 路径、Short LC/CACH、FLCO 门牌回指、四柜对照、现场分诊、五则工作例子、数字账本、十则误区、八题自测、资料库路径与九条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「Full LC 与 Short LC 为何不是截短关系、门牌正文如何经 Header/嵌入两路到达、CACH 短广播怎么拼、为何不能把 EMB/SLOT 叫成 LC」，并进入第 23 课 CSBK 控制信令块。*
