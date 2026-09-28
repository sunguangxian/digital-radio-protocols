# 第 18 课 · CACH 与 Guard

> DMR 深入学习 · **阶段 C 空口深入第 4 课**  
> 适合：已吃透第 15 课「时隙 30 ms / TDMA frame 60 ms」、第 16 课「突发 264 = 108+48+108」、第 17 课「语音超帧 A–F / 360 ms」，但听到「缝」「CACH」「Guard」「AT 忙闲」仍像三件无关事的人  
> 阅读量：约 **30–40 分钟** · 几乎不推公式 · 要把「**30 ms = ≈27.5 ms 业务 + ≈2.5 ms 缝；出站缝 = CACH（24 bit）；入站 / DM 缝 = Guard（PA / 传播 / 护邻槽）；缝不是 264 货箱的一部分**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**，符号率约 **4800 baud**，总比特率约 **9.6 kbps**。CACH / Guard **不换频、不改调制**——它们只住在绿灯尾巴那条约 **2.5 ms** 的缝里。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是**缝里到底塞了什么、入/出站为何不对称**。

---

## 1. 为什么本课重要（动机）

第 15 课埋下过一句：「约 2.5 ms 缝，入站叫 Guard，出站叫 CACH；CACH 字段留给第 18 课。」  
第 16 课又钉过：「CACH 的 24 bit **不算**在 264 里面。」  
第 17 课把语音火车 A–F 排齐了。

同事接下来会问更「贴现场」的问题：

- 协议分析仪：中继**出站**两路突发之间，为什么总有一小段不是 264 货箱？那是 **CACH**。  
- 用户投诉「按了 PTT 上不去 / 随机接入总失败」：先看 CACH 里的 **AT（Access Type）**——入站侧是不是已经被标成 **busy**？  
- 写频选 Slot1，却总踩到别人的 Slot2：可能是 **TC（TDMA Channel）** 读错，或入/出站编号偏移没对齐。  
- 直通 / Talkaround：没有基站持续发 CACH「报站」，同步与礼貌接入压力更大——别用中继出站的直觉硬套 DM。  
- 培训台上：若只背「有个 2.5 ms 缝」六个字，后面会卡在同一处：

> **同一条缝，出站与入站干的是两件完全不同的事。出站缝里塞 24 bit 小广播（CACH）；入站缝里故意留空（Guard），给功放爬升、传播时延、保护邻时隙。缝不是 264 货箱的附件栏。**

本课目标是让你能自己讲清十件事：

1. **为什么**现场排障要把「缝」单独问清楚（忙闲 / 踩槽 / 上不去）；  
2. 一张总图：30 ms = ≈27.5 ms Traffic + ≈2.5 ms 缝；出站 CACH vs 入站 Guard；  
3. 白话术语：Guard、CACH、AT、TC、LCSS（CACH 侧）、Short LC、TACT、Null Short LC、入/出站不对称；  
4. CACH 24 bit 字段图：AT | TC | LCSS | FEC | Signalling 17；  
5. CACH 广播什么：入站忙闲、信道 1/2、低速 Short LC 碎片；  
6. 时序直觉：CACH 指示相对出站常**延迟约一个时隙**（解码 + 收发切换）；  
7. 现场岗位：分析仪认缝、AT=busy、「错槽」与 TC、上行必须 Guard；  
8. 完整例子：BS 连续出站夹 CACH；MS 上行留 Guard；Tier II 中继 vs DM 对照；  
9. 数字账本：2.5 ms、24 bit、≈566.67 bit/s、264 vs 24 vs 96；  
10. 误区 + 自测 + 资料库路径 + 核验外链。

---

## 2. 总图 / 故事：那条 ≈2.5 ms 的缝

先把整课装进一个故事，再落到 Part1 clauses **4.2 / 4.5 / 4.6 / 6.3 / 9.1.4** 与资料库 `01-空中接口/帧结构与字段定义.md` **§2、§5、§10**。精神与 `00-入门/DMR术语与帧结构速查卡.md`「Guard / CACH」行一致。

### 2.1 绿灯 30 ms 怎么切？

每个时隙绿灯总长 **30.0 ms**，但业务货箱只吃掉约 **27.5 ms**：

```text
时间 →（单个 Timeslot = 30 ms）

[======== ≈27.5 ms · Traffic burst 264 bit =========][≈2.5 ms 缝]
 │                                                    │
 │  108 + 48 + 108（第 16 课货箱）                      │  本课主场
 │  语音壳 / 数据壳 / 超帧 A–F 都住在这里               │
 └────────────────────────────────────────────────────┘
```

口诀：

