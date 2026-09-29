
## 5. 对照表：CSBK vs Full LC vs Short LC vs EMB/SLOT

| 维度 | **CSBK** | Full LC | Short LC | EMB / SLOT |
|------|----------|---------|----------|------------|
| 角色 | 控制事务**外壳** | 呼叫门牌**正文** | 缝里**短广播** | **小报头** |
| 表 | Table **9.9** | Table **9.7** | Table **9.8** | Table **9.3 / 9.4** |
| Opcode | **CSBKO 6** | **FLCO 6** | **SLCO 4** | 无（PI/LCSS 或 Data Type） |
| 门牌 FID | 有（8） | 有（8） | 无此八位组布局 | 无 |
| 首八位组差异 | **LB\|PF\|CSBKO** | **PF\|R\|FLCO** | （无 LB/PF/FID 布局） | — |
| 业务数据 | **64** bit | **56** bit | **24** bit | — |
| 校验名 | **CRC-CCITT 16** | RS(12,9) 24 或 5-bit CS | CRC-8 | QR / Golay |
| 运载 | 数据壳 **Data Type=CSBK/MBC** | Header/Terminator/嵌入 B–E | **仅 CACH** | 嵌在突发结构里 |
| 和 CC 关系 | 正文不含 CC；CC 在 SLOT | 同左（嵌入路径 CC 在 EMB） | 不替代 CC | **携带 CC** |

分柜口诀：

```text
看见「CSBKO / LB / Data Type=CSBK」→ 控制事务外壳（本课）
看见「FLCO / 组地址 / 源台号」→ Full LC 门牌正文（第 22 课）
看见「CACH / SLCO / Act_Updt」→ Short LC
看见「CC + Data Type」或「CC + LCSS」→ 还在小报头，没进正文
看见「FLCO 数值拿去当 CSBKO」→ 嘴瓢，打回两张表
```

### 5.1 Opcode 三表对照（再钉一次）

| 名称 | 宽度 | 住在谁里面 | 典型例子（学习摘要） |
|------|------|------------|----------------------|
| **FLCO** | 6 | Full LC | Grp_V_Ch_Usr `000000` |
| **CSBKO** | 6 | CSBK | UU_V_Req `000100`；BS_Dwn_Act `111000` |
| **SLCO** | 4 | Short LC | Act_Updt `0001`；Nul_Msg `0000` |

注意：`000100` 在 FLCO 表里是 **Talker Alias header**，在 CSBKO 表里是 **UU_V_Req**——**同数值、不同表、不同语义**。这是现场最高频的「数字撞车」陷阱之一。

---

## 6. 现场岗位对照

| 现场现象 | 先看什么 | 本课解释 |
|----------|----------|----------|
| 个呼前先闪 **UU_V_Req / Ans** | Data Type 是否 CSBK；CSBKO/FID | 办手续阶段；还不是 Voice LC Header |
| 中继久闲后首包像「控制」 | 是否 BS_Dwn_Act（CSBKO `111000`） | 唤醒出站；别当成组呼门牌 |
| 扫描台漏收短数据/控制 | 是否有 **Pre_CSBK**；CBF 是否合理 | 前导在「敲窗户」；壳对了再查后续块 |
| 对端礼貌拒绝 | NACK_Rsp：Reason / Service Type | 控制面拒绝 ≠ 射频解调失败 |
| 分析仪显示 CSBK 但解不出业务 | FID 是否 SFID？CRC16 是否过？ | 先门牌与校验，再查 CSBKO 表 |
| 在语音超帧里找 CSBK | — | CSBK 走**数据壳**；别在 B–E 嵌入里找 CSBKO |
| 把 CACH Act_Updt 叫成 CSBK | Short LC 的 SLCO | 活动看板 ≠ 控制块外壳 |
| 色码不对整网静音 | SLOT 的 **CC**（第 20–21 课） | 先过色码门，再谈 CSBK 正文 |
| 博客说「只有集群才有 CSBK」 | Part2 常规 CSBKO 表 | Tier III **大量用**外壳；常规**也有**控制 CSBK |

