# 第 17 课 · 语音超帧 A–F

> DMR 深入学习 · **阶段 C 空口深入第 3 课**  
> 适合：已吃透第 15 课「时隙 30 ms / TDMA frame 60 ms」与第 16 课「突发 264 = 108+48+108」，但听到「超帧」「Burst A」「迟后进入」仍像三件无关事的人  
> 阅读量：约 **30–40 分钟** · 几乎不推公式 · 要把「**同一逻辑信道上连续 6 个业务突发 A–F = 360 ms；A 中心 Voice SYNC；B–E 典型拼一条 Full LC；语音 SYNC 机会约每 360 ms 一次**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**，符号率约 **4800 baud**，总比特率约 **9.6 kbps**。超帧并不另开频点，也不改调制——它只是在**时间轴**上把 6 个 30 ms 绿灯货箱排成一列火车。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是**语音列车的车厢分工**。

---

## 1. 为什么本课重要（动机）

第 15 课站住了时间车道：绿灯 30 ms、一对时隙拼成 60 ms 的 TDMA frame。  
第 16 课站住了货箱：每次绿灯里扔出 **264 bit = 108+48+108**，中间 48 要么是 SYNC，要么是嵌入。

同事接下来会问更「贴空口」的问题：

- 抓包 / 协议分析仪：一串语音突发刷过去，为什么**有的中间是 Voice SYNC，有的中间是 EMB+碎片**？  
- 用户中途开机、拧到正确组与时隙：为什么先安静半拍，然后突然进会？这就是 **Late Entry（迟后进入）**——靠 Burst **A** 的 Voice SYNC「跳上火车」，再靠 B–E 嵌入拼出「这通是谁呼谁」。  
- 排障口语：「同步不上」「有载波、无地址」「半路切入才有组号」——这些话最终都落在**超帧节奏**上，而不是落在「每个 30 ms 都贴完整门牌」的幻想上。  
- 培训台上：若只背「语音有超帧」五个字，后面会卡在同一处：

> **超帧不是第三种物理货箱。它是同一逻辑信道上、连续六节语音货箱的编组：A 挂车头灯（Voice SYNC），B–E 常递嵌入单据拼 Full LC，F 按方向可能是 Null / RC / Privacy 等；整列火车长 360 ms。**

本课目标是让你能自己讲清十件事：

1. **为什么**要用「六节车厢火车」记 A–F = 360 ms；  
2. 一张总图：…F | **A B C D E F** | A…，以及和 30 ms / 60 ms / 264 bit 的接口；  
3. 白话术语：Voice superframe、Burst A–F、Voice SYNC、嵌入信令、EMB、LCSS、Full LC、Late Entry、Terminator；  
4. 中心场分工：A = SYNC；B–E 典型拼一条 Full LC；F 常见用途脸熟；  
5. 现场岗位：分析仪认 A vs B–F、有声无地址、迟后进入静音再进会；  
6. 完整例子：Voice LC Header（可选 PI）→ 超帧 A…F → Terminator with LC；  
7. 数字账本：6×30=360、SYNC 疏密、4 碎片拼 LC、与入/出站最坏等待；  
8. 常见误区 + 自测；  
9. 资料库加深路径；  
10. 核验过的外链（Part1 超帧原文 + 协会嵌入图 + 解码 EMB/FLC 文 + 中文科普）。

---

## 2. 总图 / 故事：六节车厢的语音火车

先把整课装进一个故事，再落到 Part1 clause **5.1.2.1** figure 5.3 与资料库 `01-空中接口/帧结构与字段定义.md` **§4**。精神与 `00-入门/DMR术语与帧结构速查卡.md`「语音超帧」表一致。

### 2.1 火车长什么样

同一**逻辑信道**（例如中继 Slot1 这一路）上，语音不是「随便扔突发」，而是按固定编组前进：

```text
时间 →（同一逻辑信道，示意）

… | F | A | B | C | D | E | F | A | B | …
          └──────── Voice superframe = 360 ms ────────┘

每个字母 = 一个 Traffic burst
  · 时隙绿灯：30 ms
  · 货箱内容：264 bit ≈ 27.5 ms（108 + 48 + 108）
  · 六节连拍：6 × 30 ms = 360 ms
```

