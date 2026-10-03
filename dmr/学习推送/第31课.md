# 第 31 课 · 控制信道 vs 业务信道

> DMR 深入学习 · **阶段 E · 集群 Tier III 第 1 课（约 10 课之首）**（接第 30 课「小综合：跟一次语音呼叫空口」）  
> 适合：已经能跟读 Tier II 常规语音空口（Header → 超帧 → Terminator），但一进机房集群录波就问「Voice LC Header 呢？人还在控制信道上啊」——把 **TSCC 叫号** 和 **Payload 通话** 画成同一条常规时间线——的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**控制信道发号令 / 业务信道才说话；Grant = 房间号小票；离开 TSCC 再谈超帧**」钉成肌肉记忆  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。**换控制/业务信道故事，不改射频账本**——听不见、Grant 丢了、人还停在 TSCC，都不等于「调制坏了」。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是 **阶段 E 开场：TSCC（控制）vs Payload（业务）+ Grant 转台门牌**。

---

## 1. 为什么本课重要（动机）

第 25 / 30 课把常规中继的「门牌发车 → 超帧火车 → 终止下车」练成了跟读清单。机房下一句要命的话往往是：

- 分析仪停在「控制信道」上，同事喊：「跟一下这通组呼！」——你按第 30 课盯 Data Type=`0001`，却半天看不见 Voice LC Header。  
- 屏上反复闪 CSBKO=`110001`（TV_GRANT）——有人说「这就是在说话」；有人说「还没上车」。谁对？  
- MS 明明 PTT 了，空口先见一串 C_RAND / C_AHOY / C_ACKD，再 Grant——你却把它们全当成「Header 前面的可选 CSBK 手续」（第 30 课 CP0），时间轴越画越歪。  
- 调度台说「人还在控制信道露营」；写频同事说「业务信道没载波」——两边对的是**两个房间**，你却只开了一个频点。  
- 新人把 Tier III Grant 时间和常规 Header 画在同一条轴上——整晚对不上（第 30 课例 7 / 误区 9 已警告；本课展开）。

培训台若只背「集群就是自动分配信道」八个字，后面会卡在同一处：

> **会背「有控制信道」≠ 会分诊。** 分诊 = 先问「分析仪停在 TSCC 还是 Payload？」→ 再问「此刻是叫号（Grant）还是已经在说话（超帧）？」→ 最后才碰射频与写频。本课不是把 Part4 全文 dump 一遍，而是把 **控制 vs 业务** 钉成可现场演示的第一张地图。

本课目标：能画出「MS 守 TSCC → C_RAND →（可选 AHOY/ACK）→ Channel Grant → 改频到 Payload → 再谈像第 30 课那样的语音超帧」总图；会说 Dedicated / Non-Dedicated TSCC 各是什么味道；会把 Grant 当成「房间号小票」而不是「已经在通话」；会对照 Tier I/II「固定中继信道」与 Tier III「控制+业务」；会做现场分诊、六～八则例子与自测；并为第 32 课「登记与 Aloha」留好边界感。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不贴完整 SDL、不发明 ETSI 条款号（入口锚点以资料库 `04-集群协议/集群协议字段速览.md` **§1–§4 / §12**、`总索引.md` **集群 / Tier III** 已有编号为准）、**不深挖登记过程与 Aloha 退避细节**（第 32 课）、**不铺开全部 Grant 变体与 Reason Code 全表**（第 33–34 课）、**不讲鉴权/RC4**（第 35）、**不深挖 CHAN 绝对频率公式**（第 36）、**不讲 Hunt/拨号/Stun**（第 37–39）。本课只钉 **控制 vs 业务 + Grant 转台门牌**。

---

## 2. 总图 / 故事：「调度台发号令 vs 通话房间」

先把整课装进一个故事，再落到 `集群协议字段速览.md` **§1** 与第 9 / 25 / 30 课回唤。

### 2.1 一句话故事：旅馆前台 + 客房

把 Tier III 想成一座旅馆：

1. **前台（TSCC · 控制信道）** = 昼夜值班的调度台：广播「现在可以怎么排队」（Aloha 一句指针）、接受你按铃（C_RAND）、有时点名问你在不在（C_AHOY）、确认/排队/拒绝（ACK 族），最后发一张 **房间号小票（Channel Grant）**；  
2. **客房（Payload · 业务信道）** = 真正说话/传数据的房间：你拿到小票后**离开前台**，改到指定物理信道 + 时隙，才开始像第 30 课那样的 Voice LC Header / 超帧 A–F / Terminator；  
3. **小票上写什么** = Logical Physical Channel Number（哪间房的门牌逻辑号）+ Logical Channel Number（TDMA 时隙 ch1/ch2）+ 谁找谁；  
4. **小票常重复、通常不要求你回执** = Grant 不要求 ACK，所以空口上常连发几遍，怕你漏听；  
5. **前台不等于客房** = 人还蹲在 TSCC 上时，你不该用「Voice LC Header 去哪了」当第一句骂人——他可能还在等小票，或小票已经发了但分析仪没跟过去。

口诀：**先前台叫号 → 再拿房间小票 → 离开前台进客房 → 客房里才像第 30 课那样说话。分析仪要跟着人走，不要只守一个频点骂天线。**

### 2.2 总图：从 TSCC 到 Payload

