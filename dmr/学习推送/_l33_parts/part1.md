# 第 33 课 · Grant 变体地图

> DMR 深入学习 · **阶段 E · 集群 Tier III 第 3 课（约 10 课之三）**（接第 32 课「登记与 Aloha」）  
> 适合：已经会画「守 TSCC →（登记）→ RAND → Grant → 进 Payload」总图，但现场一听 **PV / TV / BTV / PD / TD / DX / P_GRANT / CG_AP** 就懵——把 **Grant = 房间小票的种类地图** 钉成肌肉记忆——的人  
> 阅读量：约 **30–40 分钟** · **少公式、不贴矩阵、不画完整 SDL** · 要把「**看见 Grant ≠ 知道是哪种小票；先读 CSBKO → 再读位 A/B → 再看信道号（含 0xFFF→CG_AP）→ 若在业务信道则认 P_GRANT**」钉牢  
> **频谱 / 调制提醒（一小段，不是本课主线）**：RF 仍是整条 **12.5 kHz** 上路；调制仍是 **4FSK**；空口仍是 **2-slot TDMA**，时隙 **30 ms**。**换小票种类，不改射频账本**——看见 TV 却当 PV、看见 0xFFF 却当「坏信道号」、看见业务信道上的 P_GRANT 却当「又一次新呼叫建立」，都不等于「调制坏了」。频率/带宽/调制四句话见 `学习推送/加餐_频率带宽与调制解调.md`；本课主线是 **阶段 E 第 3 站：把 Grant 小票摊成变体地图**。

---

## 1. 为什么本课重要（动机）

第 31 课把门钉在「前台 vs 客房 + Grant 小票」；第 32 课补了「办入住 + 读 Aloha 告示」。机房下一句要命的话往往是：

- 监听员喊：「有 Grant！」——同事问「哪种？」——对方答不上来：是个呼还是组呼？语音还是数据？半双工还是双工？  
- 屏上闪过 **PV_GRANT / TV_GRANT / BTV_GRANT / PD_GRANT / TD_GRANT / PV_GRANT_DX / PD_GRANT_DX**，外加业务信道上的 **P_GRANT**，偶尔还有信道号 = **0xFFF** 后面跟 **CG_AP**——新人把它们全叫成「Grant」，然后用错分诊单。  
- 写频同事说「信道号对啊」；分析仪说「看见 Grant 了」；调度说「组呼迟后进不来」——三个人都对了一半，却对不上「**这一张小票差在哪几个字段**」。  
- 有人把 **Late_Entry** 当成「紧急」；把 **Offset** 当成「双工」；把 **HI_RATE** 当成「高速调制」——字段名听起来像射频，语义却是控制面小票上的开关。  
- 领导问：「为什么同一次双工呼叫好像看见两张 Grant？」——你若只背「有 Grant 就能进房」，答不上 **DX + Call Direction** 的味道。

培训台若只背「Grant = 房间小票」六个字，后面会卡在同一处：

> **看见 Grant ≠ 知道是哪种小票。** 分诊 = 先读 **CSBKO（Opcode 48–56 一带）** → 分清语音/数据、个呼/组呼、半双工/双工 → 再读 **位 A / 位 B**（Late_Entry / HI_RATE / Reserved vs Offset / Call Direction）→ 再看 **Logical Physical Channel Number**（0 无效；1…0xFFE 逻辑号；**0xFFF → 找 CG_AP**）→ 若报文已在 **Payload** 上，再问是不是 **P_GRANT**（沿用原 TSCC Grant 的 CSBKO）。本课不是把 Part4 Grant MSC / FEC / Reason 全表 dump，而是把 **旅馆小票种类地图** 钉成可现场演示的第三张地图。

本课目标：能画出「C_RAND →（可选 ACK/QACK/WACK）→ TSCC Grant 族 → 进 Payload；Grant 本身不要求 ACK，故常重复」总图；会背共用 64-bit 骨架；会用一张 CSBKO 表分诊 PV/TV/BTV/PD/TD/DX；会说 Late_Entry / Emergency / Offset / HI_RATE / Call Direction 各是什么味道；会认信道号规则与 CG_AP 指针；会认业务信道上的 P_GRANT；会做现场分诊、例子与自测；并为第 34 课「Reason Code」留好边界——**成功路径是 Grant（无 Reason）；失败路径才是 NACK Reason**。

**本课硬禁令（写进脑子）**：不 dump FEC 矩阵、不贴完整 SDL、不发明 ETSI 条款号（入口锚点以资料库 `04-集群协议/ReasonCode与Grant变体.md` **§10–§14**、`集群协议字段速览.md` **§1 / §3**、`总索引.md` **集群 / Tier III** 已有编号为准）、**不 dump Reason Code 全表**（第 34 课；本课只强调「Grant 本身无 Reason」）、**不讲鉴权/RC4**（第 35）、**不深挖 CHAN 绝对频率换算公式**（第 36——本课只给 **CG_AP 指针**）、**不讲 Hunt/拨号/Stun**（第 37–39）、**不回头把第 32 课登记 MSC / Aloha 字段再 dump 一遍**。本课只钉 **Grant 变体地图**。