口诀：

- **一节车厢** = 第 16 课的 264 bit 货箱；  
- **一列火车** = 连续六节 **A–F**；  
- **车长** = **360 ms**；  
- **只用于语音**——数据/控制突发**没有**超帧编组（Part1 定义：superframe 仅语音业务）。

### 2.2 谁当车头灯？谁递调度单？

规范把六节的**中心 48 bit**分工写死了大方向（figure 5.3 + clause 7.1.3）：

```text
Burst A : 中心 = Voice SYNC
          · 超帧边界标志
          · 迟后进入的「上车点」
          · 左右仍是 216 bit 语音载荷（约 60 ms 压缩话）

Burst B–E: 中心 = 嵌入信令（EMB + 碎片）
          · 典型：四个嵌入场拼完一条 Full LC（72 bit LC + FEC → BPTC 分片）
          · 左右继续流语音

Burst F : 中心仍多为嵌入类窗口
          · 出站：可为 RC / Privacy / Null 等（按场景）
          · 入站：常为 Null 嵌入
          · 本课先脸熟「F 不一定继续拼同一条 Full LC」
```

可以想成：

| 车厢 | 中间驾驶舱在干什么 | 两侧货仓 |
|------|--------------------|----------|
| **A** | 贴 **Voice SYNC** 大标签（车头灯） | 压缩语音 |
| **B–E** | 递嵌入碎片（多帧拼门牌） | 压缩语音 |
| **F** | 嵌入窗口，用途随方向/特性变化 | 压缩语音 |

### 2.3 和第 15、16 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 15 | 时隙 30 ms、frame 60 ms、Guard/CACH 缝 |
| 第 16 | 264 = 108+48+108；语音壳 vs 数据壳；中间可 SYNC 可嵌入 |
| **本课** | 六个语音壳排成 A–F；A 必 Voice SYNC；B–E 拼 Full LC；SYNC ≈ 每 360 ms |

三句话串起来：

1. **车道**是 30 ms（第 15）；  
2. **货箱**是 264 bit（第 16）；  
3. **编组**是 A–F 六箱一列（本课）。

别把三者合成一个词：「超帧」≠「TDMA frame」≠「burst」。

### 2.4 为什么语音 SYNC 不能每 30 ms 贴一次？

接收机当然喜欢更密的 SYNC，但语音载荷要占满两侧 216 bit。规范的折中是：

- **每个超帧开头（Burst A）**贴一次 Voice SYNC → 标边界 + 给迟后进入；  
- **其余语音突发**把中心 48 让给嵌入，继续带地址/业务信息，同时左右继续哼歌。

于是现场直觉成立：

> 语音通话里，**Voice SYNC 机会大约每逻辑信道 360 ms 一次**，不是每 30 ms 一次。

数据/控制突发则不同：它们**没有**超帧，中心常常可以是 Data SYNC——所以入站数据 SYNC 可密到约每 **60 ms**；出站因双时隙可见，数据 SYNC 甚至可密到约每 **30 ms**（Part1 clause **4.3**）。本课主线是语音；疏密对照表见第 6 节账本。

### 2.5 调制账本钩子（巩固弱项，不重开加餐）

加餐四句话在本课落成「时间复用」一句：

1. **频率**：载波仍停在写频的那个 MHz；超帧不换频。  
2. **带宽**：地皮仍约 **12.5 kHz**；六节火车共用同一条地皮。  
3. **调制**：每节车厢仍是 **4FSK** 卸下的 264 bit。  
4. **解调**：先对齐时隙与突发，再认中心是 Voice SYNC 还是嵌入——超帧计数器（A…F）通常在认出 Voice SYNC 时归零到 A。