```text
  时间 →

  ┌─ 守 TSCC（控制信道 / 前台）────────────────────────────┐
  │  MS 空闲时「露营」在这里听 Aloha / BCAST / Grant 广播   │
  │  （登记要求等 → 第 32 课；本课只知「有这块告示牌」）     │
  └──────────────────────┬─────────────────────────────────┘
                         ▼
  ┌─ 入站请求 C_RAND（按铃）───────────────────────────────┐
  │  Service_Kind = 语音/数据/登记/短数据…（本课只认形状）  │
  │  壳：仍是 Part1 CSBK；Opcode 在 Part4 地图              │
  └──────────────────────┬─────────────────────────────────┘
                         ▼
  ┌─ （可选）可达性 / 排队：C_AHOY、C_ACKD/NACK/QACK… ────┐
  │  有时先问「你还在吗 / 先排队」；Reason 全表 → 第 34 课  │
  │  本课：看见它们 ≠ 已经在 Payload 说话                   │
  └──────────────────────┬─────────────────────────────────┘
                         ▼
  ┌─ Channel Grant（房间号小票）× 常重复 ──────────────────┐
  │  PV_GRANT / TV_GRANT / BTV / PD / TD…（名单一眼地图） │
  │  含：Logical Physical Channel + TDMA slot + 地址       │
  │  Grant 不要求 ACK → 常连发；漏听 = 「有人说话你却静」   │
  └──────────────────────┬─────────────────────────────────┘
                         ▼
  ┌─ MS 离开 TSCC → 改频到 Payload（进客房）───────────────┐
  │  主叫 / 被叫（或组）按小票到同一业务信道+时隙           │
  └──────────────────────┬─────────────────────────────────┘
                         ▼
  ┌─ Payload 上「像第 30 课」说话 ─────────────────────────┐
  │  Voice LC Header → 超帧 A–F → Terminator →（可 Hang）   │
  │  建立方式变了，客房里的语音积木仍是阶段 D 那一套        │
  │  （业务信道上还可再 P_GRANT 换房 → 本课一句指针）       │
  └────────────────────────────────────────────────────────┘
```

极简对照（速览 §1 同款）：

```text
  典型语音建立（学习口径）：
    MS --C_RAND--> TSCC
    TSCC --C_ACKD / C_AHOY / …--> MS   （可达性/排队等，可选）
    TSCC --C_GRANT (×重复)--> 主被叫   （房间号 + 时隙）
    MS / 对端 --> Payload channel 通话   （再谈第 30 课超帧故事）
```

### 2.3 和第 9 / 25 / 30 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 9 | Tier I/II/III 全貌——本课把 III 的「控制+业务」拆开摸 |
| 第 11 | Part1–4 文档地图——本课钉死：**叫号看 Part4；客房语音仍回 Part2** |
| 第 15–24 | 时隙/突发/超帧/SYNC/CSBK 积木——客房里继续用 |
| 第 25 / 30 | Tier II 常规 Header 时间线——本课对照「发车故事换了」 |
| 第 29 | 三层书架——本课入口换成 `04-集群协议/` + 总索引「集群」 |
| **本课** | **TSCC vs Payload + Grant 转台 = 阶段 E 开门** |
| 第 32（预告） | 登记与 Aloha——前台「怎么排队、要不要先登记」 |
| 第 33–34 | Grant 全变体 / Reason Code——小票种类与拒绝理由细表 |

四句话串起来：

1. **Tier II 常规**：人本来就在「那间固定中继房」里；门牌是 Voice LC Header。  
2. **Tier III 集群**：人先在前台；门牌第一步是 **Grant 小票**，第二步才进客房说 Header/超帧。  
3. **分析仪**：停错房间 = 整晚「看不见 Header」或「Grant 当语音」。  
4. **射频账本不变**：仍是 12.5 kHz / 4FSK / 双时隙——换的是**故事轴**，不是调制。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；控制信道与业务信道可以是**不同物理频点**，但每一条上路仍按同一本射频尺子量。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**；Grant 里的 Logical Channel Number 就是在告诉你「进哪一扇时隙门」。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps** 毛速率——前台叫号与客房说话，比特语义不同，**调制方式相同**。  
4. **解调直觉**：先问「我在 TSCC 还是 Payload？」→ 再认 CSBKO（Grant/Aloha/RAND）或 Data Type（Header）→ 最后才怀疑天线。  
   **听不见 ≠ 「射频没解调」**，也可能是：还在等 Grant、Grant 漏听、分析仪没跟到 Payload、或人仍露营 TSCC。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **TSCC** | Trunked Station Control Channel，集群**控制信道**（前台） | ≠ 业务信道；≠ Tier II「固定中继信道」本身 |
