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

## 4. 变体地图总表（CSBKO）

Canonical：`ReasonCode与Grant变体.md` **§10.1 / §14**。

| 别名 | CSBKO (6) | Opcode | 用途（一句话） | 位 A 附近 | 位 B 附近 | 表 |
|------|-----------|--------|----------------|-----------|-----------|----|
| **PV_GRANT** | `110000₂` | **48** | 个呼语音（半双工） | Reserved | Offset | 7.9 |
| **TV_GRANT** | `110001₂` | **49** | 组呼语音 | Late_Entry | Offset | 7.11 |
| **BTV_GRANT** | `110010₂` | **50** | 广播组呼语音 | Late_Entry | Offset | 7.12 |
| **PD_GRANT** SI | `110011₂` | **51** | 个呼数据（单条目） | HI_RATE | Offset | 7.13 |
| **TD_GRANT** SI | `110100₂` | **52** | 组呼数据（单条目） | HI_RATE | Offset | 7.15 |
| **PV_GRANT_DX** | `110101₂` | **53** | 个呼语音**双工** | Reserved | Call Direction | 7.10 |
| **PD_GRANT_DX** | `110110₂` | **54** | 个呼数据**双工** | HI_RATE 固定 0 | Call Direction | 7.14 |
| **PD_GRANT** MI | `110111₂` | **55** | 个呼数据（多条目） | HI_RATE | Offset | 7.13 |
| **TD_GRANT** MI | `111000₂` | **56** | 组呼数据（多条目） | HI_RATE | Offset | 7.15 |
| **P_GRANT** | **沿用**原 TSCC Grant 的 CSBKO | — | 业务信道换信道 / 开叫前公告 / 新呼叫公告 | 按原类型解释 | 按原类型解释 | 7.29 |
| **CG_AP** | **与头块相同** | — | Grant MBC 续块：绝对 Tx/Rx 参数 | — | — | 7.16 |

**SI / MI（数据）**：Single Item / Multi-Item——由 **CSBKO** 区分（51 vs 55；52 vs 56），不是骨架里单独再开一个 1-bit 场。C_RAND 的 Service_Options 里另有 SIMI 位（Announcement 文件指针），本课认「票样用 Opcode 分开」即可。

**Opcode 56 注意**：Annex B.1 中 `111000₂` 亦被 **Part2 BS_Dwn_Act** 使用——**上下文靠 FID/场景区分**。现场看见 56，先问：「我在看 Tier III 控制面数据组呼 Grant，还是 Part2 下行激活故事？」

口袋口诀（48→56）：

```text
  48 PV半双工语音 | 49 TV组呼 | 50 BTV广播组呼
  51 PD个呼数据SI | 52 TD组呼数据SI
  53 PV双工 | 54 PD双工
  55 PD_MI | 56 TD_MI（兼 Part2 语境注意）
```

---

## 5. 语音族：PV / TV / BTV / DX

### 5.1 PV_GRANT — 个呼半双工语音（Table 7.9）

- **CSBKO=`110000₂`（48）**  
- 位 A = Reserved=`0`；位 B = **Offset**  
- Target = 被叫个号/网关；Source = 主叫/网关  
- 旅馆说法：**「两人半双工对讲的标准房间小票」**——你讲我听、我讲你听，不是同时双向。

现场一问：看见 48，先问「个呼语音半双工？」再读 Offset / Emergency / 信道号。

### 5.2 TV_GRANT — 组呼语音（Table 7.11）

- **CSBKO=`110001₂`（49）**  
- 位 A = **Late_Entry**：`0` 建链授予；`1` 建链后的迟后进入授予  
- Target = **Talkgroup**；若为 ALLMSIDL / ALLMSIDZ / ALLMSID 等，按广播解释（规范 A.4 指针）  
- 旅馆说法：**「会议室小票」**——组地址是会议室号。

**Late_Entry 直觉**：建链后，TSCC 可继续发 `Late_Entry=1` 的 TV/BTV Grant，让**后来才上线的组员**被拉进已在进行的组呼（过程指针 6.6.1.6）。  
**不是 Emergency**，也不是「网络故障重发」的唯一解释——重发 Grant 很常见；要看 Late_Entry 位。

