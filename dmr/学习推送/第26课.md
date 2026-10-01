# 第 26 课 · 补充业务（迟后进入等）

> DMR 深入学习 · **阶段 D 语音与数据第 2 课**（接第 25 课「语音呼叫过程直觉」）  
> 适合：已能背出「可选 CSBK → Voice LC Header → 超帧 A–F → Terminator → Hangtime → Idle」，但仍会把「迟了半句才听到」当成天线坏了、把 Hangtime 和迟后进入搅成一锅、或以为 Talker Alias / GPS 是另开一路模拟副载波的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**补充业务 = 贴在语音主菜上的加料；迟后进入 = Voice SYNC@A 上车 + 嵌入 Full LC 认门牌；别名/GPS/活动广播/唤醒前导是同阶段常一起遇见的相关件**」钉死  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。补充业务与迟后进入**不换频、不改调制、不另开带宽**——它们只是「同一条 264 bit 突发列车」上，**门牌怎么重复贴、别名/位置怎么嵌进车厢、缝里怎么刷活动看板**。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是**补充业务全景 + 迟后进入细讲 + 现场分诊**。

---

## 1. 为什么本课重要（动机）

第 25 课把一次语音呼叫排成了时间线，并为 **late entry（迟后进入）** 开了一扇窗：错过开头 Header ≠ 这通呼叫对你永久不可见。  
同事在机房还会再问四句要命的话：

- 扫描晚到、中途开机、拧到正确组：为什么**先静半拍再进会**？这是射频坏了，还是协议故意留的「半路上车」？  
- 分析仪上明明看见语音突发，终端却不开声——是错过了 Header，还是**嵌入拼不出门牌**、色码/组号不匹配？  
- 屏幕上突然出现主叫名字、地图上飘出位置点——那是「另一路模拟音」吗？还是**嵌在同一趟语音超帧里**的加料？  
- 培训台上若把「补充业务」背成「第三种能单独拨打的电话」，后面会卡在同一处：

> **补充业务（Supplementary）= 依附在语音（或相关过程）上的加料，不是第三道主菜。本课主线迟后进入 = 抓 Burst A 的 Voice SYNC 对齐超帧 + 用 B–E 嵌入（或仍可见的头）拼出地址 Full LC + 色码/组（或个号）匹配后开声。门牌不会只在开头贴一次——这正是迟到还能上车的原因。**

本课目标：能讲清补充业务 vs 基本语音呼叫；画出迟后进入两步上车；对照 Talker Alias / GPS / Act_Updt / BS_Dwn_Act / Pre_CSBK 各自坐哪节车厢；分清 Hangtime 与 late entry；做现场分诊与自测；并为第 27 课 PDP 留好「语音加料讲完，下一站数据主菜」的接口。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不 dump Idle 96-bit、不贴 Annex E 符号表、不发明 ETSI 条款号（只用资料库与前课已出现的锚点，如 Part 1 **5.1.2**、Part 2 clause **5.2** / Table **7.x**）、不把 Tier III Grant「控制信道周期性重播」冒充本课主线的迟后进入（可提边界：集群里还有另一套「grant update」故事，阶段 E 再讲）。

---

## 2. 总图 / 故事：主菜上的加料，半路上车

先把整课装进两个故事，再落到资料库 `02-语音业务/语音业务字段速览.md` **§2 / §7**、第 13 课业务全景、第 17 课超帧上车点。

### 2.1 一句话故事：餐厅主菜 + 加料贴纸

回想第 13 课的餐厅比喻：

1. **主菜** = 基本语音呼叫（组呼 / 个呼 Tele-service）——第 25 课那条时间线；  
2. **加料** = 补充业务 / 语音伴随能力——迟后进入、主叫别名、嵌入 GPS、紧急/优先级贴纸、广播位等；  
3. **跑堂喊话** = 可选 CSBK（唤醒 BS、个呼先敲门、扫描前导）与 CACH 缝里的 **Act_Updt**（「哪一槽在忙」小广播）。

口诀：**先有主菜（Header→超帧→Terminator），再谈加料；加料多数骑在同一趟语音车上，不是另开一家店。**

### 2.2 迟后进入总图：两步上车

```text
  时间 →

  [Voice LC Header]  A B C D E F  A B C D E F  A B C D E F  [Terminator] …
       ↑门牌整包           ↑每列超帧重复贴门牌碎片（B–E）

  你太晚开机，只赶上这里 →        ↑
                                  │
                     ┌────────────┴────────────┐
                     │ 步骤 1：上车点            │
                     │  等到下一个 Burst A       │
                     │  认到 Voice SYNC          │
                     │  → 对齐超帧相位           │
                     └────────────┬────────────┘
                                  ▼
                     ┌────────────────────────┐
                     │ 步骤 2：认门牌            │
                     │  B–E 拼回 Full LC         │
                     │  （组/个 FLCO + 地址 +     │
                     │   Service Options…）      │
                     │  + Colour Code / 时隙匹配 │
                     └────────────┬────────────┘
                                  ▼
                           开声（或继续静音：
                           组不对 / CC 不对 /
                           嵌入拼失败）
```

