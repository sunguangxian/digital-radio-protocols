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

