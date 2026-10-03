# 第 30 课 · 小综合：跟一次语音呼叫空口

> DMR 深入学习 · **阶段 D 语音与数据第 6 课（阶段 D 收官小综合）**（接第 29 课「Part2/Part3 字段文怎么查」）  
> 适合：已经跟过语音呼叫直觉（第 25）、迟后进入与补充（第 26）、空口积木（第 15–24）、三层书架查表（第 29），但**还不会把「时间线」和「当场翻表」叠成一条可演示跟读**——分析仪一响就不知道先看 SYNC 还是先骂天线——的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**跟读一次组呼/个呼空口：每个检查点翻哪张表、看哪个 Opcode/Data Type**」练成肌肉记忆  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。**跟读空口不改射频**——听不见、卡 Hangtime、组号写错，都不等于「调制坏了」。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是 **阶段 D 小综合：一条语音呼叫时间线 × 第 29 课翻表肌肉**。

---

## 1. 为什么本课重要（动机）

第 25 课把「一次 PTT 的上下车」画成了故事；第 26 课补了迟后进入与加料；第 29 课把「三层书架」钉进手指。机房下一句要命的话往往是：

- 分析仪已经在跑，同事喊：「跟一下这通组呼空口！」——你记得 Header、超帧、Terminator，但**此刻先翻哪一节**？  
- 屏上闪过 CSBKO=`111000`——是唤醒 BS，还是已经在说话？该开 Part2 §4.1 还是 §3.1？  
- 只看见 Burst A 的 Voice SYNC、没有 Header——算不算「没听到呼叫」？迟后进入该查总索引哪一行？  
- 中继「占着组不放」——是 Hangtime 正常，还是射频卡死？Terminator Data Type 是不是 `0010`？  
- 新人把 Tier III Grant 时间和常规 Header 时间线画在同一条轴上——整晚对不上。

培训台若只背「去看第 25 课总图」六个字，后面会卡在同一处：

> **会背时间线 ≠ 会跟读空口。** 跟读 = 在每个检查点知道「看什么壳（SYNC / Data Type / EMB）→ 看什么 Opcode（FLCO / CSBKO）→ 打开资料库哪一篇哪一节 → 何时才回 PDF」。本课不是把第 25/26/29 课再 dump 一遍，而是把它们**叠成一条可现场演示的跟读路径**。

本课目标：能画出「可选手续 → Header → 超帧 A–F → Terminator → Hangtime → EOC」总图，并在每个检查点说出翻表路径；会区分组呼 / 个呼（含 OACSU 可选一步）；会用 Late Entry 窗口解释「错过 Header 仍可能上车」；会分诊 Hangtime vs EOC、Tier II 常规 vs Tier III Grant；做现场分诊、六～七则例子与自测；并为第 31 课「控制信道 vs 业务信道」留好边界感。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不 dump Idle 96-bit、不贴完整 SDL、不发明 ETSI 条款号（入口锚点以资料库 `02-语音业务/语音业务字段速览.md` **§1–§9**、`01-空中接口/CSBK与LC字段详表.md`、`总索引.md` **§0–§5** 已有编号为准）、**不重讲第 25 课全文时间线细节**（只短回唤）、**不重讲第 26 课补充业务全景**（只开 Late Entry 窗口）、**不重讲第 29 课三层书架全文**（只在检查点「当场翻」）、**不展开 Tier III Grant/控制信道**（留给第 31+ 课）、**不展开 PDP/短数据**（第 27–28 课，本课只一句对照）。

---

## 2. 总图 / 故事：「跟读一次空口」

先把整课装进一个故事，再落到 `语音业务字段速览.md` **§2**、第 25 课总图、第 29 课三层书架。

### 2.1 一句话故事：旁白员跟着火车报站

把「跟读一次语音呼叫空口」想成你站在站台边当旁白员：

1. **（可选）手续车** = 中继睡着时先敲门（`BS_Dwn_Act`）；个呼有时先问在不在（`UU_V_Req` → `UU_Ans_Rsp` / `NACK`）；扫描台前还可发前导（`Pre_CSBK`）——**还不是语音**；  
2. **发车门牌** = Voice LC Header（Data Type=`0001`，Full LC 整包：谁找谁）；  
3. **列车 A–F** = 超帧开动：A 亮 Voice SYNC（边界+晚入上车点），B–E 贴嵌入门牌碎片，F 收尾；话长就多挂几列；  
4. **下车广播** = Terminator with LC（Data Type=`0010`，通常同门牌）；  
5. **（中继）留灯** = Hangtime：站台灯先不灭，同组回一句优先；  
6. **灯灭放空** = EOC / Idle：信道真正空出来。

口诀：**手续可选 → 门牌发车 → 超帧跑起来 → 终止下车 → 中继可留灯 → 最后才放空。每个站都翻一次表。**

### 2.2 总图：时间线 + 每个检查点的「翻表挂钩」