对比「从头听完整呼叫」：

```text
  准时上车：Header 一眼看清门牌 → 超帧直接听
  半路上车：错过 Header → 等 A 的 Voice SYNC → 拼嵌入 → 再开声
            （听感：略顿半拍～约一个超帧量级，不是永远听不见）
```

### 2.3 和第 13 / 17 / 18 / 22–25 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 13 | Bearer / Tele-service / Supplementary 三层；补充是加料 |
| 第 17 | A–F=360 ms；A=Voice SYNC 上车点；B–E 拼门牌 |
| 第 18 | CACH；出站缝可刷 Act_Updt |
| 第 22 | Full LC 三处运载；Short LC ≠ Full LC；late entry 证明嵌入不是装饰 |
| 第 23 | BS_Dwn_Act / Pre_CSBK / UU_V_* 等「帮你赶上车」的手续边缘 |
| 第 25 | 整条呼叫时间线；迟后进入只开窗 |
| **本课** | 补充业务全景 + 迟后进入细讲 + 别名/GPS/活动/边缘 CSBK 对照 |

四句话串起来：

1. **主业务**靠第 25 课时间线（Header / 超帧 / Terminator）；  
2. **迟后进入**靠第 17 课两步（SYNC@A + 嵌入门牌）；  
3. **别名 / GPS** 是嵌入车厢里的「另一类乘客」（FLCO 不同）；  
4. **Act_Updt / 唤醒 / 前导** 帮扫描与感知，**替代不了**话务 Full LC 门牌。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；迟后进入与别名都不另开频。  
2. **多址**：仍是 **2-slot TDMA**；TS1/TS2 各有各的超帧相位与 Hangtime。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps**。  
4. **解调直觉**：先认 SYNC（语音壳还是数据壳）→ 再解嵌入 / Full LC → 再比对组与色码。  
   **听不见 ≠ 「射频没解调」**，也可能是：还在等 Burst A、嵌入拼失败、组/CC/时隙写错、或卡在 Hangtime 礼貌接入。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **Supplementary（补充业务）** | 依附主呼叫的加料能力 | ≠ 第三种可单独「拨打」的主菜电话 |
| **Tele-service（电信业务）** | 用户感知的主业务：组呼/个呼等 | ≠ 补充加料本身 |
| **Late Entry（迟后进入）** | 通话已开始后半路加入：Voice SYNC@A + 地址 LC | ≠ Hangtime；≠ 「永远没听见」 |
| **Voice SYNC @ Burst A** | 超帧边界标签；迟后进入的「上车点」 | ≠ Data SYNC（Header/Terminator/CSBK 壳） |
| **Embedded LC（嵌入 LC）** | 超帧 B–E（典型）中心碎片拼回 Full LC | ≠ Short LC（走 CACH） |
| **Voice LC Header** | 通话开头整包门牌（DT=`0001`） | ≠ 迟后进入的唯一门票——错过仍可能靠嵌入 |
| **Talker Alias** | 主叫可读名字；FLCO `000100`–`000111` 嵌入 | ≠ 源地址数字本身；≠ 另开模拟副载波 |
| **GPS_Info** | 嵌入位置信息；FLCO=`001000` | ≠ Part3 完整 LIP/短数据主战场（本课只记「可嵌在语音里」） |
| **Service Options** | Full LC 里 8 bit：Emergency / Broadcast / OVCM / Priority… | ≠ FLCO；Broadcast **仅组呼** |
| **Act_Updt** | CACH Short LC（SLCO=`0001`）：两槽活动类型 + hashed 地址 | ≠ 话务 Full LC 门牌替身 |
| **BS_Dwn_Act** | CSBKO=`111000`：唤醒/激活 BS 出站 | ≠ Late Entry 机制本身 |
| **Pre_CSBK** | CSBKO=`111101`：扫描/节电前导，提高命中 | ≠ 门牌；帮「赶上」非语音/后续块 |
| **Hangtime** | EOT 后中继短暂保留本组优先 | ≠ Late Entry；≠ TxHang |
| **OVCM** | Open Voice Call Mode：Service Options 一比特 | ≠ Broadcast |
| **Emergency Interrupt** | 请求打断正在发射台（过程在 Part2；本课记「有这件事」） | ≠ 普通 Emergency 贴纸位 |

---

## 4. 机制拆解：补充业务全景 + 迟后进入细讲

Canonical 来源：`02-语音业务/语音业务字段速览.md` **§1–§2 / §3.3–3.5 / §5 / §6–§7**；第 13 课 §6；第 17 课 §4.3；Part 1 **5.1.2**（late entry 指针）；Part 2 clause **5.2**（组/个呼）。下列**故意不画完整 SDL**。