---

## 2. 总图 / 故事：「旅馆小票种类」

先把整课装进旅馆故事，再落到 `ReasonCode与Grant变体.md` **§0 / §10** 与第 31 / 32 课回唤。

### 2.1 一句话故事：不是一张票，是一整柜票样

第 31 课把 Tier III 想成旅馆：**前台（TSCC）发房间小票；客房（Payload）才说话。** 第 32 课说：**先办入住、先读 Aloha 告示，再按铃要房间。** 本课仍站在前台发票窗口，把「小票」拆开：

1. **按铃仍是 C_RAND** = 你要办哪类业务（语音/数据、个呼/组呼……）写在 Service_Kind 等里；本课不重讲登记类。  
2. **前台可能先给中间条** = ACK / QACK / WACK（「收下了 / 排队 / 请稍等」）——这些才带 **Reason**（第 34 课细读）。  
3. **成功就发 Grant 小票** = 告诉你去哪间房（逻辑信道号 + TDMA 时隙）、谁跟谁说话（Target/Source）、这张票是哪种业务形状。  
4. **Grant 不要求确认** = 旅馆把小票塞给你就完事，常常**连喊好几遍**，怕你没听见——所以分析仪上「同一张 Grant 重复」很正常，不等于协议卡住。  
5. **小票种类很多** = 个呼语音、组呼语音、广播组呼、个呼数据、组呼数据、双工变体……**CSBKO 不同 = 票样不同**。  
6. **特殊附页** = 信道号写成 **0xFFF** 时，后面跟 **CG_AP** 绝对频率附块（本课只认「要翻附页」，公式留给第 36 课）。  
7. **进客房之后还可能再发票** = **P_GRANT**：换房、开叫前再广播一次、或公告新呼叫——**CSBKO 沿用当初那张 TSCC Grant**。

口诀：**先认票样（CSBKO）→ 再读开关（位 A/B）→ 再看房号（信道号；FFF 翻附页）→ 再问人在前台还是已在客房（P_GRANT）。**

### 2.2 总图：从按铃到进房（Grant 族放大）

```text
  时间 →

  ┌─ 守 TSCC（第 31–32 课：前台）─────────────────────────┐
  │  已读 Aloha；需要时已办登记；现在按铃要房间              │
  └──────────────────────┬──────────────────────────────────┘
                         ▼
  ┌─ C_RAND（入站按铃 · CSBKO=`011111`）──────────────────┐
  │  Service_Kind / Service_Options 说明「要哪种业务」       │
  └──────────────────────┬──────────────────────────────────┘
                         ▼
  ┌─ 可选中间条：C_ACKD / C_QACKD / C_WACKD / C_NACKD … ─┐
  │  这些才带 Reason（排队/拒绝/稍等）→ 细表第 34 课         │
  │  失败常停在 NACK；成功才继续发小票                       │
  └──────────────────────┬──────────────────────────────────┘
                         ▼
  ┌─ TSCC Grant 族（出站小票 · 不要求 ACK · 常重复）───────┐
  │  PV / TV / BTV / PD / TD / PV_DX / PD_DX …               │
  │  共用骨架：信道号 + TDMA ch + 位A + Emergency + 位B      │
  │           + Target(24) + Source(24)                      │
  │  若信道号 = 0xFFF → 头块 + CG_AP 附块（绝对频率指针）     │
  └──────────────────────┬──────────────────────────────────┘
                         ▼
  ┌─ 迁到 Payload（业务信道 / 客房）───────────────────────┐
  │  在此说话 / 传数据                                      │
  │  可能再看见 P_GRANT：换信道 / 开叫前公告 / 新呼叫公告    │
  └─────────────────────────────────────────────────────────┘
```

极简对照（`ReasonCode与Grant变体.md` §0 同款学习口径）：

```text
  MS --C_RAND(Service_Kind)--> TSCC
  TSCC --(可选) ACK/QACK/WACK/NACK--> MS     # Reason 在这里
  TSCC --C_GRANT×重复--> 主被叫               # 成功；Grant 本身无 Reason
  MS/组 迁到 Payload 信道
```

### 2.3 和第 9 / 11 / 15–24 / 25 / 30 / 31 / 32 课怎么咬合？

| 课 | 你已经会 / 本课加上 |
|----|---------------------|
| 第 9 | Tier I/II/III 全貌——本课把 III「小票种类」摸清楚 |
| 第 11 | Part1–4 文档地图——Grant **认 Part4** |
| 第 15–24 | 时隙/突发/CSBK 外壳——Grant 仍是 CSBK（或 MBC 头+续）壳 |
| 第 25 / 30 | Tier II 常规语音时间线——进 Payload 后仍用；本课在前台发票窗口细读 |
| 第 31 | TSCC vs Payload + Grant 小票总名——本课把「小票」摊成变体地图 |
| 第 32 | 登记 + Aloha——本课假设你已会「先入住再要房」；不重 dump 登记 MSC |
| **本课** | **Grant 变体地图 = 阶段 E 第 3 站** |
| 第 34（预告） | Reason Code——失败/排队理由；**Grant 成功路径不靠 Reason** |