```text
  时间 →

  ┌─ CP0 可选 CSBK ─────────────────────────────────────┐
  │  BS_Dwn_Act / Pre_CSBK /（个呼）UU_V_Req→Ans/NACK    │
  │  壳：Data SYNC + Data Type=CSBK                      │
  │  翻：速览 §1.2 CSBKO → §4.x PDU；总索引「CSBK」       │
  └──────────────────────┬──────────────────────────────┘
                         ▼
  ┌─ CP1 Voice LC Header（BOT/BOC）─────────────────────┐
  │  Data Type = 0001；Full LC 整包                      │
  │  FLCO=000000 组呼 或 000011 个呼                     │
  │  翻：速览 §2 过程表 + §3.1/§3.2；详表 §4 FULL LC     │
  └──────────────────────┬──────────────────────────────┘
                         ▼
  ┌─ CP2 超帧 A–F（可多列，≈360 ms/列）─────────────────┐
  │  A: Voice SYNC（边界 + Late Entry 上车点）           │
  │  B–E: EMB + 嵌入 Full LC 碎片（同 FLCO/地址）         │
  │  F: 超帧收尾                                         │
  │  翻：详表 §2 EMB / §8 SYNC；速览 §2；总索引「超帧」   │
  │  （可选加料：Talker Alias / GPS → 速览 §3.3–3.5/§7） │
  └──────────────────────┬──────────────────────────────┘
                         ▼
  ┌─ CP3 Late Entry 窗口（半路上车，可与 CP2 重叠）──────┐
  │  等下一个 A 的 Voice SYNC → 拼 B–E → 比对 CC/时隙/组 │
  │  翻：总索引「迟后进入」→ 速览 §2/§7；第 26 课回唤     │
  └──────────────────────┬──────────────────────────────┘
                         ▼
  ┌─ CP4 Terminator with LC（EOT）──────────────────────┐
  │  Data Type = 0010；通常同 Voice Channel User LC      │
  │  翻：速览 §8；详表 Data Type；≠ Part3 TD_LC          │
  └──────────────────────┬──────────────────────────────┘
                         ▼
  ┌─ CP5 Hangtime（中继可选）→ CP6 EOC / Idle ──────────┐
  │  BS 可继续发 Terminator with LC 表示保留             │
  │  Hangtime ≠ TxHang ≠ Late Entry ≠ 「射频卡死」       │
  │  翻：速览 §8；总索引「Hangtime」；实现参数只对齐语义 │
  └─────────────────────────────────────────────────────┘
```

组呼 vs 个呼（路径分叉，记形状即可）：

```text
  组呼（常见跟读）
    （可选 BS_Dwn_Act / Pre_CSBK）
         → Voice LC Header（Grp_V_Ch_Usr，FLCO=000000）
         → 超帧 A–F…（可 Late Entry）
         → Terminator with LC → Hangtime → Idle

  个呼（可多一步「先问在不在」）
    （可选 BS_Dwn_Act）
         → UU_V_Req ──→ UU_Ans_Rsp(Proceed) ──→ Voice LC Header（UU，FLCO=000011）
         │                 └→ Deny / NACK → 不进入语音（跟读停在 CP0）
         → 超帧 A–F… → Terminator → Hangtime → Idle
```

### 2.3 和第 11 / 15–26 / 29 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 11 / 15–16 | 文档地图、30 ms、264 bit——本课当「尺子」 |
| 第 17–18 | 超帧 A–F、Voice SYNC@A、CACH/Act_Updt——本课钉在 CP2 |
| 第 19–21 | SYNC 认壳、CC、EMB/SLOT Data Type——本课每个 CP 先认壳 |
| 第 22–23 | Full LC 三处运载、可选 CSBK——本课 CP0/CP1/CP4 |
| 第 24 | FEC 原则——本课**不重讲矩阵**，只知「头/终止 RS24；嵌入 CS5」 |
| 第 25 | 呼叫时间线故事——本课**跟读 + 翻表**，不重画 SDL |
| 第 26 | Late Entry / 补充——本课只开 CP3 窗口 |
| 第 27–28 | PDP / 短数据——本课**一句对照**：语音跟读 ≠ 数据车次 |
| 第 29 | 三层书架——本课每个 CP **当场翻** |
| **本课** | **一条空口 × 检查点翻表 = 阶段 D 收官** |
| 第 31（预告） | 控制信道 vs 业务信道——Tier III 另一套「发车」故事 |

四句话串起来：

1. **壳**靠 SYNC / Data Type / EMB（第 19–21）；**门牌**靠 Full LC（第 22）；**可选手续**靠 CSBK（第 23）。  
2. **故事形状**靠第 25 课；**半路上车**靠第 26 课；**翻哪一节**靠第 29 课。  
3. **本课**只做一件事：把它们排成**可跟读的检查点清单**。  
4. **Tier III Grant** 不是本课轴——看见 Grant 先问「是不是集群控制信道故事」。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；跟读空口不另开频。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**；TS1/TS2 各走各的呼叫与 Hangtime。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps** 毛速率——跟读的是**比特语义时间线**，不是换调制。  
4. **解调直觉**：先认 SYNC（语音壳还是数据壳）→ Data Type / EMB → FLCO/CSBKO → 地址与 Service Options。  
   **听不见 ≠ 「射频没解调」**，也可能是：错过 Header 还在等 A、卡在 Hangtime、组/CC/时隙写错、或把个呼 Req 当成已经在说话。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **跟读空口** | 按时间线逐检查点认壳、认 Opcode、翻资料库 | ≠ 把第 25 课总图背一遍；≠ 只盯射频电平 |
