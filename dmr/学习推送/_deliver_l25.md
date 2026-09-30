# 第 25 课 · 语音呼叫过程直觉

> DMR 深入学习 · **阶段 D 语音与数据第 1 课**（阶段 D 开篇）  
> 适合：已吃透第 17 课超帧、第 21 课 EMB/SLOT、第 22 课 Full/Short LC、第 23 课 CSBK、第 24 课 FEC 原则，但仍会把「一次语音呼叫」想成「按住 PTT 就有声音」、分不清 Header/嵌入/Terminator、或把 Hangtime 当成中继故障、或把 Tier II 常规与 Tier III Grant 搅在一起的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**一次语音呼叫 =（可选）唤醒/个呼检查 CSBK → Voice LC Header（门牌）→ 超帧 A–F 语音+嵌入 LC（迟到也能上车）→ Terminator with LC（下车）→（中继）Hangtime 保留 → Idle**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。呼叫过程**不换频、不改调制、不另开带宽**——它只是「同一条 264 bit 突发列车」上，**单据类型与门牌怎么按时间排队**。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是**时间线直觉 + 组呼/个呼路径 + 现场对照**。

---

## 1. 为什么本课重要（动机）

阶段 C（第 15–24 课）像拆快递积木：时隙、突发、超帧、CACH、SYNC、色码、EMB/SLOT、Full/Short LC、CSBK、FEC……  
同事在机房常会问四句要命的话：

- 按住 PTT 之后，空口上**先出什么、后出什么**？为什么有时先静音半拍才进会？  
- 分析仪上同时看见 **Voice LC Header、语音、Terminator、CSBK、Idle**——哪一段才叫「这次通话」？  
- 为什么中继「已经没人说话」却还占着组、别人换组呼不进去？这是坏了还是 **Hangtime**？  
- 培训台上若开始背 Part 2 整本 SDL，后面会卡在同一处：

> **一次语音呼叫 =（可选）唤醒/个呼检查 CSBK → Voice LC Header（门牌）→ 超帧 A–F 语音+嵌入 LC（迟到也能上车）→ Terminator with LC（下车）→（中继）Hangtime 保留 → Idle。Header / 嵌入 / Terminator 复用同一份 Full LC 门牌正文；本课只建立时间线直觉，不背状态机。**

本课目标：能讲清时间线口诀；画 BOT→Header→超帧→Terminator→Hangtime→Idle；分清组呼/个呼与可选 CSBK；对照第 7/15–24 课角色；做现场分诊与自测；并知道细讲迟后进入在第 26 课。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不 dump Idle 96-bit、不贴 Annex E 符号表、不发明 ETSI 条款号（只用资料库与前课已出现的锚点）、不把 Tier III Grant 冒充本课主线。

---

## 2. 总图 / 故事：一次 PTT 的「上下车」

先把整课装进一个故事，再落到 Part 2 clause **5.2**（组呼/个呼过程摘要）、Part 1 Data Type、以及资料库 `02-语音业务/语音业务字段速览.md` **§2 / §8**。

### 2.1 一句话故事：门牌 → 火车 → 下车 → 站台留灯

把「按住 PTT 说一句话」想成坐城际火车：

1. **（可选）唤醒 / 办手续** = 中继睡着时先敲门（`BS_Dwn_Act`）；个呼有时先打电话确认对方在不在（`UU_V_Req` → `UU_Ans_Rsp` / `NACK`）；扫描/节电台前还可发前导（`Pre_CSBK`）；  
2. **Voice LC Header** = 站台上贴大海报：**谁找谁、组呼还是个呼**（Full LC，Data Type=`0001`）；  
3. **超帧 A–F 语音** = 火车开动：Burst **A** 亮 Voice SYNC（边界+晚入上车点），**B–E** 把同一份门牌撕成贴纸贴车厢上，**F** 收尾本超帧；话长就多挂几列超帧；  
4. **Terminator with LC** = 到站广播「本趟结束」（Data Type=`0010`，通常仍带同一份 Voice Channel User LC）；  
5. **（中继）Hangtime** = 站台灯先不灭，给同组回一句的优先权；  
6. **Idle / 放载波结束** = 灯灭、站台空出来，别人才能换组新开一趟。

口诀：**先贴门牌（Header），再坐火车（A–F），再下车广播（Terminator），中继可先留灯（Hangtime），最后才 Idle。**

### 2.2 总图：BOT / BOC → Header → 超帧 → EOT → Hangtime → EOC