四句话串起来：

1. **第 31 课**：人先在前台；门牌第一步是 Grant。  
2. **第 32 课**：Reg=1 时没办入住就别想要房间。  
3. **本课**：要到了房间，还要认清**这张票是哪种**——个呼/组呼/数据/双工/附页/客房再发票。  
4. **射频账本不变**：仍是 12.5 kHz / 4FSK / 双时隙——换的是**小票样**，不是调制。

### 2.4 调制账本钩子（巩固弱项，不重开加餐）

1. **带宽**：仍是 **12.5 kHz**；Grant 发生在 **TSCC**（或 Payload 上的 P_GRANT），不另发明一套射频尺子。  
2. **多址**：仍是 **2-slot TDMA**，时隙 **30 ms**；Logical Channel Number 只告诉你占 **ch1 还是 ch2**，不是「换调制」。  
3. **调制**：仍是 **4FSK** ≈ **4800 baud** → ≈ **9.6 kbps** 毛速率——PV 与 TV 比特语义不同，**调制方式相同**。  
4. **解调直觉**：先问「我在看 TSCC 还是 Payload？」→ 再认 CSBKO 票样 → 再认信道号/附页 → 最后才怀疑天线。  
   **「Grant 看不懂」≠ 「射频没解调」**，也可能是：把 Opcode 48–56 混成一种、把 Late_Entry 当 Emergency、把 0xFFF 当坏值、或把 P_GRANT 当「又一次完整建链」。  
细节回 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 3. 共用骨架（64 bit · Octet 2–9）

Canonical：`ReasonCode与Grant变体.md` **§11**；代表表见速览 **§3.1 / §3.2**。

### 3.1 外壳先认：仍是 Part1 CSBK，Opcode 在 Part4

| 项 | 学习口径 |
|----|----------|
| 外壳 | Part1 CSBK：LB \| PF \| CSBKO \| FID \| … |
| Octet 0–1 | 所有 TSCC Grant **相同模板**：LB / PF / **CSBKO（变体差在这里）** / FID=`00000000` |
| Octet 2–9 | **共用 64-bit 骨架**；变体差在「位 A / 位 B」怎么解释 |
| LB | 单块 CSBK=`1`；若要跟 CG_AP，头块 LB=`0`（MBC 头） |
| 方向 | **TS → MS**（出站小票）；**不征求响应** |

口诀：**外壳认 Part1；票样认 CSBKO；开关认位 A/B。**

### 3.2 64-bit 骨架图

```text
  Octet 2–9（所有 TSCC Grant 同款拼法）：

  ┌────────────── 12 bit ──────────────┐
  │ Logical Physical Channel Number    │  房号（逻辑信道）
  └────────────────────────────────────┘
  ┌ 1 ┐
  │LC │  Logical Channel Number：0=TDMA ch1；1=ch2
  └───┘
  ┌ 1 ┐
  │ A │  变体位 A：Reserved / Late_Entry / HI_RATE
  └───┘
  ┌ 1 ┐
  │ E │  Emergency（BTV 称 Emergency_Flag）
  └───┘
  ┌ 1 ┐
  │ B │  变体位 B：Offset / Call Direction
  └───┘
  ┌────────────── 24 bit ──────────────┐
  │ Target / Destination Address       │
  └────────────────────────────────────┘
  ┌────────────── 24 bit ──────────────┐
  │ Source Address                     │
  └────────────────────────────────────┘
```

### 3.3 位 A / 位 B：同一格子，不同票样不同释义

| 变体 | 位 A | 位 B | 地址语义（学习口径） |
|------|------|------|----------------------|
| **PV_GRANT** | Reserved=`0` | **Offset**：`0` aligned / `1` offset | Target=被叫个号/网关；Source=主叫/网关 |
| **PV_GRANT_DX** | Reserved=`0` | **Call Direction**（无 Offset 场；NOTE：总是 offset timing） | Target=本 Grant 对象；Source=对端 |
| **TV_GRANT** | **Late_Entry** | Offset | Target=**Talkgroup**（ALLMSID* 按广播解释） |
| **BTV_GRANT** | Late_Entry | Offset | Destination=组；All Call 地址见规范 A.4 指针 |
| **PD_GRANT** | **HI_RATE**：`0` 单时隙数据；`1` 双时隙 | Offset | Destination=个号/网关 |
| **PD_GRANT_DX** | HI_RATE **固定 0** | **Call Direction**（总是 offset） | 同 PV_GRANT_DX 地址味道 |
| **TD_GRANT** | HI_RATE | Offset | Destination=Talkgroup |

**必背三句：**

1. **骨架相同，释义靠票样**——看见「第 16 信息比特附近」先问 CSBKO，再解释 A/B。  
2. **Emergency 几乎家家有**——别把 Late_Entry / HI_RATE / Offset 误当成 Emergency。  
3. **DX 没有「半双工那种 Offset 开关」**——规范 NOTE：双工业务信道**总是 offset timing**；位 B 改叫 Call Direction。

---