| **检查点（CP）** | 本课把呼叫拆成 CP0–CP6 的「报站」 | ≠ ETSI 正式术语；是教学脚手架 |
| **BOT / BOC** | 发射开始 / 呼叫开始（Header 常落在这里） | BOT ≠ BOC；可多段发射组成一次呼叫 |
| **EOT / EOC** | 发射结束（常见 Terminator）/ 呼叫结束（Hangtime 后放空） | EOT ≠ EOC |
| **Voice LC Header** | 语音开始数据壳；DT=`0001`；整包 Full LC | ≠ 语音突发；中心是 Data SYNC |
| **Terminator with LC** | 语音结束数据壳；DT=`0010`；通常同门牌 | ≠ 数据终止 TD_LC（FLCO=`110000`，Part3） |
| **Grp_V_Ch_Usr / UU_V_Ch_Usr** | 组呼 / 个呼 Voice Channel User；FLCO=`000000` / `000011` | 别中途把 FLCO 当成「同一趟车换了业务」 |
| **Voice SYNC @ A** | 超帧边界标签；Late Entry 上车点 | ≠ Data SYNC（Header/Terminator/CSBK） |
| **嵌入 LC** | 超帧 B–E 中心碎片拼回 Full LC | ≠ Short LC（CACH）；≠ 另开副载波 |
| **Late Entry** | 错过 Header 后靠 SYNC@A + 嵌入拼门牌半路上车 | ≠ Hangtime；≠ 「永远听不见」 |
| **Hangtime** | EOT 后中继短暂保留本组优先（可继续发 Terminator with LC） | ≠ TxHang；≠ Late Entry；≠ 坏机 |
| **TxHang** | 实现用语：Hangtime 后再挂载波多久 | ≠ 规范呼叫 Hangtime 语义本身 |
| **BS_Dwn_Act / Pre_CSBK** | CSBKO=`111000` / `111101`：唤醒出站 / 扫描前导 | ≠ Voice Header；还在 CP0 |
| **UU_V_Req / UU_Ans_Rsp / NACK** | 个呼存在性检查（OACSU）；CSBKO=`000100`/`000101`/`100110` | 看见 Req ≠ 已经在说话 |
| **OACSU** | 进语音前「先问在不在」的可选路径 | ≠ 每一次个呼空口都必有 |
| **Service Options** | Full LC 里 8 bit：Emergency / Broadcast / OVCM / Priority… | ≠ FLCO；Broadcast **仅组呼** |
| **Tier II 常规时间线** | Header / 嵌入 / Terminator 门牌故事（本课） | ≠ Tier III 控制信道 Grant（第 31+） |
| **三层书架（回唤）** | 总索引 → 速览 → PDF（第 29 课） | 本课每个 CP 当场用，不重讲全文 |

---

## 4. 机制拆解：跟读时间线（检查点 + 查表路径）

Canonical 来源：`02-语音业务/语音业务字段速览.md` **§1–§2 / §3–§4 / §7–§8**；`01-空中接口/CSBK与LC字段详表.md` **§2 / §4 / §6 / §8**；`总索引.md` **§2（语音关键词）/ §4（语音业务最小打开集）**；第 25–26 / 29 课回唤。下列**故意不画完整 SDL**，每个检查点只给「认什么 → 翻哪」。

### 4.1 CP0 · 可选手续：Pre_CSBK / BS_Dwn_Act /（个呼）OACSU

**空口上你可能看见**：Data SYNC + Data Type = CSBK；CSBKO 落在速览 §1.2。

| 现象 | CSBKO | 白话 | 翻表路径 |
|------|-------|------|----------|
| 中继刚被叫醒出站 | `111000` BS_Dwn_Act | 敲门唤醒，**还不是语音** | 速览 **§1.2 → §4.1**；总索引「CSBK」 |
| 扫描/节电台前导 | `111101` Pre_CSBK | 帮你提高命中，**替代不了门牌** | 速览 **§4.5** |
| 个呼先问在不在 | `000100` UU_V_Req | 存在性检查请求 | 速览 **§4.2** |
| 对方同意/拒绝 | `000101` UU_Ans_Rsp | Proceed 才准进语音；Deny 停 | 速览 **§4.3** + §6.2 |
| 否定/不支持 | `100110` NACK_Rsp | 礼貌拒绝，**不进超帧** | 速览 **§4.4** |

**跟读口令**：

1. 先认壳：这是 **CSBK 数据壳**，不是 Voice Header。  
2. 读 CSBKO（不要误读成 FLCO——第 29 课已钉死两张 Opcode 表）。  
3. 只有「个呼 Proceed 之后」或「组呼直接进 Header」才进入 CP1。  
4. **不是每次呼叫都有 CP0**——直通组呼常常直接从 Header 开闸。

**一句对照（数据）**：确认/非确认 PDP、短数据三姐妹是第 27–28 课的「另一条车次」——本课跟读轴上**不要把 Data Header 当成 Voice LC Header**。

### 4.2 CP1 · Voice LC Header：发车门牌（当场翻 Full LC）

**空口上你应看见**：Data SYNC + **Data Type = `0001`（Voice LC Header）** + 整包 Full LC。

**跟读步骤（叠第 29 课肌肉）**：

```text
  分析仪：Data Type=0001
      │
      ▼
  总索引 §2「个呼/组呼」→ 语音业务字段速览
      │
      ▼
  §2 过程表确认阶段 =「语音开始」
      │
      ▼
  读 Full LC：FLCO（§1.1）→ FID → Service Options → 地址
      │
      ├─ FLCO=000000 → §3.1 Grp_V_Ch_Usr（组呼）
      └─ FLCO=000011 → §3.2 UU_V_Ch_Usr（个呼）
      │
      ▼
  外壳位宽有争议？→ 详表 §4 FULL LC / Part1 PDF（第三层）
```

岗位顺序口诀：**先 FLCO（组还是个）→ 再 Service Options 贴纸 → 最后读地址数字。**  
Broadcast 位**仅组呼**侧有广播/全呼语义；别在个呼 LC 上硬找 Broadcast 故事。

### 4.3 CP2 · 超帧 A–F + 嵌入 LC：火车在跑

一列超帧 = Burst **A–F** = **6 × 30 ms ≈ 360 ms**：

```text
  [Voice LC Header] → A B C D E F → A B C D E F → … → [Terminator]
                       │         │
                       │         └─ B–E：EMB + 嵌入 Full LC 碎片
                       └─ A：Voice SYNC（边界 + Late Entry 上车点）
```