### 5.3 BTV_GRANT — 广播组呼语音（Table 7.12）

- **CSBKO=`110010₂`（50）**  
- 同样有 Late_Entry、Emergency_Flag、Offset  
- Destination = 组；All Call 地址味道更「广播」  
- 旅馆说法：**「大厅广播小票」**——不是两人私聊，也不是普通会议室那么「会话感」。

分诊：49 vs 50——都是组向语音；BTV 更偏广播组呼语义。别把二者和 PV（48）混成「都是语音就行」。

### 5.4 PV_GRANT_DX — 个呼语音双工（Table 7.10）

- **CSBKO=`110101₂`（53）**  
- 位 A = Reserved=`0`；位 B = **Call Direction**（`0` Target=被叫侧味道；`1` Target=主叫侧味道——学习口径：Target=本 Grant 对象，Source=对端）  
- **总是 offset timing**（规范 NOTE）——不要再找半双工那种 Offset 开关  
- 旅馆说法：**「双人同时可说的对讲小票」**；一次双工呼叫，TSCC **常发两条 DX Grant**，每条 Target 填该参与者自己的 MS ID。

现场：看见两张 53、Target 各写一方——先想到「双工一对票据」，不要报「重复异常建链」。

### 5.5 语音族对照速记

```text
           个呼                    组/广播
  半双工   PV 48                   TV 49 / BTV 50
  双工     PV_DX 53                （本课地图以个呼 DX 为主）

  组呼多一个 Late_Entry 开关
  双工多一个 Call Direction；总是 offset
```

---

## 6. 数据族：PD / TD / DX + SI/MI

### 6.1 PD_GRANT — 个呼数据（Table 7.13）

- **SI：CSBKO=`110011₂`（51）**；**MI：CSBKO=`110111₂`（55）**  
- 位 A = **HI_RATE**：`0` 单时隙数据；`1` 双时隙数据  
- 位 B = Offset  
- Destination = 个号/网关  

旅馆说法：**「寄个人包裹的库房小票」**——SI/MI 是「单件/多件」票样（用 Opcode 分开）。

### 6.2 TD_GRANT — 组呼数据（Table 7.15）

- **SI：CSBKO=`110100₂`（52）**；**MI：CSBKO=`111000₂`（56）**  
- 同样 HI_RATE + Emergency + Offset  
- Destination = Talkgroup  

旅馆说法：**「会议室分发资料的库房小票」**。

**Opcode 56 再提醒一次**：Part4 语境 = TD_GRANT_MI；Part2 语境可能撞上 BS_Dwn_Act——分诊先看 **FID/所在文档房间**。

### 6.3 PD_GRANT_DX — 个呼数据双工（Table 7.14）

- **CSBKO=`110110₂`（54）**  
- **HI_RATE 固定 `0`**（双工数据总是单时隙）——别指望在 DX 数据票上看到「双时隙高速」开关  
- 位 B = **Call Direction**；总是 offset timing  
- 地址味道同 PV_GRANT_DX  

### 6.4 HI_RATE 直觉（别当成「换调制」）

| HI_RATE | 学习口径 |
|---------|----------|
| `0` | 单时隙数据业务信道 |
| `1` | 双时隙数据（占更宽的「房间资源」味道） |
| DX 数据 | **固定 0** |

口诀：**HI_RATE 管数据占几个时隙资源，不改 4FSK/12.5 kHz 账本。**

### 6.5 数据族对照速记

```text
  个呼数据：PD SI 51 / PD MI 55 / PD_DX 54
  组呼数据：TD SI 52 / TD MI 56
  共同开关：HI_RATE（DX 固定 0）+ Emergency +（非 DX 的）Offset
```

---

## 7. 信道号与 CG_AP 附块（指针级）

Canonical：`ReasonCode与Grant变体.md` **§10.1 信道号规则 / §13**；速览 **§3 / §3.4**。

### 7.1 Logical Physical Channel Number 三态