口算复习：264 bit / 0.0275 s ≈ **9600 bit/s**（用内容窗，不用 30 ms）。超帧只是把六个这样的货箱排成列，不改变单箱比特率。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **Voice superframe（语音超帧）** | 同一逻辑信道上连续 **6** 个业务突发，标号 **A–F**，长 **360 ms** | ≠ TDMA frame（60 ms）；≠ 单突发 |
| **Burst A–F** | 超帧内六节的名字；A 开头，F 收尾 | 不是「六个时隙编号」；时隙仍是 1/2 |
| **Voice SYNC** | Burst **A** 中心的 48 bit 语音同步图案 | ≠ Data SYNC；≠ Colour Code；≠ Talkgroup |
| **嵌入信令** | B–F 中心不用 Voice SYNC 时，改塞 EMB+信令碎片 | 第 21–22 课再拆字段位 |
| **EMB** | 嵌入窗口两侧的小头（共 16 bit 信息+校验叙事），夹 32 bit 碎片 | 别把整个 48 bit 都叫 EMB |
| **LCSS** | EMB 里的「分片起止」指示，帮接收机拼碎片顺序 | ≠ FLCO |
| **Full LC** | 完整链路控制：谁呼谁、FLCO、FID、业务选项等 | 可走 Voice LC Header，也可走嵌入拼装 |
| **Voice LC Header** | 通话开头常见的**数据壳**突发，先报门牌 | 中心是 **Data SYNC**，不是 Voice SYNC |
| **PI Header** | 可选的隐私指示头；常规系统里常跟在 Voice LC Header 后 | 细节非本课主线 |
| **Terminator with LC** | 语音尾常见的数据壳收尾，宣告散会并可再带 LC | 中心是 **Data SYNC** |
| **Late Entry（迟后进入）** | 通话已开始后半路加入：抓 A 的 Voice SYNC + 拼嵌入/头中的地址 LC | ≠ 「永远没听见」 |
| **Logical channel** | 你正在跟的那一路时隙业务（如 Slot1） | 另一路 Slot2 可有自己的超帧相位 |
| **Colour Code** | 同频系统区分用色码；可出现在嵌入/数据相关场 | 不是超帧字母 |

---

## 4. 现场对照：这些节奏落在岗位上

### 4.1 协议分析仪：先认「A 还是 B–F」

典型认图顺序（直觉版）：

1. 锁定逻辑信道与突发边界（第 15、16 课）。  
2. 看中心 **48**：像不像 **Voice SYNC** 图案？  
   - 像 → 这很可能是 **Burst A**（超帧边界）。  
   - 不像 → 语音壳上更像 **嵌入**；结合前后计数判断 B–F。  
3. 若刚看到数据壳 + Data Type = Voice LC Header：下一拍常进入超帧 A。  
4. 若看到 Terminator with LC：这一列火车准备到站。

岗位翻译：**先找车头灯（A），再谈拼门牌（B–E）。**

### 4.2 「有声、无地址 / 组号晚半拍才出」

| 现象 | 优先怀疑 | 和本课关系 |
|------|----------|------------|
| 完全无声，RSSI 好 | 错槽、错色码、错组、错频 | 第 15 + 色码课 |
| 有语音能量，控制台迟迟无源/目的 | LC 还在拼：等 B–E 四个碎片，或错过了 Header | 本课嵌入 |
| 中途开机：先静音，约零点几秒后进会 | 迟后进入，在等下一次 Burst **A** | 本课主线 |
| 只显示 CSBK/Idle，无语音壳 | 你在看另一逻辑信道或控制突发 | 第 16 课两种读法 |
| 两端超帧「对不齐」 | 两路语音超帧可错开；出站最坏 SYNC 等待可到约 **330 ms** | 账本 §6 |

### 4.3 迟后进入：半路上车到底在等什么？

用户拧到正确组与时隙时，接收机通常要完成两件事：

1. **对齐超帧**：等到下一次 **Voice SYNC**（Burst A）——「跳上火车」；  
2. **确认门牌**：从嵌入碎片（和/或先前漏掉的 Header）拼出 Full LC——「确认这通是不是我的组/个呼」。

所以听感常常是：

