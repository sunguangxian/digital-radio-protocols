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

## 6. 现场岗位对照

| 岗位动作 | 先看什么 | 本课用得上的钉子 |
|----------|----------|------------------|
| 写频 / 开站 | 频点、时隙、**CC**、组 | CC 在 EMB/SLOT；本课不改写频格，但解释分析仪字段 |
| 空口分析仪 | SYNC 类型 → **Slot Type / EMB** → Data Type / LCSS | 语音无 SLOT；别把 48 标成「EMB」 |
| 有能量没声 | 射频 → SYNC → **CC** → **Data Type/组** | 错 CC vs 错 Data Type 分诊（下节） |
| 晚入网投诉 | 是否听到 Header；嵌入 LC 是否拼齐 | LCSS 首/续/末；B–E 四片 |
| 控制面抓包 | Data Type=CSBK/MBC/Idle | Idle 不是「坏语音」 |
| 双时隙怪异信令 | EMB 的 **PI** | 是否对端 RC 窗 |
| 培训口述 | 两套小报头 + 四柜对照 | 用 §5 表，不背厂商黑话 |

**错 CC vs 错 Data Type（分诊口诀）**

```text
症状 A：SYNC 有，CC 与写频不一致
  → 第 20 课：不当本系统 / 有能量没合法声
  → 先改色码对齐，再谈单据

症状 B：CC 对，但 Data Type 显示 Idle / 预留 / 与现场业务不符
  → 可能：抓到填充、抓错时隙、极性/壳误判、或业务本就不是语音
  → 别先骂色码；看 SLOT 的 Data Type 与中心 SYNC 是否「数据壳」

症状 C：语音超帧 A 同步很好，但拼不出 LC
  → 查 B–E 是否有合法 EMB、LCSS 是否成套、碎片是否丢
  → 这是 EMB/LCSS 问题，不是「再改一次 CC」就能糊弄过去
```

---

## 7. 工作例子（5 则）

### 例子 A · 完整语音：Header → A → B–E → Terminator

园区中继上，组呼一次 PTT。

1. 空口先出现 **数据壳**：Slot Type 解出 `Data Type = Voice LC Header (0001)`，CC=7；196 Info 里是 Full LC（地址等）。  
2. 进入语音超帧：**A** 中心 = **BS Voice SYNC**（无 EMB、无 SLOT）。  
3. **B–E**：中心拆成 EMB+32；LCSS 走 01→11→11→10；EMB 内 CC 仍为 7。  
4. 末了再出 **Terminator with LC**（`Data Type=0010`）。  

培训一句：**发车单/到站单看 SLOT；车上四片看 EMB+LCSS。**

### 例子 B · 分析仪读 CSBK

空闲时隙上偶发控制。分析仪：Data SYNC 稳定；`Slot Type: CC=3, Data Type=CSBK (0011)`；payload 解出某 CSBKO。  

要点：这是 **SLOT 路由成功** 的故事——若 CC 写成 5，同一 CSBK 可能根本不当本系统；若误把该突发当语音去找 EMB，会缘木求鱼。

### 例子 C · Idle 填充

中继键上但无话务，双时隙刷 **Idle**（`Data Type=1001`）。新手常报「有数字信号怎么没声音」。  

要点：Idle 是合法填充单据，不是坏掉的 Voice LC Header。先看 Data Type，再决定要不要找声码。

### 例子 D · 晚入网：错过 Header，靠 B–E

手台中途开机，没听到 Voice LC Header，仍能进组听——因为超帧 **B–E** 重复嵌着 Full LC 碎片；EMB 的 LCSS 帮接收机拼页。  

要点：**Late entry 吃的是嵌入路径 + LCSS，不是再变一次 SYNC 图案。**（拼 LC 的字段细节 → 第 22 课。）

### 例子 E · 误读「EMB = 整段 48」

同事指着解码树说：「这 48 全是 EMB。」  
你纠正：嵌入时是 **8+32+8**；只有两侧合起来的 **16** 叫 EMB PDU；中间 **32** 是碎片载荷。A 突发更是整段 SYNC，更不该标 EMB。  

这是本课最高频的嘴瓢——用总图打回去。

---

## 8. 数字账本