| **Dedicated TSCC** | **专用**控制：这条（逻辑）信道主要干叫号/管理 | ≠ 「永远不能带任何业务」的绝对口号；学口径：专职前台 |
| **Non-Dedicated TSCC** | **非专用**控制：控制功能与业务共享形态（资源更省、故事更绕） | ≠ 「没有控制信道」；仍有控制角色，只是形态不同 |
| **Payload channel / 业务信道** | 真正承载语音/数据的「客房」；由 Grant 指定 | ≠ TSCC；人没改频过去就还在前台 |
| **Channel Grant** | 房间号小票：指定逻辑物理信道 + 时隙 + 地址 | ≠ Voice LC Header；≠ 「已经在说话」 |
| **C_RAND** | MS 在 TSCC 上的随机接入请求（按铃） | ≠ 登记全文（第 32）；≠ Header |
| **Aloha（C_ALOHA）** | 出站广播：退避/Mask/是否要求登记等「排队规则告示」 | 本课一句指针；过程 → 第 32 课 |
| **C_AHOY** | 出站点名/查询，常要求 MS 响应 | ≠ Grant；看见 Ahoy ≠ 进客房 |
| **Logical Physical Channel Number** | Grant 里 12-bit「房间逻辑号」；`0` 无效；`0xFFF` 常接绝对频率附块（深挖 → 第 36） | ≠ 绝对 MHz 本身（本课不展开公式） |
| **Logical Channel Number（slot）** | Grant 里 1-bit：TDMA **ch1 / ch2** | ≠ 物理频点；两扇时隙门 |
| **PV / TV / BTV / PD / TD Grant** | 个呼语音 / 组呼语音 / 广播组呼 / 个数据 / 组数据 等小票**名字** | 本课地图级；字段差异 → 第 33 课 |
| **P_GRANT** | **业务信道上**再授予/换信道（客房里换房通知） | ≠ TSCC 上的首张 C_GRANT；一句指针即可 |
| **Tier II 固定中继信道** | 写频就钉死的中继上/下行；人直接在那说话 | ≠ Tier III「先前台再客房」 |
| **露营 TSCC** | MS 空闲时守在控制信道听广播、等叫号 | ≠ 「卡死」；是集群常态 |

---

## 4. 机制拆解：控制 vs 业务（本课够用的厚度）

Canonical 来源：`04-集群协议/集群协议字段速览.md` **§1–§3 / §12**；`总索引.md` **集群 / Tier III**；Grant 变体细表仅作地图指针 → `ReasonCode与Grant变体.md`（**本课不 dump**）。下列**故意不画完整 SDL**。

### 4.1 Dedicated vs Non-Dedicated：两种前台形态

| 形态 | 白话 | 现场直觉 |
|------|------|----------|
| **Dedicated TSCC** | 专职前台：这条控制逻辑信道主要跑 Aloha/BCAST/Grant/RAND… | 分析仪「钉死在控制频点」能长时间看见控制 CSBK 流 |
| **Non-Dedicated TSCC** | 控制与业务共享资源：前台有时要给客房让路（实现与配置相关） | 更省信道，但「控制是否一直在」要问清站点模式；别用 Dedicated 脑补硬套 |

学口径（速览 §1）：Dedicated / Non-Dedicated 是 **5.3.1–5.3.2** 锚点下的系统模型差；本课只要能回答「我们站是专用控制还是共享控制？」并据此决定录波策略。**不要**在本课展开 TSCCAS 交替时隙全文——速览有一行指针即可。

### 4.2 什么住在控制信道？什么住在业务信道？

```text
  ┌────────────── TSCC（前台）──────────────┐
  │  C_ALOHA / C_BCAST（告示、系统参数）     │
  │  C_RAND（入站按铃）                      │
  │  C_AHOY / C_ACK*（点名、确认/排队/拒绝） │
  │  Channel Grant（发房间小票）             │
  │  控制信道短数据 UDT（指针，不深挖）      │
  │  ……登记相关（第 32 课）                  │
  └──────────────────────────────────────────┘

  ┌────────────── Payload（客房）───────────┐
  │  语音：Header / 超帧 / Terminator（第30）│
  │  数据：Part3 PDP 车次（第27–28）         │
  │  业务信道侧 P_GRANT / 部分确认（指针）   │
  │  ……通话中的功率/停发 RC 等（后课边界）   │
  └──────────────────────────────────────────┘
```

口诀：**前台管「能不能进、进哪间」；客房管「进了以后怎么说」。** 把 Voice LC Header 找前台 = 找错柜台。


### 4.2.1 现场「两台分析仪」心智模型

很多机房其实需要**两台眼睛**（或一台可快速跳频的眼睛）：

```text
  眼睛 A ──钉──→ TSCC 下行：Aloha / BCAST / Grant / Ahoy / ACK…
  眼睛 B ──跟──→ 最新一张 Grant 指向的 Payload：Header / 超帧 / 数据车次…
```

口令：

1. **先听到小票，再搬眼睛 B**——不要让眼睛 A 的热闹代替眼睛 B 的语音。  
2. **眼睛 A 长期安静**（Dedicated 站）→ 先查控制链路/站点是否倒换，再查射频。  
3. **眼睛 B 有语音、眼睛 A 没看到 Grant**→ 回放控制下行是否漏采、是否 Non-Dedicated 角色切换、是否看错时隙。  
4. **两眼都静**→ 才进入「是不是整站射频/电源」大单；仍优先排除写频控制列表与系统码。

这和第 30 课「一个频点跟完 CP0–CP6」不同：**集群跟读常常是跨频点的**。把「跨频点」当成故障，是阶段 E 最常见的新人税。

### 4.3 Grant = 房间号小票（地图级，不dump变体）

代表名（速览 §2 / §3；细字段 → 第 33 课）：