### 4.1 补充业务是什么？和「基本语音呼叫」差在哪？

第 13 课已钉死电信习惯三分法：

| 层 | 白话 | 例子 |
|----|------|------|
| Bearer（承载） | 管道能力 | 语音承载、数据承载 |
| Tele-service（电信业务） | 用户点的主菜 | 组呼、个呼 |
| Supplementary（补充业务） | 贴在主菜上的加料 | 迟后进入、紧急、优先级、广播位、主叫识别… |

资料库 §7 把「概念 → 字段」收成一张表（本课必认）：

| 补充/特性 | 主要字段落点 | 本课怎么用 |
|-----------|--------------|------------|
| Late Entry | Voice SYNC + 地址 LC | **主线细讲** |
| Talking Party / Talker Alias | FLCO `000100`–`000111` | 嵌入乘客 |
| Emergency | Service Options.Emergency；Act_Updt 亦可反映紧急语音 | 门牌贴纸 |
| Priority | Service Options.Priority | 门牌贴纸 |
| Broadcast / All Call | Broadcast 位 + 组地址约定 | 仅组呼侧 |
| OVCM | Service Options.OVCM | 记位即可 |
| Emergency Interrupt | Part2 过程（如 6.3.4 一带） | 记「有打断请求这件事」 |

**防晕句**：补充业务多数**不能**脱离一次组呼/个呼单独「打一通补充电话」。你打的仍是组呼；迟后进入、别名、紧急位是这次组呼上的能力。

### 4.2 迟后进入：为什么需要？

现实里你会错过 Header 的场景太多了：

- 中途开机、换电池刚上电；  
- 扫描刚扫到这个信道/时隙；  
- 弱场导致开头几个数据壳 CRC/RS 失败，但后面语音壳还能锁；  
- 用户拧旋钮晚了半秒才到正确谈组。

若门牌**只在开头贴一次**，这些人会「永远进不了正在进行的会」。  
DMR 的设计意图（协会 Feature Evolution 与 Part1 超帧叙述同向）：把「呼叫类型、源 ID、目的 ID、业务选项」**嵌进语音超帧 B–E**，让迟到者仍能拼出门牌——这就是 **Late Entry**。

白皮书一句话语感（DMR Association Benefits）：迟后进入补充业务提供 **continuous call-in-progress updates**，让晚到者能加入正在进行的呼叫。

### 4.3 迟后进入机制：两步，不是「每个 30 ms 重贴完整地址」

#### 步骤 1 —— 上车点：Voice SYNC @ Burst A

- 一列语音超帧 = **A–F = 6 × 30 ms ≈ 360 ms**（第 17 课）；  
- **Burst A** 中心多为 **Voice SYNC**（不是 Data SYNC）；  
- 接收机对齐超帧相位，知道「火车从哪一节算起」。

听感：最多大约等一个超帧量级的 SYNC 机会，然后才谈得上开声。  
双时隙都在跑、相位错开时，最坏等待可能更长一点（第 17 课提过约 330 ms 量级的教学指针）——仍远好于「永远对不上」。

#### 步骤 2 —— 认门牌：嵌入 Full LC（B–E）+ 匹配

- **B–E** 携带嵌入碎片，经 EMB/LCSS 拼回与 Header **同类**的 Full LC（第 21–22 课）；  
- 组呼常见 `Grp_V_Ch_Usr`（FLCO=`000000`：组地址 + 源地址 + Service Options）；  
- 个呼常见 `UU_V_Ch_Usr`（FLCO=`000011`）；  
- 还要过 **Colour Code**（EMB/SLOT 上的色码门，第 20–21 课）与**本机监听的组/个号、时隙**匹配。

口诀：

> **SYNC 让你跳上火车；嵌入让你认出车次；色码/组号决定你该不该掏出耳机。**

#### 和「必须听到 Voice LC Header」的对比

| | 从头听 | 迟后进入 |
|--|--------|----------|
| 门牌来源 | Header 整包（DT=`0001`）最干净 | 主要靠嵌入拼装；若还能看见后续 Header 副本更好 |
| 保护链直觉 | Header：RS24 + BPTC（第 24 课原则） | 嵌入：CS5 + 变长 BPTC（另一条路） |
| 失败时 | 头坏了仍可能靠后面嵌入上车 | 嵌入连续拼失败 → 有声壳但不开业务声 / 显示无地址 |

**重要诚实注**：有的实现（含开源解码器/扫描逻辑）要求「**两次一致的嵌入 LC**」才放行半路上车——这是**工程稳健性**（防一次误纠错造幽灵呼叫），**不是**资料库另发明的一种 PDU，也**不要**把它背成 ETSI 强制条款号。岗位话术：「嵌入要拼得出来，而且最好前后一致，机器才敢开声。」