**分诊三步（建议贴显示器旁）**：

1. **壳对不对？** Data SYNC + Slot Type？（第 19/21 课）  
2. **色码与类型？** CC 过了吗？Data Type 是 CSBK 还是 Voice LC Header？  
3. **FID → CSBKO → Data64？** 标准馆吗？是唤醒/请求/应答/前导哪一种？

---

## 7. 工作例子（5 则）

### 例子 A · BS_Dwn_Act：叫醒中继出站

场景：中继入站侧有台要发起业务，出站可能处于省电/未激活（教学叙事）。

1. 空口先见**数据突发**：Data SYNC + SLOT（CC + Data Type=**CSBK**）。  
2. 解 CSBK：`LB=1`，`PF=0`，`FID=0x00`，`CSBKO=111000`（BS_Dwn_Act）。  
3. Data64 直觉（Part2 §4.1）：保留位 + **BS 地址 24** + **源地址 24**（数字教学用即可）。  
4. 之后才可能进入语音门牌（Voice LC Header / 超帧）——**先手续，后门牌**。

### 例子 B · 个呼：UU_V_Req → UU_Ans_Rsp / NACK

场景：源台 `1001` 呼叫个号 `1002`（OACSU 存在性检查精神）。

```text
1001 → UU_V_Req  (CSBKO=000100)  「你在吗？要语音个呼」
1002 → UU_Ans_Rsp (CSBKO=000101)  Proceed / Deny
  或 → NACK_Rsp   (CSBKO=100110)  礼貌拒绝 / 不支持
（通过后）→ Voice LC Header（FLCO=UU_V_Ch_Usr）→ 超帧语音…
```

要点：

- 前半段 Opcode 读 **CSBKO**；后半段门牌读 **FLCO**——**不要混表**。  
- `UU_V_Req` 的 CSBKO=`000100` **不是** Full LC 的 Talker Alias header。  
- Answer Response / Reason Code 细比特 → 资料库 §4.3–4.4，本课记流程骨架。

### 例子 C · Pre_CSBK：给扫描台「敲窗户」

场景：要投递非语音控制/数据，目标台可能在扫描或睡眠。

1. 先发 **Pre_CSBK**（CSBKO=`111101`），`LB=1`（单块前导常见）。  
2. Data 直觉：Data/CSBK 标志、组/个标志、**CBF**（后续块数，**不含**当前 preamble）、目标/源地址。  
3. 现场：若只有业务块、从不发前导，扫描台「偶发漏收」——先查产品是否启用 Pre_CSBK，再查射频。

### 例子 D · LB 与 MBC 草图（不深挖业务体）

```text
单块 CSBK：
  [Data Type=CSBK]  LB=1 | PF | CSBKO | FID | Data64 | CRC16
  → 一页读完

MBC（精神图）：
  [Data Type=MBC Header]       LB=0 | … | （封面，后面还有）
  [Data Type=MBC Continuation] LB=0 | … | （续页）
  [Data Type=MBC Continuation] LB=1 | … | （末页，读完）
```

分诊：看见 **LB=0** 却按「单块 CSBK 业务」强行解释完整故事——会半截读歪。

### 例子 E · 误读「CSBK = 短一点的 LC」

同事说：「CSBK 不就是控制用的 LC 吗？截短版。」  
你纠正：

| | Full LC | CSBK |
|--|---------|------|
| 首字段 | PF\|R\|**FLCO** | **LB**\|PF\|**CSBKO** |
| 数据 | 56 bit | **64** bit |
| CRC | RS24 或 CS5 | **CRC-16** |
| 典型 Data Type | Voice LC Header / Terminator | **CSBK / MBC** |
| 角色 | 话务门牌 | 控制事务 |

再补一句：Short LC 更是第三条路（CACH），更不是 CSBK。

---
