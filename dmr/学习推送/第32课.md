# 第 32 课 · 登记与 Aloha

> DMR 深入学习 · **阶段 E · 集群 Tier III 第 2 课（约 10 课之二）**（接第 31 课「控制信道 vs 业务信道」）  
> 适合：已经会画「守 TSCC → RAND → Grant → 进 Payload 说话」总图，但现场一听「没登记」「Aloha Reg 位」「PTT 叫不动」就懵——把 **登记 = 前台入住登记**、**Aloha = 排队规则告示牌** 钉成肌肉记忆——的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**Reg=1 先登记再活跃；Aloha 管 Mask/Backoff/NRand_Wait/Service Function；未登记却要业务 → 常撞 `MS_Not_Registered`**」钉牢  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。**换登记/Aloha 故事，不改射频账本**——PTT 无声、Aloha 看得见却叫不动、登记失败，都不等于「调制坏了」。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是 **阶段 E 第 2 站：留在 TSCC 前台——登记（入住）+ Aloha（排队告示）**。

---

## 1. 为什么本课重要（动机）

第 31 课把门钉在「前台 vs 客房 + Grant 小票」。机房下一句要命的话往往是：

- 同事喊：「这台机 PTT 了，怎么没有叫号？」——分析仪在 TSCC 上能看见 Aloha，却看不见这台机的 C_RAND；或者见了 RAND，立刻来一记 NACK。  
- 调度台说「未登记」；写频同事说「系统码对啊」；监听员说「Aloha 一直在」——三个人各说各的对，却对不上同一条分诊链。  
- 屏上 Aloha 的 **Reg 位** 有时是 0、有时是 1：有人说「Reg=0 就不能登记」；有人说「Reg=1 才是要求登记」。谁对？  
- 凌晨站点做了 **Mass Registration**（大规模重登记），一堆台同时挤登记窗——你却当「控制信道堵死了」开射频单。  
- 新人把 Aloha 当成「站点心跳广告」就完事，从不读 Mask / Backoff / NRand_Wait——拥塞时只会骂「随机接入坏了」。

培训台若只背「集群要先登记」六个字，后面会卡在同一处：

> **会背「要登记」≠ 会分诊。** 分诊 = 先问「Aloha/CACH 的 Reg 位要不要登记？」→ 再问「有没有看见登记类 C_RAND（Service_Kind=`1110`）？」→ 再问「ACK 还是 NACK？若 NACK，是不是 `MS_Not_Registered` 一类指针？」→ 最后才碰写频系统码与射频。本课不是把 Part4 登记 MSC / Aloha SDL 全文 dump，而是把 **入住登记 + 排队告示牌** 钉成可现场演示的第二张地图。

本课目标：能画出「守 TSCC → 读 Aloha →（Reg=1 则须登记）→ C_RAND(登记类) → ACK/AHOY 路径 → 然后才可请求语音」总图；会说 Reg=0 / Reg=1 各是什么味道；会把 Aloha 当「前台告示牌」而不是「可忽略的心跳」；会认 Mask / Backoff / NRand_Wait / Service Function / System Identity / 可选 MS Address；会做现场分诊、例子与自测；并为第 33 课「Grant 变体地图」、第 34 课「Reason Code」留好边界感。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不贴完整 SDL、不发明 ETSI 条款号（入口锚点以资料库 `04-集群协议/集群协议字段速览.md` **§1 / §4–§6 / §8–§9 / §12**、`Announcement与其余枚举.md` **§3.5 MassReg / §6 Service_Kind / §10 Aloha 共享位**、`总索引.md` **集群 / Tier III** 已有编号为准）、**不铺开 Grant 全变体地图**（第 33 课）、**不 dump Reason Code 全表**（第 34 课；本课只用 `MS_Not_Registered` 等作指针）、**不讲鉴权/RC4**（第 35）、**不深挖 CHAN 绝对频率**（第 36）、**不讲 Hunt/拨号/Stun**（第 37–39）。本课只钉 **登记 + Aloha 排队规则**。

