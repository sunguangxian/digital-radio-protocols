## 6. 完整例子

### 6.1 例子 A · BS 出站语音超帧 A（Voice SYNC）

场景：Tier II 中继，Slot1 出站语音已建立。

```text
Outbound Slot1 · Burst A
  [ Voice 108 | **** BS sourced Voice SYNC (48) **** | Voice 108 ]
  缝：CACH 24（第 18 课）——与中心 SYNC 无关
```

你会在分析仪上看到：

- 中心 = **Voice SYNC**（BS sourced）；  
- 左右 = 语音载荷；  
- 随后 B–E 中心转为嵌入，**不再**每突发都刷 Voice SYNC。

教学点：Voice SYNC 的工作是「标边界 + 帮迟后进入」，不是「每个货箱都盖一次语音章」。

### 6.2 例子 B · 出站数据 CSBK（Data SYNC）

场景：基站发一条控制信令块。

```text
Outbound · CSBK（数据壳）
  [ Info 98 | SlotType 10 | ** BS sourced Data SYNC (48) ** | SlotType 10 | Info 98 ]
```

你会在分析仪上看到：

- 中心 = **Data SYNC**；  
- Slot Type 里读出 Colour Code + Data Type=CSBK；  
- **没有**超帧 A–F 编组。

教学点：同一 264 外壳，中心换成 Data SYNC，读法整本切换到数据壳。

### 6.3 例子 C · MS 入站首突发（必须 SYNC）

场景：手机按 PTT，上行第一次开门。

```text
Inbound 首突发（clause 4.3）
  [ … | ** MS sourced Voice 或 Data SYNC (48) ** | … ][ Guard ≈2.5 ms ]
```

规则：

- **第一枪必须带 SYNC**（Voice 或 Data 取决于你先发语音流还是控制/数据单据）；  
- 缝侧是 **Guard**，不是 CACH；  
- 基站靠这枚 SYNC 完成：发现信号 → 对齐中心 → 分壳。

若首突发中心被噪声打烂：表现常是「按了键中继没反应 / 同步不上」，此时别只怀疑 Talkgroup。

### 6.4 例子 D · DM TS1 vs TS2

场景：两台手台直通，不用中继。

```text
直通 MS-A 使用 TS1 发语音：
  中心匹配 → TDMA DM TS1 Voice

直通另一路（或对端时隙约定）TS2 发数据：
  中心匹配 → TDMA DM TS2 Data
```

教学点：

- DM 有**自己的图案册**，不是把 BS sourced 换个名字；  
- TS1 / TS2 在 SYNC 层就分开——写频/分析仪时隙与图案册要一致；  
- 直通通常**没有**基站 CACH 帮你报站（第 18 课），同步压力更在 Traffic 中心这本字典上。

### 6.5 例子 E · 一通语音的「SYNC 足迹」串烧

```text
时间 →
Data SYNC  : Voice LC Header（门牌单据，数据壳）
Voice SYNC : Superframe A
嵌入       : B C D E
（F 嵌入类窗口，方向相关）
Voice SYNC : 下一超帧 A …
Data SYNC  : Terminator with LC（结束单据，数据壳）
```

背这张足迹图，分析仪就不会再问「语音通话为啥出现 Data SYNC」。

---

## 7. 数字账本

| 数字 | 含义 | 别和谁搞混 |
|------|------|------------|
| **48 bit** | SYNC PDU（或嵌入窗口）长度 | ≠ CACH 24；≠ Slot Type 20 |
| **约 5.0 ms** | 中心 48 场宽（规范图注） | ≠ 缝 2.5 ms |
| **264 bit** | Traffic 货箱总长 | 含中心 48，不是「264 另外再加 SYNC」 |
| **24 bit** | CACH（出站缝） | 不在 264 内 |
| **96 bit** | standalone RC 突发（48 SYNC + 48 窗口） | ≠ Traffic 264 |
| **360 ms** | 语音超帧；语音 SYNC 机会节奏 | 6 × 30 ms |
| **≈60 ms** | 入站数据/控制 SYNC 可达到的密度量级 | 约一个 TDMA frame |
| **≈30 ms** | 出站双时隙可见时数据 SYNC 可达到的密度量级 | 约一个时隙 |
| **≈330 ms** | 出站双语音超帧错开时的语音 SYNC 最坏等待量级 | 资料库「最坏情形」 |
| **4800 baud / 9.6 kbps** | 4FSK 符号率 / 比特率 | SYNC 不另开水管 |
| **12.5 kHz** | RF 带宽 | SYNC 不劈频 |

三兄弟划界（第 16/18 课延续）：

```text
Traffic 264 ── 货箱（中心可放 SYNC 48）
CACH     24 ── 出站缝小广播
RC       96 ── 独立反向信道突发（自带 SYNC 类）
```