| 突发 | 中心你先认什么 | 翻哪 |
|------|----------------|------|
| **A** | **Voice SYNC**（不是 Data SYNC） | 详表 **§8 SYNC 类型名**；总索引「语音超帧」 |
| **B–E** | EMB（16 bit）+ 嵌入 32 bit 碎片；LCSS 帮你拼 | 详表 **§2 EMB**；速览 §2 |
| **F** | 本超帧收尾；下一列再从 A | 第 17 课回唤 |

**跟读口令**：

1. 进入语音段后，**别再按「每个 30 ms 都有完整门牌」去找 Header**——门牌整包主要在 CP1；跑起来靠嵌入重复贴。  
2. 同一通话中，组呼就一直是 `Grp_V_Ch_Usr`；个呼就一直是 `UU_V_Ch_Usr`。  
3. 若嵌入里出现 FLCO=`000100`–`000111`（Talker Alias）或 `001000`（GPS_Info）——那是**加料乘客**（第 26 课），不是「换了一趟车」；翻速览 **§3.3–3.5 / §7**。  
4. Colour Code 在 EMB/SLOT 里当「同频系统色码门」——第 20–21 课眼镜继续戴着。

### 4.4 CP3 · Late Entry 窗口：半路上车（短回唤，不重讲第 26 课）

你太晚开机 / 扫描刚扫到 / 开头 Header CRC 失败时：

1. **步骤 1**：等到下一个 Burst **A**，认到 **Voice SYNC** → 对齐超帧相位；  
2. **步骤 2**：用 **B–E 嵌入**拼回 Full LC（FLCO + 地址 + Service Options）+ 比对 CC / 时隙 / 组；  
3. 匹配则开声；不匹配继续静音——**不是「射频永久坏了」**。

**翻表路径**：总索引「迟后进入 / 主叫识别」→ 速览 **§2 / §7** →（外壳）详表 SYNC/EMB → 需要认证再回 Part1 PDF（late entry 指针在库内已桥接）。  
**本课只要会在跟读轴上标出「CP3 可与 CP2 重叠」**；确认几次嵌入才锁定、与扫描如何配合——回第 26 课，不在此展开。

### 4.5 CP4 · Terminator with LC：下车广播

**空口上你应看见**：Data SYNC + **Data Type = `0010`（Terminator with LC）**；载荷通常仍是同一份 Voice Channel User LC。

**翻表路径**：速览 **§8**（语音 Terminator 要点）→ §2 过程表「语音结束」→ 详表 Data Type / FULL LC。  

**防晕三句**：

1. 源 MS 发 Terminator → 对端静音（EOT）。  
2. **语音 Terminator ≠ 数据 TD_LC**：后者 FLCO=`110000`，属 Part3（第 27 课指针）——本课跟读语音轴上别串台。  
3. 中继可能在 Hangtime 里**继续**发 Terminator with LC——那是 CP5，不是「用户又按了一次 PTT」。

### 4.6 CP5–CP6 · Hangtime vs EOC：留灯与放空

| 概念 | 直觉 | 空口可能看见 | 别混成 |
|------|------|--------------|--------|
| **Hangtime** | EOT 后短暂「本组优先」 | BS 继续 Terminator with LC / 活动指示；CACH AT 可仍 busy | Late Entry；射频卡死 |
| **TxHang** | 实现参数：保留后再挂载波多久 | 载波还在，但已不一定强占「刚才那组」 | 规范 Hangtime 本身 |
| **EOC / Idle** | 真正放空，别组可新开 | Idle 或无业务；CACH 可走 Nul_Msg | 「还在通话中」 |

**跟读口令**：同事喊「占着组不放」→ 先问 **Hangtime 定时是否在正常窗口**，再查射频与干扰。翻：速览 **§8**；实现侧 CallHang/TxHang 名称只对齐语义，**不要背成 ETSI 条款号**。

### 4.7 组呼 vs 个呼：OACSU 何时插入

- **组呼**：多数系统 CP0 可省略，直接 CP1（`Grp_V_Ch_Usr`）→ CP2 → CP4 → …  
- **个呼**：可能多一步 CP0 的 UU_V_Req/Ans；**只有 Proceed 才进 CP1（`UU_V_Ch_Usr`）**。  
- 不是每一次个呼空口都看得到 Req——取决于终端与系统策略。岗位直觉：**看见 UU_V_Req ≠ 已经在说话；看见 Voice LC Header(UU) 才算语音段开闸。**

### 4.8 边界钉死：Tier II 常规 ≠ Tier III Grant

本课跟读轴是 **Tier II 常规（业务信道上 Header/嵌入/Terminator 门牌）**。

**不是本课主线（留给第 31+ 课）**：

- 控制信道 vs 业务信道分工；  
- Aloha / 登记 / **Grant** 变体；  
- 「语音可以不靠前面的 LC Header、门牌改由控制信令告知」的集群变体。

看见「Grant」字样时，先问自己：**这是集群控制信道故事，还是常规中继 Header 故事？** 两套时间线别画在同一条轴上硬对齐。

### 4.9 一页「跟读速查卡」（可贴显示器边）

| CP | 先认壳 | 再认 Opcode/字段 | 打开 |
|----|--------|------------------|------|
| 0 | Data SYNC + DT=CSBK | CSBKO | 速览 §1.2 / §4 |
| 1 | Data SYNC + DT=`0001` | FLCO + 地址 + SO | 速览 §2 / §3.1–3.2 |
| 2A | **Voice SYNC** | 超帧相位 | 详表 §8；总索引「超帧」 |
| 2B–E | EMB + 嵌入 | 同 FLCO 碎片 / 可选 Alias | 详表 §2；速览 §7 |
| 3 | 同 2A→2B–E | Late Entry 两步 | 总索引「迟后进入」；速览 §2/§7 |
| 4 | Data SYNC + DT=`0010` | 同 Voice Channel User LC | 速览 §8 |
| 5–6 | Terminator 重复 / Idle | Hangtime vs EOC | 速览 §8 |