---

## 2. 总图 / 故事：「入住登记 + 排队告示牌」

先把整课装进旅馆故事，再落到 `集群协议字段速览.md` **§1 / §4 / §9** 与第 9 / 25 / 30 / 31 课回唤。

### 2.1 一句话故事：前台入住 + 告示牌

第 31 课把 Tier III 想成旅馆：**前台（TSCC）发号令、发房间小票；客房（Payload）才说话。** 本课仍站在前台，只把两块牌子钉清楚：

1. **入住登记（Registration）** = 旅馆要知道「你在哪个站 / 你是否允许在本站活跃」。宽区域网靠它定位 MS；单站也可用来判断「这台机还活不活、允不允许活跃」。  
2. **Aloha 告示牌（C_ALOHA）** = 前台墙上的排队规则：谁可以按铃（Mask / 可选 MS Address）、允许哪类业务按铃（Service Function）、要等多久再试（Backoff / NRand_Wait）、**要不要先登记才能活跃（Reg 位）**、本站系统身份（System Identity Code）、站点是否支持 TSCCAS 等。  
3. **按铃仍是 C_RAND** = 登记、语音、数据……都走随机接入请求壳；差别在 **Service_Kind**（登记类学习口径 = `1110₂`，见 `Announcement与其余枚举.md` §6）。  
4. **前台可能点名（C_AHOY）** = 登记后续、可达性检查等可由 Ahoy 驱动（过程 → 速览 §6 / §9）；本课认形状，不展开鉴权挑战。  
5. **Mass Registration** = 旅馆广播「大家在窗口内重新办一次入住」（C_BCAST Announcement_type=`MassReg`）；用 Reg_Window + Mask 把人潮摊开——不是射频坏了。

口诀：**先读告示牌（Aloha）→ Reg=1 就先办入住（登记）→ 办完再按铃要房间（语音 RAND）→ 再谈 Grant 小票进客房。没读告示就 PTT，常被前台挡在门外。**

### 2.2 总图：从 Aloha 到「可以请求语音」

```text
  时间 →

  ┌─ 守 TSCC（第 31 课：露营前台）────────────────────────┐
  │  听 C_ALOHA / C_BCAST / Grant 广播流                   │
  │  本课重点：把 Aloha 当「告示牌」读完再行动               │
  └──────────────────────┬─────────────────────────────────┘
                         ▼
  ┌─ 读 Aloha（C_ALOHA · CSBKO=`011001`）─────────────────┐
  │  Reg / Mask / Backoff / NRand_Wait / Service Function   │
  │  System Identity Code / TSCCAS / 可选 MS Address …      │
  └──────────────────────┬─────────────────────────────────┘
                         ▼
          ┌──────────────┴──────────────┐
          │ Reg = 0                     │ Reg = 1
          │ MS 不应主动寻求登记         │ 须登记后才在该 TSCC 活跃
          │ （仍听告示；别误当成「禁网」）│
          └──────────────┬──────────────┘
                         ▼（Reg=1 路径）
  ┌─ 登记请求：C_RAND（Service_Kind=`1110₂` 登记/鉴权/注销/MS check）─┐
  │  随机接入争用：受 Mask / Backoff / NRand_Wait 约束                 │
  │  （鉴权细节 → 第 35 课；本课只认「登记类按铃」）                     │
  └──────────────────────┬────────────────────────────────────────────┘
                         ▼
  ┌─ 前台回应：C_ACKD / C_NACKD / … 或 C_AHOY 驱动后续 ────┐
  │  成功：登记完成，可再发语音/数据类 C_RAND               │
  │  失败指针：如未登记却要业务 → C_NACKD(MS_Not_Registered)│
  │  Reason 全表 → 第 34 课；本课只认名字当路标             │
  └──────────────────────┬─────────────────────────────────┘
                         ▼
  ┌─ 然后才走第 31 课「要房间」故事 ───────────────────────┐
  │  C_RAND(语音/数据) →（可选 AHOY/ACK）→ Grant → Payload │
  └────────────────────────────────────────────────────────┘

  旁路指针：C_BCAST MassReg（大规模重登记）
    → Reg_Window + Aloha Mask 摊人潮（Announcement §3.5）
```