- **货箱** = 264 bit ≈ 27.5 ms（第 16 课）；  
- **缝** ≈ 2.5 ms（本课）；  
- **整灯** = 30 ms（第 15 课）；  
- **别把缝算进 264**——它们首尾相接，但是两本账。

### 2.2 同一条缝，入站与出站干两件事

```text
入站 Inbound（MS → BS）典型：
  [==== Traffic 264 bit · ≈27.5 ms ====][==== Guard ≈2.5 ms ====]
                                         └─ 故意留空：PA 爬升 / 传播 / 护邻槽

出站 Outbound（BS → MS）典型：
  [==== Traffic 264 bit · ≈27.5 ms ====][==== CACH 24 bit · ≈2.5 ms ====]
                                         └─ 塞满小广播：忙闲 / 信道号 / Short LC
```

| 方向 | 缝里放什么 | 一句话为什么 |
|------|------------|--------------|
| **入站** | **Guard（保护间隔）** | 手机功放要爬升、电磁波要飞一会儿、还要给邻时隙留脚趾缝 |
| **出站** | **CACH（24 bit）** | 基站本来就在连续发，缝别浪费——塞公共通告 |

Part1 的精神（clause **4.2 / 4.5**）：基站激活后出站常**连续发射**；移动台没话就停。所以出站「缝」可以被利用成 CACH；入站「缝」必须空着当 Guard。

### 2.3 和第 15–17 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 15 | 时隙 30 ms、frame 60 ms、缝的**脸熟**（Guard vs CACH） |
| 第 16 | 264 货箱；明确 CACH **不在** 108+48+108 内 |
| 第 17 | 语音火车 A–F；火车仍跑在 Traffic 窗里，不占缝 |
| **本课** | 拆开缝：Guard 防什么；CACH 24 bit 广播什么；AT/TC/Short LC |

三句话串起来：

1. **车道**是 30 ms（第 15）；  
2. **货箱**是 264 bit（第 16），可排成 A–F（第 17）；  
3. **缝**是 ≈2.5 ms：出站 CACH、入站 Guard（本课）。

### 2.4 四种基本信道形态（先脸熟，后例子）

资料库 §10 / Part1 clause **4.6**：

| 类型 | 典型场景 | 间隙用途 |
|------|----------|----------|
| Traffic + **CACH** | 两频 BS **出站**；连续发模式 | CACH |
| Traffic + **Guard** | MS→BS **入站**；TDMA DM | Guard |
| **Bi-directional** | 同频正/反向分时 | Guard |
| **TDMA Direct Mode** | 直通；另有 Tier I 连续发变体 | — |

本课主线：**Traffic+CACH（出站）** 与 **Traffic+Guard（入站 / DM）**。Bi-directional 与 DM 细节在例子里对照一句即可。

### 2.5 调制账本钩子（巩固弱项，不重开加餐）

加餐四句话在本课落成「缝不改物理层」一句：

1. **频率**：载波仍停在写频的那个 MHz；CACH 不另开频点。  
2. **带宽**：地皮仍约 **12.5 kHz**；缝与货箱共用同一条地皮。  
3. **调制**：缝里的 24 bit 仍是 **4FSK** 卸下的比特（不是另一种调制）。  
4. **解调**：先对齐时隙与突发边界，再判断缝是「空 Guard」还是「有 CACH 比特」。

口算复习：Traffic 用 264 / 0.0275 ≈ **9600 bit/s**。CACH 是另一条小水管：24 bit / 0.030 s ≈ **800 bit/s** 毛速率；其中 Signalling 约 17 bit / 30 ms ≈ **566.67 bit/s**（见账本）。**两本账不要加在一起冒充「总吞吐」口误。**

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **Guard time（保护间隔）** | 入站 / DM 时隙之间≈2.5 ms 的**空缝** | ≠ CACH；缝里通常**没有**业务比特 |
| **CACH** | Common Announcement Channel：出站夹缝里的 **24 bit** 小广播 | ≠ Traffic 264；≠ SYNC 48；≠ Colour Code |
| **Outbound / 出站** | BS → MS | 常见形态：Traffic + **CACH** |
| **Inbound / 入站** | MS → BS | 常见形态：Traffic + **Guard** |
| **AT（Access Type）** | CACH 里 1 bit：入站侧 **idle / busy** | ≠ Colour Code；≠ 你的 Talkgroup |
| **TC（TDMA Channel）** | CACH 里 1 bit：随后 outbound 是 ch **1** 还是 ch **2** | ≠ 超帧字母 A–F |
| **LCSS（CACH 侧）** | CACH 里 2 bit：Short LC 分片起止指示 | 也出现在 EMB 里；**两处都叫 LCSS，别混成一个场** |
| **TACT** | AT+TC+LCSS+parity 共 **7 bit** 的小 PDU | 不是整段 CACH 的别名 |
| **Signalling（CACH）** | CACH 里 **17 bit** 信令载荷区（无 CACH 层再套一层 FEC 的叙事） | 常承载 Short LC 碎片 |
| **Short LC** | 经 CACH 低速拼出来的短链路控制（Part2 定义 SLCO） | ≠ Full LC（72 bit 叙事，多走 Header/嵌入） |
| **Null Short LC** | 没东西可广播时塞的空 Short LC（Part2 `Nul_Msg`，SLCO=`0000`） | ≠ 嵌入 Null；≠ Idle 突发 |
| **连续发模式** | BS 激活后出站持续发射，空业务时用 Idle 填突发 | 入站 MS 没话就停 |
| **随机接入 / 礼貌接入** | MS 想发数据等时常先看入站是否被标 idle | 细节后课；本课先认 AT |
| **DM / Talkaround** | 直通；通常**没有** BS 的 CACH 帮你报站 | 缝侧更常是 Guard |

