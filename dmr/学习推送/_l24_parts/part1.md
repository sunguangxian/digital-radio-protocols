（第24课 · 推送 part 1/3）

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

