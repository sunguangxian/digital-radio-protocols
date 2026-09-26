# DMR Part 1 附：CSBK / LC / EMB 字段详表

> **学习用整理，冲突以 ETSI 原文为准；非全文复制。**  
> 主源：ETSI **TS 102 361-1 V2.7.1 (2026-05)** clause **7 / 9**；业务 Opcode 语义见 Part 2。  
> 本文件是 [`帧结构与字段定义.md`](./帧结构与字段定义.md) 的字段级补充：八位组布局、嵌入信令分片、FEC **名称**（无矩阵）。  
> **禁止事项**：不粘贴 Table 9.2 完整 SYNC hex；不复制 Annex B FEC 生成矩阵。

空口总览 → [`帧结构与字段定义.md`](./帧结构与字段定义.md)  
语音业务 PDU → [`../02-语音业务/语音业务字段速览.md`](../02-语音业务/语音业务字段速览.md)

---

## 1. 嵌入信令在突发中的位置

引用：TS 102 361-1 **clause 6.1** figure 6.4；**7.1.3**。

```text
语音突发（中心非 SYNC 时）：
  Voice(108) | EMB(8) | Embedded signalling(32) | EMB(8) | Voice(108)
               └────── EMB PDU 共 16 bit ──────┘
               └─ Embedded signalling 32 bit ─┘
```

| 路径 | 中心 48 bit 组成 | 条款 |
|------|------------------|------|
| Voice SYNC（超帧 A） | SYNC PDU 48 | 9.1.1 |
| 嵌入 LC / RC / Privacy / Null | EMB 16 + 嵌入载荷 32 | 6.1, 9.1.2 |
| 数据突发 | SlotType 20 + SYNC/嵌入 48 | 6.2, 9.1.3 |

一条 **Full LC**（72 bit 信息 + FEC）经 BPTC 后拆入超帧 **B–E** 四个 32-bit 嵌入场（Annex **B.2.1**）。

---

## 2. EMB PDU（Table 9.3）— 16 bits

引用：clause **9.1.2**。

| IE | Bits | 含义 / 备注 | 条款 |
|----|------|-------------|------|
| Colour Code (CC) | 4 | CC0…CC15 | 9.3.1 |
| Pre-emption and power control Indicator (PI) | 1 | `0` 本逻辑信道/Null；`1` 对端 RC | 9.3.2 |
| Link Control Start/Stop (LCSS) | 2 | 分片起止，见下表 | 9.3.3 |
| EMB parity | 9 | Quadratic Residue **(16,7,6)** | B.3.2 |

**LCSS**（Table 9.19 摘要）：

| Value | Meaning |
|-------|---------|
| 00 | 单片 LC **或** CSBK 首片（视上下文） |
| 01 | LC 首片（非单片） |
| 10 | 末片 |
| 11 | 续片 |

CACH 上 Short LC **无**「单片 LC」用法；CACH LCSS 规则见 clause **9.3.3**。

---

## 3. SLOT PDU（Table 9.4）— 20 bits

| IE | Bits | 备注 | 条款 |
|----|------|------|------|
| CC | 4 | | 9.3.1 |
| Data Type | 4 | Table 9.22 | 9.3.6 |
| Slot Type parity | 12 | Golay **(20,8)** | B.3.1 |

Data Type 编码见主文件 §8；本表强调：**SLOT 决定 196 信息比特如何解**（PI / Voice LC Header / Terminator / CSBK / MBC / Data Header / Rate½·¾·1 / Idle / USBD）。

---

## 4. FULL LC PDU（Table 9.7）— 八位组直觉

引用：clause **9.1.6**；figure **7.1**。

```text
头/终止突发路径（信息场 72 + CRC 相关 → 总 PDU 96 bit）：
  Octet0:  PF(1) | Reserved(1) | FLCO(6)
  Octet1:  FID(8)
  Octet2–8: Full LC Data (56)
  + Full LC CRC：头/终止 24 bit（Reed-Solomon (12,9)）；嵌入路径 5-bit checksum
嵌入路径信息场总长 77 bits（CRC 变短）。
```

| IE | Len | 备注 | 条款 |
|----|-----|------|------|
| Protect Flag (PF) | 1 | 现行置 `0` | 9.3.10 |
| Reserved | 1 | | |
| FLCO | 6 | 业务 Opcode → Part 2 | 9.3.11 |
| FID | 8 | SFID=`0x00` / MFID | 9.3.5 |
| Full LC Data | 56 | 地址、Service Options 等 | Part 2 |
| Full LC CRC | 24 或 5 | RS(12,9) 或 5-bit CS | B.3.6 / B.3.11 |

---

## 5. SHORT LC PDU（Table 9.8）— 经 CACH

| IE | Len | 备注 | 条款 |
|----|-----|------|------|
| SLCO | 4 | Part 2 | 9.3.12 |
| Short LC Data | 24 | | Part 2 |
| Short LC CRC | 8 | 8-bit CRC | B.3.7 |

28 bit 信息场 + CRC → CACH 侧再经 **Variable length BPTC for CACH**（Annex **B.2.3**）。

---

## 6. CSBK PDU（Table 9.9）— 96 bits 外壳

引用：clause **9.1.8**；figure **7.8**。

