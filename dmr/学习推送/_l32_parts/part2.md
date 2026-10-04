## 4. 机制拆解：C_ALOHA 告示牌（本课够用的厚度）

Canonical 来源：`集群协议字段速览.md` **§4**（Table **7.19**）；共享位对照 `Announcement与其余枚举.md` **§10**；TR 附录对 Mask/Service Function/Backoff 的直觉见 `00-入门/TR附录_省电接入功率.md` **B.2**（冲突仍以 **TS Part4** 为准）。下列**故意不画完整 SDL、不贴 FEC**。

### 4.1 先认壳：仍是 Part1 CSBK，Opcode 在 Part4

| 项 | 学习口径 |
|----|----------|
| 外壳 | Part1 CSBK：LB\|PF\|CSBKO\|FID\|… |
| CSBKO | **`011001`** = C_ALOHA |
| FID | 标准业务多为全 0（SFID） |
| 方向 | **TS → MS**（出站告示） |
| 和 BCAST 重叠的位 | Reg / Backoff / System Identity；MassReg 里还有同类 Mask（§10） |

口诀：**外壳认 Part1；告示语义认 Part4。** 第 29 / 31 课书架习惯继续用。

### 4.2 Table 7.19 字段走读（学习口径，不背矩阵）

| IE | Len | 白话（本课） |
|----|-----|--------------|
| LB / PF | 1+1 | LB=`1`（单块 Aloha） |
| CSBKO / FID | 6+8 | `011001` / SFID |
| Reserved | 1 | `0` |
| **TSCCAS** | 1 | 本 TSCC 是否正支持 TSCCAS |
| **Site Timeslot Synchronization** | 1 | 站点 TSCC 与业务信道是否时隙同步 |
| **Version** | 3 | 本 Part4 文档版本控制（枚举表见 Announcement §9.3；资料库 PDF 为 V1.12.1） |
| **Offset** | 1 | TSCC aligned / offset |
| **Active_Connection** | 1 | TS 是否连网 |
| **Mask** | 5 | 地址掩码 → **细分争用人口** |
| **Service Function** | 2 | **允许的业务功能类**（可收窄按铃种类） |
| **NRand_Wait** | 4 | 随机等待参数 |
| **Reg** | 1 | **`1`=要求 MS 登记后才可活跃** |
| **Backoff** | 4 | 退避号 |
| **System Identity Code** | 16 | 系统身份 |
| **MS Address** | 24 | 可指向特定 MS（与 Mask 联用；Mask=24 时仅该台） |

**必背三句：**

1. **Reg 位**决定「要不要先办入住才能在这站活跃」。  
2. **Mask +（可选）MS Address** 决定「这轮允许谁挤门」。  
3. **Backoff / NRand_Wait / Service Function** 决定「怎么排队、允许多宽的业务按铃」——不是装饰字段。

### 4.3 Reg 位：Aloha / CACH / C_BCAST 应一致

速览 §4 / §5 / §9：

- Reg 亦出现在 **CACH**、**C_BCAST**；与 C_ALOHA **应一致**（clause **6.4** 学习口径）。  
- 现场若 Aloha 说 Reg=1、某处广播却像 Reg=0——先当**录波/解码/站点异常**分诊，不要用「以显示为准」和同事吵架。  
- **Aloha 没有 Reason Code**（Announcement §10）。拒绝理由走 ACK/NACK 族，不在 Aloha 里「夹带判决书」。

### 4.4 Service Function vs Service_Kind（别串）

| | 出现在 | 管什么 |
|--|--------|--------|
| **Service Function**（2 bit） | **C_ALOHA** | 当前告示允许哪**类**功能去随机接入（TR 附录直觉：可收到「仅登记」等） |
| **Service_Kind**（4 bit） | **C_RAND / C_AHOY / C_ACKVIT** | 这一枪具体要什么服务（语音/数据/登记类 `1110₂`…） |

口令：**告示牌用 Service Function 收窄大门；按铃单用 Service_Kind 写清要办的事。**

---

## 5. 登记过程（学习口径，不 dump MSC）