| 值 | 含义 | 空口形状 |
|----|------|----------|
| `0` | **无效** | 不该当成合法房号 |
| `1` … `0xFFE` | 逻辑信道号 → 通常 **单块 CSBK** Grant | 常见「相对/逻辑」路径 |
| `0xFFF`（4095） | **绝对频率在后续 CG_AP** | MBC 头 + 续块 |

```text
  信道号读法：

  0          → 停：无效，先查解码/录波
  1…0xFFE    → 用系统信道规划映射到频率（监听器常要 band plan）
  0xFFF      → 别当「坏值」；去找 CG_AP 附块
```

### 7.2 CG_AP 是什么（本课只到指针）

当头块信道号 = **0xFFF**：

- 头块是 Grant（LB 作 MBC 头）；  
- 续块是 **CG_AP**（Table **7.16**）；  
- **CG_AP 的 CSBKO 与头块相同**（仍是 48/49/… 那张票样）；  
- 续块里有 Colour Code、Cdeftype、**CdefParms**（含绝对 Tx/Rx 整数 MHz + 125 Hz 步分数等）。

旅馆说法：**房号栏写「见附页」——附页才写绝对楼层坐标。**

**本课硬边界**：不展开 Annex C 换算公式、不背 Table C.1–C.7——那是 **第 36 课**。本课只会说：「看见 FFF → 找 CG_AP；公式回 `鉴权与AnnexC频率.md`。」

### 7.3 和同类附块的边界（认名即可）

同一套 CdefParms 机制还出现在 C_MOVE 的 MV_AP、C_BCAST 的 BC_AP、Vote Now 的 VN_AP 等——**不是 Grant**，但骨架很像。本课只钉 **Grant 头 + CG_AP**。

### 7.4 Logical Channel Number（1 bit）别漏

- `0` = TDMA **ch1**；`1` = **ch2**  
- 这是「进哪一个 30 ms 房间座位」，不是 Colour Code，也不是系统身份。

---

## 8. 业务信道上的 P_GRANT

Canonical：`ReasonCode与Grant变体.md` **§12.8**（Table **7.29**）。

### 8.1 关键：P_GRANT 不是新的 CSBKO 号码

**P_GRANT 的 CSBKO 必须等于**当初把该 MS 拉到业务信道的那条 **TSCC Grant**。  
所以你在 Payload 上可能仍看见 Opcode 48/49/…——**别立刻喊「怎么又在控制信道建链？」**；先问：「我现在是不是已经在业务信道上？」

### 8.2 三种用途（学习口径）

1. **换信道（swap）**：除逻辑信道号（及可选绝对频率）外，其余 IE 尽量保持原 TSCC Grant。  
2. **本呼叫首次发射前公告**：IE 与原 TSCC Grant 相同——再广播一次「房间还是这个」。  
3. **公告新呼叫**：IE 用该新呼叫在 TSCC 上的值；MS 可跟随或忽略（厂商策略指针 6.6.1.6）。

旅馆说法：

- swap = **换房通知**；  
- 开叫前公告 = **进门前再喊一次房号**；  
- 新呼叫公告 = **客房喇叭里插播：隔壁又开了一场，跟不跟随你**。

### 8.3 字段怎么读

布局同对应 Grant；**位 A/B 仍按原票样解释**（数据才有 HI_RATE；DX 的第 3 位是 Call Direction）。信道号仍可走逻辑号或 `0xFFF`+CG_AP。

### 8.4 和第 31 课「门牌」怎么接

第 31 课说：Grant 是进客房的门牌。本课补一句：**进了客房，门牌还可能再更新（P_GRANT）——票样编号（CSBKO）通常仍是当初那一种。**

---

## 9. 现场分诊表 + 例子

### 9.1 分诊表