### 4.4 嵌入车厢里的「其他乘客」：Talker Alias / GPS

同一条嵌入运载通道，不只运「谁呼谁」的 Voice Channel User LC，还可穿插：

| FLCO | 别名 | 白话 |
|------|------|------|
| `000100` | Talker_Alias_hdr | 别名头：格式 + 长度 + 首段字符 |
| `000101` / `000110` / `000111` | Talker_Alias_blk1/2/3 | 别名续块 |
| `001000` | GPS_Info | 经纬度等位置信息（嵌入） |

协会材料语感：Talker Alias 适合「一台机器多人轮流用」——用户输入要显示的名字，随语音发出，对端屏幕显示**当前使用者**而不只是电台 ID。字符编码不同，长度大约在十余到二十余字符量级（协会幻灯口径；精确字段以 Part2 Table 7.4/7.5 与资料库 §3.4–3.5 为准）。

**和 Late Entry 的分工（防混）**：

```text
  嵌入 LC 车厢
     ├─ Voice Channel User LC  → 迟后进入认「组/源」（能不能进会）
     ├─ Talker Alias 头/块     → 显示「谁在说」（名字）
     └─ GPS_Info               → 附带位置（点）
```

D2ALP 等通俗文也强调：Late Entry 与 Talker Alias **都走嵌入**，但**职责不同**——一个管「进不进得去」，一个管「屏幕显示什么名字」。

本课边界：完整 LIP 轮询、USBD、Part3 短数据/IP——留给数据课；这里只要求你看见 FLCO=`001000` 时知道「位置可以嵌在语音超帧里送」。

### 4.5 语音进行中的「缝里看板」：Act_Updt（Short LC）

出站 CACH 可带 Short LC（第 18 / 22 课）：

- SLCO=`0000` → `Nul_Msg`（填空）；  
- SLCO=`0001` → **Act_Updt**：TS1/TS2 各一个 Activity ID + hashed 地址摘要。

Activity ID 教学常用值（资料库 Table 7.10）：

| Value | Meaning |
|-------|---------|
| `0000` | No activity |
| `1000` | Group voice |
| `1001` | Individual voice |
| `1100` | Emergency group voice |
| `1101` | Emergency individual voice |
| … | 另有 CSBK/数据类编码，见资料库 |

岗位直觉：

> **Act_Updt = 站台小黑板「1 号站台组呼占用、哈希地址某某」；它不能替代车厢里的 Full LC 门牌正文。**

迟后进入认组，最终仍要靠 **嵌入/头中的地址 LC**；Act_Updt 更像帮扫描/感知「这边有活动」。

### 4.6 边缘：BS_Dwn_Act / Pre_CSBK——帮你「赶上」但不是 Late Entry 本身

第 25 课时间线开头的可选 CSBK，本课放到「补充/伴随能力」边缘再钉一次：

| PDU | CSBKO | 白话 | 和迟后进入的关系 |
|-----|-------|------|------------------|
| **BS_Dwn_Act** | `111000` | 叫醒睡着的中继出站 | 没出站就谈不上收语音/嵌入；**不是**嵌入拼门牌 |
| **Pre_CSBK** | `111101` | 给扫描/节电台垫前导，后面还跟几块 | 提高「非语音投递」命中；**不是** Voice SYNC 上车点 |
| UU_V_Req / Ans | `000100` / `000101` | 个呼先问在不在 | 进语音前的手续；迟到者若通话已在进行，仍走嵌入路径 |

一句话：**唤醒与前导帮你「信道上有车可上」；迟后进入帮你「车开了也能认出车次」。**

### 4.7 Service Options 贴纸（复习，不另开加餐）

门牌 Full LC 里的 8 bit（Table 7.11）常在迟后进入拼出来的同一份 LC 里一起看见：

```text
  [ Emergency | Privacy | Reserved(00) | Broadcast | OVCM | Priority(2) ]
```

- **Emergency / Priority**：加急语义；Act_Updt 也可用 `11xx` 类活动码反映紧急语音占用；  
- **Broadcast**：仅组呼；配合全呼地址约定；  
- **OVCM**：Open Voice Call Mode 位；  
- **Privacy**：位存在 ≠ 本规范已标准化具体隐私算法（NOTE）。

岗位顺序：先认 **FLCO（组还是个）** → 再读 Service Options → 再读地址数字。

### 4.8 Hangtime vs Late Entry（本课必拆的一对双胞胎）

| | Late Entry | Hangtime |
|--|------------|----------|
| 何时 | 通话**进行中**你半路加入 | 有人**已松 PTT（EOT）** 后短暂保留 |
| 你在等什么 | 下一个 Burst **A** + 嵌入门牌 | 同组礼貌回一句的优先窗 |
| 空口线索 | 语音超帧仍在；可无 Header | 常见 BS 继续下发 Terminator with LC |
| 听感 | 先静半拍再进会 | 「已经没人说了」却占着组 |
| 误判 | 当成天线坏了 | 当成中继卡死 |