> **略顿一下（最多大约等一个超帧量级的 SYNC），然后突然有声。**  
> 不是「永远听不到」，也不是「每个 30 ms 都能立刻对上完整地址」。

协会材料把 B–E 嵌入的原始动机之一就说成：支持 Late Entry，并带上呼叫类型、源 ID、目的 ID、业务选项等（见本课外链「Feature Evolution」）。

### 4.4 写频 / 监听台 30 秒话术

你可以这样讲，不必报条款号：

> 「打电话时，空口上不是杂乱扔包，而是六包一组往前走。每组第一包中间贴同步大标签，后面几包中间改贴小便签，把『谁呼谁』撕成四片塞进去。你中途开机，要等下一组的大标签才能上车；门牌拼齐之前，机器可能先不给你完整组号。」

### 4.5 双时隙：两列火车可以错开

同一条 12.5 kHz 上：

```text
Slot1:  … A B C D E F A B …     ← 自己的 360 ms 相位
Slot2:  …   A B C D E F A …     ← 可以错开 30 ms
物理：同一 RF，时间上轮流亮绿灯（第 15 课）
```

Part1 指出：出站若两路都在跑语音且超帧错开 30 ms，**Voice SYNC 最坏等待可到约 330 ms**（仍远好于「永远对不上」）。本课先建立「每信道约 360 ms 一次」的肌肉记忆即可。

### 4.6 和岗位文档的词映射

| 你司/项目里可能出现的词 | 映射到本课 |
|--------------------------|------------|
| 超帧 / superframe / SF | **A–F，360 ms**（仅语音） |
| 同步突发 / sync burst | 多指 Burst **A** 中心 Voice SYNC |
| 嵌入 LC / embedded LC | B–E（典型）中心碎片拼 Full LC |
| 迟入 / late entry / 半路进组 | Voice SYNC@A + 地址 LC |
| 语音头 / LC Header | 数据壳 Voice LC Header（通话开头） |
| 语音尾 / Terminator | 数据壳 Terminator with LC |
| 声码帧 / AMBE 帧（厂商口语） | 落在每突发 216 bit 载荷里（非本课算法） |

---

## 5. 完整例子：跟一通组呼从发车到到站

场景：Tier II 中继，某组呼在 **Slot1** 发起。时间数字取常见教学量级；实现细节以 Part1 **5.1.2** / **7.1** 为准。

### 5.1 发车前：数据壳先报门牌（Voice LC Header）

常规系统里，真正进超帧哼歌之前，空口上常先出现**数据/控制形态**突发：

```text
Voice LC Header（数据壳 264 bit）：
  Info 98 | SLOT 10 | Data SYNC 48 | SLOT 10 | Info 98
                 └─ Data Type = Voice LC Header
  196 bit Info（经 FEC）里带着：FLCO、FID、组地址、源地址、业务选项…
```

可选再跟 **PI Header**（隐私相关初始化）。口诀：

> **先贴工卡（Header），再进会议室连续发言（超帧）。**

注意：Header 的中心是 **Data SYNC**，不是 Voice SYNC。有人口误「语音头中间也是 Voice SYNC」——那是把 Header 和 Burst A 搞混了（见误区）。

### 5.2 第一节：Burst A = 车头灯

```text
Burst A（语音壳）：
  Voice 108 | Voice SYNC 48 | Voice 108
              └─ 超帧边界；迟后进入上车点
```

左右 216 bit ≈ 约 60 ms 压缩话。听感：会场开始有人声。

### 5.3 第二～五节：Burst B–E = 四片嵌入拼 Full LC

```text
Burst B（典型）：
  Voice 108 | EMB + 碎片(32) + EMB 共 48 | Voice 108
Burst C、D、E：同结构，碎片用 LCSS 标「首/续/续/末」
```

拼装直觉（不必背矩阵）：

```text
  B 碎片 ─┐
  C 碎片 ─┼─→ 经 BPTC 等 FEC 拼回 → Full LC（72 bit 信息叙事）
  D 碎片 ─┤         └─ 谁呼谁、FLCO、业务选项…
  E 碎片 ─┘
```