| 岗位现象 | 先做的分诊动作 | 常翻 | 别一上来就 |
|----------|----------------|------|------------|
| 「有 Grant，什么业务？」 | 读 **CSBKO / Opcode 48–56** | §4 总表 | 凭「有语音声」猜票样 |
| 组呼有人进不来 | 问：TV/BTV？**Late_Entry** 是否为迟后授予？ | §5.2 | 先改天线 |
| 「双工怎么两张 Grant？」 | 查是否 **PV_GRANT_DX / PD_GRANT_DX** + Call Direction | §5.4 / §6.3 | 报重复建链故障 |
| 数据业务占槽异常 | 读 **HI_RATE**；DX 数据是否误期待双时隙 | §6.4 | 改调制参数 |
| 信道号 4095 / 0xFFF | 去找 **CG_AP**；别当坏值 | §7 | 当控制信道崩溃 |
| 信道号 0 | 当无效：查解码/录波 | §7.1 | 硬映射频率 |
| Payload 上又见「Grant」 | 问是否 **P_GRANT**（CSBKO 沿用） | §8 | 当「又回到 TSCC 建链」 |
| Opcode 56 打架 | 问 Part4 TD_MI 还是 Part2 BS_Dwn_Act | §4 / §6.2 | 各执一词骂标准 |
| 「Grant 失败原因码？」 | 纠正：**Grant 无 Reason**；失败看 NACK | 第 34 课入口 | 在 Grant 比特里找 Reason |
| 听见小票种类就怪 4FSK | 先完成 CSBKO→位A/B→信道号链 | §2.4 | 开射频单 |

分诊口诀：**CSBKO 定票样 → 位 A/B 定开关 → 信道号定房号（FFF 翻附页）→ 所在信道定是否 P_GRANT → Reason 只在失败/中间条。**

### 9.2 工作例子（10 则）

**例 1 · 干净组呼路径**  
空口：C_RAND(组呼语音类) →（可选 WACK/ACK）→ **TV_GRANT(49)** 重复若干次 → 双方进 Payload。  
向领导：「前台发了会议室小票。」

**例 2 · 迟后进入**  
组呼已在进行，TSCC 继续发 **TV_GRANT 且 Late_Entry=1**。新上线组员跟票进房。  
分诊：不是「系统抽风重发」的唯一解释；先看 Late_Entry。

**例 3 · 个呼半双工 vs 双工**  
半双工见 **PV_GRANT(48)** + Offset；双工见 **PV_GRANT_DX(53)** + Call Direction，常成对。  
纠偏：53 ≠ 「48 坏了」；是另一张票样。

**例 4 · 个呼数据 SI/MI**  
同一「寄包裹」故事，Opcode **51 vs 55** 分单条目/多条目。  
分诊：先读 CSBKO，再读 HI_RATE。

**例 5 · PD_GRANT_DX 的 HI_RATE**  
看见 54，有人问「为什么不能双时隙？」——规范：DX 数据 **HI_RATE 固定 0**。  
纠偏：别按半双工 PD 的 HI_RATE 期待去改工单。

**例 6 · 0xFFF → CG_AP**  
Grant 头信道号 = 4095，随后 MBC 续块 CSBKO 与头相同。  
分诊：找 Colour Code / Cdeftype / CdefParms；**换算公式 → 第 36 课**。

**例 7 · 无效信道号 0**  
解码出 Logical Physical Channel = 0。  
分诊：当无效；先查是否录波切错、字段对齐错，再谈规划表。

**例 8 · Payload 上的 P_GRANT swap**  
通话中信道拥塞，业务信道上出现与原 TSCC 同 CSBKO 的 Grant，信道号变了。  
分诊：换房通知；不是「呼叫从零重建」的唯一说法。

**例 9 · 把 Grant 当失败原因载体**  
同事在 Grant 里找 Reason Code。  
纠偏：`ReasonCode与Grant变体.md` §0——**Channel Grant 不要求确认、本身无 Reason**；拒绝走 NACK Reason（第 34 课）。

**例 10 · Opcode 56 语境冲突**  
一人拿 Part2 文档说 BS_Dwn_Act，一人拿 Part4 说 TD_GRANT_MI。  
分诊：对齐 FID/场景/所在信道；Annex B.1 已提示同码异义可能。

---

## 10. 术语账本 / 口袋速查