| 别名 | 一句话 | 代表 CSBKO（速览） |
|------|--------|-------------------|
| **PV_GRANT** | 个呼语音小票 | `110000` |
| **TV_GRANT** | 组呼语音小票 | `110001` |
| **BTV_GRANT** | 广播组呼语音小票 | （变体表） |
| **PD_GRANT / TD_GRANT** | 个/组**数据**小票 | （变体表） |
| **…_DX** | 双工类变体名字 | （变体表） |
| **CG_AP** | 逻辑号=`0xFFF` 时附绝对频率块 | 深挖 → 第 36 |
| **P_GRANT** | **已在业务信道**上再授予/换房 | 速览 §2.1 一行 |

Grant 里本课必认的两块门牌：

1. **Logical Physical Channel Number（12 bit）**：去哪间「物理逻辑房」；`0` 无效；`0xFFF` 常表示「看附块绝对参数」（本课不展开公式）。  
2. **Logical Channel Number（1 bit）**：TDMA **ch1（0）/ ch2（1）**——和第 15 课双时隙尺子同一世界。

**关键行为（速览 §1）**：

- Channel Grant **不要求确认** → 空口常**重复发送**；  
- 成功路径是「看见小票并改频」；失败路径常是 NACK + Reason（Reason 全表 → 第 34 课）；  
- **拿到 Grant 后 MS 离开 TSCC 去 Payload**——分析仪若仍钉在控制频点，会觉得「呼叫蒸发了」。

### 4.4 客房里为什么又「像第 30 课」？

因为阶段 D 的语音积木（Voice LC Header、超帧 A–F、Terminator、Hangtime 语义）活在**业务信道**上。Tier III 改的是**怎么被带进这间房**（控制面 Grant），不是把 4FSK/双时隙/超帧另发明一套。

对照口令：

| 问题 | Tier II 常规（第 25/30） | Tier III（本课） |
|------|-------------------------|------------------|
| 人平时停哪？ | 写频的那条中继信道 | **TSCC 前台** |
| 「可以说话了」的第一张门牌？ | Voice LC Header | **Channel Grant**（然后进房再 Header） |
| 分析仪第一刀切哪？ | 中继上/下行 | **先问 TSCC or Payload** |
| 超帧 A–F 在哪发生？ | 就在那条中继逻辑信道 | **在 Payload**，不在前台叫号流里 |

### 4.5 P_GRANT 一句：客房里还能换房

速览 §2.1：`P_GRANT` = 业务信道上再授予/换信道。白话：你已经在客房说话了，系统有时会再塞一张「请搬到另一间」的小票。本课只要知道：**不是所有 Grant 都出现在 TSCC**；看见业务信道上的再授予，别误判成「怎么又回到控制故事」。细表留给第 33 课。

### 4.6 Part1 / 2 / 3 / 4 分工（避免串读）

直接搬速览 **§12** 学习口径：

| 问题 | 去哪本 |
|------|--------|
| 突发 108+48+108、CACH、SYNC 名、CSBK **外壳** | **Part 1** |
| 常规组/个呼 LC、UU_V_Req、Talker Alias（客房语音故事） | **Part 2** |
| 业务信道确认/非确认数据、UDP 压缩头 | **Part 3** |
| TSCC、登记、Grant、Aloha、控制信道 UDT、RC Command（集群） | **Part 4** |

现场口令：**外壳认 Part1；常规语音过程认 Part2；数据车次认 Part3；前台叫号认 Part4。** 第 29 课三层书架仍然有效——只是「速览」入口从语音速览换成了集群速览。


### 4.7 本课「跟读检查点」速查卡（控制面）

把第 30 课的 CP 思路搬到控制面，**只保留阶段 E 开门需要的四个点**（登记细节仍留给第 32 课）：

| CP | 你在哪 | 期望看见 | 下一动作 |
|----|--------|----------|----------|
| **E0** | TSCC 空闲露营 | Aloha / BCAST 等告示流（可稀可密） | 确认「前台活着」 |
| **E1** | TSCC 入站 | C_RAND（按铃） | 记录 Service_Kind 味道（语音？数据？登记？） |
| **E2** | TSCC 出站手续 | 可选 Ahoy / ACK / NACK / QACK | **没 Grant 就还没进房**；Reason → 第 34 |
| **E3** | TSCC 出站小票 | PV/TV/… Grant（可重复） | **记下逻辑信道+时隙 → 搬去 Payload** |
| **（回第30）** | Payload | Header / 超帧 / Terminator | 用阶段 D 跟读清单 |

口诀：**E0 听前台活着 → E1 看按铃 → E2 分清手续 → E3 拿票搬家 → 回第 30。**

### 4.8 和「常规 CP0 可选 CSBK」为什么不能混表

第 30 课 CP0 的 `BS_Dwn_Act` / `UU_V_Req` 也是「还没说话」的手续，但：

| | 常规 CP0 | 本课 E1–E3 |
|--|----------|------------|
| 发生信道 | 常常就在那条中继业务向信道 | **在 TSCC** |
| 成功后的「开闸」 | Voice LC Header（同信道或同中继故事） | **Grant → 换到 Payload 再 Header** |
| Opcode 地图 | Part2 常规 CSBKO | **Part4 集群 CSBKO** |
| 分析仪 | 多数情况不用跨频点追小票 | **常常要跨频点** |

