# 第 24 课 · FEC 原则（不贴矩阵）

> DMR 深入学习 · **阶段 C 空口深入第 10 课**（阶段 C 收官）  
> 适合：已吃透第 21 课「EMB QR / SLOT Golay」、第 22 课「Full LC 的 RS24 vs 嵌入 CS5、Short LC 的 CRC8」、第 23 课「CSBK CRC16 + BPTC(196,96)」，但仍会把「CRC 失败」直接当成「天线坏了」、或分不清 **BPTC vs Trellis vs Rate 1**、或看见分析仪「BPTC fail」就去背生成矩阵、或把 **Idle 无 CRC** 忘得干干净净的人  
> 阅读量：约 **30–40 分钟** · **几乎不推公式、永不贴生成矩阵** · 要把「**FEC/CRC = 寄包裹先贴胶带、再按规则打散装箱：先组 PDU → 算校验(CRC/RS/CS) →（部分）Data Type CRC Mask → 块 FEC（BPTC/Trellis/短码）→ 交织入突发 → 中心场另加 Golay/QR/Hamming；永不背生成矩阵**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**，符号率约 **4800 baud**，总比特率约 **9.6 kbps**。FEC **不换频、不改调制、不另开带宽**——它只是「比特装进突发之前/之中」的**保护工序**。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是**保护链怎么排、名字挂在哪一字段、现场失败怎么分层分诊**。

---

## 1. 为什么本课重要（动机）

第 21–23 课一路把「小报头 / 门牌 / 办手续」拆开了，名字里反复出现：**QR(16,7,6)、Golay(20,8)、RS(12,9)、5-bit CS、CRC-8、CRC-CCITT、BPTC(196,96)**……  
同事在机房常会问四句要命的话：

- 分析仪报 **CRC fail**——是不是天线坏了、还是写频色码错了、还是 Data Type 解错了？  
- 为什么控制/½ 数据走 **BPTC**，¾ 数据走 **Trellis**，Rate 1 几乎「不编」？  
- 为什么 **EMB** 用 QR、**SLOT** 用 Golay、**TACT** 用 Hamming——不能统一一种短码？  
- 培训台上若开始背 Table B.2–B.22 生成矩阵，后面会卡在同一处：

> **FEC/CRC 是「寄包裹先贴胶带、再按规则打散装箱」：先组 PDU → 算校验(CRC/RS/CS) →（部分）Data Type CRC Mask → 块 FEC（BPTC/Trellis/短码）→ 交织入突发 → 中心场另加 Golay/QR/Hamming。本课只记原则、名称、挂点；永不背生成矩阵、永不贴多项式系数、永不 dump Idle 96-bit / Annex E 符号表。**

本课目标是让你能自己讲清十件事：

1. **为什么** CRC fail ≠ 天线坏了；BPTC / Trellis / Rate1 各护什么；  
2. 一张总图：B.0 + B.3.12 处理链（PDU→校验→Mask→FEC→交织→突发）；  
3. 白话术语：FEC、CRC、BPTC、变长 BPTC、Trellis、Rate1、Hamming、Golay、QR、RS、CS5、CRC 族、Mask、交织；  
4. 机制：各场挂哪种码（原则级，来自 `跳过项原则说明.md` §1）；  
5. 对照：第 16–23 课字段 → FEC 名称映射表；  
6. 现场：CRC 分层分诊；Idle 无 CRC；Header RS24 vs 嵌入 CS5；CSBK CRC16+BPTC；「BPTC fail」vs 错 Data Type；  
7. 完整例子（5+）+ ASCII 草图；  
8. 数字账本（只记比特数与名称，不记矩阵）；  
9. 误区 + 自测 + 资料库 + 核验外链；  
10. 下一课预告：第 25 课 · 语音呼叫过程直觉（阶段 D 开篇）。

**本课硬禁令（写进脑子）**：不贴生成矩阵、不写 G(x) 系数、不 dump Table B.2–B.22、不 dump Idle 96-bit、不贴 Annex E 符号表。实现查 ETSI PDF Annex B。

---

## 2. 总图 / 故事：寄包裹的保护链

先把整课装进一个故事，再落到 Part1 Annex **B.0 / B.1 / B.2 / B.3 / B.4** 与资料库 `01-空中接口/跳过项原则说明.md` **§1**、`帧结构与字段定义.md` **§11**、`CSBK与LC字段详表.md` **§9**。

### 2.1 一句话故事：胶带 + 打散装箱

把「一条要上突发的信息块」想成寄快递：