---

## 4. CACH 24 bit：字段怎么切

引用精神：Part1 clauses **4.5、6.3、9.1.4**；资料库 `帧结构与字段定义.md` **§5**。

### 4.1 它夹在哪里？

```text
  Outbound Traffic          CACH (24)         Outbound Traffic
  ├─ ≈27.5 ms ─┤           ├─ ≈2.5 ms ─┤      ├─ ≈27.5 ms ─┤
  （Slot n 货箱）            （本课）           （下一绿灯货箱）
```

- **仅出站**；与 Slot1 / Slot2 **共用**这条缝水管；  
- 大约每 **30 ms** 来一次（跟随时隙节奏）；  
- 基站没业务可塞时，Traffic 侧可发 Idle 突发；CACH 侧没载荷则发 **Null Short LC**。

### 4.2 ASCII 字段图（交织后的学习视图）

```text
  CACH 24 bits：
  ┌────┬────┬──────┬─────┬────────────────────┐
  │ AT │ TC │ LCSS │ FEC │  Signalling (17)   │
  │ 1  │ 1  │  2   │  3  │  （信令载荷区）      │
  └────┴────┴──────┴─────┴────────────────────┘
        └──────── TACT PDU = 7 bits ────────┘
                  Hamming (7,4) 护前 4 信息位
```

口算：1+1+2+3+17 = **24**。对得上。

### 4.3 TACT PDU（7 bit）——先认这三个开关

| 信息元 | 长度 | 含义（学习摘要） |
|--------|------|------------------|
| **AT** Access Type | 1 | `0` → 对应入站 **idle**；`1` → 入站 **busy**（连续发等场景下 AT 常为 busy 叙事） |
| **TC** TDMA Channel | 1 | `0` → 随后 outbound 为 **ch1**；`1` → **ch2** |
| **LCSS** | 2 | Short LC（及部分 CSBK 叙事）分片起止；见下表 |
| TACT parity | 3 | Hamming **(7,4)** |

LCSS 取值摘要（clause **9.3.3**；CACH 侧注意「无单片 LC」）：

| LCSS | 常见含义（摘要） |
|------|------------------|
| `00` | 单片 LC **或** 首片 CSBK（嵌入侧更常见「单片」叙事） |
| `01` | LC **首片** |
| `10` | **末片** |
| `11` | **续片** |

资料库提醒：**CACH 路径上没有「单片 LC」那种一口气塞完的用法**——Short LC 要靠多片 CACH 拼。实现细节以 PDF 为准；本课只要建立「LCSS = 分片交通灯」。

### 4.4 Signalling 17 bit 与 Short LC

CACH 的后 17 bit 是低速信令窗口。典型用途：

- 承载 **Short LC** 的分片（经 BPTC 等，Annex B.2.3）；  
- Short LC 信息外壳直觉（figure 7.2 精神）：

```text
  SHORT LC（拼齐后的信息叙事）：
  [ SLCO 4 ][ Short LC Data 24 ][ CRC-8 ]
```

- 没东西可发 → **Null Short LC**（Part2 `Nul_Msg`，SLCO=`0000`）。

本课边界：

- **要会**：CACH 能运低速 Short LC；空则 Null；LCSS 帮你拼片。  
- **先不必背**：每个 SLCO 业务语义（留给第 22 课 FULL/SHORT LC 专篇与 Part2）。

### 4.5 CACH 到底「广播」哪三件事？

把 §4 收成墙上三行：

