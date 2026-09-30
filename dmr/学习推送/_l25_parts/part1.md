（第25课 · 推送 part 1/3）

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

