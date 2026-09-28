# 第 21 课 · EMB / SLOT 字段

> DMR 深入学习 · **阶段 C 空口深入第 7 课**  
> 适合：已吃透第 16 课「突发 264」、第 17 课「语音超帧 A–F」、第 18 课「CACH 与 Guard」、第 19 课「SYNC 分壳」、第 20 课「Colour Code」，但仍会把「中心 48 全叫 EMB」、或在语音突发上硬找 Slot Type、或分不清「错 Data Type」与「错 CC」的人  
> 阅读量：约 **30–40 分钟** · 几乎不推公式 · 要把「**语音嵌入小报头 = EMB 16 bit（CC+PI+LCSS+QR）；数据/控制小报头 = SLOT 20 bit（CC+Data Type+Golay）；语音突发没有 Slot Type；Data Type 决定 196 Info 怎么解；LCSS 管分片起止；PI 提示对端 RC；SYNC ≠ EMB ≠ SLOT ≠ CACH**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**，符号率约 **4800 baud**，总比特率约 **9.6 kbps**。EMB / SLOT **不换频、不改调制、不另开带宽**——它们只是嵌在突发里的**小报头**。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是**两套小报头怎么读、现场怎么对症**。

---

## 1. 为什么本课重要（动机）

第 16 课把货箱钉死了：264 = 108+48+108；数据壳撕出 Slot Type。  
第 17 课把语音火车排齐了：A = Voice SYNC，B–E 嵌入 Full LC 碎片，F 常 Null/RC。  
第 18 课把缝拆开了：出站 CACH、入站 Guard——**缝不在 264 里**。  
第 19 课把中心 48 的 SYNC 字典拆开了。  
第 20 课把 **Colour Code 4 bit** 从 Slot Type / EMB 里拎出来：同频刷色、SYNC ≠ CC。

同事接下来会盯着分析仪问：

- 屏幕上写着 **EMB**、**Slot Type**、**Data Type=CSBK / Voice LC Header / Idle**——这些各住哪？谁都不该被叫成「中心 48」？  
- 语音超帧 **A** 明明有 Voice SYNC，为什么后面 **B–E** 又冒出 EMB？晚入网（late entry）靠的是哪一段？  
- 为什么「色码对了」仍解不出话务，分析仪却显示 **Data Type 不对**或 **parity 失败**？  
- 培训台上若只背「中间有个小报头」六个字，后面会卡在同一处：

> **语音壳与数据壳用两套不同的小报头。带嵌入的语音突发：中心 = EMB(8)+嵌入(32)+EMB(8)，EMB PDU 合计 16 bit（CC+PI+LCSS+QR 校验）。数据/控制突发：两侧各撕 10 bit 成 SLOT PDU 20 bit（CC+Data Type+Golay 校验），中心仍是 48 bit 的 SYNC 或嵌入。语音突发没有 Slot Type；Data Type 才决定左右 196 Info 比特按哪种单据解。SYNC 认壳，CACH 管缝，EMB/SLOT 才是「壳内小报头」。**

本课目标是让你能自己讲清十件事：

1. **为什么**要把 EMB 与 SLOT 当两套柜子记（语音 vs 数据壳）；  
2. 一张总图：两种中心布局 + 谁没有 Slot Type；  
3. 白话术语：EMB、SLOT、PI、LCSS、Data Type、parity 名；  
4. 机制：Table 9.3 / 9.4 / 9.19 / 9.22 精神，少公式；  
5. **EMB vs SLOT vs SYNC vs CACH** 对照表；  
6. 现场：分析仪读 Data Type、LCSS 拼 LC、错 CC vs 错 Data Type、PI/RC 直觉；  
7. 完整例子：Header→A→B–E→Terminator；CSBK；Idle；误读「EMB=整段 48」；  
8. 数字账本；误区 + 自测 + 资料库 + 核验外链；  
9. 下一课预告：Full LC / Short LC。

---

## 2. 总图 / 故事：两套「小报头」

先把整课装进一个故事，再落到 Part1 clauses **6.1、6.2、7.1.3、9.1.2、9.1.3、9.3.2、9.3.3、9.3.6** 与资料库 `01-空中接口/帧结构与字段定义.md` **§3、§7.1–7.2、§8**、`CSBK与LC字段详表.md` **§2–§3**。

### 2.1 一句话故事：语音贴「嵌入标签」，数据贴「单据类型」

同一只 **264 bit** 货箱，中间总有约 **48 bit** 宽的中心场——但**怎么拆**取决于这是语音还是数据：