---

## 8. 常见误区（10 则）

1. **「SYNC 是一种调制。」** → 否。仍是 4FSK 比特图案。  
2. **「SYNC 就是 Colour Code。」** → 否。CC 在 Slot Type / EMB 等处；SYNC 是中心图案。  
3. **「SYNC 就是 CACH。」** → 否。CACH 在缝里 24 bit；SYNC 在货箱中心 48 bit。  
4. **「每个语音突发中间都是 Voice SYNC。」** → 否。通常 **A** 是 Voice SYNC；**B–F** 多为嵌入。  
5. **「语音呼叫里不该出现 Data SYNC。」** → 否。Header / Terminator 等单据壳常挂 Data SYNC。  
6. **「同步成功 = 色码一定对。」** → 否。壳对上了，CC 仍可能错。  
7. **「同步不上 = 先改 Colour Code。」** → 顺序常反了：先看有没有 SYNC、册是否 BS/MS/DM 用错、射频是否够。  
8. **「入站也可以像出站那样密到每 30 ms 一个语音 SYNC。」** → 语音仍按超帧约 360 ms；密的是**数据** SYNC。  
9. **「直通可以继续用 BS sourced 图案理解。」** → 否。看 **TDMA DM TS1/TS2** 册。  
10. **「把 Table 9.2 hex 背进培训 PPT 就等于会 SYNC。」** → 类别、疏密、首突发、分壳决策更重要；hex 以 PDF 为准，资料库也刻意不全文抄录。

---

## 9. 自测（8 题）

**题 1.** Traffic 突发中心 48 bit 可能是哪两类东西？它和出站缝里的 CACH 是同一段吗？

<details><summary>简答</summary>

中心 48 = **SYNC 图案** 或 **嵌入信令（如 EMB+碎片）**。CACH 是出站 **≈2.5 ms 缝**里的 **24 bit**，**不在** 264 货箱内，不是同一段。

</details>

**题 2.** 接收机如何区分「语音壳」与「数据壳」？互补直觉里正峰 / 负峰分别暗示什么？

<details><summary>简答</summary>

用相关器匹配中心 48 与字典图案。资料库精神：语音与数据**逐符号互补**，单相关器上常表现为语音**正峰**、数据**负峰**（或等价极性叙事）。匹配 Voice 类 → 语音壳；Data 类 → 数据壳。

</details>

**题 3.** 列出至少五类 SYNC 图案名称（不要写 hex）。DM 为什么还要分 TS1 / TS2？

<details><summary>简答</summary>

例如：BS sourced Voice / Data；MS sourced Voice / Data；MS sourced standalone RC；TDMA DM TS1 Voice/Data；TDMA DM TS2 Voice/Data；（另有 Reserved）。DM 分 TS1/TS2 是为了在直通两时隙上用不同图案册区分，避免和中继 BS 册混用。

</details>

**题 4.** 语音 SYNC 大约多密？入站数据、出站数据各可密到什么量级？

<details><summary>简答</summary>

语音约每 **360 ms**（Burst A）。入站数据/控制可至约 **60 ms**；出站因双时隙可见可至约 **30 ms**。

</details>

**题 5.** 两频 BS 入站或单频传输的**首突发**有什么硬规则？为什么？

<details><summary>简答</summary>

**必须带 SYNC**（clause 4.3）。为了让对方发现信号、对齐突发中心、并立刻分清语音壳还是数据壳。

</details>

**题 6.** Voice LC Header 与 Terminator with LC 的中心更常是 Voice SYNC 还是 Data SYNC？Burst A 呢？

<details><summary>简答</summary>

Header / Terminator 更常是 **Data SYNC**（单据壳）。Burst A 是 **Voice SYNC**。

</details>

**题 7.** 同事说「同步不上，把 Colour Code 从 1 改成 2 试试」。你怎样用三问帮他降温？

<details><summary>简答</summary>

三问：① 中心是 SYNC 还是嵌入？② 若是 SYNC，Voice/Data 与 BS/MS/DM 册是否匹配场景？③ 射频与首突发是否干净？——SYNC 失败与 CC 失败不是同一病；先分诊再改写频。

</details>

**题 8.** （巩固调制弱项）SYNC 有没有改用别的调制或劈开 12.5 kHz？48 bit 中心大约对应多少毫秒？能否把 SYNC 和 CACH 的比特率直接加总对外乱讲？

<details><summary>简答</summary>

没有改调制，也不劈频；仍是 **12.5 kHz + 4FSK**。中心约 **5.0 ms**。**不能**把 SYNC（货箱内）和 CACH（缝里另一水管）比特率随便加总当对外口径。

</details>

---