所以：味道都是「手续」，**柜台与地图不同**。把 `C_RAND` 写成 `UU_V_Req`，或把 `TV_GRANT` 写成「组呼 Header」，是串表，不是「差不多」。

---

## 5. 对照表：Tier I/II 常规信道 vs Tier III 控制+业务

| 维度 | Tier I / II 常规（第 9/25/30） | Tier III 集群（本课） |
|------|-------------------------------|----------------------|
| 信道故事 | 写频钉死的直通/中继信道 | **TSCC + 一池 Payload** |
| 空闲时人在哪 | 守在那条业务向信道（或扫描列表） | **常露营 TSCC** |
| 呼叫「批准」形态 | 中继可有唤醒 CSBK；门牌主线是 Header | **Grant 小票**（可先 RAND/AHOY/ACK） |
| 语音超帧发生地 | 就在该中继逻辑信道 | **Payload** |
| 分析仪常见误停 | 停错时隙 / 停错中继 | **只停 TSCC 或只停一条 Payload** |
| 文档主入口 | Part2 语音速览 + Part1 外壳 | **Part4 集群速览** + 客房回 Part2 |
| 第 30 课轴 | Header/嵌入/Terminator 跟读 | 本课之前的「发车」；进房后可再跟读第 30 |
| 本课钉的一句话 | 「固定房间里直接说话」 | 「前台叫号 → 小票 → 进房再说话」 |

和第 9 课全貌的咬合：Tier III = 「有一个控制器自动调节通信」——落到空口，就是 **控制信道管调节，业务信道管通信载荷**。

---

## 6. 现场岗位对照 / 分诊

| 岗位现象 | 先做的分诊动作 | 常翻 | 别一上来就 |
|----------|----------------|------|------------|
| 「跟一下集群组呼，怎么没有 Header？」 | 问：分析仪在 **TSCC 还是 Payload**？人拿到 Grant 了吗？ | 速览 §1 总图；本课 §2 | 按第 30 课 CP1 硬找 DT=`0001` |
| 频点「不对」 | 问：是控制频错了，还是 Grant 指向的业务频没跟上？ | 写频控制列表；Grant 逻辑信道号 | 先改功放/天线 |
| 人还在露营 TSCC | 看 Aloha/BCAST 是否正常；有没有 Grant；登记是否被挡（指针→32） | 速览 §1/§4 | 断言射频全坏 |
| Grant 疑似漏听 | 回放控制下行是否连发 Grant；MS 是否改频 | 速览 §1「Grant 不要求 ACK」 | 只骂话筒键 |
| 「在控制信道上说话」 | 确认：是 Non-Dedicated/共享形态，还是误把控制 CSBK 当语音？ | §4.1；站点模式 | 用常规 Hangtime 硬套 |
| 分析仪停错信道 | 列表：TSCC 一个；Payload 随 Grant 变——**要跟票走** | 本课总图 | 钉死一个频点录一夜 |
| 看见 TV_GRANT 就说「在通话」 | 纠正：小票 ≠ 超帧；进 Payload 再谈第 30 课 | §4.3 | 开「语音超帧丢失」单 |
| 同事把 Grant 画进常规 Header 轴 | 停：两套发车故事 | 第 30 误区 9；本课 §5 | 继续对齐时间戳硬掰 |


| 控制下行很热闹、业务全空 | 问：是只有叫号没有接通，还是 Grant 后大家都没跟？ | 回放是否有 Grant；MS 是否改频 | 直接判「业务中继坏了」 |
| 只有一个物理信道的站点 | 问：是否 Non-Dedicated / 控制与业务时分共享？ | §4.1；厂家站点模式 | 用多信道 Dedicated 脑补硬套 |


分诊口诀：**先定房间（TSCC / Payload）→ 再定阶段（叫号 / 已进房）→ 再认 CSBKO 或 Data Type → 再翻集群速览 → 最后才碰射频与写频。**

---

## 7. 工作例子（10 则）

**例 1 · 干净组呼：前台小票 → 进房说话**  
空口（控制）：C_RAND → TV_GRANT（可重复）→ MS 改频。  
空口（业务）：Voice LC Header → 超帧 → Terminator。  
跟读：本课总图走完；进房后切第 30 课速查卡。向领导一句话：「先叫号发小票，再进房说话。」

**例 2 · 分析仪钉在 TSCC：整晚「没有 Header」**  
控制下行看得见 Grant，业务侧没人跟。  
分诊：不是「没有呼叫」，是**录波没进客房**。动作：按 Grant 的逻辑信道+时隙改守 Payload。

**例 3 · Grant 漏听**  
控制侧 Grant 只闪一两次，弱场 MS 没跟上；同事在业务信道已经说话。  
分诊：想起「Grant 不要求 ACK、常靠重复」——查下行是否连发、MS 是否停在旧频。不要第一句改调制。

**例 4 · 把 Ahoy/ACK 当成已经在说话**  
PTT 后先见 C_AHOY、C_ACKD（或 QACK 排队），尚未 Grant。  
分诊：仍在前台手续；Reason/排队细表 → 第 34 课。本课判断句：**没小票就还没进房。**

**例 5 · Tier II 脑子进 Tier III 站**  
新人用第 30 课 CP0–CP6 直接套控制录波，把 C_RAND 写成「UU_V_Req」。  
纠偏：Opcode 地图换 Part4；手续名字不同；进房后才共用语音积木。

