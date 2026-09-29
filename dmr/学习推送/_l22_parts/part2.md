## 5. 对照表：Full LC vs Short LC vs CSBK vs EMB/SLOT

| 维度 | Full LC | Short LC | CSBK（预告） | EMB / SLOT |
|------|---------|----------|--------------|------------|
| 角色 | 呼叫门牌**正文** | 缝里**短广播** | 控制块**外壳** | **小报头**（运货标签） |
| 表 | Table **9.7** | Table **9.8** | Table **9.9** | Table **9.3 / 9.4** |
| Opcode | **FLCO 6** | **SLCO 4** | **CSBKO 6** | 无（有 PI/LCSS 或 Data Type） |
| 门牌 FID | 有（8） | 无此八位组布局 | 有（8） | 无 |
| 典型长度叙事 | 信息 72；头终止≈96；嵌入+CS | 信息 28+CRC8 | 信息+CRC16≈96 壳 | 16 / 20 |
| 运载 | Header / Terminator / 嵌入 B–E | **仅 CACH** | 数据壳 Data Type=CSBK | 嵌在突发结构里 |
| 校验名 | RS(12,9) 或 5-bit CS | CRC-8 | CRC-CCITT 16 | QR / Golay |
| 和 CC 关系 | 正文不含 CC；CC 在 EMB/SLOT | 不替代 CC | 同左 | **携带 CC** |

分柜口诀：

```text
看见「组地址 / FLCO / 源台号」→ 你在读 Full LC 正文（或拼出来的同一类）
看见「CACH / SLCO / Act_Updt」→ Short LC
看见「CSBKO / LB」→ 下一课 CSBK
看见「CC + LCSS」或「CC + Data Type」→ 还在小报头（EMB/SLOT），没进正文
```

---

## 6. 现场岗位对照

| 现场现象 | 先看什么 | 本课解释 |
|----------|----------|----------|
| 分析仪已解出 **FLCO / 组 / 源** | Full LC 是否完整（Header 或拼装成功） | 门牌正文已在；再查组配、权限、加密选项 |
| 只有 **EMB / LCSS**，地址栏空 | 碎片是否收齐 B–E？校验是否过？ | 小报头在，正文还没拼出来或 CS 失败 |
| 错过 Header 仍进组 | 后续超帧嵌入 LC | **late entry** 设计如此；不是「神秘补包」 |
| 出站缝里刷 **Act_Updt** | CACH Short LC | 活动看板；**不能**当成话务 Full LC |
| 同频同色仍「各说各话」 | **FID/FLCO** 是否标准馆 | 第 14 课：门牌错 ≠ CC 错 |
| 色码不对整网静音 | EMB/SLOT 的 **CC**（第 20/21 课） | 先过色码门，再谈 LC 正文 |
| 语音壳上硬找 Slot Type | — | 语音无 SLOT；Header/Terminator 才是数据壳 |

**分诊三步（建议贴显示器旁）**：

1. **壳对不对？** SYNC / 语音还是数据（第 19 课）。  
2. **色码过没过？** EMB/SLOT 的 CC（第 20–21 课）。  
3. **门牌正文在哪？** Header/Terminator 整包，或 B–E 拼装；缝里另看 Short LC。

---

## 7. 工作例子（5 则）

### 例子 A · 组呼：Header + 嵌入 Full LC

场景：台源 `1001` 向组 `200` 发起标准组呼（数字仅为教学用）。

1. 空口先见 **Voice LC Header**（Data Type 名，SLOT 里 CC+类型）。  
2. 解 Full LC：`PF=0`，`FID=0x00`，`FLCO=000000`（Grp_V_Ch_Usr），Data 含 Service Options + 组 `200` + 源 `1001`。  
3. 进入超帧：A=Voice SYNC；**B–E** 再嵌入**同一类** Full LC 碎片（LCSS 走首→续→末）。  
4. 同组台即使扫描晚到，也可在下一两个超帧拼出门牌（late entry）。

### 例子 B · Terminator with LC

场景：讲话结束。

1. 末语音超帧后出现 **Terminator with LC**（数据壳 + Data SYNC）。  
2. 其中仍可携带与通话相关的 Full LC（便于对端确认「谁的呼叫结束」）。  
3. 现场：别把「有 Data SYNC」只理解成「同步图案变了」——同时要看 Data Type 是否 Terminator、LC 是否仍可读。

### 例子 C · 晚入网：中途插入超帧

场景：同事打开监听时，Header 已过，正落在某超帧的 **C** 突发。