| 量 | 值 / 关系 | 别和谁混 |
|----|-----------|----------|
| Traffic | **264** = 常记 108+48+108（语音外形） | 数据壳外形是 98+10+48+10+98 |
| 语音嵌入中心 | **8+32+8** | ≠ 「48 全 EMB」 |
| **EMB PDU** | **16** = 7 信息 + 9 校验 | 信息：CC4+PI1+LCSS2 |
| **SLOT PDU** | **20** = 8 信息 + 12 校验 | 信息：CC4+Data Type4 |
| SYNC | **48** 中心图案 | 无 CC / 无 Data Type 字段 |
| CACH | **24** 缝 | 第 18 课 |
| 数据 Info | **196** = 98+98 | 先看 Data Type |
| CC | **4** bit，16 色 | 第 20 课 |
| Data Type | **4** bit | Table 9.22 |
| LCSS | **2** bit | Table 9.19 |
| PI | **1** bit | 本信道 vs 对端 RC |
| 校验名 | EMB: QR(16,7,6)；SLOT: Golay(20,8) | 不贴矩阵 |
| 带宽/调制 | 12.5 kHz + 4FSK | 小报头**不改变**二者 |

分柜口诀：

```text
264 货箱
 ├─ 语音嵌入窗 …… 8 | 32 | 8  → EMB 标签 + 碎片
 ├─ 语音 A ……… 整段 SYNC 48
 ├─ 数据壳 ……… SlotType10 | 中心48 | SlotType10 + Info196
 └─ 缝 ………… CACH24 / Guard（第 18 课）
```

---

## 9. 常见误区（10 则）

1. **「中心 48 就叫 EMB。」** → 否。嵌入时是 8+32+8；A 常是 SYNC。  
2. **「语音突发也有 Slot Type。」** → 否。SLOT 是数据/控制壳的。  
3. **「有 SYNC 就等于读到了 Data Type。」** → 否。SYNC 认壳；Data Type 在 SLOT 里。  
4. **「CC 错和 Data Type 错是一回事。」** → 否。分诊见 §6。  
5. **「LCSS=00 在 CACH 和 EMB 上故事完全相同。」** → 不。CACH Short LC 无「单片 LC」用法。  
6. **「PI=1 就是开了加密。」** → 否。EMB 的 PI 指对端 RC / 本信道，别和业务 Privacy 口语绑死。  
7. **「Idle 就是同步失败。」** → 否。Idle 是合法 Data Type。  
8. **「改 EMB/SLOT 会换 12.5 kHz 或 4FSK。」** → 否。  
9. **「Parity 名字背错就不能工作。」** → 现场够用「SLOT 有 Golay 类 12 校验、EMB 有 QR 9 校验」；矩阵留给实现读 PDF。  
10. **「晚入网只靠 Voice SYNC。」** → SYNC 对齐超帧；**拼出是谁在叫**靠嵌入 LC + LCSS（及 Header，若听得到）。

---

## 10. 自测（8 题）

**题 1.** 画出「带嵌入的语音突发」与「一般数据突发」中心附近布局，并标出 EMB PDU、SLOT PDU 各多少 bit。

<details><summary>简答</summary>

语音嵌入：`Voice(108) | EMB(8) | Embedded(32) | EMB(8) | Voice(108)` → **EMB=16**。  
数据：`Info(98) | SlotType(10) | 中心(48) | SlotType(10) | Info(98)` → **SLOT=20**。  
语音突发**没有** Slot Type。

</details>

**题 2.** EMB 16 bit 里除了 Colour Code，还有哪两个信息字段？校验码叫什么（记名即可）？

<details><summary>简答</summary>

**PI（1）**、**LCSS（2）**；校验为 Quadratic Residue **(16,7,6)**（9 bit parity）。

</details>

**题 3.** LCSS 取值 00/01/10/11 在语音嵌入路径上大致表示什么？CACH 上有何提醒？

<details><summary>简答</summary>

常见：`00` 单片或 CSBK 首片；`01` LC 首片；`10` 末片；`11` 续片。  
提醒：CACH Short LC **无「单片 LC」用法**——同名不同柜。

</details>

**题 4.** SLOT 里的 Data Type 干什么用？举三个现场最常见的取值名。

<details><summary>简答</summary>

决定 **196 Info** 按哪种单据解。常见如：**Voice LC Header**、**Terminator with LC**、**CSBK**、**Idle**（答出三个即可）。