现场翻译：

- 语音左右不停；  
- 中间四拍把「门牌」拼齐；  
- 迟后进入若错过 Header，仍可能靠这四拍认出组号。

Full LC 的字段外壳（PF/FLCO/FID/地址…）第 14、22 课已有/将有专篇；本课只要建立：**一条 Full LC ↔ 四个嵌入场（B–E）** 的肌肉记忆。

### 5.4 第六节：Burst F

```text
Burst F（语音壳）：
  Voice 108 | 嵌入窗口 48 | Voice 108
```

资料库摘要（与 Part1 出/入站嵌入规则一致的方向感）：

- **出站**：F 的嵌入位置可承载 RC / Privacy / Null 等（视特性与对端需要）；  
- **入站**：常为 **Null** 嵌入。  

本课要求：知道 **F 仍是超帧的第六节**，但**不要默认 F 还在继续拼同一条 Full LC**。RC 细节以后课再展开。

### 5.5 到站：Terminator with LC

语音尾常跟数据壳：

```text
Terminator with LC：
  数据壳 + Data SYNC + Slot Type（Data Type = Terminator with LC）
  并可再带一次 LC（散会公文）
```

听感：话停了；空口上还可能闪一下控制型突发。规范还强调：数据 SYNC 本身就足以提示「语音段结束」——实现是否深解 LC 由产品决定。

### 5.6 一张时间轴总表（建议能默画）

```text
时间 →

[Voice LC Header] (可选 [PI Header])
        ↓
   ┌────超帧 360 ms────┐
   A(SYNC) B C D E F
   └───────────────────┘
        ↓  （可重复多列超帧）
   A B C D E F
        ↓
[Terminator with LC]
```

| 阶段 | 外壳 | 中心 48 | 你在找什么 |
|------|------|---------|------------|
| Voice LC Header | 数据壳 | Data SYNC | 地址/FLCO（完整门牌） |
| Burst A | 语音壳 | **Voice SYNC** | 超帧边界 / 迟入上车 |
| Burst B–E | 语音壳 | 嵌入碎片 | 拼 Full LC |
| Burst F | 语音壳 | 嵌入（用途可变） | 别误当成第二个 A |
| Terminator | 数据壳 | Data SYNC | 散会 |

### 5.7 集群补充一句（防定势）

Part1 写明：集群场景下语音**可以**不带前面的 LC Header（靠集群控制信令告知源/目的）；常规系统则 Voice LC Header 更「标配」。本课例子按**常规中继组呼**讲；你遇到 Tier III 时，把「门牌从哪来」换成控制信道叙事即可，**超帧 A–F 本身不变**。

---

## 6. 数字账本（建议钉在速查卡旁）

| 项 | 值 | 备注 |
|----|-----|------|
| Timeslot | **30 ms** | 第 15 课 |
| TDMA frame | **60 ms** | 两时隙 |
| Traffic 内容窗 | **≈ 27.5 ms** | 264 bit |
| Traffic 总比特 | **264 = 108+48+108** | 第 16 课 |
| 语音载荷 / 突发 | **216 bit** | ≈ 60 ms 压缩话 |
| **Voice superframe** | **6 × 30 ms = 360 ms** | 仅语音；标号 A–F |
| Burst A 中心 | **Voice SYNC（48）** | 超帧边界；迟入 |
| Burst B–E 中心 | **嵌入（EMB+碎片）** | 典型拼一条 Full LC |
| Full LC 嵌入拼装 | **4** 个嵌入场 | 72 bit LC + FEC → BPTC（Annex B.2.1） |
| 语音 SYNC 机会（每逻辑信道） | 约每 **360 ms** | 在 Burst A |
| 入站数据/控制 SYNC | 可至约每 **60 ms** | 无超帧 |
| 出站数据/控制 SYNC（双时隙可见） | 可至约每 **30 ms** | clause 4.3 |
| 出站语音最坏 SYNC 等待 | 约 **330 ms** | 两路超帧错 30 ms |
| 符号率 / 比特率 | **≈ 4800 baud / 9.6 kbps** | 4FSK；超帧不改 |

