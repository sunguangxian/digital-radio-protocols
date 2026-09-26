# TR 102 398：附录 A/B/C/D（省电 · 接入 · 架构 · 功率）

> **学习用整理，冲突以 ETSI 原文为准；非全文复制。**  
> 源：ETSI **TR 102 398 V1.5.1 (2023-11)** Annex **A–D**（informative 导读）。  
> 规范性细节以 **TS 102 361-4**（省电/接入/闭环功率）与 **TS 102 361-1**（架构/RC）为准。  
> 覆盖清单：[`../附录覆盖清单.md`](../附录覆盖清单.md)

---

## Annex A — Tier III 省电（Power Save）

### A.0 动机
- 休眠电流远低于空闲监听；代价是睡眠期间收不到寻址到自己的出站 PDU，呼叫建立可能被 TSCC **推迟到下一醒窗**。
- 本地侧仍可被用户操作唤醒去发起呼叫/数据。
- 电池标称常见 **5-5-90**（Tx-Rx-Idle）；省电主要砍 Idle 监听占比。

### A.1 四种 MS 能耗态
| 态 | 含义 | 能耗直觉 |
|----|------|----------|
| Transmit | 发 PDU | 最高 |
| Receive | 通话中收语音、音频开 | 高 |
| Idle | 听 TSCC、处理过路 PDU | 接近 Receive |
| Sleep | 大部分关电 | 极低；不能收发 |

### A.1 Wake-up 省电直觉
- 仅当 TSCC **确定 MS 醒着**时才对其寻址；MS 仅在约定 **Power Save Frame** 醒窗听出站。
- 一帧省电窗示例尺度：**480 ms**（与 Part 4 Common Slot Counter / PS_Counter 对齐，见 A.2）。
- 例：MS(B) **4:1** → 醒 1 窗、睡 3 窗。个呼恰逢醒窗时建立时延≈无省电；落在睡窗则 TSCC **延迟 Grant**。

典型时序（导读级）：
```text
MS(A) --C_RAND(语音请求)--> TSCC
TSCC  --C_AHOY--> MS(B)（仅在已知醒窗）
MS(B) --ACK--> TSCC
TSCC  --C_GRANT--> A & B
```

### A.2 同步省电（与 Part 4 对齐）
- 规范过程：**TS 102 361-4 clause 6.4.7**。
- TSCC 在 CACH 带 **Common_Slot_Counter**（与 SYScode、Reg）；**PS_Counter = 计数器高 7 bit**，约每 **480 ms** +1 → MS 收到一次即可对齐省电帧界。
- **登记时**协商：`PowerSave_RQ`（3 bit）非 0 请求省电比；0 = 关闭/取消。

| PowerSave_RQ | 醒:睡 约 | Offset 范围（直觉） |
|--------------|----------|---------------------|
| 0 | OFF | 0 |
| 1 | 1:2 | 0…1 |
| 2 | 1:4 | 0…3 |
| 3 | 1:8 | 0…7 |
| 4 | 1:16 | 0…15 |
| 5+ | 1:32… | 见 PDF Table A.4 |

单组 / 多组 talkgroup 下的醒窗对齐细节见 TR A.2.2–A.2.3 与 Part 4。

---

## Annex B — Tier III 信道接入（导读）

### B.0
- 受管 TSCC 上，MS **只能**用随机接入（slotted Aloha + 受管退避）。
- 目标：控碰撞、控时延、保稳定、重载下保吞吐。
- 异步场景：TSCC 去键后，首次随机接入可唤醒物理 TSCC，之后由出站突发规管。

### B.1 抽槽（Withdrawn slots）
- TSCC 发出**需要特定 MS 应答**的 PDU 后，可通过 CACH **AT=busy** 把后续某入站时隙标为不可随机接入，留给该应答，避免与 RAND 相撞。
- **Aloha 本身不抽槽**；但 Mask=特殊值 + 空地址等可**禁止**随机接入（即便未抽槽）。
- MS 若选中已抽槽，则改选后续时隙再试。

### B.2 Mask / Service Function / Backoff
| 参数 | 作用 |
|------|------|
| **Mask** | 只允许 MS 地址子集接入（可细到“几乎全体”→“单个”），用于优先级/拥塞分割 |
| **Service Function** | 只允许某类业务请求（如仅登记） |
| **Random Backoff** | 以 TDMA frame 为单位广播；首次可尽快发，其后因 Mask/SF/抽槽/无应答而退避重试 |

细则与字段：Part 4 `C_ALOHA` / 随机接入条款（本库 [`../04-集群协议/集群协议字段速览.md`](../04-集群协议/集群协议字段速览.md)）。

---

## Annex C — 协议架构（与 Part 1 同构）

```text
L3 Call Control（C-plane：呼叫/固有/短数据/分组控制）
L2 Data Link（C-plane 信令 + U-plane 语音/数据流）
L1 Physical（突发比特、调制、同步、RF）
```

| 层 | 主规范 |
|----|--------|
| L1 / L2 | TS 102 361-1 |
| L3 语音等 | TS 102 361-2 |
| L3 数据 | TS 102 361-3 |
| Tier III 扩展 | TS 102 361-4 |

空口分层表：[`../01-空中接口/帧结构与字段定义.md`](../01-空中接口/帧结构与字段定义.md) §1。

---

## Annex D — 功率控制

- **开环直觉**：MS 可按收电平自行降发（常见 PMR 做法）。
- **闭环（规范）**：Tier III 若支持，见 **TS 102 361-4**；TS 测 MS 上行 RSSI，与上/下门限比：
  - 过高 → 发 **降功率** PDU；过低 → **升功率** PDU。
- 依赖 **Reverse Channel**；RC 并非始终可用；网内可混有不支持闭环的 MS。

---

## Annex E — Bibliography
**SKIP**（书目）。

---

## 回 PDF
TR Annex A–D 全文；Part 4：6.4.7 省电、6.2 随机接入、RC 功率相关条款。