极简对照（速览 §1 / §9 同款）：

```text
  学习口径：
    MS 守 TSCC，读 C_ALOHA
    若 Reg=1 → MS --C_RAND(Service_Kind=登记类)--> TSCC
    TSCC --C_ACKD / C_AHOY / C_NACKD…--> MS
    登记成功后 → 再 C_RAND(语音/…) → Grant → Payload
```

### 2.3 和第 9 / 25 / 30 / 31 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 9 | Tier I/II/III 全貌——本课把 III「控制面要不要先登记」摸清楚 |
| 第 11 | Part1–4 文档地图——登记/Aloha **认 Part4** |
| 第 15–24 | 时隙/突发/CSBK 外壳——Aloha/RAND 仍是 CSBK 壳 |
| 第 25 / 30 | Tier II 常规语音时间线——进 Payload 后仍用；本课在前台更早一步 |
| 第 31 | TSCC vs Payload + Grant 小票——本课补「进前台之后、要小票之前」的入住与排队 |
| **本课** | **登记 + Aloha 告示牌 = 阶段 E 第 2 站** |
| 第 33（预告） | Grant 变体地图——小票种类细表 |
| 第 34（预告） | Reason Code——拒绝/排队理由细表（含登记相关码） |

四句话串起来：

1. **第 31 课**：人先在前台；门牌第一步是 Grant。  
2. **本课**：前台墙上有 Aloha 告示；Reg=1 时，**没办入住就别想要房间**。  
3. **分析仪**：只看见 Aloha 心跳 ≠ 这台机已登记；要看有没有登记类 C_RAND + ACK。  
4. **射频账本不变**：仍是 12.5 kHz / 4FSK / 双时隙——换的是**前台手续**，不是调制。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；登记/Aloha 发生在 **TSCC** 上，不另发明一套射频尺子。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**；随机接入争的是**入站时隙机会**，不是「换调制」。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps** 毛速率——告示牌与登记请求比特语义不同，**调制方式相同**。  
4. **解调直觉**：先问「我在 TSCC 吗？」→ 再认 Aloha 的 Reg/Mask → 再认 C_RAND 的 Service_Kind → 最后才怀疑天线。  
   **PTT 无声 ≠ 「射频没解调」**，也可能是：Reg=1 未登记、登记 NACK、Mask 没轮到你、Backoff 还在等、或分析仪根本没看登记类 RAND。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **Registration / 登记** | 向系统声明「我在这站 / 我要活跃」；宽区定位 + 单站活跃检查 | ≠ Grant；≠ 已经在通话；≠ 鉴权全文（第 35） |
