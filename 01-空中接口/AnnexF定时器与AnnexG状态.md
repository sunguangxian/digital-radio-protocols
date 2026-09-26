# Part 1：Annex F 定时器/常数 · Annex G 高层状态

> **学习用整理，冲突以 ETSI 原文为准；非全文复制。**  
> 源：ETSI **TS 102 361-1 V2.7.1** Annex **F**（normative）、**G**（informative）。  
> Part 2/3/4 另有各自 Annex 定时器；Tier III 见 [`../04-集群协议/Stun_DGNA_UDT与定时器.md`](../04-集群协议/Stun_DGNA_UDT与定时器.md)。  
> 覆盖清单：[`../附录覆盖清单.md`](../附录覆盖清单.md)

---

## Annex F — Layer 2 timers

范围类由实现在规范给定界内选取；部分给默认值且可配置。

| 定时器 | 含义 | 量级（规范） |
|--------|------|----------------|
| **T_ChMonTo** | 信道活动监测超时 | min **40 ms** |
| **T_ChSyncTo** | 信道同步活动超时 | min **390 ms** |
| **T_MSInactiv** | MS 无活动 | 默认 **5 s**；max ∞ |
| **T_CallHt** | 呼叫 hangtime | 默认 **3 s**；max ∞ |
| **T_ChHt** | 信道 hangtime | **= T_MSInactiv − T_CallHt** |
| **T_Monitor** | 监测/寻同步时长 | 实现选；max **720 ms** |
| **T_TxCC** | 直通：活动信道上寻 CC | 实现选；max **360 ms** |
| **T_SyncWu** | 发 Wakeup 后寻 BS SYNC | 实现选；max **360 ms** |
| **T_TxCCSlot** | 寻 CC+时隙编号 | 实现选；max **720 ms** |
| **T_IdleSrch** | 已匹配 CC/时隙后确认空闲 | 实现选；max **540 ms** |
| **T_Holdoff** | 忙信道非实时重试随机退避 | min 0；建议 max **1000 ms**（非实时 CSBK ACK 类） |

关系直觉：`T_ChHt` 由两个 hangtime 相减得到，保证“呼叫保留”落在“信道保留”之内。

---

## Annex F — Layer 2 constants

| 常数 | 含义 | 量级 |
|------|------|------|
| **N_RssiLo** | 礼貌接入 RSSI 门限 | Polite to Own CC 建议 **−122 dBm**；Polite to All 按频段约 **−101 / −107 / −113 dBm**（50–137 / >137–300 / >300 MHz）；精度 ±4 dB（50 Ω） |
| **N_Wakeup** | Wakeup 循环次数门限 | 实现选；建议 **2** |
| **n_DFragMax** | 数据分片最大长度 | **1500** octets（L2 需能缓到此长再交上层） |
| **N_BlockMax** | 一包最大块数（含头） | 见 PDF F.2 |

---

## Annex G — High level states（informative）

实现可不同；Part 2 信道接入等会引用这些状态名。

### G.1 MS Level 1（同步 / CC / 时隙）
| 状态 | 含义 |
|------|------|
| **Out_of_Sync** | 未获得或丢失 SYNC |
| **In_Sync / Unknown_System** | 已检到 DMR SYNC，但 CC（及中继/时隙结构）未知或不匹配 |
| **In_Sync / My_System** | CC（及中继时隙号）已确认属本系统 |

直通 / 中继 / TDMA 直通各有 Level-1 SDL（Fig G.1–G.3）。

### G.1.2 MS Level 2（在 My_System 内）
| 状态 | 含义 |
|------|------|
| **Not_in_Call** | 尚不能判定目的 ID（中继上常见于信道 hangtime） |
| **My_Call** | 语音头/嵌入 LC 解出本机个号或本组 → 本呼叫参与方 |
| **Others_Call** | 解出他方 ID；含他方通话与其 call hangtime |
| **In_Session** | 经 **Terminator with LC** 解出本 ID → call hangtime 会话中 |
| **Transmit** | 本机在对应时隙发语音/数据/CSBK |

### G.2 BS（摘要）
- **Both Slots**：`BS_Hibernating`（等 Wakeup，出站关）→ `Hangtime` → `Repeating_Slot_1` / `_2` / `_Both`。
- **Single Slot**：单时隙上的转发、call/channel hangtime（Fig G.6）。
- 事件名如 BOR/EOR 为概念级，具体设施在 Part 2。

不抄 SDL 图；状态迁移以 PDF 为准。