1. **入站忙闲（AT）** —— 别人能不能礼貌地随机接入；  
2. **信道编号（TC）** —— 随后这路 outbound 是 1 号还是 2 号；  
3. **低速 Short LC 碎片（Signalling + LCSS）** —— 活动更新等慢消息的水管。

再加一句 Part1 原话精神：CACH 用于 **channel management（framing and access）** 以及 **low speed signalling**。

---

## 5. 时序直觉：为什么 CACH 指示常「晚一拍」？

引用精神：Part1 **figure 4.8 / 4.9**（资料库 §5 摘要）。

### 5.1 问题：手机需要反应时间

基站是全双工叙事：一边收着入站，一边在出站缝里广播「入站忙不忙」。  
但手机不是瞬时机器——它要：

1. **收到**这一拍 CACH；  
2. **解码** AT / TC / …；  
3. **决定**要不要抢接入；  
4. **切换**到发射（Tx/Rx switch）。

所以规范把关系设计成：

> **某一拍 CACH 指示的入站 busy / 信道号，相对 outbound 往往延迟约一个时隙。**  
> 例（figure 4.8 精神）：**紧挨在 outbound Slot2 突发前面的那拍 CACH**，指示的是 **inbound Slot2** 的状态。

### 5.2 现场翻译（别背图号）

你可以对外讲：

> 「基站报的忙闲，不是『此刻这一微秒』的玄学，而是给手机留出大约一个时隙量级的看报 + 决策 + 切换时间。所以排障时，别用示波器眼神把 CACH 边沿和入站边沿当成零延迟对齐。」

入/出站突发**中心对齐**、编号上常见 **30 ms 偏移**方案，也是为了让 **同一套信道号**能同时指「这一侧入站 / 出站」（clause **4.2.1**；第 15 课已预告）。本课把它和 CACH 的 TC 放在同一张直觉图里即可。

### 5.3 和「连续发」怎么共存？

- BS 出站：常持续发 → 缝里永远有机会塞 CACH；  
- 业务空：Traffic 用 **Idle** 填；CACH 用 **Null Short LC** 填；  
- MS 入站：没话就停 → 缝必须是 Guard，不能假装也有 CACH。

这就是**入/出站不对称**的根。

---

## 6. 现场对照：这些缝落在岗位上

### 6.1 协议分析仪：先认「缝是空还是 24 bit」

典型认图顺序（直觉版）：

1. 锁定 30 ms 绿灯与 264 货箱边界（第 15、16 课）。  
2. 看货箱**后面**那条约 2.5 ms：  
   - **出站**：应能解出 **CACH 24 bit**（AT/TC/LCSS/…）；  
   - **入站**：通常是 **Guard 空缝**（能量上可能只见噪声底或 PA 边沿）。  
3. 若出站两路 Traffic 之间看不到 CACH：先怀疑是否其实在看入站、或未进「连续出站」状态、或解码器没开 CACH 层。  
4. 语音超帧 A–F 仍只住在 Traffic 窗——**不要把 CACH 数进 Burst A–F**。

岗位翻译：**先分清货箱与缝，再谈 AT/TC。**

### 6.2 「按了上不去」vs AT=busy

| 现象 | 优先怀疑 | 和本课关系 |
|------|----------|------------|
| 有载波、出站很热闹，PTT 数据/控制总失败 | 对应入站已被标 **AT=busy**；礼貌接入在等 idle | 本课 AT |
| 出站安静却仍上不去 | 错频、错色码、中继未激活、权限/鉴权等 | 非本课主线 |
| 明明选了 Slot1，却像踩到 Slot2 | **TC** 解读/写频槽位/偏移编号 | 本课 TC |
| 直通双方对不齐 | DM 无 BS CACH 报站；靠 DM 同步规则 | 本课不对称 |
| 分析仪只见 264不见 24 | 看的是入站，或过滤器藏了 CACH | 本课划界 |

### 6.3 上行必须 Guard：功放与邻槽

手机在自己的逻辑时隙发射时：

- 突发内容仍是 264 bit；  
- 尾巴要留 **Guard**——给 **PA ramp**、**传播时延**、**晶振误差**留余量；  
- 若不留缝硬顶满 30 ms，最容易的现场后果是：**踩到邻时隙脚趾**（邻槽误码、对方投诉「有杂音/有干扰」）。

口诀：

> **出站缝是广播站；入站缝是安全气囊。**

### 6.4 写频 / 监听台 30 秒话术

你可以这样讲，不必报条款号：

> 「中继往下发的时候，两个时隙货箱之间会夹一段只有二十四个比特的小广播，告诉大家：上行这会儿忙不忙、接下来是 1 号还是 2 号槽，顺便捎点慢消息。手机往上发的时候，同样位置故意留空，好让功放爬起来、电波飞到位，还不踩邻居的槽。所以分析仪上『出站有小包、入站是空缝』是正常的，不是设备坏了。」