| **Reg 位** | Aloha / CACH / C_BCAST 上的 1 bit：`1`=须登记后才可活跃；`0`=MS **不应主动寻求登记** | ≠ 「Reg=0 禁止入网」的口号；与三处应一致（clause **6.4** 学习口径） |
| **C_ALOHA** | 出站随机接入参数广播（告示牌）；CSBKO=`011001`；Table **7.19** | ≠ Channel Grant；≠ Reason Code 载体（Aloha **没有** Reason） |
| **Mask** | 5 bit 地址掩码：细分谁可以参与这次随机接入争用 | ≠ Colour Code；≠ System Identity |
| **Backoff** | 4 bit 退避号：碰撞/未获应答后怎么拉长再试节奏 | ≠ Hangtime；≠ 业务信道静默 |
| **NRand_Wait** | 4 bit 随机等待参数：配合随机接入选隙/等待 | ≠ Backoff 的别名；两者常一起出现在 Aloha |
| **Service Function** | 2 bit：当前允许哪类业务功能去按铃（如可收窄到「仅登记」味道） | ≠ Service_Kind（后者在 C_RAND/AHOY 里选具体服务） |
| **TSCCAS** | Aloha 中的 1 bit：本 TSCC 是否正支持交替控制时隙类能力 | ≠ Dedicated/Non-Dedicated 全文；一句认标志即可 |
| **System Identity Code** | 16 bit 系统身份；Aloha/BCAST 等携带，帮 MS 认「这是哪套系统」 | ≠ Colour Code；≠ 个号 |
| **MS Address（Aloha）** | 24 bit；可与 Mask 配合指向特定 MS（Mask=24 时仅该台） | ≠ Grant 里的 Target/Source 故事轴 |
| **C_RAND** | MS 入站随机接入请求；CSBKO=`011111`；登记也走它 | ≠ Voice LC Header；≠ UU_V_Req（Part2 地图） |
| **Service_Kind=`1110₂`** | 登记/鉴权（及注销）/ MS 无线检查（Table **7.49**） | 本课认「登记类」；鉴权过程 → 第 35 |
| **C_AHOY** | 出站点名；可驱动登记后续等；CSBKO=`011100` | ≠ Aloha 告示；看见 Ahoy ≠ 已 Grant |
| **Mass Registration** | C_BCAST 公告触发大规模重登记；Reg_Window + Mask 摊峰 | ≠ 单台日常登记；≠ 站点倒换全文 |
| **Denied Registration List** | MS 侧缓存「被否决过的登记区域」并老化 | ≠ 永久黑名单口号；寿命指针见定时器资料 |
| **MS_Not_Registered** | Reason 指针：系统要求先登记，MS 未登记却要业务 → 常 `C_NACKD(...)` | **全表 → 第 34 课**；本课只当路标 |

---

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

## 10. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| C_ALOHA CSBKO | **`011001`** | 告示牌（Table 7.19） |
| C_RAND CSBKO | **`011111`** | 入站按铃（含登记） |
| C_AHOY CSBKO | **`011100`** | 点名 / 登记后续等 |
| C_ACKD 族 CSBKO | **`100000`** 等 | 确认/拒绝外壳 |
| C_BCAST CSBKO | **`101000`** | 含 MassReg 公告 |
| Service_Kind 登记类 | **`1110₂`** | 登记/鉴权/注销/MS check（Table 7.49） |
| Reg | **1 bit**：`1`=须登记后活跃 | Aloha/CACH/BCAST |
| Mask | **5 bit** | 争用人口细分 |
| Backoff | **4 bit** | 退避号 |
| NRand_Wait | **4 bit** | 随机等待 |
| Service Function | **2 bit** | 允许的业务功能类 |
| System Identity Code | **16 bit** | 系统身份 |
| MS Address（Aloha） | **24 bit** | 可点名单台（配合 Mask） |
| MassReg Reg_Window | Table **7.77**；`0`=取消 | 大规模登记窗 |
| MS_Not_Registered | Reason 指针 `0010 1101₂`（0x2D） | **全表第 34 课** |
| Part4 官方版本 | **TS 102 361-4 V1.12.1 (2023-07)** | 集群硬出处 |
| 速览主节 | **§4 Aloha / §8 RAND / §9 登记 / §12 分工** | 本课入口 |
| Announcement 主节 | **§3.5 MassReg / §6 Kind / §10 共享位** | 枚举加深 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 换手续不换射频 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |

---

## 11. 十则误区（看见就打回）

1. **「看见 Aloha = 已经登记。」** → Aloha 是告示牌，不是入住回执。  
2. **「Reg=0 表示禁止入网。」** → 学习口径：MS **不应主动寻求登记**；不是「永久封站」口号。  
3. **「Reg=1 只是建议，PTT 一样能叫。」** → Reg=1 站未登记常被挡；典型路标 `MS_Not_Registered`。  
4. **「Aloha 可以当 Grant 读。」** → CSBKO 与语义都不同；告示 ≠ 房间小票。  
5. **「Mask 是 Colour Code。」** → Mask 细分随机接入人口；CC 是另一套同频区分故事。  
6. **「Backoff 就是 Hangtime。」** → 一个管随机接入再试节奏；一个管通话后保持——别混房间。  
7. **「Service Function = Service_Kind。」** → 前者在 Aloha 收窄大门；后者在 RAND/AHOY 写清要办的事。  
8. **「MassReg 等于控制信道故障。」** → 常是策略性大规模重登记；先看 Reg_Window/Mask。  
9. **「登记失败就要学鉴权/RC4。」** → 边界：登记地图本课；鉴权挑战 → 第 35；别抢跑。  
10. **「PTT 无声说明 4FSK/12.5 kHz 坏了。」** → 先读 Reg/登记 RAND/ACK；调制账本最后背锅。