**例 6 · 「控制信道上有人说话」投诉**  
先问站点：Dedicated 还是 Non-Dedicated？再看空口是语音超帧还是密集控制 CSBK。  
可能：共享形态下资源角色切换；或监听员把快速 Grant/Aloha 误听成「有人唠嗑」。用 §4.1 + 认壳分诊。

**例 7 · 个呼 PV_GRANT vs 组呼 TV_GRANT**  
同样是「小票」，CSBKO 不同（`110000` vs `110001`），地址场一个偏个号、一个偏组号（速览 §3 代表表）。  
本课只要会：**先认哪类小票，再决定跟哪间房**；字段差异表留给第 33 课。

**例 8 · 业务信道上冒出 P_GRANT**  
通话中途系统换信道：Payload 上下发 P_GRANT，MS 再搬一次家。  
分诊：不是「突然回到 TSCC 故事」；是**客房内换房**。回速览 §2.1 一行指针，细表 → 第 33 课。


**例 9 · 双时隙：Grant 指错门**  
Grant 逻辑物理信道对了，但 Logical Channel Number 看反：人进了 ch2，分析仪守 ch1。  
分诊：业务频「有载波但无本组语音」时，先对时隙门再骂天线。回第 15 课尺子 + 本课术语表。

**例 10 · 领导问「为什么集群要比常规多一台接收机」**  
一句话：因为呼叫常从控制跳到业务，**单眼钉死一个频点会瞎**。Dedicated 站尤其明显。可用 §4.2.1「两台眼睛」画白板。

---

## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| 时隙尺子 | **30 ms** · **2-slot** | 进房后仍用；Grant 指定 ch1/ch2 |
| 超帧 | **A–F ≈ 360 ms** | **Payload** 上（第 17/30） |
| PV_GRANT CSBKO | **`110000`** | 个呼语音小票（速览 §3.1） |
| TV_GRANT CSBKO | **`110001`** | 组呼语音小票（速览 §3.2） |
| C_ALOHA CSBKO | **`011001`** | 排队告示（过程 → 第 32） |
| C_RAND CSBKO | **`011111`** | 入站按铃 |
| C_AHOY CSBKO | **`011100`** | 点名（速览 §6） |
| C_ACKD 族 CSBKO | **`100000`** 等 | 确认/拒绝外壳（Reason → 第 34） |
| C_BCAST CSBKO | **`101000`** | 系统公告（指针） |
| Logical Physical Ch | **12 bit**；`0` 无效；`0xFFF`→附绝对块 | 房间逻辑号 |
| Logical Channel Number | **1 bit**：`0`=ch1，`1`=ch2 | 时隙门 |
| Voice LC Header DT | **`0001`** | **进 Payload 之后**才找（第 30） |
| Part4 官方版本 | **TS 102 361-4 V1.12.1 (2023-07)** | 集群硬出处 |
| 速览主节 | **§1 概念 / §2 PDU 地图 / §3 Grant 代表 / §12 分工** | 本课入口 |
| 总索引 | **集群 / Tier III** | 门牌：TSCC/Grant → 速览 → Part4 PDF |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 换故事不换射频 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |

---

## 9. 十则误区（看见就打回）

1. **「集群组呼也该在控制信道上先看到 Voice LC Header。」** → Header 在 Payload；控制上看 Grant。  
2. **「看见 Grant = 已经在通话。」** → 小票 ≠ 超帧；还要改频进房。  
3. **「C_RAND 就是常规个呼 UU_V_Req。」** → 都是「先问/先请求」味道，但 Opcode 地图与故事轴在 Part4。  
4. **「分析仪钉一个频点就能跟完集群呼叫。」** → 通常要跟 TSCC→Payload；小票指向哪跟到哪。  
5. **「Dedicated / Non-Dedicated 不用问，都一样。」** → 录波策略与「控制是否常在」味道不同。  
6. **「Grant 没 ACK 就是协议坏了。」** → 规范学习口径：Grant **不要求确认**，故常重复。  
7. **「进了业务信道就用不上第 30 课。」** → 相反：进房后正是第 30 课战场。  
8. **「P_GRANT 出现说明又回到控制信道。」** → 可能是业务信道上的再授予/换房。  
9. **「Logical Physical Channel Number 就是 MHz。」** → 先是逻辑号；`0xFFF`/绝对参数深挖留给第 36 课。  
10. **「听不见说明 4FSK/12.5 kHz 坏了。」** → 先定房间与阶段；调制账本最后背锅。

---

## 10. 自测题（含答案）

**题 1.** 用三句话说明：为什么「在 TSCC 上找 Voice LC Header」常常找错柜台？

<details><summary>答案</summary>

TSCC 是前台：跑 RAND/AHOY/ACK/Grant 等叫号信令。Voice LC Header 是客房（Payload）里语音开始的门牌。人还没拿 Grant 改频时，控制录波上本来就不该以 DT=`0001` 当第一期望。

</details>

**题 2.** 画出（文字版即可）MS 从空闲到说话的五步骨架，并标明哪一步离开 TSCC。

<details><summary>答案</summary>