Canonical：速览 **§9**；Service_Kind 表：Announcement **§6**；MassReg：Announcement **§3.5**。

### 5.1 为什么要登记？

| 场景 | 白话 |
|------|------|
| 宽区域网 | 系统要知道 MS **在哪个站/区域**，呼叫才能找对人 |
| 单站 | 也可用来判断 MS **是否活跃 / 是否允许在本 TSCC 活跃** |
| Reg=1 站 | 未登记却要业务 → 前台常直接挡（指针：`MS_Not_Registered`） |

### 5.2 Reg=0 vs Reg=1

| Reg | MS 侧学习口径 | 现场别误解 |
|-----|----------------|------------|
| **0** | MS **不应主动寻求登记** | ≠ 「系统坏了」；≠ 「永远禁止登记」；可能是策略上不要求主动登记 |
| **1** | **须登记后**才在该 TSCC 上活跃 | = 「先办入住再点餐」；PTT 前先完成登记路径 |

### 5.3 两条登记驱动路径（本课地图级）

```text
  路径 A · 随机接入登记（常见「自己去办」）
    读 Aloha(Reg=1) → 选隙 → C_RAND(Service_Kind=`1110₂`)
    → TS 回 C_ACKD / C_NACKD / …（或先 AHOY）
    → 成功后可再请求语音/数据

  路径 B · C_AHOY 驱动（前台点名「你来办/你应答」）
    TS 出站 C_AHOY（Service_Kind 随场景；登记后续在 6.4 过程族）
    → MS 必须响应（C_ACKU / …）
    → 本课认「点名可驱动登记后续」；鉴权挑战细节 → 第 35 课
```

速览 §9 原句口径：**登记可用随机接入（C_RAND + Service_Kind=登记类）或由 C_AHOY 驱动。**

### 5.4 Mass Registration（大规模重登记）指针

Announcement §3.5（Tables **7.76 / 7.77**）：

| 子场 | 作用 |
|------|------|
| **Reg_Window** | 登记时间窗；`0`=**取消**大规模登记；其它值对应 Treg_Window 秒档 |
| **Aloha Mask** | 与 C_ALOHA Mask **同类**，把重登记人口切开 |
| 地址 | ADRNULL 或指定 MS 个号 |

过程锚点学习口径：6.4.6 / 6.7.1.5；**MS 用 Reg_Window + Mask 决定何时重登记**。  
现场：凌晨/割接后控制面突然「很热闹」——先问有没有 MassReg，再开「控制信道射频故障」单。

### 5.5 Denied Registration List（拒绝列表）指针

速览 §9：MS 可维护 **Denied Registration List**（被否决区域缓存）并**老化**。  
定时器资料里有 **T_DENREG**（Denied Registration 表项寿命）指针——本课只要知道：**被否决 ≠ 永远死在该站**；有老化/再试策略，细节回库，不在本课展开全表。

登记失败相关 Reason 名（**仅路标，全表第 34 课**）：`Reg_Refused` / `Reg_Denied`；未登记却要业务：`MS_Not_Registered`。

### 5.6 登记类 Service_Options 一句（不深挖）

Announcement §8.4（Table **7.55**）登记选项里有 IP_Inform、PowerSave_RQ、Reg_Dereg 等组合。本课只要知道：**C_RAND 的 Service_Options 在登记场景有专用布局**；逐 bit 对照留给加深阅读，不在本课默写。

---

## 6. 随机接入直觉：Mask / Backoff / 碰撞再试

Canonical：速览 §1「Random access」、§4；TR 附录 B.1–B.2（冲突以 TS 为准）。**不 dump 完整 SDL / 抽槽状态机。**

### 6.1 为什么需要 Aloha「规则」？

TSCC 入站是多台 MS **争用**的：大家都想按铃（登记、呼叫、短数据…）。没有规则就会撞成一团。Aloha 系列思想（历史背景：随机发、撞了再随机退）在 DMR Tier III 里落成：**由出站 C_ALOHA 广播参数，MS 按参数选隙、退避、限制谁可接入。**