```text
  时间 →

  [可选 CSBK]
   · BS_Dwn_Act（唤醒 BS 出站）
   · UU_V_Req → UU_Ans_Rsp / NACK（个呼存在性检查 OACSU）
   · Pre_CSBK（扫描/节电前导）
         │
         ▼
  ┌─────────────────────┐
  │ BOT / BOC            │  通话 / 呼叫「开始」边界（见术语表）
  │ Voice LC Header      │  Data Type = 0001
  │  Full LC 门牌整包     │  FLCO=000000 组呼 或 000011 个呼
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ 超帧 A–F（可多列）    │  每列 ≈ 360 ms = 6 × 30 ms
  │  A: Voice SYNC       │  边界 + 迟后进入上车点
  │  B–E: 嵌入 Full LC   │  同一门牌碎片；迟到也能拼
  │  F: 超帧收尾         │
  │ （可嵌 Talker Alias / GPS 等，细讲见后续课）
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ EOT                  │  发射结束边界
  │ Terminator with LC   │  Data Type = 0010；同 FLCO/地址
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ （中继）Hangtime      │  BS 可继续发 Terminator with LC 表示保留
  │  同组礼貌回一句优先   │  ≠ TxHang（载波还挂着的另一层计时）
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ EOC / Idle           │  呼叫结束；信道空闲可被别组占用
  └─────────────────────┘
```

组呼 vs 个呼（路径分叉，记形状即可）：

```text
  组呼（常见）
    （可选 BS_Dwn_Act / Pre_CSBK）
         → Voice LC Header（Grp_V_Ch_Usr，FLCO=000000）
         → 超帧 A–F…
         → Terminator with LC
         → Hangtime → Idle

  个呼（可多一步「先问在不在」）
    （可选 BS_Dwn_Act）
         → UU_V_Req ──→ UU_Ans_Rsp(Proceed) ──→ Voice LC Header（UU_V_Ch_Usr，FLCO=000011）
         │                 └→ Deny / NACK → 不进入语音
         → 超帧 A–F…
         → Terminator with LC
         → Hangtime → Idle
```

### 2.3 和第 7 / 15–24 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 7 | 个呼/组呼寻址直觉 → 本课落到 FLCO 与地址场 |
| 第 15–16 | 30 ms 时隙、264 bit 突发 |
| 第 17 | 超帧 A–F、Voice SYNC@A、嵌入拼门牌、迟后进入「上车点」 |
| 第 18 | CACH；语音中可有 Act_Updt（活动广播） |
| 第 19–20 | SYNC 认壳；Colour Code 色码门 |
| 第 21 | SLOT 的 Data Type 路由：`0001` Header / `0010` Terminator |
| 第 22 | Full LC 三处运载：Header / 嵌入 / Terminator；Short LC ≠ Full LC |
| 第 23 | 可选手续 CSBK：唤醒、个呼请求/应答、NACK、Pre_CSBK |
| 第 24 | Header/Terminator 走 RS24+BPTC；嵌入走 CS5+变长 BPTC——本课不重讲矩阵 |
| **本课** | 把上述积木排成**一次呼叫时间线** |

四句话串起来：

1. **壳**靠 SYNC（第 19），**色码门**靠 CC（第 20）；  
2. **单据类型**靠 SLOT Data Type（第 21）：Header=`0001`，Terminator=`0010`；  
3. **门牌正文**靠 Full LC（第 22），可整包也可嵌入；  
4. **可选手续**靠 CSBK（第 23）——不是每次呼叫都必有。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；呼叫过程不另开频。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**；**同一载波可两路通话**（TS1/TS2 各走各的）。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps**。  
4. **解调直觉**：先认 SYNC → 看是数据壳（Header/Terminator/CSBK）还是语音壳 → 再解 Full LC / 嵌入。  
   **听不见 ≠ 「射频没解调」**，也可能是错过 Header、卡在 Hangtime、或组号/时隙写错。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **BOT** | Beginning of Transmission，一次发射（按住 PTT 这一段）的开始 | ≠ BOC（呼叫级） |
