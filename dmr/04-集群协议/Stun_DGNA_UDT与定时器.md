# DMR Part 4：Stun / Kill / Revive、DGNA、USBD、UDT 载荷与定时器

> **学习用整理，冲突以 ETSI 为准；非全文复制。**  
> 源：ETSI **TS 102 361-4 V1.12.1 (2023-07)**（`pdftotext -layout` 归纳）。  
> PDF：同目录 `TS102361-4_V1.12.1.pdf`  
> 总览：[`集群协议字段速览.md`](./集群协议字段速览.md)  
> Reason / Grant：[`ReasonCode与Grant变体.md`](./ReasonCode与Grant变体.md)  
> Announcement / Service_Kind：[`Announcement与其余枚举.md`](./Announcement与其余枚举.md)  
> 鉴权 / Annex C 频率：[`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md)

本文件补：Stun / Revive / Kill 过程场、**DGNA** PDU、**USBD** 轮询场、Annex **B.3** UDT 载荷格式、Annex **A** 定时器名表。不抄 MSC 长文、FEC 矩阵、SYNC hex。

---

## 0. 怎么认出这些业务

补充业务走 **Service_Kind = `1101₂`**（Supplementary Service，Table **7.49**）。细分靠 **Gateway / Identifier**（clause **A.4** / Table **A.8**），不是单独一套 Opcode。

| 业务 | Gateway Alias | DMR ID | 关键 Flag / Opcode | 过程条款 |
|------|---------------|--------|-------------------|----------|
| Stun / Revive | **STUNI** | `FFFECC₁₆` | C_AHOY `Service_Kind_Flag`：`0`=Stun，`1`=Revive | 6.4.9 |
| Kill | **KILLI** | `FFFECF₁₆` | Flag 固定 `0`；**必须鉴权** | 6.4.10 |
| DGNA | **DGNAI** | `FFFED6₁₆` | UDT Opcode `C_DGNAHD`/`C_DGNAHU` | 6.6.8 |
| 鉴权挑战源 | **AUTHI** | `FFFECD₁₆` | 登记/呼叫鉴权（PDU/K/PSN 见鉴权文件） | 6.4.8 |
| UDT 短数据 | **SDMI** | `FFFEC5₁₆` | `C_UDTHD`/`C_UDTHU` | 6.6.4 |
| 补充用户数据 | **SUPLI** | `FFFEC4₁₆` | SF=`1` 的 UDT | 6.4.13 |

USBD **不是** CSBKO 业务：Table **B.1** 无 `C_USBDD`/`C_USBDU`。它是独立单块（Tables **5.1 / 5.2**），LIP 子集见 6.6.11。

---

## 1. Stun / Revive / Kill

### 1.1 效果（6.4.9.0 / 6.4.10.0）

| 动作 | 效果 | 仍可用 | 空口恢复 |
|------|------|--------|----------|
| **Stun** | 不得请求/接收该网上用户发起的业务 | 猎站、登记、鉴权、Stun/Revive、**定位** | Revive（仍从 STUNI） |
| **Revive** | 恢复被 Stun 的能力 | — | — |
| **Kill** | **永久**失去全部 DMR 功能 | 无 | **任何空口消息都不能 Revive** |

本文只允许从 TSCC 网关 **STUNI** / **KILLI** 发起（6.4.9.1.1 / 6.4.10.0）。只对**个号**。

### 1.2 识别场（C_AHOY 外壳）

C_AHOY 通用外壳 Table **7.22**，CSBKO=`01 1100₂`（28）。Stun/Kill 把若干 IE 钉死：

**Stun/Revive — Table 6.19**（6.4.9.1.1；带鉴权仍用本表发首包）

| IE | Len | 取值 | 条款 |
|----|-----|------|------|
| Service_Options_Mirror | 7 | `000 0000₂`（Table **7.62** 亦全 0） | 7.2.14.2 |
| **Service_Kind_Flag** | 1 | **`0` Stun；`1` Revive** | 7.2.12.1 |
| Ambient Listening Service | 1 | `0` 不适用 | |
| G/I | 1 | `0` 个号 | |
| Appended_Blocks | 2 | `00₂` | |
| Service_Kind | 4 | 补充业务 `1101₂` | 7.2.12 |
| Target address | 24 | 被 Stun/Revive 的 MS 个号 | |
| Source Address or Gateway | 24 | **STUNI** | A.4 |

**Kill — Table 6.23**（6.4.10.1）

| IE | Len | 取值 |
|----|-----|------|
| Service_Options_Mirror | 7 | `000 0000₂`（Table **7.63**） |
| Service_Kind_Flag | 1 | **`0`（不适用 Revive）** |
| Ambient Listening Service / G/I / Appended_Blocks | 1+1+2 | `0` / `0` / `00₂` |
| Service_Kind | 4 | `1101₂` |
| Target address | 24 | 被 Kill 的 MS 个号 |
| Source Address or Gateway | 24 | **KILLI** |

Kill **没有**无鉴权变体。Stun/Revive 可选鉴权（MS 是否挑战由实现决定）。

### 1.3 过程摘要（不展开 MSC）

```text
无鉴权 Stun/Revive（Fig 6.31）
  TSCC --C_AHOY(STUNI, Flag=0/1)--> MS
  MS   --C_ACKU(Message_Accepted)  或  C_NACKU(MSNot_Supported)--> TSCC

带鉴权 Stun/Revive（Fig 6.32） / Kill（Fig 6.33，源=KILLI）
  TSCC --C_AHOY(STUNI|KILLI)--> MS
  MS   --C_ACKVIT(Target=Challenge 00 0000…FF FCDF₁₆)--> TSCC   # 兼作对 AHOY 的确认
  TSCC --C_ACKD(Reason=Authentication_Response 0110 0100₂, AddInfo=响应)--> MS
  MS   --C_ACKU(MS_Accepted)  成功并执行 stun/revive/kill
     或 --C_NACKU(Recipient_Refused)  鉴权失败，不改变状态
```

- 不支持该特性：一律 `C_NACKU(MSNot_Supported = 0000 0000₂)`，**不**做 Stun/Kill。  
- Kill 成功后 MS 关全部 DMR；若终 ACK 丢失，TS 再发 Kill 将收不到任何响应（6.4.10.0 NOTE）。  
- 散文与表对终 ACK Reason 用词不完全一致：6.4.9.2.0 写 `Message_Accepted`，Table **6.22 / 6.26** 写 `MS_Accepted = 0100 0100₂`。实现以 **7.2.8** 码值为准（见 Reason 文件）。

### 1.4 鉴权响应 / Ackvitation / 终 ACK 场

**TS → MS 鉴权响应 — Table 6.20（Stun）/ 6.24（Kill）**，外壳即 C_ACKD（Table **7.23**）

| IE | Len | 取值 |
|----|-----|------|
| Response_Info | 7 | 普通 G/I+Response_Check（非登记特例） |
| Reason Code | 8 | `0110 0100₂` Authentication Response |
| Reserved | 1 | `0` |
| Target address | 24 | 目标 MS |
| Additional Information (Source Address) | 24 | **Authentication Challenge Response** |

**MS → TS C_ACKVIT — Table 6.21 / 6.25**，CSBKO=`01 1110₂`（30）

| IE | Len | Stun/Revive | Kill |
|----|-----|-------------|------|
| Service_Options_Mirror | 7 | `000 0000₂` | `0000 000₂` |
| Service_Kind_Flag | 1 | `0` Stun / `1` Revive | `0` |
| Reserved | 2 | `0` | `0` |
| Appended_Blocks | 2 | `00₂` | `00₂` |
| Service_Kind | 4 | `1101₂` | `1101₂` |
| Target address | 24 | Challenge `00 0000₁₆`…`FF FCDF₁₆` | 同左 |
| Source | 24 | MS 个号 | MS 个号 |

**终 ACK — Table 6.22 / 6.26**（C_ACKU / C_NACKU）

| IE | Len | 取值 |
|----|-----|------|
| Reason | 8 | 成功 `MS_Accepted 0100 0100₂`；失败 `Recipient_Refused 0001 0100₂` |
| Target address | 24 | STUNI 或 KILLI |
| Additional Information (Source Address) | 24 | 本 MS 个号 |

### 1.5 本过程用到的 Reason（已在 Reason 文件全表）

| 方向 | Alias | Value | 何时 |
|------|-------|-------|------|
| MS→TS | MSNot_Supported | `0000 0000₂` | 不支持 Stun/Revive/Kill |
| MS→TS | MS_Accepted | `0100 0100₂` | 鉴权通过并执行 |
| MS→TS | Recipient_Refused | `0001 0100₂` | 鉴权失败，状态不变 |
| MS→TS | Message_Accepted | `0100 0100₂` 同码（散文名） | 无鉴权成功 |
| TS→MS | Authentication Response | `0110 0100₂` | 对 C_ACKVIT 的挑战响应 |

无独立 “Stun Result Code” 表。

---

## 2. DGNA（Dynamic Group Number Assignment）

引用：clause **6.6.8**；载荷格式 B.3.2（地址）/ B.3.9（Mixed 别名）。

### 2.1 规则

- **只对个号**。最多 **16** 个动态组：Address 模式 15 个 + Alias 模式 1 个。  
- 发起方可是 MS 或网关。网关发起时**只有出站 UDT 阶段**。  
- 走 multipart：`C_RAND(Target=DGNAI, Service_Kind=1101₂)` → AHOY 要上行 → `C_DGNAHU+AD` → 出站 `C_DGNAHD+AD` → 被叫 ACK → 镜像给主叫。

| 模式 | UDT_Format | 载荷 | 容量 |
|------|------------|------|------|
| **DGNA_Address** | `0001₂`（MS/TG Address） | B.3.2：OK + ADDRESS1…15 | 1…4 附块 → 3 / 7 / 11 / 15 个 24-bit 组号 |
| **DGNA_Alias** | `1010₂`（Mixed） | B.3.9：OK + 一个 ADDRESS + 最多 21 个 UTF-16BE | 给该组挂别名；也可给 Address 模式已下发的组补别名 |

收到 **Address 模式**成功传输：MS **删除**原 ADDRESS1…15，整表替换。空位填 **ADRNULL**（`000000₁₆`）。  
`OK=1` 且 ADDRESS1（Address 模式）或 ADDRESS（Alias 模式）= **One-key_talkgroup**（一键组）。`OK=0` 不改变已有一键组。

删除：

| 目标 | 做法 |
|------|------|
| 清空 Address 列表（15） | UAB 对应 1 块（`UAD1=00₂`），`OK=0`，ADDRESS1…3=ADRNULL |
| 删除第 16 个（仅 Alias 可赋） | Alias：ADDRESS=ADRNULL，`OK=0`，Pad Nibble=0，UAB=`00₂`，ALIAS=0 |

### 2.2 C_RAND 请求 — Table 6.70

| IE | Len | 取值 |
|----|-----|------|
| Service_Options | 7 | 全不适用/`0`（Emergency/SUPED_SV/BCAST/Priority 等） |
| Proxy Flag | 1 | `0` |
| Appended_Supplementary_Data (**SUPED_VAL**) | 2 | 需要的附块数 |
| Appended_UDT Short Data | 2 | `00₂` |
| Service_Kind | 4 | `1101₂` Supplementary |
| Target_address or Gateway | 24 | **DGNAI** |
| Source_address | 24 | 请求 MS 个号 |

被叫个号**不**在 C_RAND 里，等到上行 UDT 头的 Target。

### 2.3 合法即时响应（6.6.8.2.1 / 6.6.8.3.2）

`C_NACKD` / `C_QACKD` / `C_WACKD`；鉴权 `C_AHOY(Source=Challenge)`；或  
`C_AHOY(Service_Kind=1101₂, Source=DGNAI, Target=主叫, Appended_Blocks=请求的 UAB)` 令主叫上行。

### 2.4 UDT 头：出站 C_DGNAHD / 入站 C_DGNAHU

Opcode（Table **B.1**）：出站 **`10 0100₂`（36）`C_DGNAHD`**；入站 **`10 0101₂`（37）`C_DGNAHU`**。  
Table **6.66** 入站头 Opcode 写作 `10 0101₂`，与 6.71 一致。

**出站 Table 6.69 / 入站 Table 6.71**（阴影行来自 Part 1 UDT_HEAD）

| IE | Len | 出站 C_DGNAHD | 入站 C_DGNAHU |
|----|-----|---------------|---------------|
| G/I | 1 | `0` 个号 | `0` 个号 |
| A | 1 | `1` 要求个号响应 | `1` 要求响应 |
| Emergency / Reserved | 1 | Emergency=`0` | Reserved=`0` |
| UDT_Option_Flag / UDT_DIV | 1 | Table 7.51 | UDT_DIV=`0`（非改向） |
| Data Packet Format | 4 | `0000₂` | `0000₂` |
| SAP Identifier | 4 | `0000₂` UDT | `0000₂` |
| **UDT_Format** | 4 | Address=`0001₂`；Alias=`1010₂` | 同左 |
| Target | 24 | 被叫 MS | 被叫 MS |
| Source | 24 | 主叫 MS 或网关 | 主叫 MS |
| Pad Nibble | 5 | Address=`0 0000₂`；Alias 见 Table **B.9** | 同左 |
| Reserved | 1 | `0` | `0` |
| Appended_Blocks (UAB) | 2 | `00`…`11` = 1…4 附块 | 同左 |
| Supplementary_Flag (SF) | 1 | `0` 用户发起 | `0` |
| PF | 1 | RFU | RFU |
| Opcode | 6 | **`100100₂` C_DGNAHD** | **`100101₂` C_DGNAHU** |

### 2.5 Address 模式块数 ↔ 组号（Table 6.67）

| UAB（附块数−1） | 附块 | 写入的 ADDRESS |
|-----------------|------|----------------|
| `00₂` | 1 | 1…3 |
| `01₂` | 2 | 1…7 |
| `10₂` | 3 | 1…11 |
| `11₂` | 4 | 1…15 |

块 1：`RSVD(7) \| OK(1) \| ADDRESS1(24) \| ADDRESS2(24) \| ADDRESS3(24)`；后续块续编 24-bit 地址（跨块拆分见 B.3.2 图 B.6–B.9）。

### 2.6 Alias 模式块数 ↔ 别名字符（Table 6.68 / B.9）

块 1：`RSVD(7) \| OK(1) \| ADDRESS(24) \| ALIAS1…3`（各 UTF-16BE 16 bit）。其后每附块续 16-bit 字符，最多 ALIAS21。Pad Nibble 与字符数对照 Table **B.9**（§5.9）。

### 2.7 终 ACK

被叫对出站 UDT：`C_ACKU(MS_Accepted)`。TS 镜像 `C_ACKD(Mirrored_Reason=MS_Accepted)` 给主叫（6.6.8.2.3）。失败随时 `C_NACKD`。等待用 **TNP_Timer**。

---

## 3. USBD（Unified Single Block Data）轮询

引用：6.6.11；Tables **6.76–6.80**；IE **7.2.38 / 7.2.39**。

### 3.1 能力

| 方向 | PDU | 用户数据 |
|------|-----|----------|
| TSCC / TSCCAS → MS | **C_USBDD** Poll Request | 最多 **48** bit Parameters |
| MS → TSCC / TSCCAS | **C_USBDU** Poll Response | 最多 **68** bit（LIP 短报告场合计） |

单块、无附块。可在 **TSCCAS** 上与 Aloha 交错，实现大批量定位轮询。Response Delay 决定应答时隙；TSCC 上该时隙须从随机接入**收回**（6.6.11.1）。

不支持该 Service Type：可在预留时隙回 `C_NACK(MSNot_Supported 0000 0000₂)`。

### 3.2 Poll Request — Table 6.76（+ 7.99 / 7.100）

| IE | Len | 编码 |
|----|-----|------|
| **Service Type** | 4 | `0000₂` Short Location / LIP；`0001₂`…`0111₂` 保留；`1000₂`…`1111₂` 厂商 |
| **Response Delay (RD)** | 2 | 见下表 |
| **PC** (Payload Contents) | 1 | `0` 给被轮询 MS 的数据；`1` Privacy（本 Part 未定义） |
| Reserved | 1 | `0` |
| Parameters | 48 | 依 Service Type；LIP 且 PC=`0` 时为 `0x000000` |
| Target / LLID | 24 | 被轮询 MS |

**RD（Table 6.76 / 7.99）** — 从收完 Poll 到发 Response：

| RD | Aligned | Offset |
|----|---------|--------|
| `00₂` | 30 ms（下一 TDMA 帧） | 60 ms（下一帧 +1 时隙） |
| `01₂` | 90 ms（两帧） | 120 ms（两帧 +1 时隙） |
| `10₂` | 150 ms（三帧） | 180 ms（三帧 +1 时隙） |
| `11₂` | 210 ms（四帧） | 240 ms（四帧 +1 时隙） |

LIP 请求（Table **6.77**）：Service Type=`0000₂`，PC 有效，Parameters 在 PC=`0` 时全 0。端到端 LIP 时，MS 把该 Poll **解压**成 LIP Immediate Location Report Request（Table **6.78** 默认：Short Location Request、立即报告、短报告优先、位置/速度/航向 required、Max Age=Best Effort `1111111₂`）。其它 LIP 消息仍走控制信道 UDT。

### 3.3 LIP Poll Response — Table 6.79

| IE | Len | 备注 |
|----|-----|------|
| Service Type | 4 | `0000₂` Location (LIP) |
| Time Elapsed | 2 | TS 100 392-18-1 |
| Longitude | 25 | 同上 |
| Latitude | 24 | |
| Position Error | 3 | |
| Horizontal Velocity | 7 | |
| Direction of Travel | 4 | |
| **Reason for Sending** | 3 | Table **6.80**：仅 `000₂` = Response to Immediate Request（LIP value = **32**）；其余保留 |
| Hashed Source Address | 8 | Part 1 clause B.3.7 的 8-bit CRC 压缩源地址 |

这是 **3-bit LIP 场**，与 ACK 的 8-bit Reason Code **无关**。

---

## 4. 控制信道 UDT 头（C_UDTHD / C_UDTHU）

引用：7.1.1.1.8 / 7.1.1.2.4；载荷 Annex **B.3**。DGNA 用专用 Opcode，短数据用本对。

**Figure B.1 / 6.42 头八位组（学习用）**

```text
Octet0: G/I | A | RSVD | DPF/FORMAT(4)
Octet1: SAP(4) | UDT_Format(4)
Octet2–4: Target or Gateway (24)
Octet5–7: Source or Gateway (24)
Octet8: Pad Nibble(5) | 0 | UAB(2)
Octet9: SF | PF | Opcode(6)
```

### 4.1 出站 C_UDTHD — Table 7.24，Opcode `01 1010₂`（26）

| IE | Len | 含义 |
|----|-----|------|
| G/I | 1 | `0` 个号（可要求响应）；`1` 组（不指望响应） |
| A | 1 | `1` 要求响应（个号） |
| Emergency | 1 | `1` 紧急 |
| UDT_Option_Flag | 1 | Table 7.51（替代 Ahoy 检查时 = OACSU/FOACSU） |
| Data Packet Format | 4 | `0000₂` |
| SAP | 4 | `0000₂` UDT |
| **UDT_Format** | 4 | Table **7.88** |
| Target / Source | 24+24 | |
| Pad Nibble | 5 | 填满附块的 DigitNULL nibbles；二进制格式置 0 |
| UAB | 2 | `00`…`11` = **1…4** 附块 |
| SF | 1 | `0` 用户短数据/轮询；`1` 补充数据挂在其它业务上（6.5 NOTE） |
| PF | 1 | RFU=`0` |
| Opcode | 6 | `011010₂` C_UDTHD |

### 4.2 入站 C_UDTHU — Table 7.28，Opcode `01 1011₂`（27）

与出站几乎同构，差别：无 Emergency，改为 Reserved + **UDT_DIV**（`1`=本 UDT 携带改向目的）。组订阅列表请求时 Target=**TATTSI**。

附块须**连续**发送（6.5）。个号且 A=`1` 时收端要 ACK。

---

## 5. Annex B：Opcode 与 UDT 载荷格式

### 5.1 Opcode 速查 — Table B.1（与本文相关）

| OPCODE | OPCODE₂ | Alias | 用途 |
|--------|---------|-------|------|
| 26 | `01 1010₂` | C_UDTHD | UDT 出站头 |
| 27 | `01 1011₂` | C_UDTHU | UDT 入站头 |
| 28 | `01 1100₂` | C_AHOY / P_AHOY | 点名（Stun/Kill/DGNA 首包） |
| 30 | `01 1110₂` | C_ACKVIT | 鉴权挑战 |
| 31 | `01 1111₂` | C_RAND | 随机接入（含 DGNA 请求） |
| 32 / 33 | `10 0000₂` / `10 0001₂` | C_ACKD / C_ACKU | 确认 |
| 36 | `10 0100₂` | **C_DGNAHD** | DGNA 出站头 |
| 37 | `10 0101₂` | **C_DGNAHU** | DGNA 入站头 |
| 25 / 40 | `01 1001₂` / `10 1000₂` | C_ALOHA / C_BCAST | 已在其它文件 |

Grant / MOVE / P_CLEAR 等其余码：Reason/Grant 文件 §14 与 Announcement §9.6。SLCO：Table **B.2**（`0010₂` SYS_Parm，`0011₂` P_SYS_Parms）。

### 5.2 UDT_Format — Table 7.88（7.2.27）

| Value | 格式 | 条款 | 最大约 |
|-------|------|------|--------|
| `0000₂` | Binary | B.3.1 | 367 bit（末位置 0 定界） |
| `0001₂` | MS or TG Address | B.3.2 | 15×24-bit |
| `0010₂` | 4-bit BCD | B.3.3 | 92 位 |
| `0011₂` | ISO 7-bit（ISO/IEC 646） | B.3.4 | 52 符 |
| `0100₂` | ISO 8-bit（ISO/IEC 8859） | B.3.5 | 46 符 |
| `0101₂` | NMEA（IEC 61162-1） | B.3.6 | 1 或 2 附块 |
| `0110₂` | IP address | B.3.7 | IPv4 1 块 / IPv6 2 块 |
| `0111₂` | UTF-16BE | B.3.8 | 23 符 |
| `1000₂`/`1001₂` | 厂商 | | |
| `1010₂` | **Mixed**（1 地址 + UTF-16BE） | B.3.9 | 1 地址 + 21 符（DGNA_Alias） |
| `1011₂` | LIP | B.3.10 | ≤46 字节应用数据（格式在 TS 100 392-18-1） |
| `1100₂`…`1111₂` | 保留 | | |

UAB 在表里常写成 0…3，等于 2-bit 场值 = **附块数 − 1**。头块后最多 4 个附块；续块 12 八位组（96 bit），**末块**用户区常按 10 八位组（80 bit）计。

### 5.3 Binary — B.3.1（UDTF=`0000₂`）

Pad Nibble=`0 0000₂`。变长：用户比特后加一个 `0`，其余填 `1`；收端从块尾回扫到第一个 `0`，其前一比特为用户末位。  
容量：1 块 1…79；2 块 80…175；3 块 176…271；4 块 272…**367**（96+96+96+79）。

### 5.4 Address — B.3.2（UDTF=`0001₂`，DGNA_Address）

未用地址 = ADRNULL。

| 附块 | 地址数 | 首块布局 |
|------|--------|----------|
| 1 | 3 | `RSVD(7)\|OK(1)` + ADDRESS1…3（各 24） |
| 2 | 7 | ADDRESS4 跨块（16+8） |
| 3 | 11 | |
| 4 | 15 | |

OK：`1` ⇒ ADDRESS1 为一键组（DGNA）。

### 5.5 BCD — B.3.3（UDTF=`0010₂`）

每 nibble 一数字，拨号顺序（先发的数字在 octet0 高 nibble）。填充 nibble=`1111₂` **DigitNULL**。  
**规则**（替代 Table B.3 92 行）：满块容量 = `20 + 24×UAB` 位；`Pad Nibble = 容量 − 用户位数`。  
1–20 → UAB=0；21–44 → 1；45–68 → 2；69–92 → 3。电话缩写编码见 7.2.9。

### 5.6 ISO 7 / ISO 8 / Unicode — B.3.4–B.3.5 / B.3.8

| 格式 | 每符 | 最多 | Pad | 表 |
|------|------|------|-----|----|
| ISO 7 | 7 bit 紧排 | 52 | DigitNULL nibbles，Table **B.4**（1 符 Pad=18 … 52 符 Pad=1） | 图 B.14–B.17 |
| ISO 8 | 1 八位组 | 46 | 每符少 2 nibble；满块 10/12/12/12 符 | Table **B.5** |
| UTF-16BE | 16 bit | 23 | Table **B.8**（1 符 Pad=16 … 23 符 Pad=0） | 图 B.27–B.30 |

不抄位图。需要精确 Pad 时查对应表。

### 5.7 NMEA — B.3.6（UDTF=`0101₂`）

Pad Nibble 固定 `0`。UAB 选格式（Table **B.6**）：

| 格式 | UAB | 内容 |
|------|-----|------|
| Short | `00₂` | 1 块；UTC 秒用 **UTCss3**（10 s 步进） |
| Long specified | `01₂` | 2 块；**UTCss6**（1 s）；MFID=SFID=`0`；第 2 块含 COG(9)+Spare |
| Long unspecified | `10₂` | 2 块厂商；末八位组 MFID；其余 Spare |
| 保留 | `11₂` | |

**Table B.7 场（短/长指定共用）**

| Alias | Len | 含义 |
|-------|-----|------|
| C | 1 | `0` 未加密；`1` 加密 |
| NS | 1 | `0` 南；`1` 北 |
| EW | 1 | `0` 西；`1` 东 |
| Q | 1 | `0` 无定位；`1` 有效 |
| SPEED | 7 | 节 0…126；127=>126 |
| NDEG / NMINmm / NMINF | 7+6+14 | 纬度 度 / 分 / 分小数 0000…9999 |
| EDEG / EMINmm / EMINF | 8+6+14 | 经度 度 / 分 / 分小数 |
| UTChh / UTCmm | 5+6 | UTC 时/分 |
| UTCss3 / UTCss6 | 3 / 6 | 见上 |
| DOP | 5 | 1…31（长格式相关） |
| COG | 9 | 对地航向 0…359 |
| MFID | 8 | 厂商 FID（Part 1 Annex H） |

### 5.8 IP — B.3.7（UDTF=`0110₂`）

| 变体 | 附块 | 布局 |
|------|------|------|
| IPv4 | 1 | IPv4(32) + RSVD(48) |
| IPv6 | 2 | IPv6(128) 跨两块 + RSVD(48) |

IP 连接通告（6.4.11）用本格式，Target=**IPI**。

### 5.9 Mixed — B.3.9（UDTF=`1010₂`，DGNA_Alias）

`RSVD(7)\|OK(1)\|ADDRESS(24)\|` 随后 UTF-16BE 字符。Table **B.9**：

| 字符数 | UAB | Pad Nibble | 字符数 | UAB | Pad |
|--------|-----|------------|--------|-----|-----|
| 1 | 0 | 8 | 12 | 2 | 12 |
| 2 | 0 | 4 | 13 | 2 | 8 |
| 3 | 0 | 0 | 14 | 2 | 4 |
| 4 | 1 | 20 | 15 | 2 | 0 |
| 5 | 1 | 16 | 16 | 3 | 20 |
| 6 | 1 | 12 | 17 | 3 | 16 |
| 7 | 1 | 8 | 18 | 3 | 12 |
| 8 | 1 | 4 | 19 | 3 | 8 |
| 9 | 1 | 0 | 20 | 3 | 4 |
| 10 | 2 | 20 | 21 | 3 | 0 |
| 11 | 2 | 16 | | | |

### 5.10 LIP 作为 UDT 载荷 — B.3.10

UDTF=`1011₂`：最多 46 字节 LIP 应用数据，**块内格式不在 Part 4 展开**（TS 100 392-18-1）。控制信道大批量立即位置用 **USBD** 压缩子集（§3），其它 LIP 仍走本格式 UDT。

---

## 6. Annex A 定时器 / 常数 / 网关

### 6.1 Layer 3 定时器 — Table A.1

规范给的是**可配置范围**，不是单一出厂默认。Broadcast `CallTimer_Parms`（Table 7.70）另用 token 编紧急/分组/MS–MS/MS–Line 时长。

| Mnemonic | 范围（表内） | 用途 |
|----------|--------------|------|
| **Trand_TC** | 2…60 s | MS 随机接入尝试超时 |
| **T_Nosig** | 1…15 s | 收不到 TSCC 则进入猎站 |
| **T_EMERG_TIMER** | 1…510 s；511=∞ | 紧急呼叫定时；token 见 A.2 |
| **T_PACKET_TIMER** | 1…30 s；31=∞ | 分组呼叫；token A.3 |
| **T_MS-MS_TIMER** | 1…4094 s；4095=∞ | MS–MS / 组；token A.4 |
| **T_MS-LINE_TIMER** | 同上 | 线路连接呼叫；token A.5 |
| **TP_Timer** | 4…60 s | 主叫等**需要业务信道**的呼叫 |
| **TNP_Timer** | 2…60 s | 主叫等**仅控制信道**业务（登记/UDT/DGNA/Stun 后续） |
| **T_Awake** | 0.1…60 s（0.1 s 步） | 省电：收 PDU 后保持醒 |
| **TV_Hangtime** | 1…60 s | 语音业务信道挂机保持 |
| **TV_Item** | 10…60 s | 语音最大 item |
| **TV_Inactive** | 0…20 s | 语音无活动 |
| **TD_Inactive** | 0…20 s | 数据无活动 |
| **TD_Item** | 1…60 s | 分组最大 item |
| **TD_Hangtime** | 1…60 s | 数据挂机保持 |
| **T_AnswerCall** | 2…60 s | 被叫收 FOACSU AHOY 后等待 |
| **T_Pending** | 2…60 s | 被叫收 OACSU AHOY 后等待 |
| **T_dereg** | 0.2…2 s（0.1 s 步） | 关机/换网前注销，超时则放弃 |
| **T_BS_Inactive** | 1…300 s | 非管制 TSCC 入站无活动则休眠 |
| **T_DENREG** | 0=关；1…1000 ×10 s | Denied Registration 表项寿命 |
| **T_Late** | — | **V1.9.1 起废弃** |
| **T_ALS** | 10…300 s | ALS 普通优先级 |
| **T_ALS_E** | 10…14400 s | ALS 紧急 |
| **T_ALS_REQUEST_LIFE_SPAN** | 1…10 s | AHOY 到 GRANT 的最大间隔，超时被叫取消 ALS |
| **T_ALS_RETRANSMIT_DELAY** | 0…5 s | ALS 目标被打断后最短再键控间隔 |

过程用法：主叫在 C_RAND 后启 TP_ 或 TNP_；收到适用 ACK/AHOY 刷新；超时放弃（6.2.1.2 / 6.6.1.5）。

### 6.2 Call Timer token（A.2–A.5）— 只记档位

C_BCAST `CallTimer_Parms` 的 9/5/12/12 bit 场按下列**非线性档**解释（`0` 在 7.70 表示“用 MS 内部定时器”）：

| 场 | 细档 | 随后 | ∞ |
|----|------|------|---|
| T_EMERG_TIMER (A.2) | 1…10 = 秒 | 11…20 每 5 s；21…28 每 15 s；29…40 每 30 s；41…51 每 1 min；52…510 每 5 min | 511 |
| T_PACKET_TIMER (A.3) | 1…5 = 秒 | 6…10 每 5 s；11…12 每 15 s；13…20 每 30 s；21…25 每 1 min；26…30 每 5 min | 31 |
| T_MS-MS / T_MS-LINE (A.4 / A.5) | 1…59 = 秒 | 60…107 每 5 s；108…138 每 30 s；139…4094 每 1 min | 4095 |

### 6.3 Layer 3 常数 — Table A.6（同 Annex，便于对照）

| Mnemonic | 值 | 用途 |
|----------|----|------|
| NDefault_NW | 5 | 开机 NRand_Wait |
| NRand_NR | 6 | 普通/高优先级随机接入次数 |
| NRand_NE | 10 | 紧急随机接入次数 |
| N_Maint | 4 | MS 发 P_MAINT 清业务信道次数 |
| Nmax_Ch | 50 | Short Hunt 最少信道数 |
| Ch_Pref | 50 | Vote_Now 优选 TSCC 标记数 |
| Low_Comp_Ch / High_Comp_Ch | 1…4095 | 全猎逻辑信道范围 |
| Comp_Flag | True/False | 抑制 Comprehensive Hunt（Annex D） |
| NSYSerr | 1…3 | 与已验证 C_SYScode 不符的次数门限 |
| DMRLA | 1…10 | C_SYScode 中 SYS_AREA 场长 |
| VOTE_BLK | 2…10 | Vote Now 后 TSCC 收回随机接入的 TDMA 帧数 |

电平 L_*（Table **A.7**）为厂商单位，不抄。

### 6.4 网关 / 全呼 ID — Table A.8（本文用到的 + 邻近）

| ID | Alias | 用途 |
|----|-------|------|
| `FFFEC0₁₆` / `FFFED0₁₆` | PSTNI / PSTNDI | PSTN 网关（aligned / offset） |
| `FFFEC1₁₆` / `FFFED1₁₆` | PABXI / PABXDI | PABX |
| `FFFEC2₁₆` / `FFFED2₁₆` | LINEI / LINEDI | 线路 |
| `FFFEC3₁₆` / `FFFED5₁₆` | IPI / IPDI | IP 网关 |
| `FFFEC4₁₆` | SUPLI | 补充数据 |
| `FFFEC5₁₆` | SDMI | UDT 短数据 |
| `FFFEC6₁₆` | REGI | 登记 |
| `FFFEC9₁₆` | DIVERTI | 取消改向 |
| `FFFECA₁₆` | TSI | TS 自身 |
| `FFFECB₁₆` / `FFFED3₁₆` | DISPATI / DISPATDI | 调度 |
| **`FFFECC₁₆`** | **STUNI** | Stun/Revive |
| `FFFECD₁₆` | AUTHI | 鉴权 |
| **`FFFECE₁₆`** | GPI | 改向到组 |
| **`FFFECF₁₆`** | **KILLI** | Kill |
| `FFFED4₁₆` | ALLMSI | 全部个号+组 |
| **`FFFED6₁₆`** | **DGNAI** | DGNA |
| `FFFED7₁₆` | TATTSI | 组订阅/附着 |
| `FFFFFD/FE/FF₁₆` | ALLMSIDL / ALLMSIDZ / ALLMSID | 单站 / 站子集 / 全网组呼 |
| `000000₁₆` | ADRNULL | 空地址 |
| `000₁₆` | CHNULL | 空逻辑信道 |
| `1111₂` | DigitNULL | BCD 填充 |

aligned vs offset 后缀：业务信道时序（6.6.1.6）。

---

## 7. 覆盖与缺口

### 已覆盖

| 条款 / 表 | 内容 |
|-----------|------|
| 6.4.9–6.4.10 Tables **6.19–6.26** | Stun/Revive/Kill 场与 Reason |
| 7.2.14.2–3 Tables **7.62–7.63** | Service_Options_Mirror |
| 6.6.8 Tables **6.66–6.71** | DGNA 模式、C_RAND、两向 UDT 头 |
| 6.6.11 Tables **6.76–6.80** | USBD + LIP 压缩子集 |
| 7.1.1.1.8 / 7.1.1.2.4 Tables **7.24 / 7.28** | C_UDTHD / C_UDTHU |
| 7.2.27 Table **7.88**；B.3.0–B.3.10 | UDT_Format 与各载荷规则 |
| A.1–A.4 Tables **A.1–A.8** | 定时器名/范围、token 档、常数、网关 |
| B.1 | 相关 Opcode |

### 未展开 / 仍缺

| 项 | 说明 |
|----|------|
| 鉴权算法、K / PSN、挑战响应计算 | 已迁出 → [`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md) |
| Stun/Kill 完整时序图与 aligned/offset 槽位 | 以 Fig 6.31–6.33 PDF 为准 |
| NMEA / ISO7 位图（Fig B.14–B.24） | 场名已收；不抄跨页图 |
| LIP 全 PDU（TS 100 392-18-1） | 仅 USBD 子集 + UDT 指针 |
| USBD 物理块外壳（Part 1 Data Type） | Part 4 只给 80-bit 信息场 |
| CdefParms / Annex C 频率公式 | 已迁出 → [`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md) |
| Annex D 猎站状态机 | 已迁出 → [`AnnexD猎站Hunt.md`](./AnnexD猎站Hunt.md) |
| 组订阅/附着（TATTSI）完整 PDU | 仅网关指针；过程 6.4.4.1.13 |

---

*学习向整理。实现与互操作请核对 ETSI TS 102 361-4 V1.12.1 原文。*