### 6.5 和岗位文档的词映射

| 你司/项目里可能出现的词 | 映射到本课 |
|--------------------------|------------|
| 公共通告信道 / CACH / 嵌入帧缝 | **出站 24 bit CACH** |
| 保护间隔 / guard / 时隙间隙 | **入站 / DM ≈2.5 ms Guard** |
| 接入指示 / busy/idle 位 | **AT** |
| 时隙标识 / channel 1·2 指示 | **TC** |
| 短 LC / Short LC / 活动更新 | CACH 低速 **Short LC** |
| 空短 LC / Null LC | **Null Short LC** |
| 踩槽 / 邻时隙干扰 | Guard 不够或定时漂 |

---

## 7. 完整例子：中继出站夹 CACH · 手机上行留 Guard

场景：Tier II 两频中继，Slot1 跑组呼，Slot2 可另有个呼或空闲。时间数字取常见教学量级；实现以 Part1 **4.2 / 4.5 / 4.6** 为准。

### 7.1 出站：BS 连续发，缝里永远有 CACH

```text
时间 →（Outbound，教学示意）

… | Traffic Slot1 | CACH | Traffic Slot2 | CACH | Traffic Slot1 | CACH | …
      ≈27.5 ms     ≈2.5   ≈27.5 ms        ≈2.5   …

某一拍 CACH 示例（字段直觉，非实时抓包）：
  AT=1 (该指示对应的入站侧 busy)
  TC=0 (随后 outbound 为 ch1) 或 TC=1 (ch2)
  LCSS=…（若在拼 Short LC）
  Signalling= Short LC 碎片 或 Null
```

观察点：

1. 出站频谱/示意上常接近**连续数字载波**（第 5 课已有语感）；  
2. 内部用时隙切开两路 Traffic，缝里塞 CACH；  
3. Slot1 即使在跑第 17 课的 A–F 火车，**火车仍在 Traffic 窗**；CACH 在车厢与车厢的**站台缝**里，不是第七节车厢。

### 7.2 入站：MS 只在自己的槽发，尾巴留 Guard

```text
时间 →（Inbound Slot1 有人讲话时，示意）

… | Traffic(MS) | Guard | （Slot2 入站窗：他人或其他用途） | Guard | …
      ≈27.5 ms    ≈2.5

MS 没话时：入站该槽直接安静（不发），更没有「假 CACH」。
```

观察点：

1. 同一物理入站频率上，两槽仍靠时间分开；  
2. 每个有发射的突发后面留 Guard；  
3. 手机一次通常只占**自己的那一槽**上行（第 15 课占空比语感）。

### 7.3 一张对照表（建议能默画）

| 时刻窗（示意） | 出站 BS | 入站 MS | 听众 MS |
|----------------|---------|---------|---------|
| 0–≈27.5 ms | 发 Slot1 Traffic（可能是超帧某节） | Slot1 讲话者若在讲，发 Traffic | 收 Slot1 |
| 随后 ≈2.5 ms | 发 **CACH**（AT/TC/…） | **Guard** / 或安静 | 解 CACH（看忙闲/信道号） |
| 下一 ≈27.5 ms | 发 Slot2 Traffic | Slot2 侧若有人在讲则发 | 收 Slot2（若关心这一路） |
| 再 ≈2.5 ms | 又一个 **CACH** | 又一段 **Guard** | 继续解 CACH |

### 7.4 Tier II 中继 vs DM / Talkaround

| 项 | Tier II 中继（两频 BS） | DM / Talkaround |
|----|------------------------|-----------------|
| 出站缝 | 常有 **CACH** | **通常没有** BS CACH 报站 |
| 入站缝 | **Guard** | 多为 **Guard** / DM 定时规则 |
| 谁报忙闲 | BS 经 CACH 的 **AT** 等 | 靠直通同步与监听，压力更大 |
| 同步压力 | BS 出站持续发，终端好「蹭节拍」 | 要自己找齐队伍（第 15 课已提醒） |
| 写频提醒 | 槽位 + 色码 + 入出频 | 同频同槽；别幻想有中继小广播 |

可选一句直通话术（与第 15 课衔接）：

> 「离开中继改 Talkaround，仍要选同一 Slot；并明白此时没有基站的 CACH 帮你报站——同步与接入礼貌都更吃硬功夫。」

### 7.5 突发长度三兄弟（防膨胀）

同场亮相时别认错：