| **BOC** | Beginning of Call，整次呼叫的开始（可含多段发射） | ≠ BOT |
| **EOT** | End of Transmission，松开 PTT / 本段发射结束（常见 Terminator） | ≠ EOC |
| **EOC** | End of Call，整次呼叫结束（Hangtime 过后真正放空） | ≠ EOT |
| **Voice LC Header** | 语音开始的数据壳；Data Type=`0001`；整包带 Full LC 门牌 | ≠ 语音突发；中心是 Data SYNC |
| **Terminator with LC** | 语音结束的数据壳；Data Type=`0010`；通常同门牌 | ≠ 数据终止 TD_LC（FLCO=`110000`，Part 3） |
| **Grp_V_Ch_Usr** | 组呼 Voice Channel User；FLCO=`000000` | ≠ UU 个呼 |
| **UU_V_Ch_Usr** | 个呼 Voice Channel User；FLCO=`000011` | ≠ 组呼 |
| **Late entry（迟后进入）** | 错过 Header 后，靠 Voice SYNC@A + 嵌入/头中地址 LC 半路上车 | ≠ 「永远听不见」；细机制第 26 课 |
| **Hangtime** | 中继在 EOT 后短暂保留本通话/本组优先（可继续发 Terminator with LC） | ≠ TxHang（载波仍开着的另一层）；≠ 坏机 |
| **TxHang** | 实现/中继参数：Hangtime 后再挂载波多久才关发射机（常见业余实现用语） | ≠ 规范里的呼叫 Hangtime 语义本身 |
| **BS_Dwn_Act** | CSBKO=`111000`：唤醒/激活 BS 出站 | ≠ Voice Header |
| **UU_V_Req / UU_Ans_Rsp** | 个呼存在性检查请求/应答（OACSU）；CSBKO=`000100` / `000101` | ≠ 已经在语音超帧里 |
| **NACK_Rsp** | 否定应答；CSBKO=`100110`；可礼貌拒绝不支持的业务 | ≠ Terminator |
| **Pre_CSBK** | 前导 CSBK；CSBKO=`111101`；帮扫描/节电台提高命中 | ≠ 门牌 Full LC |
| **Service Options** | Full LC / 部分 CSBK 里 8 bit：Emergency / Privacy / Broadcast / OVCM / Priority… | ≠ FLCO 本身 |
| **OVCM** | Open Voice Call Mode：业务选项里一比特；与「开放语音」类行为相关 | ≠ Broadcast |
| **Broadcast** | 业务选项比特；**仅组呼**侧用于广播/全呼类语义（配合全呼地址约定） | ≠ 个呼 FLCO |

---

## 4. 机制拆解：时间线上发生什么

Canonical 来源：`02-语音业务/语音业务字段速览.md` **§2（过程表）/ §3–4（PDU）/ §6（Service Options）/ §8（Terminator）**；Part 2 clause **5.2**；Part 1 Data Type 与 late entry 指针（Part 1 **5.1.2**）。下列**故意不画完整 SDL**。

### 4.1 组呼路径（直通 + 中继）

**直通（MS↔MS）直觉**：

1. 主叫按 PTT → 发 **Voice LC Header**（`Grp_V_Ch_Usr`：组地址 + 源地址 + Service Options）；  
2. 紧接 **语音超帧 A–F**（可多列）；  
3. 松 PTT → **Terminator with LC**（同门牌）；  
4. 对端静音。直通场景通常**没有**「中继 Hangtime 留灯」那一层（没有 BS 替你占信道）。

**中继（MS→BS→MS）直觉**：

1. （可选）BS 休眠时先发 **BS_Dwn_Act** 唤醒出站；  
2. 上行 Header → BS 校验后下行转发同门牌；  
3. 语音超帧双向转发（你仍按「同一时间线」理解）；  
4. 源 MS 发 Terminator → BS 可在 **Hangtime** 内继续发 Terminator with LC，表示「这组还留着」；  
5. Hangtime 结束 → 进入 Idle / 关载波（实现上可能还有 TxHang）。

现场口语对照：「占着组不放」常常是 **Hangtime 正常工作**，不是射频卡死。

### 4.2 个呼路径：可选 OACSU 检查

个呼 Full LC 用 **UU_V_Ch_Usr**（FLCO=`000011`：目标个号 + 源地址）。

许多系统在进语音前可先做 **OACSU** 式存在性检查（资料库 §2 / §4.2–4.4）：

1. 主叫发 **UU_V_Req**（CSBK）；  
2. 被叫（或经 BS）回 **UU_Ans_Rsp**：Proceed=`00100000` 继续；Deny=`00100001` 拒绝；  
3. 也可能收到 **NACK_Rsp**（不支持/无法提供等）；  
4. 只有 Proceed 路径才进入 **Voice LC Header（UU）→ 超帧 → Terminator**。

不是每一次个呼空口上都看得到 Req/Ans——取决于终端配置与系统策略。你的岗位直觉应是：**看见 UU_V_Req 不代表已经在说话；看见 Voice LC Header(UU) 才算语音段开闸。**

### 4.3 三份门牌：Header / 嵌入 / Terminator 复用同一 Full LC

第 22 课已钉死：Full LC 门牌正文约 72 bit 信息（PF|Reserved|FLCO|FID|Data56）。语音呼叫里它至少出现三次「运载形态」：

| 形态 | 壳 | 校验直觉（第 22/24 课） | 作用 |
|------|----|------------------------|------|
| Voice LC Header | 数据壳 + Data Type=`0001` | RS(12,9) 24-bit + BPTC | **发车门牌**（最完整的一次「整包」） |
| 嵌入 LC（超帧 B–E） | 语音壳 + EMB/LCSS | CS5 + 变长 BPTC | **中途上车**仍能拼出谁呼谁 |
| Terminator with LC | 数据壳 + Data Type=`0010` | 同 Header 路径（RS24+BPTC） | **下车广播**；中继 Hangtime 也可继续发 |