</details>

**题 5.** 为什么说「语音超帧 A 通常读不到 EMB」？那语音过程中的 CC 去哪读？

<details><summary>简答</summary>

A 中心常是整段 **Voice SYNC 图案**，不是 EMB 拆法。语音中的 CC 到 **B–F 的 EMB**，以及前后 **Header/Terminator 的 Slot Type** 上读。

</details>

**题 6.** 用对照表各用一句话区分 EMB、SLOT、SYNC、CACH。

<details><summary>简答</summary>

EMB=语音嵌入小报头(16)；SLOT=数据壳小报头(20)；SYNC=中心认壳图案(48)；CACH=出站缝广播(24)。

</details>

**题 7.** 现场「有 SYNC、CC 也对，但没有语音」——你如何用 Data Type 做下一步？

<details><summary>简答</summary>

看是否落在 **Idle / CSBK / 数据块** 而非 Voice LC Header+语音超帧；或是否抓错时隙。先分清单据类型，再查组地址/业务，避免只在色码上打转。

</details>

**题 8.** PI=1 的学习直觉是什么？它是不是「Colour Code 的一部分」？

<details><summary>简答</summary>

直觉：嵌入窗指向**对端时隙 RC**（定时对齐），而非默认本信道 Null/LC。  
PI 是 EMB 内独立 1 bit，**不是** CC 的一部分（CC 另有 4 bit）。

</details>

---

## 11. 资料库加深

按这个顺序读，避免一上来背厂商解码树黑话：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `00-入门/DMR术语与帧结构速查卡.md` | 264 / 超帧 / SYNC / CACH 总尺 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§3** | 语音 108+48+108；数据 98+SLOT+48；嵌入 8+32+8 |
| 3 | 同上 **§7.1 / §7.2** | EMB PDU、SLOT PDU |
| 4 | 同上 **§8** | LCSS、Data Type、Table 9.22 速查 |
| 5 | `01-空中接口/CSBK与LC字段详表.md` **§1–§3** | 嵌入位置、EMB、SLOT、LCSS 表 |
| 6 | `01-空中接口/跳过项原则说明.md` §1.4 | Golay/QR **记名不贴矩阵** |
| 7 | `学习推送/第16课.md`–`第17课.md` | 货箱与超帧；EMB 出场 |
| 8 | `学习推送/第18课.md`–`第19课.md` | CACH LCSS vs SYNC 分壳 |
| 9 | `学习推送/第20课.md` | CC 与同频；本课的前门 |
| 10 | 官方 **TS 102 361-1 V2.7.1** clause **6.1–6.2、9.1.2–9.1.3、9.3.2–9.3.3、9.3.6**；Tables **9.3、9.4、9.19、9.22** | 原文；冲突以 PDF 为准 |
| 11 | **TR 102 398** | 概念导读，**不是**替代 TS |
| 12 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍怀疑「小报头会换调制」 |

官方版本锚点：**Part1 V2.7.1**；**TR V1.5.1**。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 12. 下一课预告

**第 22 课 · FULL LC / SHORT LC**

本课站住了两套小报头：**EMB 16**（CC+PI+LCSS+QR）与 **SLOT 20**（CC+Data Type+Golay），并钉死「语音无 Slot Type、Data Type 路由 196、LCSS 管分片」。下一课进入报头背后的**链路控制正文**：Full LC 八位组（PF/FLCO/FID/地址…）、头/终止与嵌入两条路径、以及 CACH 上的 Short LC（SLCO+数据）——仍少公式，多对照字段表与呼叫「门牌」。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-28**（傍晚推送）检索核验；真实打开过内容页/PDF；**不编造地址**。策略 = **Part1 EMB/SLOT 原文 + TR 导读 + GopherTrunk 突发/EMB/Slot Type 深文 + Late Entry 嵌入文 + Wavecom 帧图 + 协会/ETSI 镜像**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **6.1 / 6.2** 给语音嵌入与数据壳布局；**9.1.2 / 9.1.3** 与 Tables **9.3 / 9.4** 定义 EMB、SLOT；**9.3.2–9.3.3、9.3.6** 与 Tables **9.19 / 9.22** 钉 PI、LCSS、Data Type。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读里对突发/嵌入/控制块的叙事比纯条款好读，便于和本课总图对账。  
   - **适合哪一段**：第 2、7、11 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：把 Slot Type（CC+Data Type）与 EMB+嵌入 LC 拼装画进同一套解码叙事；明确数据壳两侧 10+10、语音走另一套读法——与本课钉子同向。  
   - **适合哪一段**：第 2、4、5、7、12 节。  
   - **注意**：实现向；文中 Slot Type 或称 Hamming(20,8)，资料库/ETSI Annex B 学习记名用 **Golay(20,8)**——**以 ETSI 为准**。  
   - **基础**：中级～进阶；英文网页。