1. **组 PDU** = 把货填进纸箱（LC / CSBK / Data Header / 用户数据…，clause 7–9）；  
2. **算校验** = 先贴一层「胶带」（CRC / RS / 5-bit CS）——撕开能发现「货坏了」；  
3. **Data Type CRC Mask**（部分类型）= 再按单据类型盖一个「专用封签」（XOR 掩码）——收发必须同一掩码；  
4. **块 FEC** = 按规则把箱子打散、加格子加固（BPTC / Trellis / Rate1 pad / 场内短码）；  
5. **交织** = 故意打散装进车厢左右货舱，避免一块泥点子砸烂整箱；  
6. **中心短场另加短码** = 车厢中缝的「小报头」另贴 Golay / QR / Hamming；  
7. 最后才是 Annex **E** 拆 dibit + clause **10.2** 的 4FSK——那是调制侧，不是本课主线。

口诀：**先贴胶带（校验），再打散装箱（块 FEC+交织），中缝另贴短签（Golay/QR/Hamming）；永不背生成矩阵。**

### 2.2 总图：B.0 + B.3.12 处理链

```text
  ┌──────────────┐
  │ 1. 组 PDU     │  LC / CSBK / Data Header / 用户块…
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │ 2. 算校验     │  CRC / RS(12,9) / 5-bit CS / CRC-9…
  │   （若 Table B.1 该行有 Checksum）
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │ 3. Data Type  │  对「整段 CRC 场」XOR 掩码（B.3.12）
  │    CRC Mask   │  发：CRC后、FEC前；收：FEC后、CRC前
  │               │  Idle / 部分续块末块 → 按原文 note 不套
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │ 4. 块 FEC     │  BPTC(196,96) / 变长 BPTC / Trellis¾ / Rate1
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │ 5. 交织入突发 │  左右 Info（各约 98）等
  └──────┬───────┘
         ▼
  ┌──────────────────────────────────────────┐
  │ 6. 中心场另加短码                          │
  │    SLOT → Golay(20,8)   EMB → QR(16,7,6) │
  │    CACH TACT → Hamming(7,4)              │
  └──────────────────────────────────────────┘
         ▼
  Annex E 拆 dibit → clause 10.2 调 4FSK（调制侧）
```

Table **B.1** 是「场 → FEC 码 → 校验」总表。学习只需记住这一句：

> **控制/头/Idle/½ 数据走 BPTC(196,96)；¾ 数据走 Trellis；Rate 1 几乎不编；嵌入/CACH/RC 走变长 BPTC；中心短场走 Golay / QR / Hamming。**

### 2.3 和第 16–23 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 16 | 突发 264 = 108+48+108；Info 左右各 98 |
| 第 17–18 | 语音超帧；CACH / TACT |
| 第 19–20 | SYNC 认壳；Colour Code |
| 第 21 | EMB 用 **QR**；SLOT 用 **Golay**；Data Type 路由 |
| 第 22 | Full LC：**RS(12,9)** 头/终止 vs 嵌入 **CS5**；Short：**CRC8** + 变长 BPTC |
| 第 23 | CSBK：**CRC-CCITT16** + 典型 **BPTC(196,96)** |
| **本课** | 把上述名字收成**一条保护链地图**；现场分层分诊 |

四句话串起来：

1. **壳**靠 SYNC（第 19）；**色码门**靠 CC（第 20）；  
2. **小报头短码**靠 QR/Golay/Hamming（第 21 / 18）；  
3. **单据校验**靠 RS/CS/CRC 族（第 22–23）；  
4. **整块载荷保护**靠 BPTC/Trellis/Rate1——本课把顺序钉死。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；FEC 不另开频。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps**。  
4. **解调直觉**：先对齐 SYNC → 读中心短场（EMB/SLOT，各自短码）→ 再解 Info 的块 FEC → 再解 Mask/CRC。  
   **CRC 失败 ≠ 「没解调出射频」**，而是「保护链某一层没过」。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **FEC** | Forward Error Correction，前向纠错：多加冗余比特，收端尽量自己修 | ≠ 重传（ARQ）；≠ 单纯 CRC 检错 |