同一通话中，组呼就一直是 `Grp_V_Ch_Usr`；个呼就一直是 `UU_V_Ch_Usr`——**别在中途把 FLCO 换成别的业务还以为是「同一趟车」**（Talker Alias / GPS 是嵌入里的「另一类乘客」，见资料库 §3.3–3.5，细讲留给补充业务课）。

### 4.4 超帧在时间线上的位置（复习 + 钉角色）

一列超帧 = Burst **A–F** = **6 × 30 ms ≈ 360 ms**：

```text
  … → [Voice LC Header] → A B C D E F → A B C D E F → … → [Terminator] → …
                              │         │
                              │         └─ B–E：嵌入 Full LC 碎片（迟到拼门牌）
                              └─ A：Voice SYNC（边界 + late entry 上车点）
```

- **A**：中心多为 **Voice SYNC**（不是 Data SYNC）；  
- **B–E**：EMB + 嵌入碎片，拼回与 Header 同类的 Full LC；  
- **F**：本超帧收尾；下一列再从 A 开始。

话越长，超帧列数越多；**门牌不会只在开头出现一次**——这正是迟后进入能成立的原因。

### 4.5 迟后进入直觉（本课只开窗，细讲归第 26 课）

你已经在第 17 / 22 课见过「半路上车」：

1. 抓到某个 Burst **A** 的 Voice SYNC → 对齐超帧；  
2. 用 **B–E 嵌入**（或若还能看见后续 Header 副本）拼出组号/个号与源地址；  
3. 确认色码、时隙、组匹配后开声。

本课只要记住：**错过开头 Header ≠ 这通呼叫对你永久不可见**。如何「确认几次嵌入才算锁定」、与扫描/补充业务如何配合——**第 26 课**展开。

### 4.6 Hangtime vs TxHang（现场高频混淆）

| 概念 | 直觉 | 空口上可能看见 |
|------|------|----------------|
| **Hangtime（呼叫保留）** | EOT 后短暂「本组优先」；别人换组硬上会忙 | BS 继续下发 Terminator with LC / 活动指示 |
| **TxHang（实现用语）** | Hangtime 结束后，发射机载波还可再挂一会儿再关 | 载波还在，但已不再为「刚才那组」强占业务 |
| **Idle / EOC** | 真正空闲，别组可新开呼叫 | Idle 或无业务；CACH 可走 Nul_Msg 等 |

业余中继（如 MMDVM 系）常用 **CallHang / TxHang / ModeHang** 等参数名描述类似层次——名称是实现配置，**语义要对齐「先保留通话、再挂载波、再释放模式」**，不要背成 ETSI 条款号。

### 4.7 范围钉死：Tier II 常规 ≠ Tier III Grant

本课时间线是 **常规（Tier II）语音呼叫**：门牌主要靠 Voice LC Header / 嵌入 / Terminator；可选 CSBK 做唤醒与个呼检查。

**不是**本课主线：

- Tier III 控制信道上的 **Grant / Aloha / 登记**（阶段 E，约第 31–34 课）；  
- 集群里「语音可以不带前面的 LC Header、门牌改由控制信令告知」的变体（第 17 课已提过指针）。

看见「Grant」字样时，先问自己：**这是集群控制信道故事，还是常规中继 Header 故事？** 两套别混。

### 4.8 Service Options / OVCM / Broadcast（门牌上的「贴纸」）

Full LC 里常有 **Service Options（8 bit）**（资料库 Table 7.11）：Emergency / Privacy / **Broadcast（仅组呼）** / **OVCM** / Priority…  
岗位顺序：先认 **FLCO（组还是个）** → 再读 Service Options → 最后读地址数字。细节字段表回资料库 §6，不在本课背满。

---

## 5. 对照表：先前各课 → 本课时间线角色

| 时间线位置 | 空口形态 | 你用哪一课的眼镜看 |
|------------|----------|-------------------|
| 可选唤醒 | CSBK `BS_Dwn_Act` | 第 23 |
| 可选个呼检查 | CSBK `UU_V_Req` / `UU_Ans_Rsp` / `NACK` | 第 23 |
| 可选前导 | CSBK `Pre_CSBK` | 第 23 |
| BOT/BOC 门牌 | Voice LC Header，DT=`0001`，Full LC | 第 21 Data Type + 第 22 Full LC |
| 语音列车 | 超帧 A–F，A=Voice SYNC，B–E 嵌入 | 第 17 + 第 21 EMB |
| 门牌碎片保护 | 嵌入 CS5 + 变长 BPTC；头/终止 RS24+BPTC | 第 24（原则）+ 第 22 |
| 色码 / 同频 | CC 在 SLOT/EMB | 第 20–21 |
| EOT 下车 | Terminator with LC，DT=`0010` | 第 21–22；资料库 §8 |
| Hangtime 留灯 | BS 侧 Terminator with LC 等 | 本课 §4.6；资料库 §8 |
| 缝里活动广播 | CACH Short LC `Act_Updt` | 第 18 + 第 22 Short LC |
| EOC / 空闲 | Idle 等 | 第 23/24 提过 Idle 无 CRC 等原则 |
| 寻址是组还是个 | FLCO `000000` / `000011` | 第 7 + 第 14 + 资料库 §1.1 |

