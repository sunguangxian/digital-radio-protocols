
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

---