| **CRC** | Cyclic Redundancy Check，循环冗余校验：主要**检错**「货坏了没」 | ≠ 一定能纠错；≠ BPTC |
| **BPTC(196,96)** | 块积码：196 码字护约 96 信息；多数控制/½ 数据 | ≠ Trellis；≠ Rate1 |
| **变长 BPTC** | 嵌入 Full LC / 单突发嵌入 / CACH Short LC / RC 用的「短版」行列加固 | ≠ 196×96 那一档 |
| **Trellis ¾** | Rate ¾ 网格码：约 144 信息 → 196 码字；¾ 数据续块 | ≠ BPTC；≠ 语音声码 FEC |
| **Rate 1** | 几乎**无块 FEC**：192 用户 + 4 pad → 196；靠 CRC/上层重传 | ≠「不需要任何校验」 |
| **Hamming** | 短汉明码族；BPTC 行列、TACT(7,4) 等都用它作积木 | ≠「只有一种 Hamming」 |
| **Golay(20,8)** | SLOT：8 信息 + 12 校验 | ≠ EMB 的 QR |
| **QR(16,7,6)** | Quadratic Residue：EMB 7 信息 + 9 校验 | ≠ Golay |
| **RS(12,9)** | Reed-Solomon 缩短码：Full LC 头/终止 24-bit 校验路径 | ≠ 嵌入 CS5 |
| **CS5** | 5-bit Checksum：嵌入 Full LC 短校验 | ≠ RS24；≠ CRC16 |
| **CRC-8 / 16 / 9 / 32 / 7** | 不同挂点的 CRC 族（见 §4.5） | 长度不同 ≠ 可互换 |
| **Data Type CRC Mask** | 按 Data Type 对 CRC 场 XOR；收发同一掩码 | ≠ 改 PDU 正文；Idle 等不套 |
| **交织（Interleaving）** | 打散比特位置抗块差错/衰落 | ≠ 加密；≠ 调制 |

---

## 4. 机制拆解：按场挂码（只讲原则）

Canonical 来源：`01-空中接口/跳过项原则说明.md` **§1**（Annex B）。下列每节**故意不写矩阵**。

### 4.1 BPTC(196,96)（B.1.1）——多数控制与 ½ 数据

直觉（寄包裹「格子加固」）：

- 信息约 **96 bit** 排成 **9 行 × 11 列**，再补少量保留位凑阵；  
- **每行**加 Hamming **(15,11,3)**，**每列**加 Hamming **(13,9,3)**——行列双重护；  
- 再按规范公式交织，填入通用数据突发左右 Info（各 98 bit），共 **196**。

适用（B.0 精神）：PI / Voice LC Header / Terminator+LC / CSBK / Idle / Data Header / Rate ½ 续块与末块 / Response / MBC / UDT / USBD 等。

**关键钉子**：

- **Idle 无 CRC、无 Mask**——只有 BPTC + 规定伪随机信息图案（图案本身不 dump）；  
- 确认数据另可挂 CRC-9 / 末块 32-bit CRC（仍是**先校验、后 BPTC**）。

```text
  96 info  →  行列 Hamming 加固  →  交织  →  196 进左右 Info
              （不背矩阵，只记「行列积木」）
```

### 4.2 变长 BPTC（B.2）——嵌入、单突发、CACH、RC

共同直觉：**行 Hamming + 列偶/奇校验 → 按列读出写入发送阵**；消息变长就加行。

| 子款 | 用在哪 | 原则级积木 | 怎么进突发 |
|------|--------|------------|------------|
| **B.2.1** | 语音超帧嵌入 Full LC | Hamming(16,11,4) + 列偶校验 | 拆成 **4×32**，超帧 **B–E** 嵌入场 |
| **B.2.2.1** | 非 RC 单突发嵌入 | 同形；交织入 32-bit 嵌入 | 单突发嵌入场 |
| **B.2.2.2** | Reverse Channel | 列**奇**校验；另带 **7-bit CRC** | RC 嵌入/独立 RC |
| **B.2.3** | CACH Short LC | Hamming(17,12,3) + 列偶校验 | 经 **4 个 CACH**；TACT 再交错 |

钉子：嵌入 Full LC = **72-bit LC + CS5** 入阵；CACH Short = **28-bit + CRC8** 再 BPTC。

### 4.3 中心短场：EMB / SLOT / TACT（不走 196 BPTC）

| 场 | 码 | 原则 |
|----|-----|------|
| **EMB** | QR **(16,7,6)** | 7 信息 + 9 校验；无额外 checksum |
| **Slot Type** | Golay **(20,8)** | CC+Data Type 等 8 信息 + 12 校验 |
| **CACH TACT** | Hamming **(7,4)** | AT+TC+LCSS 共 4 + 3 校验 |

为什么三种不同？——场长不同、要护的信息量不同、和突发布局绑死；**不要强行统一**。生成矩阵 → **SKIP**。