---

## 6. 现场岗位对照

| 现场现象 | 时间线解释 | 先查什么 |
|----------|------------|----------|
| 晚半拍才按进组，开头几秒听不见 | 错过 Header；在等下一列 Burst **A** + 嵌入拼门牌（late entry） | 组号/时隙/色码是否本就错；再看是否弱场导致嵌入拼失败 |
| 「没人说话了」却占着组，换组呼不进去 | **Hangtime** 保留；礼貌接入下别组会忙 | 是否同组回传；中继 CallHang/Hangtime 配置；终端礼貌/不礼貌 |
| 同组有人能回、异组一直忙 | Hangtime 按「当前通话/组」保留（时隙独立） | 别把 TS1 的保留当成整机坏了 |
| 终端设「不礼貌」才能强上 | 部分机型对 Hangtime/色码忙检测不友好；或不想等保留 | 培训上优先教**礼貌接入**；强上可能打断正在进行的组 |
| 对端一直开着静噪尾、分析仪偶发无 Terminator | 漏收 Terminator；靠 Hangtime/超时收尾 | 弱场、错 CC、错时隙；不要只骂「对方没松键」 |
| Header CRC/RS 失败，但稍后仍听到声音 | 头没赶上，**嵌入 late entry** 仍可能上车 | 第 22/24 课：头 RS24 vs 嵌入 CS5 是两条路 |
| 以为是组呼，其实是个呼（或相反） | FLCO 看错；或只看了源地址没看目的类型 | 先看 FLCO=`000000` vs `000011`，再看地址场语义 |
| 语音进行中 CACH 里刷 Activity | **Act_Updt**：广播 TS1/TS2 活动类型与哈希地址 | 第 18/22 课；Activity ID 如 Group voice=`1000` 等（资料库 §5.2） |
| 个呼一直失败，空口只有 UU_V_Req/NACK | 卡在 OACSU，**还没进 Voice Header** | 被叫是否开机/同系统；Deny/NACK 原因；别在语音超帧里找 |
| 双时隙一个在说话一个空闲 | Tier II 两时隙独立；Hangtime 也按时隙 | 不要用「整机载波还在」判断两个时隙都忙 |

---

## 7. 工作例子（6 则）

### 例子 A · 中继组呼「最常见幸福路径」

```text
MS(主叫) --BS_Dwn_Act?--> BS 唤醒
MS --Voice LC Header(Grp, DT=0001)--> BS --转发 Header--> 组内 MS
MS --A B C D E F-- A B C D E F-- …（语音）-->
MS --Terminator(Grp, DT=0010)--> BS
BS --Hangtime 内继续 Terminator with LC--> 组内
BS --Hangtime/TxHang 结束--> Idle
```

要点：门牌三次形态（Header / 嵌入 / Terminator）；Hangtime 不是故障。

### 例子 B · 直通组呼（无 Hangtime 留灯）

```text
MS1 --Header(Grp)--> MS2
MS1 --超帧 A–F…--> MS2
MS1 --Terminator--> MS2（静音）
（无 BS → 通常无「站台留灯」层）
```

### 例子 C · 个呼 OACSU：Proceed 才进语音

```text
MS_A --UU_V_Req--> MS_B
MS_B --UU_Ans_Rsp(Proceed)--> MS_A
MS_A --Header(UU_V_Ch_Usr)--> …
MS_A --超帧…--> Terminator
```

若 `Deny` 或 `NACK_Rsp`：时间线在 CSBK 段结束，**不会出现** Voice LC Header(UU)。

### 例子 D · 迟后进入：错过 Header，仍从超帧中途上车

```text
时间线真实存在：
  [Header] A B C D E F  A B C D E F  A B C D E F  [Term]

你开机太晚，只赶上：
                 ↑从这里听
                 A B C D E F …
  1) 锁定 Voice SYNC@A
  2) B–E 拼出 Grp/Src
  3) 组匹配 → 开声（细节确认策略 → 第 26 课）
```

### 例子 E · Hangtime 挡别组（礼貌 vs 不礼貌）

```text
t0  组9 通话结束，EOT Terminator
t0–tH  Hangtime：组9 同组可礼貌回传；组10 礼貌接入 → 忙
tH  Hangtime 结束
tH–tX  （实现）TxHang：载波或仍开，但业务保留已放
tX  Idle：组10 可新开
```

口语：「等中继掉载波才能说话」——有时是 TxHang/Idle 等待，有时是终端对 Hangtime 处理不友好。