---

## 12. 自测题（含答案）

**题 1.** 用旅馆比喻各一句话解释：登记、Aloha、Grant。

<details><summary>答案</summary>

登记 = 入住登记（系统知道你在哪站/是否允许活跃）。Aloha = 前台排队规则告示牌（Reg/Mask/Backoff…）。Grant = 房间号小票（第 31 课）。先读告示、办入住，再拿小票进客房。

</details>

**题 2.** Reg=0 与 Reg=1 各用速览口径写一句；并写一个现场分诊问题。

<details><summary>答案</summary>

Reg=0：MS **不应主动寻求登记**。Reg=1：须登记后才在该 TSCC 上活跃。分诊问题：「当前 Aloha/CACH/BCAST 的 Reg 是几？有没有登记类 C_RAND + ACK？」

</details>

**题 3.** 写出 C_ALOHA 与 C_RAND 的代表 CSBKO；登记类 Service_Kind 取值。

<details><summary>答案</summary>

C_ALOHA=`011001`；C_RAND=`011111`；登记类 Service_Kind=`1110₂`（登记/鉴权/注销/MS check，Table 7.49）。

</details>

**题 4.** 为什么说「Aloha 没有 Reason Code」？未登记却发业务，常见空口路标是什么？

<details><summary>答案</summary>

Announcement §10：Aloha 不承载 Reason。未登记却要业务 → TS 常用 `C_NACKD(MS_Not_Registered)`。Reason 全表见第 34 课。

</details>

**题 5.** Mask、Backoff、NRand_Wait 各管什么直觉？碰撞后下一步是什么（一句话）？

<details><summary>答案</summary>

Mask：细分谁可参与争用。Backoff：退避节奏。NRand_Wait：随机等待/选隙参数。碰撞或无应答后：按告示参数退避再试（不在本课背完整 SDL）。

</details>

**题 6.** Service Function 与 Service_Kind 差在哪？举一个「大门收窄」的现场说法。

<details><summary>答案</summary>

Service Function 在 **C_ALOHA** 上允许哪类功能按铃；Service_Kind 在 **C_RAND/AHOY** 上声明这一枪具体服务。现场说法：告示暂时只开登记门，语音 RAND 会被挡，但登记 RAND 仍可能看见。

</details>

**题 7.** Mass Registration：哪个 PDU？Reg_Window=`0` 表示什么？为何常配 Mask？

<details><summary>答案</summary>

C_BCAST，Announcement_type=MassReg。Reg_Window=`0` = 取消大规模登记。Mask（Aloha Mask）用来把重登记人口切开、摊峰，避免同时挤爆。

</details>

**题 8.** 判断：分析仪在 TSCC 上持续解码 C_ALOHA，即可认为该 MS 已完成登记。（对 / 错）并改写正确证据链。

<details><summary>答案</summary>

**错。** 正确证据链：Reg 要求（若 Reg=1）→ 看见该 MS 的登记类 C_RAND → 看见成功 ACK（或完成 AHOY 驱动路径）→ 之后才谈语音 RAND/Grant。

</details>

**题 9.（加分）** 画出（文字版）Reg=1 时从空闲到「可以请求语音」的六步骨架。

<details><summary>答案</summary>

①守 TSCC → ②读 Aloha(Reg=1) → ③C_RAND(登记类) → ④ACK/AHOY 路径成功 → ⑤再 C_RAND(语音/数据) → ⑥Grant →（第 31 课）进 Payload。