```text
  多台 MS 想入站
       │
       ▼
  读 Aloha：Mask 是否轮到我？Service Function 是否允许我这类业务？
       │
       ▼ 是
  按 NRand_Wait / Backoff 等规则选时隙发 C_RAND
       │
       ├─ 成功路径：TS 听见 → ACK/AHOY/Grant…
       └─ 碰撞/无应答：按 Backoff 等再试（次数/优先级常数见 Annex 定时器指针，本课不背全表）
```

### 6.2 Mask：把争用人口切开

- **Mask** = 地址掩码思路：只允许地址满足条件的 MS 参与本轮随机接入。  
- 可从「几乎大家都能来」收到「只剩一台」（与 **MS Address**、Mask=24 等联用的学习口径见速览 §4）。  
- MassReg 里的 **Aloha Mask** 同族：大规模重登记时用来**摊峰**，避免整网同一秒挤爆。

现场口令：**控制面「忽然变安静/忽然很挑台」——先看 Mask 是否在收窄，再骂射频。**

### 6.3 Backoff / NRand_Wait：撞了怎么退

| 参数 | 白话 |
|------|------|
| **Backoff** | 退避号：拉长「再试」的节奏，减轻持续碰撞 |
| **NRand_Wait** | 随机等待参数：配合选隙/等待；开机默认等常数见定时器表指针（如 NDefault_NW） |

TR 附录直觉（B.2）：首次可尽快发；其后因 Mask / Service Function / 抽槽 / 无应答等而退避重试。  
**本课不展开「抽槽（Withdrawn slots）状态机」**——知道 Aloha 本身不抽槽、但系统可用其它机制保护应答时隙即可（TR B.1 一句指针）。

### 6.4 和「经典 Aloha / 时隙 Aloha」背景怎么对齐？

公开资料里的 Aloha / slotted Aloha 讲的是：**共享信道上随机发、碰撞、随机再试**。DMR 的 C_ALOHA **借用这个名字与思想**，但字段与过程以 **ETSI TS 102 361-4** 为准。  
读维基/教材时请贴标签：**背景直觉 OK；Opcode/Reg/Mask 细节以本库速览 + Part4 为准**（冲突规则：**TS > TR > 博客/幻灯/课文**）。

---

## 7. 对照表：第 31 课「要房间」vs 本课「先入住」

| 维度 | 第 31 课 | 本课 |
|------|----------|------|
| 前台主题 | Grant = 房间号小票 | **登记 = 入住；Aloha = 告示牌** |
| 关键成功门牌 | Channel Grant | 登记成功（ACK 路径）+ 之后才 Grant |
| 分析仪第一刀 | TSCC or Payload？ | **Aloha Reg？有无登记类 C_RAND？ACK/NACK？** |
| 常见误诊 | 在 TSCC 找 Header | 看见 Aloha 就当「已登记」 |
| 文档入口 | 速览 §1–§3 / §12 | 速览 **§4 / §8 / §9** + Announcement §3.5/§6/§10 |
| 下一课边界 | 本课 | 第 33 Grant 变体；第 34 Reason 全表 |

和第 31 课 E0–E3 检查点咬合：E0「听前台活着」本课加厚为 **「读懂 Aloha 告示」**；E1 的 C_RAND 要先会分 **登记类 vs 语音类**。

---

## 8. 现场岗位对照 / 分诊