| 名字 | 长度 | 住哪 |
|------|------|------|
| Traffic burst | **264** bit | 时隙内容窗 ≈27.5 ms |
| **CACH** | **24** bit | 出站缝 ≈2.5 ms |
| Standalone **RC** | **96** bit | 独立反向信道突发（后课/别课）；**不是** CACH |

Part1 clause **3** 定义级对照：264 / 24 / 96。本课只要会把 CACH 从 264 与 96 里摘出来。

---

## 8. 数字账本（建议钉在速查卡旁）

| 项 | 值 | 备注 |
|----|-----|------|
| Timeslot | **30 ms** | 第 15 课 |
| TDMA frame | **60 ms** | 两时隙 |
| Traffic 内容窗 | **≈ 27.5 ms** | 264 bit |
| **Guard / CACH 缝** | **≈ 2.5 ms** | 入站 Guard；出站 CACH |
| Traffic 总比特 | **264 = 108+48+108** | 第 16 课 |
| **CACH** | **24 bit** | **仅出站**；约每 **30 ms** 一次 |
| CACH 字段切分 | 1+1+2+3+17 | AT\|TC\|LCSS\|FEC\|Signalling |
| TACT | **7 bit** | AT+TC+LCSS+parity；Hamming (7,4) |
| Signalling 载荷率（约） | **17 bit / 30 ms ≈ 566.67 bit/s** | 资料库 §5；TACT 另计 |
| CACH 毛比特率（约） | **24 / 0.030 ≈ 800 bit/s** | 教学口算；勿与 9.6 kbps 混加 |
| Standalone RC | **96 bit** | 与 CACH 不同物种 |
| Voice superframe | **360 ms** | 只占用 Traffic 窗（第 17） |
| 入/出站编号 | 常见 **30 ms** 偏移 | 便于 CACH 同信道号 |
| CACH 指示延迟 | 约 **一个时隙** | figure 4.8/4.9 精神 |
| 符号率 / 比特率 | **≈ 4800 baud / 9.6 kbps** | 4FSK；缝不改调制 |
| 信道形态 | Traffic+CACH / Traffic+Guard / … | clause 4.6 |

口算口诀：

> **三十窗、二七五货箱、二五缝；出站缝塞二十四，入站缝留空气囊；忙闲看 AT，槽号看 TC，慢信走 Short LC。**

---

## 9. 常见误区

1. **「CACH 的 24 bit 算在 Traffic 的 264 里面。」**  
   错。CACH 在出站 **≈2.5 ms 缝**，与 108+48+108 **首尾相接但分账**（第 16 课已判错，本课再钉死）。

2. **「Guard 和 CACH 是同一个东西的两个名字。」**  
   错。同一条时间缝，**出站塞 CACH、入站留 Guard**——用途相反。

3. **「入站也有 CACH。」**  
   错。典型入站是 Traffic + **Guard**。CACH **仅出站**（连续发模式等场景按 Part1）。

4. **「AT=busy 表示我的 Talkgroup 忙。」**  
   错。AT 指示的是**对应入站时隙**忙闲，服务随机接入/礼貌接入，不是组号本身。

5. **「TC 就是超帧字母 A–F。」**  
   错。TC 只标 **信道 1/2**；A–F 是语音超帧车厢号（第 17 课）。

6. **「DM 直通也有基站那种 CACH 报站。」**  
   错。Talkaround / TDMA DM 通常**没有** BS 出站 CACH；同步压力更大。

7. **「CACH 换了一套调制或另开了 6.25 kHz。」**  
   错。仍是 **12.5 kHz + 4FSK**；只是时间缝里的比特。

8. **「Null Short LC 等于 Idle 突发。」**  
   错。Idle 填的是 **Traffic** 窗；Null Short LC 填的是 **CACH** 载荷空窗。两层都「空」，但不是同一个 PDU。

9. **「CACH 里的 LCSS 和嵌入 EMB 里的 LCSS 是同一个寄存器。」**  
   错。名字相同、职责类似（分片起止），但分属 **CACH TACT** 与 **EMB** 两处；解码时看你在解哪一层。

10. **「缝只有 2.5 ms，所以可以忽略定时误差。」**  
    错。正因为它短，PA 爬升、传播、晶振漂才更要守时——Guard 存在的理由就是这些「小误差」。

---

## 10. 自测（请先自己答，再展开）

**题 1.** 一个 30 ms 时隙，业务内容窗与缝大约各多长？出站缝与入站缝分别叫什么？

<details><summary>简答</summary>

内容窗约 **27.5 ms**（264 bit）；缝约 **2.5 ms**。出站缝 = **CACH**；入站缝 = **Guard**。

</details>