冲突规则回唤：**TS > TR > 博客/幻灯/课文**。课文是跟读脚手架，**实现与认证以 ETSI PDF 为准**。

---

## 5. 对照表：先前各课 → 本课时间线角色

| 时间线位置 | 空口形态 | 你用哪一课的眼镜 + 本课翻哪 |
|------------|----------|------------------------------|
| CP0 可选唤醒 | CSBK `BS_Dwn_Act` | 第 23 + 速览 §4.1 |
| CP0 可选个呼检查 | `UU_V_Req` / `UU_Ans` / `NACK` | 第 23/25 + 速览 §4.2–4.4 |
| CP0 可选前导 | `Pre_CSBK` | 第 23/26 + 速览 §4.5 |
| CP1 门牌 | Voice LC Header，DT=`0001` | 第 21–22/25 + 速览 §3 + 详表 §4 |
| CP2 列车 | 超帧 A–F；A=Voice SYNC；B–E 嵌入 | 第 17/21 + 详表 §2/§8 |
| CP3 半路上车 | Late Entry 两步 | 第 17/26 + 速览 §2/§7 |
| 加料乘客 | Talker Alias / GPS / SO 贴纸 | 第 26 + 速览 §3.3–3.5/§6–§7 |
| CP4 下车 | Terminator，DT=`0010` | 第 21–22/25 + 速览 §8 |
| CP5 留灯 | Hangtime 侧 Terminator | 第 25/26 + 速览 §8 |
| CP6 放空 | EOC / Idle | 第 25 + 速览 §8 |
| 查表肌肉 | 三层书架 | **第 29**（本课每个 CP 当场用） |
| **本课** | **把上表串成跟读清单** | — |
| 下一站边界 | 控制信道 / Grant | **第 31+**（本课只钉「别混」） |

---

## 6. 现场岗位对照 / 分诊

| 岗位现象 | 先做的跟读动作 | 常翻 | 别一上来就 |
|----------|----------------|------|------------|
| 「跟一下这通组呼」 | 从当前屏回放：有没有 Header？在哪一列超帧？有没有 Terminator？ | 速览 §2；本课速查卡 | 拆天线 / 改频率 |
| 只有 Voice SYNC、没有 Header | 标 CP3：等 A → 拼嵌入 → 比对组/CC | 总索引「迟后进入」；速览 §7 | 断言「没这通呼叫」 |
| 看见 UU_V_Req 就说「在通话」 | 停在 CP0：等 Ans 或等 Header(UU) | 速览 §4.2–4.3 | 按语音故障单处理 |
| FLCO=`000100` 当组呼 | 辨加料：Talker Alias header | 速览 §1.1 / §3.4 | 改组号乱试 |
| 「占着组不放」 | 问 Hangtime 窗口；看是否仍在发 Terminator with LC | 速览 §8 | 判发射机硬件卡死 |
| Data Type=`0010` 且 FLCO=`110000` | 这是数据 TD_LC 轴，不是本课语音跟读 | Part3 指针；第 27 课 | 硬套语音 Hangtime |
| 同事把 Grant 画进常规轴 | 停：问是不是 Tier III 控制信道 | 总索引「集群」；第 31 预告 | 用 Header 时间线硬解 Grant |
| 弱场开头坏、后面能听 | 可能 Header 丢、嵌入仍拼得动（Late Entry） | 详表 SYNC/EMB；第 26 | 只加功放不解时间线 |
| 两时隙串台感 | 确认跟的是 TS1 还是 TS2；各有 Hangtime | 第 15/18；调制钩子 | 当成单时隙模拟机 |

分诊口诀：**先定检查点 → 再认壳 → 再读 Opcode → 再翻速览 → 最后才碰射频与写频。**

---

## 7. 工作例子（7 则）

**例 1 · 直通组呼「干净跟读」**  
空口：Voice LC Header（FLCO=`000000`）→ 两列超帧 → Terminator。  
跟读：CP0 缺省；CP1 翻 §3.1；CP2 认 Voice SYNC@A；CP4 翻 §8。直通通常无中继 Hangtime 层。

**例 2 · 中继组呼带唤醒**  
先见 CSBKO=`111000`（BS_Dwn_Act）→ 再 Header → 超帧 → Terminator → BS 继续若干 Terminator（Hangtime）→ Idle。  
跟读：CP0 翻 §4.1（**还不是说话**）→ CP1–CP6 按速查卡。向领导一句话：「先敲门，再发车，再留灯。」

**例 3 · 个呼 OACSU 被拒**  
UU_V_Req → UU_Ans_Rsp(Deny) 或 NACK → **没有** Voice LC Header。  
跟读：停在 CP0；翻 §4.3/§4.4；不要按「语音超帧丢了」开单。

**例 4 · 扫描台半路上车**  
用户拧到谈组时，呼叫已在第二列超帧。屏上先锁 Voice SYNC@A，再拼出组地址，约半拍～约一个超帧量级后开声。  
跟读：标 CP3；翻总索引「迟后进入」+ 速览 §2/§7；回唤第 26 课两步，不重讲全文。

**例 5 · Hangtime 被当成故障**  
松 PTT 后中继仍占组约数秒，同组回一句很顺；别组硬上忙。  
跟读：CP5 正常；翻 §8；把 CallHang/TxHang 配置名对齐「先保留通话、再挂载波」，不要发明条款号。

**例 6 · 嵌入里出现 Talker Alias**  
超帧 B–E 拼出的不全是 Grp_V_Ch_Usr，间或 FLCO=`000100`…  
跟读：仍在同一趟组呼车上；加料乘客翻 §3.4–3.5；**不要**改 FLCO 当「换了个呼」。

