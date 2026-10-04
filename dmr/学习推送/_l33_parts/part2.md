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