### 例子 F · Header 校验失败，但嵌入救场

```text
[Header RS/BPTC 挂了] → 你没锁定门牌
        A B C D E F → 嵌入 CS5 通过 → 拼出组9
        A B C D E F → 再确认一次（实现策略各异）
        → 开声
[Terminator] → 正常下车
```

对照第 24 课：这是「保护链不同层」，不是「天线一会儿好一会儿坏」的唯一解释。

---

## 8. 数字账本

| 数字 / 编码 | 含义 | 别记成 |
|-------------|------|--------|
| **30 ms** | 一时隙一突发时长 | ≠ 一列超帧 |
| **60 ms** | 一个 TDMA frame（TS1+TS2） | ≠ 超帧 |
| **360 ms** | 一列语音超帧 A–F | ≠ Hangtime 默认值 |
| **264 bit** | 一突发 | ≠ Full LC 72 |
| **Data Type `0001`** | Voice LC Header | ≠ Terminator |
| **Data Type `0010`** | Terminator with LC | ≠ Idle；≠ CSBK |
| **FLCO `000000`** | Grp_V_Ch_Usr 组呼门牌 | ≠ CSBKO |
| **FLCO `000011`** | UU_V_Ch_Usr 个呼门牌 | ≠ SLCO |
| **CSBKO `111000`** | BS_Dwn_Act | ≠ Header |
| **CSBKO `000100` / `000101`** | UU_V_Req / UU_Ans_Rsp | ≠ 已在语音 |
| **CSBKO `100110`** | NACK_Rsp | ≠ Terminator |
| **CSBKO `111101`** | Pre_CSBK | ≠ Full LC |
| **SLCO `0001`** | Act_Updt（CACH） | ≠ FLCO |
| **Answer Proceed / Deny** | `00100000` / `00100001` | 见资料库 §6.2 |
| **Activity ID `1000` / `1001`** | Group / Individual voice（Act_Updt） | 见资料库 §5.2 |

Hangtime / TxHang 的**具体秒数**是系统/中继配置，不是本课背诵表；岗位记层次，不记「全球统一 3 秒」。

---

## 9. 常见误区（10 则）

1. **「按住 PTT = 立刻语音突发，没有 Header。」**  
   → 常规语音常见先（或伴随）**Voice LC Header** 再进超帧；分析仪上先认 Data Type。

2. **「Terminator 可有可无，反正松键就结束。」**  
   → 规范路径用 Terminator with LC 宣告 EOT；漏收时靠 Hangtime/超时收尾，现象会「拖尾」。

3. **「Hangtime 是中继坏了、载波卡死。」**  
   → 多数是**正常保留**，方便同组回一句；先分 Hangtime vs TxHang vs 真故障。

4. **「迟后进入靠每个 30 ms 重传完整门牌大海报。」**  
   → 靠 **A 的 Voice SYNC + B–E 嵌入拼装**；不是每突发整包 Header。

5. **「Header CRC 失败 = 这通呼叫彻底没了。」**  
   → 嵌入路径仍可能 late entry；分层看（第 22/24 课）。

6. **「组呼和个呼只是地址数字不同，FLCO 无所谓。」**  
   → **FLCO 先分流**（`000000` vs `000011`），地址场语义才跟着变。

7. **「看见 CSBK 就一定是集群 Grant。」**  
   → Tier II 也有唤醒/个呼检查/前导/NACK 等 CSBK；**Grant 叙事留给阶段 E**。

8. **「Voice LC Header 中间也是 Voice SYNC。」**  
   → Header 是**数据壳**，中心是 **Data SYNC** + Slot Type；Voice SYNC 在超帧 **A**。

9. **「Short LC（CACH）就是通话门牌的缩小版。」**  
   → Short LC 是另一套 PDU（第 22 课）；`Act_Updt` 广播活动，不替代 Full LC。

10. **「数据终止 TD_LC（FLCO=110000）就是语音 Terminator。」**  
    → 语音结束是 **Terminator with LC**（Data Type=`0010` + Voice Channel User LC）；TD_LC 属 Part 3 数据挂起。

---

## 10. 自测（8 题）

**题 1.** 用一句话写出「一次语音呼叫」的时间线口诀（含可选 CSBK、Header、超帧、Terminator、Hangtime、Idle）。

<details><summary>参考答案</summary>

一次语音呼叫 =（可选）唤醒/个呼检查 CSBK → Voice LC Header（门牌）→ 超帧 A–F 语音+嵌入 LC（迟到也能上车）→ Terminator with LC（下车）→（中继）Hangtime 保留 → Idle。

</details>

**题 2.** Voice LC Header 与 Terminator with LC 的 Data Type 各是多少？它们通常是否携带同一类 Full LC？

<details><summary>参考答案</summary>