### 10.1 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **Channel Grant** | TS 发给 MS 的「去哪间业务房」小票 | ≠ Aloha 告示；≠ Reason 判决书 |
| **CSBKO / Opcode** | 6 bit 票样编号；Grant 族约 48–56 | ≠ Colour Code；≠ Service_Kind |
| **Logical Physical Channel Number** | 12 bit 逻辑房号 | ≠ TDMA ch 位；0 / 1…FFE / FFF 三态 |
| **Logical Channel Number** | 1 bit：TDMA ch1/ch2 | ≠ 逻辑物理信道号 |
| **位 A** | Reserved / Late_Entry / HI_RATE（随票样） | ≠ Emergency |
| **位 B** | Offset / Call Direction（随票样） | ≠「双工开关」口号（DX 用 Call Direction） |
| **Late_Entry** | 组呼建链后迟后进入授予 | ≠ Emergency；≠ 单纯重发 |
| **Offset** | aligned / offset timing | DX 半双工票上的 Offset；DX 票无此场 |
| **Call Direction** | DX 票：Target 填哪一端 | ≠ Offset 的别名 |
| **HI_RATE** | 数据占单时隙/双时隙 | ≠ 换 4FSK；DX 数据固定 0 |
| **Emergency** | 紧急标志 | 别跟 Late_Entry/HI_RATE 抢名字 |
| **SI / MI** | 数据单条目/多条目；用 CSBKO 分开 | ≠ Service Function |
| **CG_AP** | 绝对频率 MBC 续块；头块信道号=0xFFF | ≠ 自己就是一种新 CSBKO 号码 |
| **P_GRANT** | 业务信道上的再授予；CSBKO 沿用原 TSCC Grant | ≠ 「新的 Opcode」 |
| **Reason Code** | 在 ACK/NACK/QACK/WACK 里 | **不在 Grant 里**（第 34 课） |

### 10.2 口袋速查：CSBKO 48–56

| Dec | 二进制 | 别名 |
|-----|--------|------|
| 48 | `110000` | PV_GRANT |
| 49 | `110001` | TV_GRANT |
| 50 | `110010` | BTV_GRANT |
| 51 | `110011` | PD_GRANT（SI） |
| 52 | `110100` | TD_GRANT（SI） |
| 53 | `110101` | PV_GRANT_DX |
| 54 | `110110` | PD_GRANT_DX |
| 55 | `110111` | PD_GRANT（MI） |
| 56 | `111000` | TD_GRANT（MI）／兼 Part2 语境注意 |

相关非 Grant（别误收进本课口袋当小票）：

| Dec | 别名 | 备注 |
|-----|------|------|
| 25 | C_ALOHA | 第 32 课告示牌 |
| 28 | C_AHOY | 点名 |
| 31 | C_RAND | 按铃 |
| 32/33 | C_ACKD/U 族 | Reason 载体 → 第 34 |
| 57 | C_MOVE | 迁 TSCC；非 Grant |

### 10.3 数字与符号账本

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| Grant 共用载荷 | Octet 2–9 **64 bit** | 信道+ch+A+E+B+地址 |
| 信道号无效 | **0** | 停 |
| 信道号逻辑 | **1…0xFFE** | 单块 CSBK 常见 |
| 信道号绝对指针 | **0xFFF** | → CG_AP |
| FID（标准） | `00000000` | SFID |
| Part4 官方版本 | **TS 102 361-4 V1.12.1 (2023-07)** | 硬出处 |
| 库内 canonical | `ReasonCode与Grant变体.md` **§10–§14** | 本课主入口 |
| 速览入口 | `集群协议字段速览.md` **§1 / §3** | 代表表 + 指针 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 换票样不换射频 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |

---

## 11. 十则误区（看见就打回）

1. **「看见 Grant = 知道业务类型。」** → 必须先读 CSBKO；Grant 是一大族，不是一种。  
2. **「Late_Entry 就是紧急。」** → Late_Entry 管迟后进入；Emergency 是另一 bit。  
3. **「Offset 等于双工。」** → Offset 是 aligned/offset timing；双工票是 DX + Call Direction，且总是 offset。  
4. **「HI_RATE 表示换了高速调制。」** → 管数据占几个时隙资源；调制仍是 4FSK。  
5. **「信道号 0xFFF 是坏值。」** → 常是「请看 CG_AP 附页」的合法写法。  
6. **「CG_AP 有自己的新 Opcode。」** → 续块 CSBKO **与头块相同**。  
7. **「P_GRANT 是 Opcode 新号码。」** → 沿用原 TSCC Grant 的 CSBKO；差在所在信道与用途。  
8. **「Grant 里一定有 Reason Code。」** → Grant **无 Reason**；失败看 NACK（第 34 课）。  
9. **「Opcode 56 永远是 TD_GRANT_MI。」** → Part2 也可能用同码；看 FID/场景。  
10. **「小票种类看不懂说明 12.5 kHz/4FSK 坏了。」** → 先完成票样分诊链；调制账本最后背锅。