**题 2.** CACH 有多少 bit？是否包含在 Traffic 的 264 bit 内？它出现在入站还是出站？

<details><summary>简答</summary>

**24 bit**。**不包含**在 264 内。出现在**出站**缝；入站同位置通常是 Guard。

</details>

**题 3.** 默画（或默写）CACH 字段切分：AT、TC、LCSS、FEC、Signalling 的比特数，并指出 TACT 是哪一段。

<details><summary>简答</summary>

**1 + 1 + 2 + 3 + 17 = 24**。TACT = 前 **7** bit（AT+TC+LCSS+parity），由 Hamming (7,4) 保护。

</details>

**题 4.** AT 与 TC 各回答现场哪句话？同事说「AT=busy 就是我的组忙了」如何纠正？

<details><summary>简答</summary>

AT → 对应**入站时隙** idle/busy（接入用）。TC → 随后 outbound 是 ch1 还是 ch2。纠正：AT 不是 Talkgroup 忙闲标志。

</details>

**题 5.** 为什么规范常让 CACH 的忙闲/信道指示相对 outbound **延迟约一个时隙**？缺这拍延迟会伤到谁？

<details><summary>简答</summary>

给 MS 留出 **收 CACH → 解码 → 决策 → Tx/Rx 切换** 的时间（figure 4.8/4.9 精神）。没有延迟，手机来不及礼貌接入或选对槽。

</details>

**题 6.** 对比 Tier II 中继出站与 DM Talkaround：谁更常看到 CACH？上行缝通常是什么？

<details><summary>简答</summary>

中继出站常有 **CACH**；DM / Talkaround **通常没有** BS CACH。上行（及 DM）缝多为 **Guard**。

</details>

**题 7.** 写出突发长度三兄弟：Traffic / CACH / standalone RC 各多少 bit？哪一个住在 ≈2.5 ms 出站缝？

<details><summary>简答</summary>

**264 / 24 / 96**。住在出站缝的是 **CACH（24）**。

</details>

**题 8.** （巩固调制弱项）CACH / Guard 有没有改用别的调制或劈开 12.5 kHz？Signalling 约 17 bit/30 ms 的速率大约多少？能否把它和 9.6 kbps 直接相加当「空口总速率」对外乱讲？

<details><summary>简答</summary>

没有改调制，也不劈频；仍是 **12.5 kHz + 4FSK**。约 **566.67 bit/s**。**不能**随便和 Traffic 的 9.6 kbps 混加成对外口径——那是不同水管。

</details>

---

## 11. 资料库加深

按这个顺序读，避免一上来背 Short LC 全表或 BPTC 矩阵：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `00-入门/DMR术语与帧结构速查卡.md` | Guard / CACH 行 + 四种信道形态 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§2** | 时序数字；入站 Guard / 出站 CACH 总图 |
| 3 | 同上 **§5** | CACH 24 bit、TACT、AT/TC/LCSS、延迟一拍、Null Short LC |
| 4 | 同上 **§10** | Traffic+CACH / Traffic+Guard / Bi-directional / DM |
| 5 | `学习推送/第15课.md` | 缝的第一次预告与双时隙例子 |
| 6 | `学习推送/第16课.md` §5.8 | 264 vs 24 vs 96 划界 |
| 7 | `学习推送/第17课.md` | 确认 A–F 只住 Traffic 窗 |
| 8 | 官方 **TS 102 361-1 V2.7.1** clause **4.2、4.5、4.6、6.3、9.1.4**；figure **4.8 / 4.9** | CACH/Guard 原文；**冲突以 PDF 为准** |
| 9 | **TR 102 398** 对应导读 | 概念对照，**不是**替代 TS |
| 10 | `学习推送/加餐_频率带宽与调制解调.md` | 若 12.5 kHz / 4FSK 仍糊 |

官方版本锚点：**Part1 V2.7.1**；**TR V1.5.1**。冲突规则：**TS > TR > 手册/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 12. 下一课预告

**第 19 课 · SYNC：语音/数据如何区分**