Header = `0001`，Terminator = `0010`。通常携带**同一类** Voice Channel User Full LC（同 FLCO/地址），分别承担发车与下车。

</details>

**题 3.** 组呼与个呼的 FLCO 各是什么别名？

<details><summary>参考答案</summary>

组呼：`000000` = Grp_V_Ch_Usr；个呼：`000011` = UU_V_Ch_Usr。

</details>

**题 4.** BOT/BOC/EOT/EOC 四个缩写各指哪一层边界？为什么「松 PTT」更接近 EOT 而不是 EOC？

<details><summary>参考答案</summary>

BOT=一次发射开始；BOC=整次呼叫开始；EOT=一次发射结束；EOC=整次呼叫结束。松 PTT 结束的是**本段发射**（EOT，常见 Terminator）；中继 Hangtime 过后才更接近 EOC/放空。

</details>

**题 5.** 用户中途开机，错过了 Header，为何仍可能听到后半段组呼？指出两个关键空口元素。

<details><summary>参考答案</summary>

迟后进入：① 超帧 Burst **A** 的 **Voice SYNC** 对齐；② **B–E 嵌入 Full LC**（或后续能拼出的地址 LC）识别组/源。细策略见第 26 课。

</details>

**题 6.** Hangtime 与 TxHang 在岗位上如何一句话区分？

<details><summary>参考答案</summary>

Hangtime：EOT 后**业务/组保留**（同组优先、异组常忙）；TxHang：保留结束后**载波还可再挂多久才关**（常见实现参数名）。先保留、再挂载波、再 Idle。

</details>

**题 7.** 空口上只看到 `UU_V_Req` 和 `NACK_Rsp`，没有 Voice LC Header——通话进入语音段了吗？

<details><summary>参考答案</summary>

没有。仍停在个呼检查/拒绝手续段；进入语音段的标志是 **Voice LC Header（UU_V_Ch_Usr）** 及后续超帧。

</details>

**题 8.** 为什么本课反复强调「不要把 Tier III Grant 当成这条时间线」？

<details><summary>参考答案</summary>

本课是 **Tier II 常规**叙事：门牌靠 Header/嵌入/Terminator，可选 CSBK 做唤醒与个呼检查。Tier III 用控制信道 **Grant** 等另一套状态机（阶段 E），混谈会把「门牌从哪来」讲错。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `02-语音业务/语音业务字段速览.md` **§2** | **本课 canonical 过程表**：阶段↔Data Type↔PDU↔FLCO/CSBKO |
| 2 | 同上 **§3 / §4 / §6 / §8** | Grp/UU Full LC；CSBK 手续；Service Options；Terminator 要点 |
| 3 | `学习推送/第17课.md` | 超帧 A–F、Voice SYNC、late entry 上车点 |
| 4 | `学习推送/第21课.md` | Data Type `0001`/`0010`；EMB/SLOT |
| 5 | `学习推送/第22课.md` | Full LC 三处运载；与 Short LC 边界 |
| 6 | `学习推送/第23课.md` | BS_Dwn_Act / UU_V_* / NACK / Pre_CSBK |
| 7 | `学习推送/第24课.md` | 头/终止 vs 嵌入的保护链原则（不背矩阵） |
| 8 | `01-空中接口/CSBK与LC字段详表.md` | 外壳与 Opcode 详表 |
| 9 | 官方 **TS 102 361-2 V2.5.1** clause **5.2** 等（库内 PDF：`02-语音业务/TS102361-2_V2.5.1.pdf`） | 组呼/个呼过程原文 |
| 10 | 官方 **TS 102 361-1 V2.7.1**（Data Type、late entry 指针 **5.1.2**、超帧图） | 空口壳与超帧 |
| 11 | **TR 102 398** | 系统设计导读，**不是**替代 TS |
| 12 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「听不见」一律怪调制 |

官方版本锚点：**Part2 V2.5.1**（语音业务过程/字段）、**Part1 V2.7.1**（空口/Data Type/超帧）。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。FEC 矩阵、Idle 比特、符号表：**永远回 PDF**，本课不补第二份。

---

## 12. 下一课预告

**第 26 课 · 补充业务（迟后进入等）**