---

## 12. 自测题（含答案）

**题 1.** 用旅馆比喻各一句话：Grant、CSBKO、CG_AP、P_GRANT。

<details><summary>答案</summary>

Grant = 房间小票。CSBKO = 票样编号（个呼/组呼/数据/双工等）。CG_AP = 房号栏写「见附页」时的绝对坐标附页。P_GRANT = 进客房之后的换房/再广播/新呼叫公告（票样编号通常沿用）。

</details>

**题 2.** 写出 Grant 共用 64-bit 骨架从前往后的七段名称。

<details><summary>答案</summary>

Logical Physical Channel Number(12) → Logical Channel Number(1) → 位 A(1) → Emergency(1) → 位 B(1) → Target(24) → Source(24)。

</details>

**题 3.** 给出 PV_GRANT / TV_GRANT / BTV_GRANT / PV_GRANT_DX 的 Opcode（十进制）与 CSBKO 二进制。

<details><summary>答案</summary>

48=`110000`；49=`110001`；50=`110010`；53=`110101`。

</details>

**题 4.** TV_GRANT 的位 A 叫什么？`0` 与 `1` 各表示什么（学习口径）？

<details><summary>答案</summary>

Late_Entry。`0`=建链授予；`1`=建链后的迟后进入授予。

</details>

**题 5.** PD_GRANT 的 SI/MI 如何区分？HI_RATE=`1` 表示什么？PD_GRANT_DX 的 HI_RATE 呢？

<details><summary>答案</summary>

SI=Opcode 51（`110011`），MI=Opcode 55（`110111`）。HI_RATE=`1`=双时隙数据。PD_GRANT_DX 的 HI_RATE **固定 0**。

</details>

**题 6.** 信道号 0、1…0xFFE、0xFFF 各怎么处理？

<details><summary>答案</summary>

0=无效。1…0xFFE=逻辑信道号（常单块 CSBK）。0xFFF=绝对参数在后续 CG_AP。

</details>

**题 7.** 为什么说「Grant 不要求确认」？分析仪上常见什么现象？

<details><summary>答案</summary>

规范学习口径：Channel Grant 不征求响应，故常重复发送。分析仪上同一张 Grant 连喊多遍很正常，不等于协议死锁。

</details>

**题 8.** P_GRANT 的 CSBKO 从哪来？列出三种用途关键词。

<details><summary>答案</summary>

必须等于当初 TSCC Grant 的 CSBKO。用途：换信道（swap）；本呼叫首次发射前公告；公告新呼叫。

</details>

**题 9.（加分）** 判断：失败呼叫应在 Grant 比特里找 Reason Code。（对/错）并改写正确路径。

<details><summary>答案</summary>

**错。** 成功路径是 Grant（无 Reason）；失败路径是 C_NACKD 等确认族里的 Reason Code（第 34 课）。

</details>

**题 10.（加分）** 现场分诊顺序（五步）写出来；并指出 Opcode 56 的额外陷阱。

<details><summary>答案</summary>

①读 CSBKO 定票样 → ②读位 A/B → ③读信道号（FFF→CG_AP）→ ④判断所在信道是否 Payload 上的 P_GRANT → ⑤失败才查 NACK Reason。Opcode 56：Part4 为 TD_GRANT_MI，亦可能在 Part2 BS_Dwn_Act 语境出现，需靠 FID/场景区分。

</details>

---