口诀：**一个是「车开了你还赶得上」；一个是「车到站灯先不灭」。**

### 4.9 范围钉死：Tier II 嵌入迟入 ≠ Tier III Grant 重播

本课主线是 **常规（Tier II）**：门牌靠 Voice LC Header / 嵌入 / Terminator。

集群（Tier III）里还有另一种口语也叫 late entry 的故事——控制信道**周期性重播 Grant / grant update**，让晚到的台发现「某谈组正在某业务信道」。那是**控制信道调度叙事**，阶段 E（约第 31–34 课）再讲。  
看见外链或同事说「late entry」时，先问：

> **你说的是语音超帧里的嵌入门牌，还是控制信道上的 Grant 更新？**

两套别混进本课主线。

---

## 5. 对照表：先前各课 → 本课角色

| 角色 | 空口形态 | 你用哪一课的眼镜看 |
|------|----------|-------------------|
| 主菜时间线 | Header→A–F→Terminator→Hangtime | 第 25 |
| 上车点 | Voice SYNC @ A | 第 17 / 19 |
| 门牌碎片 | 嵌入 B–E + EMB/LCSS | 第 21 / 22 |
| 门牌保护原则 | 头 RS24 vs 嵌入 CS5 | 第 24（不贴矩阵） |
| 色码门 | CC | 第 20–21 |
| 别名 / GPS 乘客 | FLCO `000100`–`001000` | 资料库 §3；本课 §4.4 |
| 缝里活动 | Act_Updt Short LC | 第 18 / 22；本课 §4.5 |
| 唤醒 / 前导 | BS_Dwn_Act / Pre_CSBK | 第 23；本课 §4.6 |
| 补充分类地图 | Bearer/Tele/Supplementary | 第 13 |
| 贴纸位 | Service Options | 第 13 / 25；资料库 §6 |

---

## 6. 现场岗位对照

| 现场现象 | 补充业务 / 过程解释 | 先查什么 |
|----------|---------------------|----------|
| 中途开机：先静音，约零点几秒后进会 | **Late Entry** 正常：等 Burst A + 拼嵌入 | 组/时隙/色码是否本就对；再看弱场是否导致嵌入连续失败 |
| 分析仪有语音突发，终端一直不开声 | 可能嵌入拼不出、组不匹配、CC 不对；或实现要求「两次一致」未满足 | 抓嵌入 LC / EMB CC；对照本机监听列表；别先换天线 |
| Header CRC/RS 失败，稍后仍听到声音 | 头没赶上，**嵌入路径 late entry** 仍可能上车 | 第 22/24：两条门牌路；不必断言「没 Header 就绝不可能听」 |
| 有声但屏幕无组号/无源 | 语音壳锁了，门牌未拼齐或显示策略滞后 | 等下一两个超帧；查是否只开了「听音频、不解码 LC」类模式 |
| 屏幕突然出现主叫中文/英文名 | **Talker Alias** 嵌入拼齐 | FLCO `000100`–`000111`；与源地址数字对照；别去找「第二路模拟音」 |
| 语音中地图点更新 | **GPS_Info** 嵌入或其它定位路径 | FLCO=`001000`；完整 LIP/轮询细节不在本课死磕 |
| 「没人说话了」却占着组 | **Hangtime**，不是 late entry | 同组回传？CallHang 配置？礼貌/不礼貌？ |
| 把 Hangtime 当成「迟后进入失败」 | 概念反了：Hangtime 在 EOT 后；late entry 在通话中 | 看时间线：还有没有 A–F 语音？还是只剩 Terminator？ |
| CACH 刷 Group voice=`1000` | **Act_Updt** 看板 | 用它感知占用；进组仍靠 Full LC |
| 中继刚睡醒第一通晚半拍 | 可能先走了 **BS_Dwn_Act**；或扫描命中靠 **Pre_CSBK** | 空口开头有没有 CSBK；与「超帧内 late entry」分层看 |
| 紧急键红了仍像普通组呼波形 | Emergency 常是 **Service Options 位** + 过程，不是另调一个载波 | 读门牌贴纸；Act_Updt 是否变 `1100`/`1101` |
| 同事把 Tier III「grant update」教程套到常规中继 | 边界混了 | 问清有没有控制信道；本课主线是嵌入 LC |

写频 / 监听台 30 秒话术：

> 「组呼不是只在开头喊一次『这是 1001 组』。火车开了以后，每隔一列超帧还会把『谁呼谁』撕成四片贴纸贴在车厢上。你晚到，先等车头大标签（Voice SYNC）跳上车，再拼贴纸确认是不是咱们组——拼对了才给你出声。屏幕上的名字是另一叠贴纸（Talker Alias），不是第二根天线。」