### 4.4 Rate ¾ Trellis vs Rate 1

| 类型 | 原则 | 何时见到 |
|------|------|----------|
| **¾ Trellis** | 144 信息 → 串成 tribit → 8 态 FSM → 约 196 码字；再交织抗瑞利块差错 | Data Type = Rate ¾ 数据 |
| **Rate 1** | **无块 FEC**；192 用户 + 4 个 0 pad → 196；位序入突发 | 信道好/要吞吐时；确认路径仍可带 CRC-9 / 末块 CRC-32 |

口诀：**½ 像「厚纸板箱」（BPTC）；¾ 像「网格捆绳」（Trellis）；Rate1 像「几乎裸箱 + 上层重传胶带」。**

### 4.5 CRC 族挂点（只讲挂法，不写 G(x)）

| 名称 | 典型挂点 | 原则 |
|------|----------|------|
| RS **(12,9)** | Voice LC Header / Terminator 的 Full LC | 9 八位组 → 3 校验八位组（24 bit） |
| **5-bit CS** | 嵌入 Full LC | 短校验，与变长 BPTC 同行 |
| **CRC-8** | CACH Short LC；Act_Updt Hash | 信息后挂 8 bit |
| **CRC-CCITT(16)** | CSBK、Data/MBC/UDT/USBD/PI Header 等 | **先 CRC →（Mask）→ 再 BPTC** |
| **CRC-9** | 确认数据块（DBSN+User） | 仅当突发内存在 CRC-9 时才套 9-bit Mask |
| **CRC-32** | 确认/非确认**末块**、Response data | 跨块消息 CRC；Last Block **不套** Data Type Mask |
| **CRC-7** | RC Info | 与 RC 单突发 BPTC 叠用 |
| **Data Type CRC Mask** | 见 §2.2 | 按 Data Type 选掩码；收发一致才能过 CRC |

**禁止**：不写 G(x)、不写掩码十六进制表（Table B.21/B.22 → PDF）。

### 4.6 CACH 帧交织（B.4.1）一句

24-bit CACH 上：AT/TC/LCSS 及其 3-bit Hamming 被**拆开散布**抗衰落；17-bit 载荷填空档。记住「**控制比特散开、载荷顺序填缝**」即可——位图不抄。

---

## 5. 对照表：先前各课字段 → FEC 名称

| 先前课 / 字段 | 校验名 | 块 FEC / 短码 | 备注 |
|---------------|--------|---------------|------|
| 第 18 · CACH TACT | （场内） | Hamming(7,4) | 中心短场 |
| 第 18/22 · Short LC | CRC-8 | 变长 BPTC for CACH | 经 4×CACH |
| 第 21 · EMB | （无额外 checksum） | QR(16,7,6) | 语音壳中缝 |
| 第 21 · SLOT | （无额外 checksum） | Golay(20,8) | 数据壳中缝；含 Data Type |
| 第 22 · Full LC Header/Term | RS(12,9) 24-bit | BPTC(196,96) | Data Type 头/终止 |
| 第 22 · 嵌入 Full LC | 5-bit CS | 变长 BPTC B.2.1 | 超帧 B–E |
| 第 23 · CSBK / MBC | CRC-CCITT 16 | BPTC(196,96) | Data Type 0011/0100/0101 |
| Idle | **无** | BPTC(196,96) | 无 Mask |
| Rate ½ 数据 | CRC-9 / 末 CRC-32（确认路径） | BPTC(196,96) | 先校验后 BPTC |
| Rate ¾ 数据 | （按业务） | Trellis ¾ | ≠ BPTC |
| Rate 1 数据 | CRC-9 / 末 CRC-32（确认路径） | 几乎无块 FEC | pad 凑 196 |
| RC | CRC-7 | 单突发变长 BPTC（奇校验） | 第 21 课 PI 相关预告 |

读表口诀：**中缝看短码；单据看 CRC/RS/CS；整舱看 BPTC/Trellis/Rate1。**

---

## 6. 现场岗位对照