**例 7 · 新人把 Tier III Grant 时间戳贴到常规录波**  
录波是常规中继，笔记却写「等 Grant」。  
跟读：用 §4.8 边界叫停；本课轴是 Header/嵌入/Terminator；Grant 留给第 31 课控制信道故事。

---

## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| 时隙 | **30 ms** | 跟读尺子 |
| 超帧 | **A–F ≈ 360 ms** | CP2 一列 |
| Voice LC Header Data Type | **`0001`** | CP1 |
| Terminator with LC Data Type | **`0010`** | CP4 |
| FLCO 组呼 / 个呼 | **`000000` / `000011`** | CP1/嵌入/终止门牌 |
| CSBKO 唤醒 / 前导 | **`111000` / `111101`** | CP0 |
| CSBKO 个呼 Req/Ans/NACK | **`000100` / `000101` / `100110`** | CP0 OACSU |
| Talker Alias FLCO | **`000100`–`000111`** | CP2 加料 |
| GPS_Info FLCO | **`001000`** | CP2 加料 |
| TD_LC FLCO（对照） | **`110000`** | **不是**本课语音终止 |
| Part2 官方版本 | **TS 102 361-2 V2.5.1 (2023-05)** | 语音过程硬出处 |
| Part1 官方版本 | **TS 102 361-1 V2.7.1 (2026-05)** | 外壳 / SYNC / EMB |
| 速览主节 | **§1–§2 / §3–§4 / §7–§8** | 本课跟读入口 |
| 详表主节 | **§2 EMB / §4 FULL LC / §6 CSBK / §8 SYNC** | 认壳 |
| 总索引 | **§2 语音关键词 / §4 语音最小打开集** | 门牌 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 跟读不改射频 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |

---

## 9. 十则误区（看见就打回）

1. **「跟读 = 把第 25 课总图再背一遍。」** → 跟读 = 每个 CP 认壳 + 翻表。  
2. **「看见 CSBK 就等于通话开始。」** → CP0 是手续；语音开闸看 Header（或 Late Entry 拼门牌）。  
3. **「错过 Header = 这通呼叫对你永久不可见。」** → CP3 Late Entry：SYNC@A + 嵌入。  
4. **「FLCO 和 CSBKO 混用一张嘴。」** → 两张 Opcode 表；外壳还在 Part1。  
5. **「Hangtime = 射频卡死 / = Late Entry / = TxHang。」** → 三者分家；先翻 §8。  
6. **「Terminator Data Type=`0010` 就一定是语音结束。」** → 再看 FLCO；`110000` 是数据 TD_LC。  
7. **「UU_V_Req 已经在说话。」** → 先问在不在；Proceed 后才 Header(UU)。  
8. **「嵌入里换了 FLCO = 换了一趟呼叫。」** → 可能是 Alias/GPS 加料乘客。  
9. **「Tier III Grant 可以画进本课常规轴。」** → 控制信道故事留给第 31+；别硬对齐。  
10. **「听不见说明 4FSK/12.5 kHz 坏了。」** → 先定 CP、认壳、对组/CC/时隙；调制账本最后背锅。

---

## 10. 自测题（含答案）

**题 1.** 用三句话说明本课「跟读」和第 25 课「直觉总图」差在哪。

<details><summary>答案</summary>

第 25 课给故事形状（门牌→火车→下车→留灯）。本课在每个检查点要求：认壳（SYNC/Data Type/EMB）→ 读 Opcode（FLCO/CSBKO）→ 打开速览/总索引哪一节（第 29 课肌肉）。跟读是可演示的操作清单，不是再背一遍上下车比喻。

</details>

**题 2.** 分析仪显示 Data Type=`0001`，FLCO=`000011`。写出跟读路径（CP + 文件节）。

<details><summary>答案</summary>

CP1。总索引「个呼」→ `语音业务字段速览.md` **§2** 确认「语音开始」→ **§1.1** FLCO=`000011` → **§3.2** UU_V_Ch_Usr；外壳争议回详表 §4 / Part1 PDF。

</details>

**题 3.** 为何「只看见 Burst A 的 Voice SYNC、没有 Header」不能直接判「没有呼叫」？

<details><summary>答案</summary>

可能处于 CP3 Late Entry：错过 Header 后，靠 Voice SYNC@A 对齐超帧，再拼 B–E 嵌入门牌；组/CC/时隙匹配仍可开声。翻总索引「迟后进入」与速览 §2/§7。

</details>

**题 4.** 写出 CP0 三种常见 CSBKO 及「还没进语音」的判断句。

<details><summary>答案</summary>

`111000` BS_Dwn_Act（唤醒）、`111101` Pre_CSBK（前导）、`000100` UU_V_Req（个呼先问）。判断句：壳是 CSBK 数据壳，不是 Voice LC Header；个呼还需 Ans Proceed 才进 CP1。

</details>

**题 5.** Hangtime 与 EOC、TxHang 如何用空口现象一眼分诊？

<details><summary>答案</summary>

Hangtime：EOT 后 BS 仍可发 Terminator with LC，本组优先。EOC/Idle：保留结束，信道放空。TxHang：实现层「再挂载波多久」，名称不是规范条款。先翻速览 §8，再对配置名。

</details>

**题 6.** 判断：Data Type=`0010` 且 FLCO=`110000`，应按本课语音 Terminator Hangtime 处理。（对 / 错）

<details><summary>答案</summary>

**错。** FLCO=`110000` 是 Part3 TD_LC（数据挂起指针）；语音终止通常是 Grp/UU_V_Ch_Usr。跟读轴不要串到数据车次。

</details>