---

## 7. 工作例子（6 则）

### 例子 A · 幸福路径：准时听到 Header（对照用）

```text
[Header Grp] → A B C D E F → A B C D E F → … → [Terminator] → Hangtime → Idle
     ↑你在这里开机：门牌整包已到手，超帧直接听
```

要点：迟后进入机制仍在后台重复贴门牌，只是你用不上。

### 例子 B · 经典迟后进入：错过 Header，从第二列超帧上车

```text
真实空口：
  [Header] A B C D E F | A B C D E F | A B C D E F | [Term]
你的接收：              ↑从这里醒
  1) 锁定 Voice SYNC@A
  2) B–E 拼出 Grp=1001, Src=2002, FLCO=组呼
  3) CC/时隙匹配 → 开声（可能已丢掉开头半句语义）
```

### 例子 C · 弱场：Header 坏了，嵌入两次一致后才开声（实现策略示意）

```text
Header RS/CRC 失败
超帧1 嵌入 LC：Grp=1001（先当候选，有的实现仍静音）
超帧2 嵌入 LC：再次 Grp=1001 且一致 → 开声
```

要点：第二次确认是**常见工程策略**；教学上理解「为什么要稳」，不要背成虚构条款。

### 例子 D · Talker Alias：进会之后屏幕才跳出名字

```text
… 超帧中穿插：
  嵌入 Voice Channel User LC   ← 先解决「能不能进」
  嵌入 Talker_Alias_hdr/blk… ← 再拼显示名「张三」
```

要点：别名拼齐可能比进会更晚几个超帧；「先进会、后显示名」是正常现象。

### 例子 E · Hangtime 误判成「迟后进入失败」

```text
已出现 Terminator with LC，BS 仍在 Hangtime 留灯
新来的用户拧到该组：礼貌接入显示忙 / 无法新开
用户说：「我 late entry 不进去！」
其实：车已到站在留灯，不是「车开着拼不出门牌」
```

### 例子 F · Act_Updt 有活动，但本机组列表没有该组

```text
CACH Act_Updt：TS1 Activity=Group voice，hashed 地址某某
本机未编程该组 → 不会因看板自动「进会」
真正进会仍需：本机监听该组 + 嵌入/头中 Full LC 匹配
```

---

## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| 超帧 | 6 burst ≈ **360 ms** | 嵌入门牌重复周期量级 |
| Burst A 中心 | Voice SYNC（48 bit 场） | 上车点 |
| B–E | 嵌入碎片 + EMB | 拼 Full LC |
| Header Data Type | `0001` | 整包门牌壳 |
| Terminator Data Type | `0010` | 下车壳 |
| 组呼 FLCO | `000000` | Grp_V_Ch_Usr |
| 个呼 FLCO | `000011` | UU_V_Ch_Usr |
| Talker Alias FLCO | `000100`–`000111` | 头 + 三块 |
| GPS_Info FLCO | `001000` | 嵌入位置 |
| Act_Updt SLCO | `0001` | CACH 活动看板 |
| BS_Dwn_Act CSBKO | `111000` | 唤醒出站 |
| Pre_CSBK CSBKO | `111101` | 前导 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 不换频不改调 |

---

## 9. 十则误区（看见就打回）

1. **「补充业务是第三种能单独拨打的电话。」** → 多数是主呼叫上的加料。  
2. **「迟后进入=永远听不见。」** → 恰恰相反：设计就是让你半路听得见。  
3. **「必须听到 Voice LC Header 才能进组。」** → Header 最好，但嵌入路径就是为错过头准备的。  
4. **「每个 30 ms 都会重贴一份完整地址。」** → 完整拼装节奏跟超帧/嵌入碎片走，不是每时隙一份新门牌。  
5. **「Hangtime 就是迟后进入。」** → 一个在通话中上车，一个在 EOT 后留灯。  
6. **「Talker Alias 是另开一路模拟音。」** → 嵌在语音超帧的 Full LC 乘客。  
7. **「Act_Updt 有组呼活动=我已经进组。」** → 看板≠门牌匹配。  
8. **「迟后进入失败一定是天线坏了。」** → 先查组/CC/时隙/嵌入是否可读，再查 L1。  
9. **「实现里『确认两次嵌入』=规范新 PDU。」** → 工程策略，不是另发明单据。  
10. **「集群 Grant 更新教程可以直接当 Tier II 迟后进入讲义。」** → 边界不同；本课主线是嵌入 LC。

---

## 10. 自测题（含答案）

**题 1.** 用一句话区分：基本语音呼叫（Tele-service）vs 补充业务（Supplementary）。

<details><summary>答案</summary>

基本语音呼叫是用户点的主菜（组呼/个呼等时间线）；补充业务是贴在主菜上的加料（迟后进入、别名、紧急位等），多数不能脱离主呼叫单独「另打一通补充电话」。