| 现场现象 | 先查哪一层 | 别急着怪 |
|----------|------------|----------|
| 「CRC fail」红字 | ① SYNC/壳 ② CC ③ Data Type ④ 块 FEC ⑤ Mask/CRC | 天线（最后才查 RF） |
| Idle 突发「怎么没有 CRC」 | Table B.1：**Idle 无 checksum** | 「解码器坏了」 |
| Header 过、嵌入偶发不过 | Header 是 **RS24+BPTC**；嵌入是 **CS5+变长 BPTC** | 「同一条 LC 校验长度应一样」 |
| CSBK 解不出 | CRC16 → Mask → BPTC；再 FID/CSBKO | 去语音嵌入里找 CSBKO |
| 分析仪「BPTC fail」 | Data Type 是否解成了该走 Trellis/Rate1 的类型？ | 立刻背矩阵 |
| Rate ¾ 当 ½ 解 | 码型错了：¾≠BPTC | 「信道特别差」 |
| 同机房一台过一台不过 | 掩码/固件版本/Data Type 解释是否一致 | 先换天线 |

**CRC 分层分诊（建议贴工位）**：

```text
  L0 射频能量 / SNR          → 加餐与第 1–4 课
  L1 SYNC 认壳是否对          → 第 19 课
  L2 CC（色码门）是否过        → 第 20 课
  L3 中心短码：EMB QR / SLOT Golay / TACT Hamming
  L4 块 FEC：BPTC / Trellis / Rate1 是否选对类型
  L5 Mask + CRC/RS/CS 是否过
  L6 才轮到「天线 / 馈线 / 干扰」硬件大手术
```

---

## 7. 工作例子（6 则）

### 例子 A · CSBK：CRC16 → Mask → BPTC

```text
  [LB|PF|CSBKO|FID|Data64] --CRC16--> [+CRC] --Mask--> [加封签]
        --BPTC(196,96)--> 左右 Info --Data SYNC+SLOT(Golay)--> 突发
```

对照第 23 课：外壳先完整，再进保护链。CRC 失败时先确认 Data Type=`0011`，再查 Mask/CRC，不要先拆天线。

### 例子 B · Voice LC Header：RS24 + BPTC

```text
  Full LC 72 + RS(12,9)24  → 96 信息叙事
       →（Mask，若适用）→ BPTC(196,96) → 数据壳 Header 突发
```

晚入网主要靠嵌入路径（例子 C），Header 是「整包门牌」的高保护版本。

### 例子 C · 嵌入 Full LC：CS5 + 变长 BPTC → B–E

```text
  超帧：A(SYNC)  B(嵌入1)  C(嵌入2)  D(嵌入3)  E(嵌入4)  F
                      └──── 72+CS5 → 变长 BPTC → 4×32 ────┘
  每个语音突发中缝另有 EMB = QR(16,7,6)（护 CC/PI/LCSS，不是护整段 LC）
```

钉子：**Header 的 RS24 ≠ 嵌入的 CS5**——同一门牌正文，两条运载、两套校验预算。

### 例子 D · Idle：有 BPTC、无 CRC

```text
  规定 96-bit Idle 信息图案（不 dump）
       → BPTC(196,96) → Data Type=Idle
       → 无 checksum、无 Mask
```

现场：解出 Idle 是「占空/保活」，不是用户数据坏了。Null 嵌入（全 0 占位）≠ Idle 整突发——见原则说明 §2。

### 例子 E · 「BPTC fail」其实是 Data Type 解错

```text
  真：Data Type = Rate ¾  → 应走 Trellis
  错：分析仪按 BPTC(196,96) 解  → 报 BPTC fail
  分诊：先回 SLOT 的 Data Type（Golay 护着的那 4 bit），再换解码器档案
```

### 例子 F · Rate 1：几乎裸箱

```text
  192 用户 bit + 4 pad0 → 196 入突发（无块 FEC）
  确认路径仍可能：块内 CRC-9；消息末 CRC-32
```

信道差时 Rate1 更容易「上层重传忙」——这是设计取舍，不是「忘了加 FEC」。

---

## 8. 数字账本

| 名称 | 数字 | 别混成 |
|------|------|--------|
| 突发总长 | **264** bit | ≠ 196 Info |
| 左右 Info | **98+98** | 块 FEC 后的码字舱 |
| BPTC 信息/码字 | **96 / 196** | 控制与 ½ 数据主力 |
| Trellis 信息/码字 | **144 / 196** | ¾ 数据 |
| Rate1 用户/码字 | **192(+4 pad) / 196** | 几乎无块 FEC |
| EMB | **16** = 7+9 QR | ≠ 整段 48 中心 |
| SLOT | **20** = 8+12 Golay | 含 CC+Data Type |
| TACT | **7** = 4+3 Hamming | CACH 头 |
| Full LC 头/终止校验 | **24** RS | ≠ 嵌入 CS5 |
| 嵌入 CS | **5** | ≠ CRC16 |
| Short LC CRC | **8** | CACH 路径 |
| CSBK CRC | **16** CCITT | 先 CRC 后 BPTC |
| RC CRC | **7** | 与 RC BPTC 叠用 |
| 时隙 / 符号率 | **30 ms** / **4800** baud | 调制账本 |