**题 7.** 组呼跟读时，Broadcast 位应在哪一步读？为何「仅组呼」？

<details><summary>答案</summary>

CP1（及嵌入拼门牌后）先认 FLCO=`000000`，再读 Service Options 里的 Broadcast。资料库标明 Broadcast **仅组呼**侧用于广播/全呼类语义；个呼 FLCO 路径不走这套贴纸故事。

</details>

**题 8.** 现场：「同事把 Grant 时间戳和 Voice LC Header 画在同一条常规中继轴上」——你如何纠偏？再补一句调制提醒。

<details><summary>答案</summary>

用 §4.8：本课是 Tier II 常规 Header/嵌入/Terminator；Grant 属 Tier III 控制信道，留给第 31 课。调制提醒：选错时间线故事不改变 12.5 kHz/4FSK/双时隙——先纠跟读轴，再查射频。

</details>

**题 9.（加分）** 从「中继留灯」现象列出完整翻表路径（含与 Late Entry 的一句话区别）。

<details><summary>答案</summary>

现象 → 总索引/速览 §8 Terminator 与 Hangtime → 看是否仍在下发 Terminator with LC → 对实现 CallHang/TxHang 语义。区别：Late Entry 是半路拼门牌上车（CP3）；Hangtime 是 EOT 后保留本组优先（CP5）——不是同一件事。

</details>

**题 10.（加分）** 一列超帧里 A 与 B–E 的「先认什么」分别是什么？各翻详表哪一节？

<details><summary>答案</summary>

A：先认 **Voice SYNC**（详表 §8）。B–E：先认 **EMB + 嵌入碎片**（详表 §2），再拼回与 Header 同类的 Full LC（速览 §2/§3）。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `02-语音业务/语音业务字段速览.md` **§2 / §8** | 过程对照表 + Terminator/Hangtime（本课 canonical 时间线） |
| 2 | 同上 **§1 / §3–§4 / §7** | Opcode 入口、Full LC/CSBK PDU、补充/Late Entry 指针 |
| 3 | `01-空中接口/CSBK与LC字段详表.md` **§2 / §4 / §6 / §8** | EMB、FULL LC、CSBK 壳、SYNC 类型名 |
| 4 | `总索引.md` **§2 语音关键词 / §4 语音最小打开集** | 门牌：个呼组呼迟后进入 → 速览 → Part2 PDF |
| 5 | `学习推送/第25课.md` | 呼叫直觉总图（故事回唤，不重读全文也行） |
| 6 | `学习推送/第26课.md` | Late Entry 两步与加料（CP3 回唤） |
| 7 | `学习推送/第29课.md` | 三层书架与查表路径（每个 CP 的肌肉） |
| 8 | `学习推送/第17课.md` / `第21课.md` / `第22课.md` | 超帧、Data Type、Full LC 三处运载 |
| 9 | `00-入门/DMR术语与帧结构速查卡.md` | 墙上 30 ms / 超帧 / Data Type |
| 10 | `DMR整合学习手册.md` | 全貌与 Tier 边界 |
| 11 | 官方 **TS 102 361-2 V2.5.1**（`02-语音业务/TS102361-2_V2.5.1.pdf`） | 组/个呼过程与 PDU 原文 |
| 12 | 官方 **TS 102 361-1 V2.7.1** | Voice LC Header / Terminator / 嵌入 / SYNC 硬出处 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「跟错检查点」当成调制故障 |

官方版本锚点：**Part2 V2.5.1**、**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。FEC 矩阵、Idle 比特、完整 SDL、Tier III Grant 全表、PDP 车次细节：**永远回 PDF / 对应课**，本课不补第二份。

---

## 12. 下一课预告

**第 31 课 · 控制信道 vs 业务信道**

本课把阶段 D 收在「一条语音呼叫空口跟读 + 检查点翻表」。下一课进入 **阶段 E · 集群 Tier III**：先分清**控制信道**和**业务信道**各干什么——谁负责叫号/授权（Grant），谁承载真正的语音超帧；为什么常规中继的 Header 故事不能直接套到集群控制信道。仍然少公式；把「Tier II 常规 ≠ Tier III Grant」从本课的边界警告，展开成可跟读的集群地图第一课。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-03**（上午推送）检索核验；真实打开过内容页/PDF（协会镜像 / ETSI deliver / Tait Academy / GopherTrunk 等 HTTP 200）。**不编造地址**。策略 = **Part1 协会镜像 + Part2 协会镜像 + Part2 ETSI 官方链 + DMRA 标准目录 + Benefits 白皮书 + Feature Evolution + TR 系统总览 + Tait Intro Study Guide + Tait 课程页 + GopherTrunk E2E Part5（Link Control / Embedded LC / Late Entry，最贴「跟读时间线」）+ GopherTrunk Operator Cookbook Part3（常规双时隙语感）+ GopherTrunk Decoders Part5（Bursts/EMB/FLC）**。另检索公开「walk a DMR voice call air-interface timeline / 跟读语音呼叫空口」专题视频与长文：**未找到**达到本课「CP0–CP6 检查点 + 当场翻表」深度的独立优质短片（Tait Academy 有入门视频课，但是 **DMR 概论**；产品写频/双时隙口播亦不适用）。**已弃用**易触发浏览器挑战的第三方 wiki 页。