```text
  Octet0:  LB(1) | PF(1) | CSBKO(6)
  Octet1:  FID(8)
  Octet2–9: CSBK Data (64)   ← 业务字段，Part 2 / Part 4 定义
  + CSBK CRC 16 (CRC-CCITT, B.3.8)
```

| IE | Len | 备注 | 条款 |
|----|-----|------|------|
| Last Block (LB) | 1 | 单块 CSBK 置 `1`；MBC 头可为 `0` | 9.3.31 |
| PF | 1 | | 9.3.10 |
| CSBKO | 6 | Part 2 / Part 4 | 9.3.32 |
| FID | 8 | | 9.3.5 |
| CSBK Data | 64 | | |
| CSBK CRC | 16 | CRC-CCITT | B.3.8 |

**MBC**：多块控制用 Data Type = MBC Header / Continuation；末块 LB=`1`。Tier III 大量控制 PDU 共用此外壳（见 Part 4）。

---

## 7. RC PDU（Table 9.6）— 32 bits

| IE | Len | 备注 | 条款 |
|----|-----|------|------|
| RC Info Payload | 4 | **内容定义在 Part 4**（RC Command） | 9.1.5 NOTE |
| RC Info CRC | 7 | 7-bit CRC | B.3.13 |
| RC parity | 21 | Reverse Channel Single Burst BPTC | B.2.2.2 |

独立 RC 突发：**96 bits** = 48 SYNC + 48 嵌入窗口（clause **6.4**）。

---

## 8. SYNC 类型名（不贴 hex）

引用：clause **9.1.1** Tables **9.1–9.2**。SYNC PDU = **48 bits**。语音与数据图案**逐符号互补**。

| 类型名（学习用） | 使用场景摘要 |
|------------------|--------------|
| BS sourced Voice | 基站出站语音超帧 A |
| BS sourced Data | 基站出站数据/控制 |
| MS sourced Voice | 移动台上行语音 |
| MS sourced Data | 移动台上行数据/控制 |
| MS sourced standalone RC | 独立反向信道突发 |
| TDMA DM TS1 Voice / Data | 直通时隙 1 |
| TDMA DM TS2 Voice / Data | 直通时隙 2 |
| Reserved | 预留 |

完整 bit/hex 图案 → 打开 PDF **Table 9.2**（本库不复制）。

---

## 9. FEC / CRC 名称速查（无矩阵）

引用：Annex **B**。仅列名称、用途、条款；**实现矩阵见原文**。原则挂法：[`跳过项原则说明.md`](./跳过项原则说明.md)。

| 名称 | 典型用途 | 条款 |
|------|----------|------|
| BPTC (196,96) | 多数数据/控制 196-bit 信息块 | B.1.1 |
| Variable length BPTC（embedded） | 嵌入 LC 分片 | B.2.1 |
| Non-RC Single Burst BPTC | 单突发嵌入（非 RC） | B.2.2.1 |
| Reverse Channel Single Burst BPTC | RC PDU 奇偶 | B.2.2.2 |
| Variable length BPTC for CACH | Short LC → CACH | B.2.3 |
| Rate ¾ Trellis | Rate ¾ 数据 | B.2.4 |
| Rate 1 coded data | Rate 1 数据（无额外块 FEC） | B.2.5 |
| Golay (20,8) | SLOT parity | B.3.1 |
| Quadratic Residue (16,7,6) | EMB parity | B.3.2 |
| Hamming (17,12,3) 等 | BPTC 行列校验相关 | B.3.3–B.3.4 |
| Hamming (7,4,3) | TACT parity | B.3.5 |
| Reed-Solomon (12,9) | Full LC 头/终止 CRC 路径 | B.3.6 |
| 8-bit CRC | Short LC；Act_Updt hashed address | B.3.7 |
| CRC-CCITT (16) | CSBK / Data Header 等 | B.3.8 |
| 32-bit CRC | 确认/非确认消息 MsgCRC；C_RDATA | B.3.9 |
| CRC-9 | 确认数据块 DBSN+User | B.3.10 |
| 5-bit Checksum | 嵌入 Full LC | B.3.11 |
| Data Type CRC Mask | 头 CRC 掩码 | B.3.12 |
| 7-bit CRC | RC Info | B.3.13 |

交织：CACH interleaving 等 → **B.4**（不展开表）。

---

## 10. 其它 Layer 2 PDU 指针

| PDU | Len | 用途 | 条款 |
|-----|-----|------|------|
| TACT | 7 | CACH：AT+TC+LCSS+parity | 9.1.4 / 9.5 |
| PR FILL | 96 | Idle 填充 | 7.3 / D.2 |
| C_HEAD / U_HEAD / SP_HEAD / R_HEAD / DD_HEAD / UDT_HEAD / P_HEAD | 96 | 分组/短数据头 | 9.2 |
| C_RHEAD / C_RDATA | 96 | 确认响应 | 9.2.4–5 |
| Rate ½·¾·1 DATA / LDATA | 96/144/192… | 续块/末块 | 9.2.x |

数据头逐字段 → [`../03-数据协议/数据协议字段速览.md`](../03-数据协议/数据协议字段速览.md)。

---

## 11. 缺口

- MBC 续块八位组、Privacy Indicator 头内部字段未展开。  
- SYNC hex、FEC 矩阵、交织置换表刻意不抄。  
- FLCO/CSBKO 业务体 → Part 2；Tier III CSBKO → Part 4。