①守 TSCC → ②C_RAND → ③可选 AHOY/ACK → ④Channel Grant → ⑤改频到 Payload 再 Header/超帧。**离开 TSCC 发生在拿到 Grant 之后、进入 Payload 之时。**

</details>

**题 3.** Dedicated TSCC 与 Non-Dedicated TSCC 各用一句现场话说清；并写一个分诊问题。

<details><summary>答案</summary>

Dedicated：专职前台，控制逻辑信道主要干管理。Non-Dedicated：控制与业务共享形态，更省资源但「控制是否一直在」要问清。分诊问题：「本站控制是专用还是共享？」

</details>

**题 4.** 为什么说 Channel Grant「不要求 ACK」却还常在空口重复？对弱场有什么含义？

<details><summary>答案</summary>

学习口径（速览 §1）：Grant 不要求确认，为提高听到概率而常重复发送。弱场含义：漏听小票 → MS 不改频 → 业务侧已有人说话、漏听方却静音；分诊先回放控制下行是否连发、MS 是否跟票。

</details>

**题 5.** 填写：PV_GRANT 与 TV_GRANT 的代表 CSBKO；并各用四字说明业务味道。

<details><summary>答案</summary>

PV_GRANT = `110000`（个呼语音）；TV_GRANT = `110001`（组呼语音）。细字段差异见第 33 课，本课认名+认码即可。

</details>

**题 6.** 判断：分析仪在 TSCC 上看见 TV_GRANT，即可按第 30 课 CP2 开始数超帧 A–F。（对 / 错）并改写正确动作。

<details><summary>答案</summary>

**错。** 正确动作：记录 Grant 中的逻辑物理信道 + 时隙 + 地址 → 改守 Payload → 再按第 30 课认 Header/超帧。

</details>

**题 7.** Part1/2/3/4：下列问题各去哪本？①CSBK 外壳 bit 布局②组呼 Voice Channel User LC③业务信道确认数据④TSCC 上的 Aloha/Grant。

<details><summary>答案</summary>

①Part1 ②Part2 ③Part3 ④Part4（速览 §12）。

</details>

**题 8.** 现场：「同事把 Grant 时间戳和 Voice LC Header 画在同一条常规中继轴上」——你如何纠偏？再补一句调制提醒。

<details><summary>答案</summary>

纠偏：常规轴是 Tier II「固定房间直接 Header」；集群轴是「TSCC 小票 → Payload 再 Header」。两套发车故事不要对齐成一条。调制提醒：选错故事轴不改变 12.5 kHz/4FSK/双时隙——先纠房间与阶段，再查射频。

</details>

**题 9.（加分）** P_GRANT 与 TSCC 上的 PV/TV_GRANT 差在哪一个「房间」？为何本课只给一句指针？

<details><summary>答案</summary>

P_GRANT 出现在**业务信道**（客房内再授予/换房）；PV/TV_GRANT 典型是 **TSCC 前台**发的首张进房小票。本课目标是钉控制 vs 业务，不展开全部 Grant 变体（第 33 课）。

</details>

**题 10.（加分）** 写出 Logical Physical Channel Number 与 Logical Channel Number 各管什么；`0xFFF` 对本课意味着什么（不写公式）？

<details><summary>答案</summary>

前者：12-bit 房间逻辑号（哪条业务逻辑信道）；后者：1-bit 时隙门（ch1/ch2）。`0xFFF` 常表示「逻辑号不够，看绝对频率附块 CG_AP」——公式与 Annex C 留给第 36 课，本课只认「有附块这条岔路」。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `04-集群协议/集群协议字段速览.md` **§1** | TSCC / Dedicated / Payload / Grant 概念总图（本课 canonical） |
| 2 | 同上 **§2** | 控制 PDU 地图（出站 Grant/Aloha/Ahoy…；入站 RAND…） |
| 3 | 同上 **§3** | Grant 代表表（PV/TV 字段骨架；变体指针） |
| 4 | 同上 **§4** | C_ALOHA 代表表（**只扫一眼**；过程 → 第 32 课） |
| 5 | 同上 **§12** | Part1/2/3/4 分工（防串读） |
| 6 | `总索引.md` **集群 / Tier III** | 门牌：TSCC/Grant → 速览 → Reason/Grant 加厚 → Part4 PDF |
| 7 | `04-集群协议/ReasonCode与Grant变体.md` | **仅地图指针**：下节课才深挖；本课别整文件通读 |
| 8 | `学习推送/第9课.md` | Tier I/II/III 全貌回唤 |
| 9 | `学习推送/第25课.md` / `第30课.md` | 常规语音时间线（进 Payload 后接着用） |
| 10 | `学习推送/第11课.md` | 文档地图：Part4 管集群 |
| 11 | `04-集群协议/TS102361-4_V1.12.1.pdf` | 官方集群原文（硬冲突以 TS 为准） |
| 12 | `DMR整合学习手册.md` | 全貌与 Tier 边界 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「停错控制/业务」当成调制故障 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。登记/Aloha 过程、Grant 全变体、Reason 全表、鉴权、绝对频率、Hunt/拨号/Stun：**永远回对应课 / PDF**，本课不补第二份。

---

## 12. 下一课预告

**第 32 课 · 登记与 Aloha**