- **语音、且中心不是 Voice SYNC 时**：两侧各贴 8 bit **EMB**，中间夹 32 bit 嵌入信令碎片。EMB 告诉你：色码、是不是对端 RC、这块碎片是头/中/尾。  
- **数据/控制时**：左右 Info 各收成 98 bit，腾出两侧各 10 bit 拼成 **Slot Type（SLOT）**；SLOT 告诉你：色码 + **这张单据是 Header / CSBK / Idle / 数据块…**；中心 48 仍可是 Data SYNC 或别的嵌入。

口诀：**语音嵌入看 EMB；数据单据看 SLOT；认壳看 SYNC；缝里看 CACH。**

### 2.2 总图：两种中心布局

```text
一个 Timeslot = 30.0 ms
├── 内容窗 ≈ 27.5 ms · Traffic burst = 264 bit
│
│   【语音 · 带嵌入信令时 · 第 17 课回忆】
│         Voice(108) | EMB(8) | Embedded(32) | EMB(8) | Voice(108)
│                     └──────── EMB PDU = 16 bit ────────┘
│                          CC(4) + PI(1) + LCSS(2) + parity(9)
│         超帧 A：中心常是 Voice SYNC（整段 48）——此时**没有** EMB 这套拆法
│         ★ 语音突发：没有 Slot Type
│
│   【数据 / 控制突发】
│         Info(98) | SlotType(10) | SYNC或嵌入(48) | SlotType(10) | Info(98)
│                    └──────── SLOT PDU = 20 bit ────────┘
│                         CC(4) + Data Type(4) + parity(12)
│         左右 Info 合计 196 bit —— Data Type 决定怎么解
│
└── 缝 ≈ 2.5 ms · 入站 Guard / 出站 CACH(24)（第 18 课）
         CACH/TACT：AT / TC / LCSS（Short LC）——别和 EMB/SLOT 混柜
```

### 2.3 和第 16–20 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 16 | 264 货箱；数据壳有 Slot Type；语音嵌入有 EMB 外形 |
| 第 17 | A=Voice SYNC；B–E 嵌入；late entry 靠嵌入 LC |
| 第 18 | 缝 = CACH/Guard；CACH 也有 LCSS（Short LC 分片） |
| 第 19 | 中心 48 = SYNC 图案字典 |
| 第 20 | CC 4 bit 住在 Slot Type / EMB；SYNC ≠ CC |
| **本课** | 把 **EMB 16** 与 **SLOT 20** 整包拆开：PI、LCSS、Data Type、两段 parity |

四句话串起来：

1. **货箱**是 264（第 16）；  
2. **语音火车** A 用 SYNC，B–F 用嵌入窗（第 17）；  
3. **CC** 在小报头里刷色（第 20）；  
4. **本课**读完整小报头——EMB 管嵌入碎片标签，SLOT 管数据单据类型。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz** 一条载波；EMB/SLOT 不另开频。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps**。  
4. **解调直觉**：先对齐突发与中心（常靠 SYNC），再按壳类型解 EMB 或 SLOT；解错小报头 ≠ 「没解调出射频」，而是「路由标签读歪了」。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **EMB** | 语音嵌入时的 **16 bit** 小报头：夹在中心两侧各 8 bit | ≠ 整段中心 48；A 突发中心常是 SYNC |
| **Embedded signalling** | 夹在两半 EMB 中间的 **32 bit** 碎片载荷 | ≠ EMB 本身；可是 LC 片 / RC / Null… |
| **SLOT / Slot Type** | 数据/控制突发上的 **20 bit**：两侧各 10 | **语音突发没有**；别在 Voice SYNC 上硬找 |
| **PI**（EMB 内） | Pre-emption and power control Indicator，**1 bit** | `0`=本逻辑信道/Null；`1`=对端时隙 RC（定时对齐）。≠「加密开关」口语 |
| **LCSS** | Link Control Start/Stop，**2 bit** 分片起止 | EMB 与 CACH 都有，但用法不完全一样（见 §4） |
| **Data Type** | SLOT 内另 **4 bit**：单据种类（Table 9.22） | ≠ Colour Code；决定 196 Info 怎么解 |
| **Colour Code** | EMB/SLOT 内各有的 **4 bit** 系统色（第 20 课） | ≠ SYNC；≠ Talkgroup |
| **EMB parity** | QR **(16,7,6)**，9 bit——**记名即可** | 不贴矩阵（见跳过项原则） |
| **Slot Type parity** | Golay **(20,8)**，12 bit——**记名即可** | 实现文或称 shortened Hamming；以 ETSI Annex B / 资料库为准 |
| **SYNC** | 中心 **48 bit** 图案，认壳 | 不含 CC/Data Type 字段 |
| **CACH** | 出站缝 **24 bit** | 主场 AT/TC/短 LC；不是 EMB/SLOT |
| **196 Info** | 数据壳左右 98+98 | 须先读对 Data Type 再解 PDU |
| **Full LC / Short LC** | 链路控制整包 / CACH 短包 | **下一课**主角；本课只碰到「分片怎么标」 |