1. 先靠后续 **A** 的 Voice SYNC 对齐超帧相位（第 17 课）。  
2. 收集 **B–E**（可能跨到下一超帧）拼 Full LC；看 EMB.LCSS 是否完整。  
3. 拼出 `FLCO + 组 + 源` 后，才谈得上「该不该打开扬声器」。  
4. 提醒：实现若要求「两次一致」，属于稳健策略；规范语义仍是「嵌入携带地址 LC」。

### 例子 D · CACH Short LC 拼装草图

场景：中继出站空闲/半忙，缝里在刷短信令。

```text
CACH#n:   LCSS=首片  +  Signalling 碎片…
CACH#n+1: LCSS=续片  +  …
CACH#n+k: LCSS=末片  +  …  → 拼出 Short LC
              SLCO | Short LC Data(24) | CRC8
例：SLCO=0000 → Nul_Msg（填空）
    SLCO=0001 → Act_Updt（两槽活动 + hashed 地址）
```

要点：**没有**「一个 CACH 直接等于一条完整 Short LC 且 LCSS=单片 LC」的用法（与 EMB 路径不同）。

### 例子 E · 误读「Short LC = 截短的 Full LC」

同事指着文档说：「Short 就是 Full 去掉地址。」  
你纠正：

- Full：FLCO**6** + FID**8** + Data**56** +（RS24 或 CS5），走 Header/嵌入；  
- Short：SLCO**4** + Data**24** + CRC**8**，走 **CACH**；  
- Opcode 表不同、有无 FID 不同、CRC 不同、缝不同。  

这是本课最高频的嘴瓢——用 §5 对照表打回去。

---

## 8. 数字账本

| 量 | 值 / 关系 | 别和谁混 |
|----|-----------|----------|
| Full LC 信息场 | **72** bit（9 octets 叙事） | ≠ 264 突发；≠ 196 Info |
| Full LC Data | **56** bit（Octet2–8） | 随 FLCO 变 |
| FLCO | **6** bit | ≠ SLCO 4；≠ CSBKO |
| FID | **8** bit | ≠ 地址 24 |
| 头/终止 CRC | **24** bit，RS**(12,9)** | 嵌入不是这条 |
| 嵌入 checksum | **5** bit | B.3.11 |
| 嵌入碎片 | **4 × 32** bit（B–E） | 加 EMB 标签 |
| Short 信息 | SLCO**4** + Data**24** = **28** | + CRC8 → 再进 CACH BPTC |
| Short CRC | **8** bit | ≠ Full 的 24/5 |
| CACH | **24** bit 缝；载荷约 17 | 第 18 课 |
| EMB / SLOT | **16** / **20** | 小报头，非 LC 正文 |
| 超帧 | **360** ms = 6×30 | A SYNC；B–E 嵌 LC |
| 带宽/调制 | 12.5 kHz + 4FSK | LC **不改变**二者 |

分柜口诀：

```text
门牌正文 …… Full LC（72 信息；头终止 RS24 / 嵌入 CS5）
缝里短广播 … Short LC（4+24+8 → CACH）
运货标签 …… EMB 16 / SLOT 20
下一课外壳 … CSBK（LB|PF|CSBKO|FID|64|CRC16）
```

---

## 9. 常见误区（10 则）

1. **「Short LC 就是截短的 Full LC。」** → 否。不同 PDU、不同 Opcode 宽、不同路径。  
2. **「EMB 就是 Link Control。」** → 否。EMB 是小报头；中间 32 才是碎片载荷。  
3. **「有 Voice SYNC 就等于读到了组地址。」** → 否。A 对齐超帧；地址在 Header 或 B–E 拼装。  
4. **「嵌入 LC 和 Header LC 是两种业务。」** → 通常是**同一类 Full LC** 的不同运载；CRC 路径不同。  
5. **「CACH 上可以像 EMB 那样发单片 LC。」** → 否。CACH Short LC 无单片 LC 用法。  
6. **「FLCO 数值拿到 Short LC 当 SLCO 用。」** → 否。两张表。  
7. **「错 FLCO 和错 CC 是一回事。」** → 否。CC 是同频色；FLCO/FID 是门牌服务。  
8. **「FID 就是源地址。」** → 否。FID 8 bit 特性集；地址常见 24 bit。  
9. **「改 LC 会换 12.5 kHz 或 4FSK。」** → 否。  
10. **「分析仪只显示 EMB 就说明没有 LC。」** → 可能只是还没拼完或 CS 失败——先查 B–E 完整性。

---