## 13. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `04-集群协议/ReasonCode与Grant变体.md` **§10** | Grant 变体总览表（本课 canonical） |
| 2 | 同上 **§11** | 共用 64-bit 骨架与位 A/B 释义 |
| 3 | 同上 **§12** | 各 Grant 字段表（PV/TV/BTV/PD/TD/DX/P_GRANT） |
| 4 | 同上 **§13** | CG_AP / CdefParms 指针（公式不深挖） |
| 5 | 同上 **§14** | Opcode 速查 48–56 |
| 6 | 同上 **§0** | Reason 与 Grant 怎么配合：成功 Grant / 失败 NACK |
| 7 | `04-集群协议/集群协议字段速览.md` **§1** | TSCC / Payload / Grant 概念回唤 |
| 8 | 同上 **§3** | PV/TV 代表表 + 其余变体指针 + CG_AP 摘记 |
| 9 | `学习推送/第31课.md` | TSCC vs Payload + Grant 小票总名 |
| 10 | `学习推送/第32课.md` | 登记 + Aloha（本课前置；勿重 dump） |
| 11 | `总索引.md` **集群 / Tier III** | 门牌导航 |
| 12 | `04-集群协议/TS102361-4_V1.12.1.pdf` | 官方原文 Tables 7.9–7.16 / 7.29 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「票样分不清」当成调制故障 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。Reason 全表、鉴权/RC4、绝对频率公式、Hunt/拨号/Stun：**永远回对应课 / PDF**，本课不补第二份。

---

## 14. 下一课预告

**第 34 课 · Reason Code 怎么读**

本课把门钉在「成功就发哪种 Grant 小票」。下一课专攻 **失败与中间态**：C_ACK / C_NACK / C_QACK / C_WACK 里的 **Reason Code** 怎么拆（tt / d / aaaaa）、登记拒绝与呼叫拒绝常见码、Mirrored_Reason、Response_Info 成对读法。仍然少公式；**不回头把本课 Grant 变体再 dump 一遍**，也不抢第 35 课鉴权。

记住边界：**Grant 本身无 Reason；看见拒绝，去 ACK 族找。**

---

## 15. 推荐阅读与视频