本课把门钉在「前台 vs 客房 + Grant 小票」。下一课留在前台，把 **登记（我在哪个站/是否允许活跃）** 和 **Aloha（排队规则告示：Mask、Backoff、Reg 位…）** 讲清楚：为什么有的台「没登记就叫不动」、Aloha 广播到底在管什么。仍然少公式；不抢第 33 课的 Grant 全地图，也不抢第 34 课的 Reason 全表。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-03**（晚间推送）检索核验；真实用 HTTP 头/跳转核验过可达（协会镜像 / Tait Academy / GopherTrunk / 产品页等，**ETSI deliver 直链对部分自动化抓取返回 403，故 Part4 以 DMRA 协会镜像为准**）。**不编造地址**。策略 = **Part4 协会镜像 PDF + DMRA Tier III 现状讲稿 + Tait Academy「Channel Operation」+ Tait「Physical and Logical Channels」+ Tait Intro Study Guide + DMRA 标准目录 + Benefits 白皮书 + GopherTrunk CSBK 参考（控制信道 Grant 语感）+ Hytera Tier III 系统页（控制/业务白话）**。另检索公开「control channel vs traffic/payload channel」专题视频：Tait 有 **DMR Tier 3 Introduction** 营销向短片（YouTube 可打开），但是 **效用/行业卖点介绍**，**不是**「TSCC vs Payload + Grant 转台」技术对照课；未找到达到本课深度的独立优质技术短片。**video_found=false**（诚实备注：有 Tier III 概论片，无专门对照片）。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMRA 协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - **为什么值得看**：Tier III 控制/业务、Dedicated/Non-Dedicated、Grant/Aloha 等硬出处；与速览 §1–§3 对照。  
   - **库内副本**：`dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。  
   - **怎么用**：先读系统模型与控制信道模式章节，再回本课总图；**不要**第一天啃完所有 Annex。

2. **[State-of-the-art of ETSI DMR Tier III Standard（DMRA 讲稿 PDF）](https://dmrassociation.org/public-downloads/documents/State-of-the-art-of-ETSI-DMR-Tier-III-Standard-Critical-Comms-Russia-18Apr-2019.pdf)**  
   - **为什么值得看**：用幻灯节奏扫过 Dedicated/Non-Dedicated、控制信道能力、与 Part1–4 关系；适合阶段 E 开门建立「集群功能地图」。  
   - **怎么用**：当「导游图」，细节仍回 Part4 / 速览。

3. **[Tait Radio Academy · Channel Operation](https://www.taitradioacademy.com/topic/dmr-channel-operation-1/)**  
   - **为什么值得看**：白话解释站点上控制信道常落在哪条物理信道/时隙、控制信道主要管登记/呼叫请求/分配逻辑信道/广播系统信息——与本课「前台」比喻同向。  
   - **怎么用**：读完立刻用本课分诊表问自己：分析仪该钉控制还是跟业务。

4. **[Tait Radio Academy · Physical and Logical Channels](https://www.taitradioacademy.com/topic/dmr-physical-and-logical-channels-1/)**  
   - **为什么值得看**：明确 Tier III 上 control vs traffic（payload）逻辑信道分类；多站呼叫时每站业务信道的直觉。  
   - **怎么用**：对照本课术语表「Logical Physical Channel / slot」。

5. **[Tait · Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：Tier III 控制信道 + 业务信道、Channel Grant 建立语音的一段经典叙述（PTT→控制请求→Grant→改到 traffic 通话）。  
   - **怎么用**：当英文版「总图朗读」；与本课 §2 ASCII 对读。

6. **[DMR Association · Standards 目录](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：Part1–4 / TR 下载入口总台；阶段 E 以后找官方 PDF 少迷路。  

7. **[DMR Association · Benefits and Features of DMR（白皮书）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：Tier 分层与容量/双时隙语境；帮新人把「为什么要集群」说给领导听。  
   - **怎么用**：不替代 Part4；当背景阅读。

8. **[GopherTrunk · CSBK 参考](https://gophertrunk.org/reference/csbk/)**  
   - **为什么值得看**：强调 Tier III 控制信道上 CSBK 承载请求与 **channel grant**，解码器靠跟 Grant 跳到正确业务信道+时隙——与本课「分析仪要跟票走」同向。  
   - **怎么用**：当实现/监听语感；字段冲突仍以 ETSI / 速览为准。

9. **[Hytera · DMR Tier 3 Trunking 系统页](https://www.hytera.us/systems/dmr-tier-3-trunking-systems/)**  
   - **为什么值得看**：厂商白话：专用控制信道注册与请求，其余为共享 traffic channel。  
   - **怎么用**：产品叙事；与标准术语对照时以 Part4 为准。

**视频备注（诚实）**：公开可核验的 Tait「DMR Tier 3 Introduction」等短片偏行业价值介绍，**未**按「控制信道 vs 业务信道 + Grant 转台检查点」展开；故本课 **video_found=false**。若日后协会/学院上架专项技术片，再补进进度外链清单。

---

## 本课收束

阶段 E 开门就一件事：**分清前台与客房。**  
前台（TSCC）发号令、发小票；客房（Payload）才跑你已经会的第 30 课语音超帧。  
分析仪要跟票走；Grant 不是「已经在说话」；调制账本仍是 12.5 kHz / 4FSK / 双时隙。  
下一站留在前台：登记与 Aloha。