本课站住了那条 ≈2.5 ms 缝：出站 CACH 报忙闲与槽号，入站 Guard 护邻槽与功放。下一课钻进 Traffic 货箱正中间那 **48 bit**：为什么语音与数据用**不同 SYNC 图案**，入站与出站图案又为何不同，接收机怎样「一听」就知道这是语音壳还是数据壳。仍少公式，多对照「SYNC ≠ Colour Code ≠ CACH」。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-27** 检索核验；**不编造地址**。策略 = **Part1 CACH/Guard 原文 + TR 导读 + Wavecom 出站 CACH/入站 Guard 图 + Guido Tier II 帧文 + VK4PK 时间参数 + 中文科普（带冲突声明）**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **4.5** 专节 CACH；**4.2** 讲入站 Guard / 出站 CACH 不对称；**4.6** 四种信道形态；**6.3 / 9.1.4** 给 24 bit 与 TACT；figure **4.8 / 4.9** 即「延迟约一个时隙」的硬出处。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)（部分网络可能拦截，可用协会镜像）。  
   - **适合哪一段**：第 2、4、5、8、11 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读用同样的「入站 guard / 出站 CACH」叙事，比纯条款好读；突发长度定义（264 / 24 / 96）也常在 TR 术语里一眼能对上。  
   - **适合哪一段**：第 2、7、8 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

3. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：明确写出站含 CACH、入站留 guard；并有 BS/MS 突发与帧结构图（文中 fig.3–5 一带），和本课总图可对照。  
   - **适合哪一段**：第 2、6、7 节。  
   - **注意**：厂商/分析仪向综述；个别术语口误勿盲从；**以 ETSI 为准**。  
   - **基础**：中级；英文 PDF。

4. **[Alessandro Guido｜How DMR Works — Conventional Tier 2（PDF）](https://www.qsl.net/kb9mwr/projects/dv/dmr/How%20DMR%20Works%20Conventional%20Tier%202.pdf)**  
   - **为什么值得看**：用常规 Tier II 口吻写清：入站 2.5 ms 给 PA/传播，出站 2.5 ms 给 CACH（帧编号、接入指示、低速信令）；并列出 CACH TACT 用 Hamming (7,4)、Short LC in CACH 等 FEC 名称表，和本课账本同向。  
   - **适合哪一段**：第 4、5、8 节后对照。  
   - **注意**：培训文年代可能早于现行 Part1 V2.7.1；**硬条款以 V2.7.1 为准**。  
   - **基础**：入门～中级；英文 PDF。

5. **[VK4PK｜DMR Signal Processing Notes](https://lyonscomputer.com.au/MMDVM/DMR-Signal-Processing-Notes/DMR-Signal-Processing-Notes.html)**  
   - **为什么值得看**：一页把 264 / 108+48+108 / 2.5 ms Guard / 4FSK / 4800 baud 写在一起，方便和「缝 vs 货箱」两本账对账。  
   - **适合哪一段**：第 2.5、8 节；巩固调制弱项。  
   - **基础**：入门～中级；英文网页；业余/MMDVM 笔记，**规范数字仍以 ETSI 为准**。

6. **[科讯｜DMR 对讲机数字协议详解](http://www.cqkexun.com/service/problem/hand/292.html)**  
   - **为什么值得看**：中文专段写明：每时隙 30 ms、27.5 ms 有效信息、另 2.5 ms 在上行作保护间隔（传播+功放）、在下行作 **CACH**（业务信道管理与低速信令）——适合建立中文第一印象。  
   - **适合哪一段**：第 2–3 节。  
   - **注意**：科普文版本偏旧；文中把 2.5 ms 叙述成「左右各 1.25 ms」等细节属教学简化，**间隙总账与用途划分以 ETSI TS 为准**。  
   - **基础**：入门；中文。

7. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：协会培训向总图；可与第 17 课嵌入/迟入材料连读，帮助把「Traffic 窗里的事」和「缝里的 CACH」在头脑里分柜。  
   - **适合哪一段**：读完本课想回看超帧与嵌入边界时。  
   - **注意**：不是 CACH 专章；幻灯版本锚点可能早于现行 Part1。  
   - **基础**：入门～中级；英文 PDF。

**说明（视频）**：公开检索未找到专门把 **「≈2.5 ms 缝：出站 CACH 24 bit（AT/TC/LCSS/Short LC）vs 入站 Guard（PA/传播/护邻槽）；CACH 指示延迟约一个时隙」** 讲透的独立高质量中文/英文短片（多数入门视频只口播「有两个时隙」或厂商产品介绍）。本课**未找到合适公开视频**。建议用：**Part1 clause 4.5 + figure 4.8/4.9 + Wavecom 出站/入站图 + Guido Tier II 文 + 资料库 §5** 对照自学。

---

*推送说明：本课为阶段 C「CACH 与 Guard」。频谱/调制仅保留短提醒（缝不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、缝总图、术语、24 bit 字段、忙闲/槽号/Short LC、延迟一拍时序、现场对照、中继 vs DM 例子、数字账本、十则误区、八题自测、资料库路径与七条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「为何出站缝塞 CACH、入站缝留 Guard、AT/TC 各管什么、为何指示常晚一拍、264/24/96 如何分柜」，并进入第 19 课 SYNC。*