4. **[GopherTrunk｜DMR End to End Part 2：Bursts, Sync Words & Polarity](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-02-bursts-sync-polarity/)**  
   - **为什么值得看**：FAQ 级钉子「Do voice bursts have a slot type? **No.**」；并把 Data Type 写成「payload 之前的路由」。适合巩固 §4–§6。  
   - **适合哪一段**：第 4、5、6、9 节。  
   - **注意**：偏扫描器/实现；极性故事超纲可略读。  
   - **基础**：中级；英文网页。

5. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
   - **为什么值得看**：EMB+LCSS 如何服务 late entry；Header / Terminator / 嵌入三条运 LC 的车——本课例子 D 的加厚版，并自然滑向第 22 课。  
   - **适合哪一段**：第 4、7、12 节。  
   - **注意**：实现细节（确认两次等）是工程选择；规范语义以 ETSI 为准。文中若把 PI 写成 privacy 口语，**以 Part1「Pre-emption and power control Indicator」为准**。  
   - **基础**：中级～进阶；英文网页。

6. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：帧/突发/超帧 A–F / RC 位置图，便于回看「中心场与缝」总图，把 EMB/SLOT 钉回 264。  
   - **适合哪一段**：第 2、5 节。  
   - **注意**：厂商综述，版本锚点可能早于 V2.7.1；**硬条款以现行 Part1 为准**。  
   - **基础**：中级；英文 PDF。

7. **[Alessandro Guido｜How DMR Works — Conventional Tier 2（PDF）](https://www.qsl.net/kb9mwr/projects/dv/dmr/How%20DMR%20Works%20Conventional%20Tier%202.pdf)**  
   - **为什么值得看**：常规 Tier II 培训口吻回顾超帧与控制/语音分壳，便于和 Data Type / 嵌入叙事对读。  
   - **适合哪一段**：第 2、7、11 节后复盘。  
   - **注意**：培训文年代可能偏早；**以 V2.7.1 为准**。  
   - **基础**：入门～中级；英文 PDF。

8. **[qdmr 手册｜Technical background（Time Slot & Color Code）](https://static.dm3mat.de/qdmr/manual/ch01s09.html)**  
   - **为什么值得看**：从工程动机复习「同频靠色码」——本课 SLOT/EMB 都携带 CC，读完第 20 课后用来保活上下文。  
   - **适合哪一段**：第 1、6 节热身。  
   - **注意**：开源写频文档，**不是** EMB/SLOT 字段专论。  
   - **基础**：入门；英文网页。

**说明（视频）**：公开检索未找到专门把 **「EMB 16 = CC+PI+LCSS+QR；SLOT 20 = CC+Data Type+Golay；语音无 Slot Type；LCSS 分片；Data Type 路由 196；SYNC≠EMB≠SLOT≠CACH」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只演示写频色码或产品抓包界面，不拆 PDU）。本课**未找到合适公开专题视频**。建议用：**Part1 Tables 9.3/9.4/9.19/9.22 + GopherTrunk Part5 / E2E Part2&5 + 资料库 §3/§7/§8** 对照自学。

---

*推送说明：本课为阶段 C「EMB / SLOT 字段」。频谱/调制仅保留短提醒（小报头不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、两套小报头总图、术语、EMB（PI/LCSS/QR）与 SLOT（Data Type/Golay）机制、四柜对照、现场分诊、五则工作例子、数字账本、十则误区、八题自测、资料库路径与八条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「语音嵌入小报头与数据 Slot Type 各长什么样、Data Type 与 CC 如何分诊、LCSS 如何服务晚入网、为何不能把中心 48 整段叫作 EMB」，并进入第 22 课 FULL LC / SHORT LC。*