---

## 4. 机制拆解：先 EMB，再 SLOT

### 4.1 EMB PDU（Table 9.3）— 16 bits

引用：Part1 **9.1.2**；资料库 `帧结构与字段定义.md` §7.1、`CSBK与LC字段详表.md` §2。

```text
语音突发（中心非 SYNC 时）：
  Voice(108) | EMB(8) | Embedded signalling(32) | EMB(8) | Voice(108)
               └─────────── EMB PDU 共 16 bit ───────────┘

EMB 信息场直觉：
  ┌────────┬────┬──────┬─────────────┐
  │ CC 4   │ PI │ LCSS │ EMB parity  │
  │        │ 1  │  2   │     9       │
  └────────┴────┴──────┴─────────────┘
   └──── 信息 7 bit ────┘└── 校验 9 ──┘
```

| IE | Bits | 含义（学习用） |
|----|------|----------------|
| Colour Code | 4 | CC0…CC15（第 20 课） |
| **PI** | 1 | `0`：嵌入属**本逻辑信道**或 Null；`1`：属**对端时隙的 RC**（与本突发定时对齐） |
| **LCSS** | 2 | 分片起止，见下表 |
| EMB parity | 9 | Quadratic Residue **(16,7,6)**——只记名字 |

**何时没有这套 EMB 拆法？**  
超帧 **burst A** 中心通常是整段 **Voice SYNC（48 bit）**——那是图案，不是「SYNC 里藏了半个 EMB」。语音过程中的小报头，要到 **B–F 的嵌入窗**（以及呼叫前后的数据壳单据：Voice LC Header / Terminator 的 Slot Type）上去找。

### 4.2 LCSS（Table 9.19）— 分片「页码」

| Value | 含义（嵌入 / 语音路径常见说法） |
|-------|--------------------------------|
| **00** | **单片** LC，**或** CSBK 类首片（视上下文） |
| **01** | LC **首片**（非单片） |
| **10** | **末片** |
| **11** | **续片** |

现场直觉（语音超帧拼 Full LC，第 17 课）：

```text
典型一条 Full LC 拆进 B–E 四个 32-bit 嵌入场：
  B: LCSS=01（首）  + 碎片1
  C: LCSS=11（续）  + 碎片2
  D: LCSS=11（续）  + 碎片3
  E: LCSS=10（末）  + 碎片4
  → 四片拼齐再做嵌入侧 BPTC/校验 → 得到 Full LC（细节下节课）
```

**和 CACH 的 LCSS 差在哪？（第 18 课领地，这里只钉一句）**  
CACH 上跑 **Short LC** 分片时，规范精神是：**没有「单片 LC」那种用法**（资料库：CACH Short LC 无「单片 LC」）。同一名字 **LCSS**，柜不同——EMB 柜 vs CACH 柜，别混着背取值故事。

### 4.3 PI：对端 RC 的「指一下」

PI 不是写频软件里的「Privacy 加密勾选」口语（那是另一条业务故事）。  
在 EMB 里，它更像一块**路牌**：

- `PI=0`：这 32 bit 嵌入窗说的是**本逻辑信道**上的事（含 Null 填充）。  
- `PI=1`：嵌入窗里是**对端时隙**的 Reverse Channel 信息，且与本突发**定时对齐**——方便在「双时隙都在动」时做抢占/功率类控制信令（细则多在 Part 4 / RC PDU；本课只建立直觉）。

排障口诀：**先别把 PI 当成「有没有加密」；先问「这窗是不是对端 RC」。**

### 4.4 SLOT PDU（Table 9.4）— 20 bits

引用：Part1 **9.1.3**；资料库 §7.2 / §8。

```text
数据 / 控制突发：
  Info(98) | SlotType(10) | SYNC或嵌入(48) | SlotType(10) | Info(98)
             └────────── SLOT PDU 共 20 bit ──────────┘

SLOT 信息场直觉：
  ┌────────┬────────────┬──────────────────┐
  │ CC 4   │ Data Type  │ Slot Type parity │
  │        │     4      │        12        │
  └────────┴────────────┴──────────────────┘
   └──── 信息 8 bit ────┘└──── 校验 12 ────┘
```

| IE | Bits | 含义 |
|----|------|------|
| Colour Code | 4 | 同 EMB，系统色 |
| **Data Type** | 4 | Table **9.22**：单据种类 |
| Slot Type parity | 12 | Golay **(20,8)**——记名即可 |