| 岗位现象 | 先做的分诊动作 | 常翻 | 别一上来就 |
|----------|----------------|------|------------|
| 「PTT 了没反应 / 叫不动」 | 问：Aloha **Reg**？本机是否已完成登记？有无登记类 C_RAND？ | 本课 §2/§5；速览 §4/§9 | 先改功放/天线 |
| Aloha 一直在，仍无呼叫 | 读 Mask / Service Function：是否根本不让你这类业务按铃？ | §4.2；TR B.2 | 断言「控制信道死了」 |
| 见 C_RAND 立刻 NACK | 记 Reason 名：是否 `MS_Not_Registered` / `Reg_*` 指针？ | 第 34 课入口；本课术语表 | 当 Grant 故障 |
| 「没登记」三方扯皮 | 对齐：Reg 位证据 + 登记 RAND 证据 + ACK/NACK 证据 | 本课总图 | 只对系统码对骂 |
| 凌晨控制面挤爆 | 查 C_BCAST 是否 **MassReg**；Reg_Window/Mask | Announcement §3.5 | 直接换控制机柜 |
| 台在 A 站活、B 站死 | 问：B 站 Reg 策略？Denied List？系统身份是否同一网？ | §5.5；System Identity | 先判终端硬件坏 |
| 只看见 Aloha 不见 RAND | 问：Mask 是否排除该地址？弱场入站？Backoff 仍在等？ | §6 | 用第 30 课找 Header |
| 把 Aloha 当 Grant | 纠正：告示 ≠ 小票；CSBKO `011001` ≠ Grant 族 | 第 31 §4.3；本课 §4 | 开「有小票不进房」错单 |
| Reg=0 还强迫登记 | 纠正：Reg=0 → MS **不应主动寻求登记** | 速览 §9 | 写「强制登记」工单硬拧 |
| 领导问「登记有啥用」 | 一句话：让系统知道人在哪站、允不允许活跃，否则呼叫找不到人 | §5.1 | 背条款号 |

分诊口诀：**先读 Aloha 告示（Reg/Mask/SF）→ 再找登记类 C_RAND → 再看 ACK/NACK 路标 → 再谈语音 RAND/Grant → 最后才碰射频与写频。**

---

## 9. 工作例子（10 则）

**例 1 · 干净路径：Reg=1 → 登记 → 再要房间**  
空口：C_ALOHA(Reg=1) → C_RAND(Service_Kind=`1110`) → C_ACKD → 再 C_RAND(语音) → TV_GRANT → Payload。  
向领导一句话：「先办入住，再拿房间小票。」

**例 2 · 未登记就 PTT**  
Reg=1，MS 直接发语音类 C_RAND，TS 回 `C_NACKD(MS_Not_Registered)`。  
分诊：不是「没有集群」，是**跳过入住**。动作：完成登记路径后再试。Reason 细表 → 第 34。

**例 3 · 看见 Aloha 就宣布「已登记」**  
控制下行 Aloha 很漂亮，该 MS 从未出现登记类 RAND/ACK。  
纠偏：Aloha 是**告示**，不是**入住回执**。

**例 4 · Mask 收窄：只有部分台能按铃**  
拥塞时 Aloha Mask 变严，某地址段暂时挤不进。  
分诊：先对比前后 Aloha 解码；别第一句换天线。

**例 5 · MassReg 窗口**  
C_BCAST Announcement_type=MassReg，Reg_Window≠0，台站分拨重登记。  
分诊：控制面「忙」可能是**策略性重登记**，用 Window+Mask 摊峰；取消时 Window=`0`。

**例 6 · Reg=0 站还在「催登记」**  
写频/运维误解 Reg 极性。  
纠偏：速览 §9——Reg=0 → MS **不应主动寻求登记**；Reg=1 才是「须登记后活跃」。

**例 7 · AHOY 点名登记后续**  
未见 MS 主动登记 RAND，先见 C_AHOY，再 MS 应答。  
分诊：路径 B（Ahoy 驱动）；仍在前台，**不是 Grant**。鉴权若夹在后续 → 第 35 课边界。

**例 8 · Denied List 味道**  
某站反复 Reg_Denied 后，MS 短期内不再死磕该站。  
分诊：想起 Denied Registration List + 老化；别当「终端永久坏了」。全码与过程 → 库 + 第 34。

**例 9 · Service Function 只开「登记门」**  
告示把功能类收窄，语音 RAND 暂时不被允许，登记 RAND 仍可见。  
分诊：分清 Service Function（告示）与 Service_Kind（按铃单）；对照 §4.4。

**例 10 · 分析仪时隙/系统身份看错**  
Aloha 的 System Identity 与写频不一致，或停错 TSCC 时隙。  
分诊：先对齐「是不是这套系统的告示牌」，再谈登记失败。调制仍最后背锅。

---