串句：

```text
组 PDU → 校验(CRC/RS/CS) → Mask? → 块FEC → 交织 → 中缝短码
控制/½ …… BPTC(196,96)
¾ ……… Trellis
Rate1 …… 几乎不编
中缝 …… QR / Golay / Hamming
永不背 …… 生成矩阵
下一课 …… 语音呼叫过程直觉（阶段 D）
```

---

## 9. 常见误区（10 则）

1. **「CRC fail = 天线坏了。」** → 否。先分层：SYNC/CC/短码/块 FEC/Mask/CRC，最后才是 RF。  
2. **「FEC 和 CRC 是同一种东西。」** → FEC 侧重纠错冗余；CRC 侧重检错。DMR 里两者常叠用。  
3. **「所有数据都走 BPTC(196,96)。」** → ¾ 走 Trellis；Rate1 几乎不编；嵌入/CACH 走变长 BPTC。  
4. **「EMB 和 SLOT 用同一种短码。」** → EMB=QR，SLOT=Golay，TACT=Hamming。  
5. **「Header 与嵌入 Full LC 校验长度一样。」** → Header/Term 是 RS24；嵌入是 CS5。  
6. **「Idle 也应有 CRC。」** → Table B.1：Idle **无** checksum、无 Mask。  
7. **「分析仪 BPTC fail 就要去背矩阵。」** → 先查 Data Type 是否选错解码档案。  
8. **「Rate1 = 完全没有校验。」** → 无**块 FEC**；确认路径仍可有 CRC-9 / CRC-32。  
9. **「Data Type CRC Mask 改的是 PDU 业务字段。」** → 掩的是 **CRC 场**；且收发必须同一掩码。  
10. **「本课应把 Annex B 矩阵抄进笔记。」** → **禁止**。原则 + 名称 + 挂点即可；矩阵回 PDF。

---

## 10. 自测（8 题）

**题 1.** 用一句话讲清本课核心口诀（寄包裹）。

<details><summary>参考答案</summary>
FEC/CRC 是「寄包裹先贴胶带、再按规则打散装箱」：组 PDU → 算校验 →（部分）Mask → 块 FEC → 交织入突发 → 中心场另加短码；永不背生成矩阵。
</details>

**题 2.** 写出 B.0 处理链的 6 步顺序（不含调制）。

<details><summary>参考答案</summary>
① 组 PDU ② 算校验(CRC/RS/CS) ③ Data Type CRC Mask（若适用）④ 块 FEC ⑤ 交织入突发 ⑥ 中心场另加 Golay/QR/Hamming。
</details>

**题 3.** BPTC(196,96)、Trellis ¾、Rate 1 各主要护哪类载荷？

<details><summary>参考答案</summary>
BPTC：多数控制/头/Idle/½ 数据；Trellis：Rate ¾ 数据；Rate1：几乎无块 FEC 的高吞吐数据（仍可能有 CRC-9/32）。
</details>

**题 4.** EMB、SLOT、TACT 各用什么短码？信息比特大约多少？

<details><summary>参考答案</summary>
EMB：QR(16,7,6)，7 信息；SLOT：Golay(20,8)，8 信息；TACT：Hamming(7,4)，4 信息。
</details>

**题 5.** Voice LC Header 与嵌入 Full LC 的校验名有何不同？为什么？

<details><summary>参考答案</summary>
Header/Terminator：RS(12,9)→24 bit；嵌入：5-bit CS。运载路径与比特预算不同——整包走数据壳 BPTC，嵌入拆四片走变长 BPTC。
</details>

**题 6.** Idle 有没有 CRC？有没有 BPTC？

<details><summary>参考答案</summary>
无 CRC、无 Mask；有 BPTC(196,96)。用于占空/保活，不是用户数据。
</details>

**题 7.** 现场看到「BPTC fail」，第一步应查什么？

<details><summary>参考答案</summary>
先核对 SLOT 的 Data Type 是否本应按 BPTC 解（会不会其实是 ¾ Trellis / Rate1）；同时确认 SYNC 壳与 CC。不要先背矩阵或先拆天线。
</details>

**题 8.** CSBK 的校验与块 FEC 顺序是什么？