本课外链为 **2026-10-04**（晚间推送）检索核验；真实用 HTTP 头/跳转核验过可达（协会镜像 / Tait Academy / GopherTrunk Grant·CSBK 参考 / DMRA 白皮书 / Hytera Tier III / 开源解码器对照等，**ETSI deliver 直链对部分自动化抓取常返回 403，故 Part4 以 DMRA 协会镜像为准**）。**不编造地址**。策略 = **Part4 协会镜像 PDF + DMRA Tier III 现状讲稿 + Tait Channel Operation + Tait Study Guide + GopherTrunk Tier III 深潜（Grants & LCNs）+ GopherTrunk Channel grant 概念页 + GopherTrunk CSBK payloads（含 PV/TV/BTV/PD/TD Opcode）+ DMRA 标准目录 + Benefits 白皮书 + Hytera Tier III 系统页 + IanWraith DMRDecode CSBK.java（开源侧 Opcode 48–52 命名对照）**。另检索公开「DMR Grant variants / PV_GRANT TV_GRANT CSBKO map」专项技术视频：可见 Tier III 概论/营销短片与实现向博客，**未**找到按「CSBKO 48–56 变体地图 + 位 A/B + CG_AP + P_GRANT」展开的独立优质技术课。**video_found=false**（诚实备注：有实现向博客、标准 PDF 与开源对照，无对口技术短片）。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMRA 协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - **为什么值得看**：Tables 7.9–7.16 / 7.29 等 Grant 硬出处；与本课 §4–§8 对照。  
   - **库内副本**：`dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。  
   - **怎么用**：先翻 Channel Grant 叙述与代表表，再回本课总表；**不要**第一天啃完 Reason 全表与 Annex C 公式。

2. **[State-of-the-art of ETSI DMR Tier III Standard（DMRA 讲稿 PDF）](https://dmrassociation.org/public-downloads/documents/State-of-the-art-of-ETSI-DMR-Tier-III-Standard-Critical-Comms-Russia-18Apr-2019.pdf)**  
   - **为什么值得看**：用幻灯节奏扫过控制信道能力与 Tier III 功能地图；适合阶段 E 建立「前台发什么票」直觉。  
   - **怎么用**：当导游图；字段细节仍回 Part4 / `ReasonCode与Grant变体.md`。

3. **[Tait Radio Academy · Channel Operation](https://www.taitradioacademy.com/topic/dmr-channel-operation-1/)**  
   - **为什么值得看**：白话讲控制信道如何分配业务信道——与「Grant = 房间小票」同向。  
   - **怎么用**：读完立刻用本课分诊表问：CSBKO？位 A/B？信道号是否 FFF？

4. **[Tait · Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：节点侧信道分配与集群效率的经典叙述；帮你把「为什么要发 Grant」说给领导听。  
   - **怎么用**：当英文版动机朗读；空口票样仍回 Part4。

5. **[GopherTrunk · DMR End to End Part 8：Tier III — C_ALOHA, Grants & LCNs](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-08-tier3-trunking/)**  
   - **为什么值得看**：实现向强调 TV/PV Grant 以 12-bit LPCN + 时隙位打头、逻辑信道需 band plan 映射——与本课信道号故事同向。  
   - **怎么用**：当监听/解码语感；**字段冲突仍以 ETSI / 库内整理为准**。

6. **[GopherTrunk · Channel grant（概念页）](https://gophertrunk.org/reference/channel-grant/)**  
   - **为什么值得看**：跨标准白话解释「grant = 呼叫落到具体语音信道的那一瞬间」；并提到 group 再公告与 late entry 直觉。  
   - **怎么用**：建立故事感；DMR 具体 CSBKO 地图仍回本课 §4。

7. **[GopherTrunk · DMR CSBK payloads](https://gophertrunk.org/reference/dmr-csbk-payloads/)**  
   - **为什么值得看**：把 PV_GRANT/TV_GRANT/BTV_GRANT/PD_GRANT/TD_GRANT 等 Opcode 放在一张实现参考表里，便于和本课口袋速查对读。  
   - **怎么用**：认名 + 认码；DX/MI 细表与位释义以 `ReasonCode与Grant变体.md` §10–§12 为准。

8. **[DMR Association · Standards 目录](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：Part1–4 / TR 下载入口总台；阶段 E 找官方 PDF 少迷路。

9. **[DMR Association · Benefits and Features of DMR（白皮书）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：Tier 分层与容量语境；帮新人解释「为什么要用动态 Grant 而不是写死频率」。  
   - **怎么用**：背景阅读；不替代 Part4。

10. **[Hytera · DMR Tier 3 Trunking 系统页](https://www.hytera.us/systems/dmr-tier-3-trunking-systems/)**  
    - **为什么值得看**：厂商白话：控制信道管请求与分配、其余为共享 traffic。  
    - **怎么用**：产品叙事；与标准术语对照时以 Part4 为准。

11. **[IanWraith/DMRDecode · CSBK.java（开源对照）](https://github.com/IanWraith/DMRDecode/blob/master/src/main/java/com/dmr/CSBK.java)**  
    - **为什么值得看**：开源解码器里对 CSBKO 48–52 等命名（PV/TV/BTV/PD/TD_GRANT）的直观分支，便于和本课 Opcode 表互证。  
    - **怎么用**：只作命名对照；完整变体与 DX/MI/CG_AP 仍以 ETSI / 库内 §10–§13 为准。

**视频备注（诚实）**：公开可核验资源里，Grant 变体的**文字/PDF/实现博客/开源对照**足够支撑本课；未找到达到本课深度的对口技术短片（无「CSBKO 48–56 地图」专项课）。故 **video_found=false**。若日后协会/学院上架专项片，再补进进度外链清单。

---

## 本课收束

阶段 E 第三站就一件事：**把房间小票摊成种类地图。**  
看见 Grant，先问哪种 CSBKO；再问位 A/B；再问信道号是不是 0xFFF；再问人在前台还是已在客房。  
成功路径是重复的小票；失败路径才去翻 Reason。  
调制账本仍是 12.5 kHz / 4FSK / 双时隙。  
下一站：学会读拒绝与排队的 Reason Code。