</details>

**题 10.（加分）** Part1/2/3/4：下列问题各去哪本？①CSBK 外壳②组呼 Voice LC③业务信道确认数据④TSCC 上的 Aloha/登记。

<details><summary>答案</summary>

①Part1 ②Part2 ③Part3 ④Part4（速览 §12）。

</details>

---

## 13. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `04-集群协议/集群协议字段速览.md` **§4** | C_ALOHA Table 7.19 全字段（本课 canonical） |
| 2 | 同上 **§9** | 登记与编址要点：Reg=0/1、Denied List、Mass Reg、双路径 |
| 3 | 同上 **§8** | C_RAND 外壳与 Service_Kind 位置 |
| 4 | 同上 **§6** | C_AHOY：登记后续/点名指针 |
| 5 | 同上 **§1 / §12** | 概念回唤 + Part 分工 |
| 6 | `04-集群协议/Announcement与其余枚举.md` **§3.5** | MassReg / Reg_Window / Mask |
| 7 | 同上 **§6 / §8.4 / §10** | Service_Kind=`1110`；登记 Service_Options；Aloha 无 Reason |
| 8 | `00-入门/TR附录_省电接入功率.md` **B.1–B.2** | Mask/SF/Backoff 直觉（**冲突以 TS 为准**） |
| 9 | `04-集群协议/ReasonCode与Grant变体.md` | **仅路标**：`MS_Not_Registered` / `Reg_*`；全表 → 第 34 |
| 10 | `学习推送/第31课.md` | TSCC vs Payload + Grant（本课前置） |
| 11 | `学习推送/第9课.md` / `第11课.md` | Tier 全貌 / 文档地图 |
| 12 | `总索引.md` **集群 / Tier III** | 门牌导航 |
| 13 | `04-集群协议/TS102361-4_V1.12.1.pdf` | 官方原文（硬冲突以 TS 为准） |
| 14 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「未登记」当成调制故障 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。Grant 全变体、Reason 全表、鉴权/RC4、绝对频率、Hunt/拨号/Stun：**永远回对应课 / PDF**，本课不补第二份。

---

## 14. 下一课预告

**第 33 课 · Grant 变体地图**

本课把门钉在「前台入住 + Aloha 告示」。下一课把第 31 课只认了名字的 **PV / TV / BTV / PD / TD / DX / P_GRANT…** 摊成一张**变体地图**：各小票差在哪几个字段、什么时候会看到附块、业务信道上的再授予怎么认。仍然少公式；不抢第 34 课的 Reason 全表，也不回头把本课登记 MSC 再 dump 一遍。

---

## 15. 推荐阅读与视频