<details><summary>参考答案</summary>
先算 CRC-CCITT 16 →（按规则 Mask）→ 再 BPTC(196,96) 入数据突发；SLOT 另用 Golay 护 CC+Data Type。
</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `01-空中接口/跳过项原则说明.md` **§1** | **本课 canonical**：Annex B 挂法；故意不抄矩阵 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§11** | FEC/CRC 名称索引 |
| 3 | `01-空中接口/CSBK与LC字段详表.md` **§9** | FEC 名称速查；与外壳对照 |
| 4 | `学习推送/第21课.md` | EMB QR / SLOT Golay / Data Type |
| 5 | `学习推送/第22课.md` | RS24 vs CS5；Short CRC8 + 变长 BPTC |
| 6 | `学习推送/第23课.md` | CSBK CRC16 + BPTC；与本课例子 A 对读 |
| 7 | `01-空中接口/AnnexCDE_时序Idle比特序.md` | Idle/Null 原则短注（不 dump 比特） |
| 8 | 官方 **TS 102 361-1 V2.7.1** Annex **B**（尤其 B.0、B.1.1、B.2、B.3.1–B.3.13、B.4.1） | 原文；矩阵/多项式只在实现时查 PDF |
| 9 | **TR 102 398** | 系统设计导读，**不是**替代 TS |
| 10 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把 CRC fail 当成「调制坏了」 |

官方版本锚点：**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。矩阵、多项式系数、Idle 96-bit、E.1–E.12：**永远回 PDF**，本库不补第二份。

---

## 12. 下一课预告

**第 25 课 · 语音呼叫过程直觉**（阶段 D · 语音与数据 开篇）

本课收官了阶段 C：把空口上反复出现的保护名字收成一张**原则地图**——谁护中缝、谁护单据、谁护整舱；并钉死「失败要分层、矩阵永不背」。下一课离开「字段积木」，进入**一次语音呼叫怎么从请求走到语音超帧再走到 Terminator** 的过程直觉：把第 17（超帧）、21（EMB/SLOT）、22（Full LC）、23（CSBK 手续）串成一条时间线。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-30**（早间推送）检索核验；真实打开过内容页/PDF（HTTP 200 或协会镜像可用）；**不编造地址**。策略 = **Part1 Annex B 原文（协会镜像）+ TR 导读 + Wavecom/hamgear 帧与名称回顾 + GopherTrunk 突发/解码器深文 + 原则级 FEC/CRC/Hamming 优质通识（含一条已核验的优秀公开视频）**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：Annex **B** 是本课一切名称的原文锚点——B.0 总序、B.1.1 BPTC、B.2 变长/Trellis/Rate1、B.3 短码与 CRC 族、B.3.12 Mask、B.4.1 CACH 交织。学习时**只读条款标题与叙述顺序**，矩阵表留给实现。  
   - **备链**（部分网络对 etsi.org 直链可能 403，以协会镜像为准）：`https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf`。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读里对信道编码/链路保护的叙事比纯 Annex 好读，便于和本课「胶带+打散装箱」对账。  
   - **适合哪一段**：第 2、6、11 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：帧/突发/超帧图，帮助把「196 Info + 中心短场」钉回 264 结构，避免把 FEC 想像成另开一条射频。  
   - **适合哪一段**：第 2、5、7 节。  
   - **注意**：厂商综述，版本锚点可能早于 V2.7.1；**硬条款以现行 Part1 为准**。  
   - **基础**：中级；英文 PDF。