</details>

**题 2.** 迟后进入的「两步上车」分别等什么？为什么听感常常是「先静半拍再进会」？

<details><summary>答案</summary>

步骤 1：等到 Burst **A** 的 **Voice SYNC**，对齐超帧；步骤 2：用 **B–E 嵌入**拼出地址 Full LC，并做色码/组（或个号）/时隙匹配。静半拍，是因为最多大约要等一个超帧量级的 SYNC 机会，且门牌拼齐前接收机可能先不开声——不是永远听不到。

</details>

**题 3.** 判断：错过 Voice LC Header 就绝对不可能听到正在进行的组呼。（对 / 错）并说明为什么。

<details><summary>答案</summary>

**错。** 嵌入路径会周期性重复贴同类门牌；这正是 Late Entry 的设计意图。Header 是最干净的整包，但不是唯一门票。

</details>

**题 4.** Talker Alias 的 FLCO 范围是什么？它和 Late Entry 用的 Voice Channel User LC 有何分工？

<details><summary>答案</summary>

FLCO **`000100`–`000111`**（头 + block1/2/3）。Voice Channel User LC 解决「这通是不是我的组/个呼」（进不进得去）；Talker Alias 解决「屏幕显示主叫什么名字」。二者都可走嵌入，职责不同。

</details>

**题 5.** 现场：「没人说话了却占着组」——更应先怀疑 Late Entry 还是 Hangtime？空口上可能看见什么？

<details><summary>答案</summary>

更应先怀疑 **Hangtime**（EOT 后保留）。空口常见 BS 继续下发 **Terminator with LC** 等保留指示；此时不是「车开着拼不出门牌」的 late entry 场景。

</details>

**题 6.** Act_Updt 在哪里走？它能不能替代嵌入 Full LC 完成进组判断？

<details><summary>答案</summary>

走 **CACH Short LC**（SLCO=`0001`）。**不能**替代：它是两槽活动类型 + hashed 地址的小看板；进组仍靠头/嵌入中的话务 Full LC 与本机监听匹配。

</details>

**题 7.** BS_Dwn_Act 与 Pre_CSBK 和迟后进入是什么关系？（各用一句话）

<details><summary>答案</summary>

**BS_Dwn_Act**：唤醒 BS 出站，让信道上「有车可收」——不是嵌入拼门牌本身。**Pre_CSBK**：给扫描/节电台垫前导提高命中——帮「赶上」后续块，不是 Voice SYNC 上车点。二者是边缘「帮你赶上」的手续；迟后进入是超帧内认门牌的机制。

</details>

**题 8.** 为什么本课要把 Tier III「grant update 式 late entry」划到边界外？

<details><summary>答案</summary>

因为那是**控制信道周期性重播业务信道分配**的集群叙事；本课主线是 **Tier II 常规**下语音超帧 **Voice SYNC + 嵌入 LC**。两套都可能被口语叫 late entry，但空口载体与阶段不同，混讲会把 Grant 故事错误塞进 Header/嵌入时间线。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `02-语音业务/语音业务字段速览.md` **§7** | **补充业务概念→字段** canonical 表 |
| 2 | 同上 **§2** | 过程阶段表；Late entry 一句指针 |
| 3 | 同上 **§3.3–3.5 / §5.2 / §6** | GPS / Talker Alias；Act_Updt；Service Options |
| 4 | `学习推送/第13课.md` §6 | 补充业务地图与三层分类 |
| 5 | `学习推送/第17课.md` §4.3 | 两步上车故事 |
| 6 | `学习推送/第22课.md` | Full LC 三路径；嵌入证明 late entry |
| 7 | `学习推送/第18课.md` / `第23课.md` | CACH Act_Updt；BS_Dwn_Act / Pre_CSBK |
| 8 | `学习推送/第25课.md` | 呼叫时间线；本课窗口的前文 |
| 9 | `00-入门/DMR术语与帧结构速查卡.md` | 超帧 / 264 / CACH 一页墙 |
| 10 | `DMR整合学习手册.md` §5 | 业务全景里对补充业务的总述 |
| 11 | 官方 **TS 102 361-2 V2.5.1**（库内 PDF：`02-语音业务/TS102361-2_V2.5.1.pdf`） | 组/个呼过程、补充与字段原文 |
| 12 | 官方 **TS 102 361-1 V2.7.1** **5.1.2** 一带 | 超帧与 late entry 空口指针 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「听不见」一律怪调制 |

官方版本锚点：**Part2 V2.5.1**、**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。FEC 矩阵、Idle 比特、符号表：**永远回 PDF**，本课不补第二份。

---

## 12. 下一课预告

**第 27 课 · PDP：确认与非确认数据**