口算口诀：

> **三十窗、二六四箱、六箱一列三百六；A 亮灯、B 到 E 拼门牌、SYNC 不按三十贴。**

---

## 7. 常见误区

1. **「超帧 = TDMA frame。」**  
   错。TDMA frame = **60 ms**（两时隙）；超帧 = **360 ms**（六语音突发）。

2. **「超帧 = 六个时隙编号。」**  
   错。时隙仍是 **1/2**；A–F 是**同一逻辑信道上**连续六次业务突发的名字。

3. **「每个语音突发中间都是 Voice SYNC。」**  
   错。通常只有 **Burst A**；B–F 中心多为嵌入。

4. **「Voice LC Header 中间也是 Voice SYNC。」**  
   错。Header 是**数据壳**，中心是 **Data SYNC**；Voice SYNC 在超帧 **A**。

5. **「迟后进入靠每个 30 ms 重新对一次完整地址。」**  
   错。先等 **A** 的 Voice SYNC 上车，再靠嵌入/头拼 LC；所以会有短暂等待。

6. **「B–F 五个突发各自携带完整 Full LC。」**  
   错。典型是 **B–E 四个碎片**拼一条；F 另有用途叙事。

7. **「数据突发也有 A–F 超帧。」**  
   错。Part1 定义：superframe **仅用于语音**；数据/控制无此编组。

8. **「360 ms 是 RF 换频或换带宽的周期。」**  
   错。频率/带宽不变；只是时间轴上的编组长度。

9. **「听到语音就一定已经解出组号。」**  
   错。左右货仓可先出声，门牌可能仍在 B–E 拼装中——「有声无地址」时期存在。

10. **「两时隙共享同一超帧相位。」**  
    错。两逻辑信道的 SYNC/超帧位置**相互独立**；可以错开。

---

## 8. 自测（请先自己答，再展开）

**题 1.** 语音超帧由几个业务突发组成？标号是什么？总时长多少？它是不是 TDMA frame？

<details><summary>简答</summary>

**6** 个，标号 **A–F**，共 **360 ms**。它**不是** TDMA frame（TDMA frame = 60 ms）。

</details>

**题 2.** Burst A 的中心 48 bit 通常是什么？它对迟后进入有何意义？

<details><summary>简答</summary>

通常是 **Voice SYNC**。它标记超帧边界，并作为迟后进入接收机「跳上火车」的同步点。

</details>

**题 3.** 一条 Full LC 典型由超帧里哪几节的嵌入场拼成？大约几个碎片？

<details><summary>简答</summary>

典型由 **Burst B–E** 的嵌入场拼成，共 **4** 个碎片（经 BPTC 等 FEC 回到 Full LC）。

</details>

**题 4.** 同事说：「语音通话时每个 30 ms 都有 Voice SYNC。」请纠正，并给出正确的疏密直觉。

<details><summary>简答</summary>

纠正：Voice SYNC 通常在每个超帧的 **Burst A**，每逻辑信道大约 **360 ms** 一次，不是每 30 ms。B–F 中心多为嵌入。

</details>

**题 5.** 画出（或默写）常规组呼从发车到到站的顺序：Header、超帧、Terminator。并标明谁用 Data SYNC、谁用 Voice SYNC。

<details><summary>简答</summary>

**Voice LC Header**（可选 **PI Header**）→ **A B C D E F**（可多列）→ **Terminator with LC**。  
Header / Terminator：数据壳，中心 **Data SYNC**。  
Burst A：语音壳，中心 **Voice SYNC**。B–F：语音壳，中心多为嵌入。

</details>

**题 6.** 用户中途开机进组，先安静再突然有声。用本课两步解释。

<details><summary>简答</summary>

① 等待下一次 **Burst A 的 Voice SYNC** 对齐超帧（上车）；② 从嵌入碎片（及/或 Header）拼出 **Full LC** 确认地址/组号（认门牌）。拼齐前可能「有载波/有能量但无完整组显示」。