本课只把「一次语音呼叫」串成时间线，并为 **late entry** 开了一扇窗。下一课进入补充业务与迟后进入细讲：嵌入确认直觉、Talking Party / Talker Alias、紧急与优先级在过程中的位置、Broadcast/OVCM 等如何落在字段上——仍少 SDL、多现场对照。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-30**（晚间推送）检索核验；真实打开过内容页/PDF/Wiki（HTTP 200 或协会镜像可用）；**不编造地址**。策略 = **Part1/Part2 协会镜像 + TR 导读 + GopherTrunk 门牌/迟入/双时隙文 + MMDVM Hangtime 实现直觉 + Wavecom/hamgear 帧回顾 + 一条可选入门视频（诚实标明非呼叫时间线专题）**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：Data Type、超帧、late entry 指针（如 **5.1.2**）、SYNC/嵌入总框架——给本课「壳」与「上车点」钉原文。  
   - **适合哪一段**：第 2、4.4、4.5、8、11 节。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TS 102 361-2 V2.5.1｜Voice services（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：clause **5.2** 组呼/个呼过程、Voice Channel User LC、Terminator/Hangtime 叙述、Service Options——本课业务时间线的硬出处。  
   - **库内副本**：`dmr/02-语音业务/TS102361-2_V2.5.1.pdf`。  
   - **适合哪一段**：第 2、4、6、8、11 节。  
   - **注意**：部分网络对 etsi.org 直链可能 403，以协会镜像或库内 PDF 为准。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读，帮助把「呼叫过程」放回整网叙事。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

4. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
   - **为什么值得看**：清楚写出门牌三条运载（Header / Terminator / 嵌入）与 late entry「为何能半路上车」——与本课口诀、例子 D/F 同向。  
   - **适合哪一段**：第 4.3、4.5、7 节。  
   - **注意**：文中实现确认次数等是工程策略，**不以博客条款号替代 ETSI**。  
   - **基础**：中级～进阶；英文网页。

5. **[GopherTrunk｜Operator Cookbook Part 3：Conventional DMR Two Slots](https://gophertrunk.org/blog/tutorials/operator-cookbook-03-conventional-dmr-two-slots/)**  
   - **为什么值得看**：Tier II 双时隙两路通话、Terminator 按目的释放、hangtime 作为收尾后门——帮你建立「时隙独立 + EOT/EOC」现场感。  
   - **适合哪一段**：第 2.4、4.6、6 节。  
   - **基础**：中级；英文网页。

6. **[N4IRS Wiki｜MMDVMHost timers（CallHang / TxHang）](https://github.com/N4IRS/MMDVM-Install/wiki/MMDVMHost-timers)**  
   - **为什么值得看**：用实现语言讲清「通话 Hangtime 保留同组、TxHang 再挂载波」——正好对照本课 §4.6 与例子 E（**不是** ETSI 条文）。  
   - **适合哪一段**：第 4.6、6、9 节。  
   - **基础**：入门～中级；英文 Wiki。

7. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - 帧/突发/超帧图，把 Header→语音→Terminator 钉回 264 结构。厂商综述可能偏早；**硬条款以现行 Part1/2 为准**。

8. **[Alessandro Guido｜How DMR Works — primer PDF（hamgear）](https://hamgear.files.wordpress.com/2014/02/dmr-primer.pdf)**  
   - 培训幻灯式回顾呼叫/LC/时隙名称。年代偏早；以 V2.5.1/V2.7.1 与资料库为准。

9. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - Data Type 分支、Header vs 嵌入路径、Tier II/III 同线不同状态机——防止把 Grant 叙事塞进本课。

10. **（可选，非专题）[Scanner School｜What is DMR?（YouTube）](https://www.youtube.com/watch?v=aQX_JbTbXuY)**  
    - **为什么可以看**：对完全没听过 DMR 的同事做 10 分钟热身（时隙/色码/谈组口语）。  
    - **诚实标签**：**不是**「Voice Header → 超帧 → Terminator → Hangtime」呼叫时间线专题；看完必须回到本课 §2 / §4。  
    - **基础**：入门；英语视频。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 语音呼叫时间线：可选 CSBK → Voice LC Header → 超帧 A–F（嵌入 LC）→ Terminator with LC → Hangtime → Idle」** 按课堂深度讲透的独立高质量中文/英文短片（多数入门视频只口播双时隙/写频/产品演示）。本课 **`video_found=false`**（无合适的呼叫过程专题视频）；仅附一条可选入门视频并标明「非专题」。建议用：**语音业务字段速览 §2 + Part2 clause 5.2 + 本课总图 + GopherTrunk Part5（End-to-End / Decoders）** 对照自学。

---

*推送说明：本课为阶段 D「语音呼叫过程直觉」开篇课。频谱/调制仅保留短提醒（过程不换频、不改 4FSK/双时隙），不复述加餐全文。主文加厚覆盖动机、PTT 上下车总图与组/个分叉、术语、组呼/个呼/三份门牌/超帧/迟入开窗/Hangtime/Tier II 范围、第 7/15–24 课映射、现场对照、六则 ASCII 时间线例子、数字账本、十则误区、八题自测、资料库路径与核验外链（诚实标明无呼叫时间线专题视频，仅附可选入门视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle/符号表、不发明条款号、不把 Tier III Grant 冒充主线。读完应能向同事讲清「一次语音呼叫怎么上下车、Header/嵌入/Terminator 为何是同一门牌三形态、Hangtime 为何不是坏机」，并进入第 26 课补充业务（迟后进入等）。*