1. **[ETSI TS 102 361-2 V2.5.1｜Voice and generic services（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：组呼/个呼过程、Voice Channel User LC、Call hangtime 与 EOC 语义的硬出处；与速览 §2/§8 对照跟读。  
   - **库内副本**：`dmr/02-语音业务/TS102361-2_V2.5.1.pdf`。  
   - **适合哪一段**：第 2、4.1–4.6、8、11 节。  
   - **基础**：进阶；英文 PDF。

2. **[ETSI TS 102 361-2 V2.5.1｜ETSI 官方投递链](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/02.05.01_60/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：与协会镜像同文的官方入口；部分环境抓取异常时改用镜像或浏览器。  
   - **适合哪一段**：同上。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：Voice LC Header / Terminator with LC / 嵌入信令 / Voice SYNC 与 late entry 超帧叙述——跟读时「认壳」第三层。  
   - **适合哪一段**：第 4.2–4.4、8、11 节。  
   - **基础**：进阶；英文 PDF。

4. **[DMR Association｜DMR Standards 目录页](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：协会标准下载门牌——给新人「官方书架在哪」；跟读争议时知道回哪本 PDF。  
   - **注意**：目录页≠时间线课文；版本以 PDF 封面与总索引 §3 为准。  
   - **适合哪一段**：第 2、11 节。  
   - **基础**：入门；英文网页。

5. **[DMR Association｜Benefits and Features of DMR（白皮书 PDF）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：产品语言里的语音能力与迟后进入语感——适合向领导解释「为什么要会跟读空口」。  
   - **注意**：白皮书不是 TS；冲突以 Part1/2 为准。  
   - **基础**：入门；英文 PDF。

6. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：嵌入 LC / late entry 等能力演进图示——补 CP2/CP3 产品侧直觉。  
   - **注意**：演进叙述≠字段表；Opcode 仍回速览/Part2。  
   - **适合哪一段**：第 4.3–4.4、7 节例 4/6。  
   - **基础**：入门～中级；英文 PDF。

7. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统总览——把本课「常规语音跟读」放回 Tier 与业务全景；为第 31 课控制/业务信道铺垫。  
   - **注意**：TR 非 TS；冲突以 Part1/2 为准。  
   - **适合哪一段**：第 2.3、4.8、12 节。  
   - **基础**：中级；英文 PDF。

8. **[Tait Radio Academy｜Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：厂商学院指南，巩固「时隙 / 语音超帧 / 中继」语感，降低跟读门坎。  
   - **注意**：导读≠速览；版本较旧时以现行 ETSI / 总索引 §3 为准。  
   - **适合哪一段**：第 1、2、6 节。  
   - **基础**：入门；英文 PDF。

9. **[Tait Radio Academy｜Introduction to DMR 课程页](https://www.taitradioacademy.com/courses/introduction-to-digital-mobile-radio/)**  
   - **为什么值得看**：有入门视频课与评估——弱基础补「DMR 是什么」；**不是**「跟读语音呼叫空口检查点」专题课。  
   - **适合哪一段**：课前预习 / 第 1 节动机。  
   - **基础**：入门；英文网页/视频。

10. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
    - **为什么值得看**：把 Full LC、Header/Terminator、嵌入碎片与 late entry 串成一条实现侧故事——**最贴近本课「跟读时间线」**的公开长文。  
    - **注意**：**实现≠规范**；确认次数等策略是实现选择，冲突以 ETSI PDF 为准。  
    - **适合哪一段**：第 4.2–4.4、7、9 节。  
    - **基础**：中级～进阶；英文网页。

11. **[GopherTrunk｜Operator Cookbook Part 3：Conventional DMR Two Slots](https://gophertrunk.org/blog/tutorials/operator-cookbook-03-conventional-dmr-two-slots/)**  
    - **为什么值得看**：常规双时隙操作语感——提醒跟读时 TS1/TS2 各有各的呼叫与 Hangtime。  
    - **注意**：操作菜谱≠ Part2 过程条文。  
    - **适合哪一段**：第 2.4、6、7 节。  
    - **基础**：入门～中级；英文网页。

12. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
    - **为什么值得看**：从解码器视角看 Burst / EMB / FLC——练「先认壳再读门牌」。  
    - **注意**：解码器字段名可能简称；以速览/TS 为准。  
    - **适合哪一段**：第 4.2–4.3、8、10 题。  
    - **基础**：中级～进阶；英文网页。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 语音呼叫空口跟读：可选 CSBK → Voice LC Header → 超帧 A–F（嵌入 LC）→ Late Entry 窗口 → Terminator → Hangtime → EOC，并在每个检查点翻 Part2 速览/总索引」** 按课堂深度讲透的独立高质量中文/英文短片。Tait Radio Academy 的 Introduction to DMR 是**概论视频课**，可作弱基础补课，但不能替代本课检查点操练。本课 **`video_found=false`**。建议用：**语音业务字段速览 §2/§8 + Part2 V2.5.1 + 本课 CP 速查卡 + GopherTrunk E2E Part5** 对照自学。

---

*推送说明：本课为阶段 D 收官小综合「跟一次语音呼叫空口」。频谱/调制仅保留短提醒（跟读不换频、不改 4FSK/双时隙；跟错检查点≠射频故障），不复述加餐全文。主文加厚覆盖动机、跟读总图与 CP0–CP6 翻表挂钩、术语、各检查点机制（可选手续/Header/超帧嵌入/Late Entry 窗口/Terminator/Hangtime–EOC/组个呼 OACSU/Tier II≠Tier III Grant）、与第 11/15–26/29 课对照、现场分诊、七则例子、账本、十则误区、十题自测、资料库路径与核验外链（含 Part1/Part2、DMRA 目录与白皮书/Feature Evolution、TR、Tait 指南与课程页、GopherTrunk 三条；诚实标明无合适公开「跟读空口检查点」专题视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle、不发明条款号、不重讲第 25/26/29 课全文、不展开 Grant/PDP。读完应能向同事演示「从录波跟读一通组呼/个呼：每个站认壳并翻到速览对应节」，并带着「常规 ≠ 集群控制信道」边界进入第 31 课。*