语音主菜与补充加料（本课）告一段落。下一课进入 **Part 3 数据主战场**：分组数据协议（PDP）里确认数据与非确认数据怎么分、空口上大致长什么样、和语音时间线如何共用同一条 12.5 kHz / 双时隙载波——仍少公式，多现场对照，并提醒：短数据/头压缩细讲在第 28 课。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-01**（上午推送）检索核验；真实打开过内容页/PDF（HTTP 200 或协会镜像可用）；**不编造地址**。策略 = **Part2 协会镜像 + Feature Evolution 嵌入图 + Benefits 白皮书迟入句 + GopherTrunk 门牌/嵌入/迟入/别名深文 + Decoders 帧路径 + 一篇通俗 Late Entry 专文（意文，机制同向）**。

1. **[ETSI TS 102 361-2 V2.5.1｜Voice services（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：组呼/个呼过程、Voice Channel User LC、Talker Alias / GPS PDU、Service Options、补充相关叙述——本课字段硬出处。  
   - **库内副本**：`dmr/02-语音业务/TS102361-2_V2.5.1.pdf`。  
   - **适合哪一段**：第 4、6、8、11 节。  
   - **基础**：进阶；英文 PDF。

2. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：超帧 **5.1.2**、SYNC/嵌入总框架——给「上车点」钉空口原文。  
   - **适合哪一段**：第 2、4.3、11 节。  
   - **基础**：进阶；英文 PDF。

3. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：「Embedding Data within Voice」一页画出 A=Voice SYNC、B–E=Embedded，并写明嵌入 initially 用于 **Late Entry**（呼叫类型、源/目的 ID、业务选项）；同材料亦讲 Talker Alias / 嵌入位置语感。  
   - **适合哪一段**：第 2、4.2–4.4 节。  
   - **基础**：入门～中级；英文幻灯 PDF。

4. **[DMR Association｜Benefits and Features of DMR（白皮书 PDF）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：用产品/用户语言写 Late Entry「持续提供 call-in-progress updates」——适合给领导/新同事的一句话语感。  
   - **注意**：白皮书不是 TS；冲突以 Part1/2 为准。  
   - **基础**：入门；英文 PDF。

5. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
   - **为什么值得看**：把门牌三条运载、B–E 拼装、header-less late entry、Talker Alias 拼装写成同一条故事线——本课例子 B/C/D 的加厚版。  
   - **适合哪一段**：第 4.3–4.4、7 节。  
   - **注意**：文中「确认两次嵌入 / ~720 ms」等是**工程策略**，**不以博客条款号替代 ETSI**。  
   - **基础**：中级～进阶；英文网页。

6. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：EMB/LCSS、嵌入重装、FLCO 列表（含 Talker Alias / GPS）——防止把 Short LC 与 Full LC 搅乱。  
   - **适合哪一段**：第 4.3、4.5、5 节。  
   - **基础**：中级～进阶；英文网页。

7. **[D2ALP｜Late Entry nel DMR（通俗专文，意文）](https://www.d2alp.it/late-entry-nel-dmr-entrare-in-una-comunicazione-gia-iniziata/)**  
   - **为什么值得看**：专门解释「通话已开始仍能加入」、Header vs Embedded LC、与 Talker Alias 的分工；机制叙述与本课同向，适合非英语同事对照。  
   - **注意**：通俗博客；**硬条款以 ETSI PDF / 资料库为准**。  
   - **基础**：入门～中级；意大利文网页（浏览器翻译可用）。

8. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读，帮助把补充能力放回整网叙事。  
   - **注意**：TR **不是**规范。  
   - **基础**：入门～中级；英文 PDF。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 补充业务 + Tier II 迟后进入：Voice SYNC@A + 嵌入 Full LC 拼门牌 + Talker Alias/GPS 乘客分工 + Hangtime 对照」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只口播写频/双时隙/产品演示，或讲 P25/集群扫描器）。本课 **`video_found=false`**。建议用：**语音业务字段速览 §7 + Feature Evolution 嵌入图 + GopherTrunk E2E Part5 + 本课总图** 对照自学。

---

*推送说明：本课为阶段 D「补充业务（迟后进入等）」专课。频谱/调制仅保留短提醒（加料不换频、不改 4FSK/双时隙），不复述加餐全文。主文加厚覆盖动机、主菜加料总图与两步上车、术语、补充全景、迟后进入细讲、别名/GPS/Act_Updt/边缘 CSBK、Hangtime 对照、Tier III 边界、现场分诊、六则例子、账本、十则误区、八题自测、资料库路径与核验外链（诚实标明无合适公开专题视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle/符号表、不发明条款号、不把 Tier III Grant 更新冒充本课主线。读完应能向同事讲清「补充业务是加料不是第三道主菜、迟后进入两步怎么上车、别名与门牌如何分工、Hangtime 为何不是 late entry」，并进入第 27 课 PDP。*
