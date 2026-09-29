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