</details>

**题 7.** 出站两路同时语音且超帧错开 30 ms 时，Part1 给出的 Voice SYNC 最坏等待大约多少？这和「每信道 360 ms」如何同时成立？

<details><summary>简答</summary>

最坏约 **330 ms**。因为接收机出站可看两个时隙：两路超帧错开时，最近的一次 Voice SYNC 可能来自另一路，间隔被缩短到约 330 ms；**每一路自己**仍是约每 360 ms 一个 A。

</details>

**题 8.** （巩固调制弱项）超帧 A–F 有没有改用别的调制或劈开 12.5 kHz？264 bit 货箱验算应用 30 ms 还是 ≈27.5 ms 做分母？

<details><summary>简答</summary>

没有改调制，也不劈频；仍是 **12.5 kHz + 4FSK**。验算用 **≈27.5 ms**：264/0.0275≈9600 bit/s。

</details>

---

## 9. 资料库加深

按这个顺序读，避免一上来背 SYNC 比特图案表或 BPTC 矩阵：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `00-入门/DMR术语与帧结构速查卡.md`「语音超帧」 | 墙上三行：A–F、360 ms、SYNC 疏密 |
| 2 | `01-空中接口/帧结构与字段定义.md` **§4** | 超帧总图 + Burst 分工 + SYNC 对照表 |
| 3 | 同上 §3 | 回看 264 / 语音壳 vs 数据壳（接第 16 课） |
| 4 | `02-语音业务/语音业务字段速览.md` §2–3 | 呼叫阶段表；Late entry 一句；Full LC 业务 PDU |
| 5 | `学习推送/第15课.md`、`第16课.md` | 时隙/突发复习 |
| 6 | `01-空中接口/CSBK与LC字段详表.md` | 需要 FLCO/FID 字段名时再查 |
| 7 | 官方 **TS 102 361-1 V2.7.1** clause **5.1.2.1–5.1.2.3**、**4.3**、**7.1.3** | 超帧/发起/终止/嵌入原文；**冲突以 PDF 为准** |
| 8 | **TR 102 398** 对应导读图 | 概念对照，**不是**替代 TS |
| 9 | `学习推送/加餐_频率带宽与调制解调.md` | 若 12.5 kHz / 4FSK 仍糊 |

官方版本锚点：**Part1 V2.7.1**；**TR V1.5.1**。冲突规则：**TS > TR > 手册/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。

---

## 10. 下一课预告

**第 18 课 · CACH 与 Guard**

本课站住了语音列车：A–F = 360 ms，A 亮 Voice SYNC，B–E 拼 Full LC，迟后进入半路上车。下一课回到第 15 课埋下的那条 **≈2.5 ms 缝**：出站缝里的 **CACH（24 bit）** 到底广播什么，入站缝里的 **Guard** 在防什么。仍少公式，多对照「缝不是 264 货箱的一部分」。

---

## 11. 推荐阅读与视频

本课外链为 **2026-09-26** 检索核验；**不编造地址**。策略 = **Part1 超帧原文 + 协会「嵌入支持迟入」图 + 解码文 EMB/B–E→FLC + 厂商帧图 + 中文超帧科普**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：clause **5.1.2.1** figure 5.3 即语音超帧 A–F；**5.1.2.2 / 5.1.2.3** 讲发起与终止；**4.3** 讲 SYNC 疏密与迟后进入动机；**7.1.3** 讲嵌入。硬出处。  
   - **备链**：[ETSI 官网同版本 PDF](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf)（部分网络可能拦截，可用协会镜像）。  
   - **适合哪一段**：第 2、5、6、9 节加深。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：「Embedding Data within Voice」一页直接画出 **A = Voice SYNC、B–E = Embedded、超帧 = 360 ms**，并写明嵌入 initially 用于 **Late Entry**（呼叫类型、源/目的 ID、业务选项）。协会培训口吻，和图与本课总图同向。  
   - **适合哪一段**：第 2.2、4.3、5.3 节后对照。  
   - **注意**：幻灯年代/版本锚点可能早于现行 Part1；**硬条款以 V2.7.1 为准**。  
   - **基础**：入门～中级；英文 PDF。

3. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读用同样的超帧 / SYNC 疏密叙事，比纯条款好读。  
   - **适合哪一段**：第 2.4、6 节。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

4. **[GopherTrunk｜Protocol Decoders Part 5: DMR Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：清楚写出 Full LC 的两条到达路径——Voice LC Header **或** 语音突发 **B–E** 四个 32-bit 碎片经 EMB/BPTC 拼回；正好把本课「门牌怎么来」钉死。  
   - **适合哪一段**：第 5.1–5.3、7、9 节后深挖。  
   - **基础**：中级～进阶；英文长文；实现向，字段以 Part1 为准。

5. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - **为什么值得看**：Fig.7 Voice format 标出语音突发 **A–F**；并有出站 CACH / 入站 Guard 对照，衔接下课。  
   - **适合哪一段**：第 2、4 节；预习第 18 课缝。  
   - **注意**：文中个别「frame/superframe」口误勿盲从；**以 ETSI 定义为准**（超帧 = 6 **bursts**，不是 6 个 TDMA frame）。  
   - **基础**：中级；英文 PDF。

6. **[VK4PK｜DMR Signal Processing Notes](https://lyonscomputer.com.au/MMDVM/DMR-Signal-Processing-Notes/DMR-Signal-Processing-Notes.html)**  
   - **为什么值得看**：把 264 / 108+48+108 / 4FSK / 4800 baud 与时间参数写在一页，方便和超帧时间轴对账。  
   - **适合哪一段**：第 2.5、6 节；巩固调制弱项。  
   - **基础**：入门～中级；英文网页；业余/MMDVM 笔记，**规范数字仍以 ETSI 为准**。

7. **[科讯｜DMR 对讲机数字协议详解](http://www.cqkexun.com/service/problem/hand/292.html)**  
   - **为什么值得看**：中文专节写「语音超帧：6 突发、360 ms、A 含 SYNC、B–F 可嵌嵌入式信令」，适合建立中文第一印象。  
   - **适合哪一段**：第 2–3 节。  
   - **注意**：科普文版本偏旧；文中个别「语音头中间是语音同步码」等表述与现行 Part1 **不符**（Header 应为 Data SYNC）——**冲突以 ETSI TS 为准**。  
   - **基础**：入门；中文。

8. **[Electronics Notes｜How does DMR Mobile Radio Work](https://www.electronics-notes.com/articles/connectivity/private-land-mobile-radio-pmr-lmr/how-does-dmr-mobile-radio-work.php)**  
   - **为什么值得看**：英文通俗总览 TDMA/双时隙与数字对讲直觉，适合当「休息页」回看大图。  
   - **适合哪一段**：读完本课想换口气时。  
   - **基础**：入门；英文网页；不替代 Part1 超帧条款。

**说明（视频）**：公开检索未找到专门把 **「语音超帧 A–F = 360 ms、Burst A = Voice SYNC、B–E 四碎片拼 Full LC、迟后进入两步上车」** 讲透的独立高质量中文/英文短片（多数入门视频只口播「有两个时隙」或厂商产品介绍）。本课**未找到合适公开视频**。建议用：**Part1 figure 5.3 + 协会 Feature Evolution 嵌入图 + GopherTrunk Part5 EMB/FLC 段 + 资料库 §4** 对照自学。

---

*推送说明：本课为阶段 C「语音超帧 A–F」。频谱/调制仅保留短提醒（超帧不换频、不改 4FSK），不复述加餐全文。主文加厚覆盖动机、六车厢总图、术语、现场对照、Header→A–F→Terminator 例子、数字账本、十则误区、八题自测、资料库路径与八条核验外链（并诚实标明未找到合适公开专题视频）。读完应能向同事讲清「A–F 为何是 360 ms、为何 SYNC 不按 30 ms 贴、B–E 如何拼门牌、迟后进入在等什么」，并进入第 18 课 CACH 与 Guard。*