**关键钉子：语音突发没有 Slot Type。**  
语音壳左右是 **108+108** 声码载荷，中心是 SYNC 或 EMB+嵌入——**不会**再撕出两侧各 10 bit 的 SLOT。若分析仪在 Voice 突发上「解出」稀奇古怪的 Data Type，先怀疑：是不是把声码比特误当 Slot Type 读了（实现/极性类坑；学习层面记住「语音无 SLOT」即可）。

### 4.5 Data Type（Table 9.22）— 196 Info 的「路由表」

Data Type 回答：**左右 196 个信息比特，按哪张单据解？**（多数控制类再经 BPTC(196,96) 等——本课只记「先看类型再解」，不贴矩阵。）

| Value | Meaning | 现场一句话 |
|-------|---------|------------|
| 0000 | PI Header | 隐私/密钥指示类头（细节后课） |
| 0001 | **Voice LC Header** | 语音开始，常带地址（呼叫「发车单」） |
| 0010 | **Terminator with LC** | 语音结束，带 LC（「到站单」） |
| 0011 | **CSBK** | 控制信令块 |
| 0100 | MBC Header | 多块控制·头 |
| 0101 | MBC Continuation | 多块控制·续 |
| 0110 | Data Header | 分组数据头 |
| 0111 | Rate ½ Data | ½ 码率数据续块 |
| 1000 | Rate ¾ Data | ¾ 码率数据续块 |
| 1001 | **Idle** | 填充/保活类空单据 |
| 1010 | Rate 1 Data | 近似不编的高码率数据 |
| 1011 | Unified Single Block Data | 单块统一数据/控制 |
| 1100–1111 | Reserved | 预留 |

实用解码地图（先建立肌肉记忆）：

```text
看到 Data SYNC + SLOT 合法
  → 读 CC（第 20 课：是否本系统）
  → 读 Data Type：
        Voice LC Header / Terminator → 按 Full LC 路径解 196
        CSBK / MBC → 按控制块路径解
        Data Header / Rate… → 按数据路径解
        Idle → 填充，别当「坏语音」
  → 再谈 Opcode、地址、CRC……
```

### 4.6 语音呼叫时间线：Header → A → B–E → Terminator

把第 17 课与本课小报头串成一条时间线：

```text
[数据壳] Voice LC Header     ← Slot Type: Data Type=0001；中心常 Data SYNC
        （可选再 PI Header 等）
[语音壳] A : 中心 = Voice SYNC（48）     ← 无 EMB 拆法；无 Slot Type
         B : EMB + LC 碎片（LCSS=01）
         C : EMB + 续片（LCSS=11）
         D : EMB + 续片（LCSS=11）
         E : EMB + 末片（LCSS=10）
         F : 常 Null / RC / Privacy 嵌入（视方向与配置）
        （超帧可重复；嵌入 LC 支持 late entry）
[数据壳] Terminator with LC  ← Slot Type: Data Type=0010；中心常 Data SYNC
```

口诀：**发车单/到站单看 SLOT；车上广播碎片看 EMB；站台暗号看 SYNC。**

---

## 5. 对照表：EMB vs SLOT vs SYNC vs CACH

| | **EMB** | **SLOT** | **SYNC** | **CACH** |
|--|---------|----------|----------|----------|
| **住哪** | 语音嵌入时，中心两侧各 8 | 数据壳，中心两侧各 10 | Traffic **中心** | 出站 **缝**（不在 264 内） |
| **总长** | **16 bit** | **20 bit** | **48 bit** | **24 bit** |
| **信息里有啥** | CC+PI+LCSS | CC+Data Type | 图案（认壳） | AT+TC+LCSS（TACT）等 |
| **校验名** | QR (16,7,6) | Golay (20,8) | 靠图案相关/匹配 | TACT：Hamming (7,4) |
| **语音突发有吗** | A 常无（用 SYNC）；B–F 常有 | **无** | A 有 Voice SYNC | 与突发类型无关（缝另算） |
| **数据突发有吗** | 中心若走嵌入路径才涉及 | **有** | 常有 Data SYNC | 出站缝仍可有 |
| **主要干什么** | 给嵌入碎片贴标签 | 给 196 Info 选单据类型 | 对齐与分壳 | 忙闲、槽号、Short LC |
| **和第 20 课** | 内含 CC | 内含 CC | **不含** CC | 不是 CC 主场 |

三句钉子：

1. **SYNC 成功** ≠ 已读懂 EMB/SLOT；更 ≠ CC/Data Type 已对。  
2. **有 EMB** ≠ 中心 48 全是 EMB——中间 32 是载荷碎片。  
3. **CACH 的 LCSS** ≠ 自动等于 **EMB 的 LCSS** 故事。

---

---