4. **[Alessandro Guido｜How DMR Works — primer PDF（hamgear）](https://hamgear.files.wordpress.com/2014/02/dmr-primer.pdf)**  
   - **为什么值得看**：培训幻灯式回顾控制/LC/FEC/CRC **名称**——和本课术语表、数字账本同向。  
   - **适合哪一段**：第 3、8、11 节后复盘。  
   - **注意**：年代偏早；**以 V2.7.1 / 本库原则说明为准**。  
   - **基础**：入门～中级；英文 PDF。

5. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：明确 Data Type 分支、BPTC 保护控制/LC、语音突发无 Slot Type——和第 21 课及本课「选错解码档案 → 假 BPTC fail」同向。  
   - **适合哪一段**：第 5、6、7 节。  
   - **注意**：校验命名以 ETSI Annex B 为准。  
   - **基础**：中级～进阶；英文网页。

6. **[EcrioniX｜Forward Error Correction（Hamming / RS 等原则）](https://ecrionix.org/digital-electronics/fec/)**  
   - **为什么值得看**：用通识语言讲清「FEC 为何加冗余、距离与可纠个数」——帮助弱基础同事建立「胶带厚度」直觉，而不陷入 DMR 矩阵。  
   - **适合哪一段**：第 1、3、9 节热身。  
   - **注意**：通识文 **不是** DMR 规范；落到场名仍回 Annex B / 本课 §4。  
   - **基础**：入门；英文网页。

7. **[KnowledgeGate｜DLL Error Control：CRC and Hamming](https://www.knowledgegate.ai/blog/dll-error-control-computer-networks-complete-guide)**  
   - **为什么值得看**：把「CRC 偏检错、Hamming 偏纠错、ARQ vs FEC」对照讲清——正好支撑本课「CRC fail ≠ 没 FEC」。  
   - **适合哪一段**：第 3、6、9 节。  
   - **注意**：计算机网络教材语境；DMR 叠用方式以本课为准。  
   - **基础**：入门～中级；英文网页。

8. **[solderic｜CRC vs Hamming Code](https://solderic.com/communication/hamming-code-vs-crc)**  
   - **为什么值得看**：短文对照「检错胶带 vs 纠错格子」——给同事做 3 分钟口头解释时好用。  
   - **适合哪一段**：第 3、9 节。  
   - **注意**：通识；不替代 Annex B 挂点表。  
   - **基础**：入门；英文网页。

9. **[Wikipedia｜Hamming code](https://en.wikipedia.org/wiki/Hamming_code)**  
   - **为什么值得看**：权威通识入口，帮助理解 BPTC 行列为何反复出现 Hamming 积木名。  
   - **适合哪一段**：第 4.1、4.3 节旁证。  
   - **注意**：不讲 DMR 交织；**实现以 ETSI 为准**。  
   - **基础**：入门；英文。

10. **[Wikipedia｜Cyclic redundancy check](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)**  
    - **为什么值得看**：CRC 检错直觉与多项式故事的标准入口——本课**不抄 G(x)**，需要系数时用百科建立语感后回 PDF。  
    - **适合哪一段**：第 4.5、6 节。  
    - **注意**：通用 CRC ≠ 某一 DMR 初值/掩码；掩码表回 Annex B.3.12。  
    - **基础**：入门；英文。

11. **[3Blue1Brown｜But what are Hamming codes?（YouTube）](https://www.youtube.com/watch?v=X8jsijhllIA)**  
    - **为什么值得看**：目前公开检索到的、讲解质量最高的 **Hamming / 纠错码起源** 可视化视频之一；帮助建立「冗余如何换可纠能力」的几何直觉，与本课「永不背矩阵、先懂原则」完全同向。  
    - **适合哪一段**：第 1、3、4.1、4.3 节前后。  
    - **注意**：**不是** DMR 专题——不会讲 BPTC/Trellis/Data Type Mask；看完必须回到本课 §4 挂点表。  
    - **基础**：入门；英语视频（可开字幕）。

**说明（视频）**：公开检索**未找到**专门把 **「DMR Annex B：BPTC(196,96)/变长 BPTC/Trellis/Rate1 + Golay/QR/Hamming 挂场 + Data Type CRC Mask 收发顺序」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只演示写频、声码或产品抓包）。本课采用折中：收录一条已核验的优秀通识视频（3Blue1Brown · Hamming），并诚实标明 **DMR 专题 FEC 视频未找到**（`video_found=true` 指「有优质可用视频」，但是通识而非 DMR Annex B 专题）。建议用：**原则说明 §1 + Part1 Annex B 目录 + 本课对照表 + GopherTrunk 解码器文** 对照自学。

---

*推送说明：本课为阶段 C「FEC 原则（不贴矩阵）」收官课。频谱/调制仅保留短提醒（FEC 不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、寄包裹总图与 B.0 处理链、术语、BPTC/变长 BPTC/中心短码/Trellis/Rate1/CRC 族挂点、第 16–23 课映射表、现场分层分诊、六则工作例子、数字账本、十则误区、八题自测、资料库路径与核验外链（含一条优秀通识 Hamming 视频；诚实标明无 DMR Annex B 专题视频）。硬禁令贯穿全文：不贴生成矩阵、不写 G(x)、不 dump Idle/符号表。读完应能向同事讲清「CRC fail 为何不等于天线坏、BPTC/Trellis/Rate1 如何分工、Header RS24 与嵌入 CS5 为何不同、Idle 为何无 CRC」，并进入第 25 课语音呼叫过程直觉。*