本课外链为 **2026-10-04**（上午推送）检索核验；真实用 HTTP 头/跳转核验过可达（协会镜像 / Tait Academy / GopherTrunk / 维基背景 / 产品页等，**ETSI deliver 直链对部分自动化抓取常返回 403，故 Part4 以 DMRA 协会镜像为准**）。**不编造地址**。策略 = **Part4 协会镜像 PDF + DMRA Tier III 现状讲稿 + Tait「Channel Operation」（明确写控制信道管 registration）+ Tait Study Guide + GopherTrunk Tier III 深潜（C_ALOHA 锁台/SystemID）+ GopherTrunk CSBK payload 参考 + DMRA 标准目录 + Benefits 白皮书 + Hytera Tier III 系统页 + 维基 ALOHAnet（仅随机接入背景，非 DMR 字段课）**。另检索公开「DMR registration + Aloha」专项技术视频：可见 Tier III 概论/营销短片，**未**找到按「Reg 位 + C_ALOHA 字段 + 登记类 C_RAND + MassReg」展开的独立优质技术课。**video_found=false**（诚实备注：有实现向博客与标准 PDF，无对口技术短片）。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMRA 协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - **为什么值得看**：登记过程、C_ALOHA、随机接入、Mass Reg 等硬出处；与速览 §4/§9 对照。  
   - **库内副本**：`dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。  
   - **怎么用**：先翻 C_ALOHA / Registration 相关叙述与 Table 7.19，再回本课总图；**不要**第一天啃完鉴权与全部 Annex。

2. **[State-of-the-art of ETSI DMR Tier III Standard（DMRA 讲稿 PDF）](https://dmrassociation.org/public-downloads/documents/State-of-the-art-of-ETSI-DMR-Tier-III-Standard-Critical-Comms-Russia-18Apr-2019.pdf)**  
   - **为什么值得看**：用幻灯节奏扫过控制信道能力与 Tier III 功能地图；适合阶段 E 建立「前台管什么」直觉。  
   - **怎么用**：当导游图；字段细节仍回 Part4 / 速览。

3. **[Tait Radio Academy · Channel Operation](https://www.taitradioacademy.com/topic/dmr-channel-operation-1/)**  
   - **为什么值得看**：白话列出控制信道主要功能，**明确包含 registration requests / location management by registration**——与本课「入住登记」同向。  
   - **怎么用**：读完立刻用本课分诊表问：Reg 位？登记 RAND？ACK？

4. **[Tait · Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：节点侧「receiving radio registrations, storing them in registration database」的经典叙述；帮助把「为什么要登记」说给领导听。  
   - **怎么用**：当英文版动机朗读；空口字段仍回 Part4。

5. **[GopherTrunk · DMR End to End Part 8：Tier III — C_ALOHA, Grants & LCNs](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-08-tier3-trunking/)**  
   - **为什么值得看**：实现向说明 C_ALOHA 作为控制信道信标、用 System Identity 锁台——与本课「告示牌 + System Identity」同向。  
   - **怎么用**：当监听/解码语感；**字段冲突仍以 ETSI / 速览为准**。

6. **[GopherTrunk · DMR CSBK payloads](https://gophertrunk.org/reference/dmr-csbk-payloads/)**  
   - **为什么值得看**：把 C_ALOHA / C_RAND / C_AHOY / C_BCAST 等 Opcode 放在一张实现参考表里，便于和本课账本对读。  
   - **怎么用**：认名 + 认码；细节以 Table 7.19 等为准。

7. **[DMR Association · Standards 目录](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：Part1–4 / TR 下载入口总台；阶段 E 找官方 PDF 少迷路。

8. **[DMR Association · Benefits and Features of DMR（白皮书）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：Tier 分层与容量语境；帮新人解释「为什么集群要控制面手续」。  
   - **怎么用**：背景阅读；不替代 Part4。

9. **[Hytera · DMR Tier 3 Trunking 系统页](https://www.hytera.us/systems/dmr-tier-3-trunking-systems/)**  
   - **为什么值得看**：厂商白话：控制信道上的注册与请求、其余为共享 traffic。  
   - **怎么用**：产品叙事；与标准术语对照时以 Part4 为准。

10. **[Wikipedia · ALOHAnet（随机接入背景）](https://en.wikipedia.org/wiki/ALOHAnet)**  
   - **为什么值得看**：理解「随机发、碰撞、再试」的历史直觉，帮助消化 Mask/Backoff 为什么存在。  
   - **怎么用**：**仅背景**；DMR 的 C_ALOHA 字段与 Reg 位以 ETSI 为准，勿把课堂 Aloha 吞吐公式硬套进机房分诊。

**视频备注（诚实）**：公开可核验资源里，登记 + Aloha 的**文字/PDF/实现博客**足够支撑本课；未找到达到本课深度的对口技术短片。故 **video_found=false**。若日后协会/学院上架专项片，再补进进度外链清单。

---

## 本课收束

阶段 E 第二站就一件事：**留在前台，先读告示、再办入住。**  
Aloha 告诉你谁能按铃、要不要登记、怎么退避；登记让系统知道你在哪、允不允许活跃。  
未登记却要业务，常撞 `MS_Not_Registered` 这类路标——Reason 全表下周细读。  
调制账本仍是 12.5 kHz / 4FSK / 双时隙。  
下一站：把 Grant 小票摊成变体地图。
