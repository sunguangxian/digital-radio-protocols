# DMR Part 4：Reason Code 与 Grant 变体

> **学习用整理，冲突以 ETSI TS 102 361-4 V1.12.1 (2023-07) 为准；非全文复制。**  
> 源 PDF：同目录 `TS102361-4_V1.12.1.pdf`（`pdftotext -layout` 归纳）。  
> 总览：[`集群协议字段速览.md`](./集群协议字段速览.md)  
> 公告 / Service_Kind / Service_Options 等其余枚举：[`Announcement与其余枚举.md`](./Announcement与其余枚举.md)
> Stun / DGNA / USBD / UDT / 定时器：[`Stun_DGNA_UDT与定时器.md`](./Stun_DGNA_UDT与定时器.md)  
> 鉴权 / Annex C 频率：[`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md)

相关：Aloha / Ahoy 外壳见速览 §4–§6；ACK 外壳见速览 §7 与本文 §4。

---

## 0. 读法（Reason 与 Grant 怎么配合）

```text
MS --C_RAND(Service_Kind)--> TSCC
TSCC --C_AHOY?--> MS --C_ACKU(Reason)--> TSCC     # 可达性/鉴权/点名
TSCC --C_ACKD / C_NACKD / C_QACKD / C_WACKD--> MS # Reason + Response_Info
TSCC --C_GRANT×重复--> 主被叫                     # 成功则转业务信道；Grant 本身无 Reason
```

- **Reason Code** 只出现在确认族：`C_ACKD/C_NACKD/C_QACKD/C_WACKD`（出站）与 `C_ACKU/C_NACKU`（入站）；业务信道上对应 `P_ACKD/P_NACKD/P_ACKU`（结构同 TSCC，见 7.1.1.3.5 / 7.1.1.4.2）。
- **C_ALOHA / C_AHOY / C_RAND 不带 Reason**。Ahoy 用 `Service_Kind` + `Service_Kind_Flag` 说明“在查什么”；MS 用 ACK/NACK 的 Reason 回答。
- **Channel Grant 不要求确认**，故常重复发送（clause 4 / 7.1.1.1.1）。成功路径是 Grant，失败路径是 NACK Reason。
- 登记拒绝 **没有单独一张“Reg Reject 表”**：走 C_NACK 的 `Reg_Refused` / `Reg_Denied`（Table **7.43**），过程见 6.4.4。

---

## 1. Reason 编码骨架（clause 7.2.8）

引用：7.2.8.0；表 **7.42–7.45**。长度 **8 bit**。位布局：

```text
  bit7 bit6 | bit5 | bit4 … bit0
    t    t  |  d   |  a  a  a  a  a
    ACK类型 | 方向 |   原因码
```

| 场 | 位 | 编码 | 含义 |
|----|----|------|------|
| **tt** ACK type | 2 | `00` NACK；`01` ACK；`10` QACK；`11` WACK | 决定落哪张表 |
| **d** direction | 1 | `1` TS→MS；`0` MS→TS（或 TS **原样镜像** MS 的 Reason，称 **Mirrored_Reason**） | |
| **aaaaa** | 5 | 具体原因 | |

**Mirrored_Reason**（7.2.8.0）：被叫 MS 的 `C_ACKU/C_NACKU` Reason 由 TS 原样转发给主叫（`C_ACKD/C_NACKD`），方向位保持 MS 侧 `d=0`。

下表 Value 按规范二进制（`xxxx xxxx₂`）列出，并附十六进制便于对照。

---

## 2. C_ACK — 肯定最终确认（Table 7.42）

引用：7.2.8.1。`tt=01`。

### 2.1 TS → MS（`d=1`，形如 `0110 xxxxx₂`）

| 名称 / Alias | Value | Hex | 含义 | 条款 |
|--------------|-------|-----|------|------|
| Message_Accepted | `0110 0000₂` | 0x60 | TS 接受，继续 | 7.2.8.1 |
| Store_Forward | `0110 0001₂` | 0x61 | 存贮转发：被叫未登记，等其登记后再投递 | 7.2.8.1 |
| **Reg_Accepted** | `0110 0010₂` | 0x62 | 登记请求被接受 | 7.2.8.1；6.4.4 |
| Accepted for the Status Polling Service | `0110 0011₂` | 0x63 | 状态轮询接受；**Response_Info = Status** | 7.2.8.1；7.2.7 |
| Authentication Response | `0110 0100₂` | 0x64 | TS 对鉴权挑战的响应 | 7.2.8.1；6.4.8 |
| **Reg_Subscription/Attachment service** | `0110 0101₂` | 0x65 | 登记 + 组订阅/附着；**Response_Info = Index pattern** | 7.2.8.1；6.4.4.1.13；Table 6.10 |

### 2.2 MS → TS（`d=0`，形如 `0100 xxxxx₂`；可被镜像）

| 名称 / Alias | Value | Hex | 含义 | 条款 |
|--------------|-------|-----|------|------|
| **MS_Accepted** | `0100 0100₂` | 0x44 | MS 接受（或 TS 镜像） | 7.2.8.1 |
| CallBack | `0100 0101₂` | 0x45 | 被叫稍后回呼（或镜像） | 7.2.8.1；6.6.10 |
| MS_ALERTING | `0100 0110₂` | 0x46 | 振铃中尚未 RFC（或镜像） | 7.2.8.1；6.6.10 |
| Accepted for the Status Polling Service | `0100 0111₂` | 0x47 | 状态轮询接受；Response_Info 含 Status | 7.2.8.1 |
| Authentication Response | `0100 1000₂` | 0x48 | MS 对鉴权挑战的响应 | 7.2.8.1；Table 6.18 |

过程条款里常见写法：`C_ACKU(Reason = MS_Accepted [0100 0100₂])`，镜像为 `C_ACKD(Mirrored_Reason = MS_Accepted)`。

---

## 3. C_NACK — 拒绝 / 否定最终确认（Table 7.43）

引用：7.2.8.2。`tt=00`。规范先用散文列语义，再以 Table 7.43 汇总。

### 3.1 网络（TS）拒绝（`d=1`，形如 `001x xxxxx₂`）

| 名称 / Mnemonic | Value | Hex | 含义（学习口径） | 条款 |
|-----------------|-------|-----|------------------|------|
| Not_Supported | `0010 0000₂` | 0x20 | 已登记，但网络不支持该业务 | 7.2.8.2 a；Table 6.60 |
| Perm_User_Refused | `0010 0001₂` | 0x21 | 该用户**永久**未授权该业务（“永久”厂商定义） | 7.2.8.2 |
| Temp_User_Refused | `0010 0010₂` | 0x22 | 该用户**暂时**未授权（例：PSTN 中继故障） | 7.2.8.2 |
| Transient_Sys_Refused | `0010 0011₂` | 0x23 | 此刻网络不可提供该业务（含改向目标不允许，Table 6.60） | 7.2.8.2 |
| NoregMSaway_Refused | `0010 0100₂` | 0x24 | 被叫合法但**未登记**（关机注销等） | 7.2.8.2 |
| MSaway_Refused | `0010 0101₂` | 0x25 | 被叫已登记，但无线检查无响应 | 7.2.8.2 |
| Div_Cause_Fail | `0010 0110₂` | 0x26 | 被叫已改向，短数据轮询无法进行 | 7.2.8.2；6.6.5.1.1 |
| SYSbusy_Refused | `0010 0111₂` | 0x27 | 网络过载，无法提供 | 7.2.8.2 |
| SYS_NotReady | `0010 1000₂` | 0x28 | 网络未就绪（维护/建设），请稍后 | 7.2.8.2 |
| Call_Cancel_Refused | `0010 1001₂` | 0x29 | 主叫在 QACK/WACK 后取消，但呼叫已无法取消（可能仍会成熟） | 7.2.8.2 |
| **Reg_Refused** | `0010 1010₂` | 0x2A | 登记被**拒绝**（可再试其它站；见 6.4.4） | 7.2.8.2；6.4.4 |
| **Reg_Denied** | `0010 1011₂` | 0x2B | 登记被**否决**（优先用于把 MS 从该 TSCC 赶走；记入 Denied Registration List） | 7.2.8.2；6.4.4 |
| IP_Connection_failed | `0010 1100₂` | 0x2C | IP 连接通告失败 | 7.2.8.2；6.4.11 |
| MS_Not_Registered | `0010 1101₂` | 0x2D | 系统要求先登记再做业务，MS 未登记 | 7.2.8.2；6.4.4 |
| Called_Party_Busy | `0010 1110₂` | 0x2E | 被叫忙且网络不愿排队 | 7.2.8.2 |
| Called_Group_Not_Allowed | `0010 1111₂` | 0x2F | 组号不被本 TSCC 允许 | 7.2.8.2 |
| CRC_error_in_the_UDT_Upload_phase | `0011 0000₂` | 0x30 | UDT 上行 CRC 错，呼叫无法继续 | 7.2.8.2 |
| Duplex_Congestion | `0011 0001₂` | 0x31 | 双工资源不足；MS 可改半双工 | 7.2.8.2 |
| Refused_Reason_Unknown | `0011 1111₂` | 0x3F | 拒绝但原因未知 | 7.2.8.2 |

`0011 0010₂` … `0011 1110₂` 未在 Table 7.43 给出。

### 3.2 MS 拒绝（`d=0`，可被镜像；形如 `000x xxxxx₂`）

| 名称 / Mnemonic | Value | Hex | 含义 | 条款 |
|-----------------|-------|-----|------|------|
| **MSNot_Supported** | `0000 0000₂` | 0x00 | MS 不支持该业务/特性（Stun/ALS 等常见） | 7.2.8.2 b；Table 6.47 |
| LineNot_Supported | `0001 0001₂` | 0x11 | 需要线路侧设备但未安装 | 7.2.8.2 |
| StackFull_Refused | `0001 0010₂` | 0x12 | 被叫内部呼叫栈满且非 FIFO | 7.2.8.2 |
| EquipBusy_Refused | `0001 0011₂` | 0x13 | 被叫附属设备忙 | 7.2.8.2 |
| **Recipient_Refused** | `0001 0100₂` | 0x14 | 被叫用户拒接（FOACSU：`C_NACKD` 给主叫） | 7.2.8.2；6.6.1.4.2 |
| Custom_Refused | `0001 0101₂` | 0x15 | 厂商自定义拒因（**不含登记过程**） | 7.2.8.2 |
| **MS_Duplex_Not_Supported** | `0001 0110₂` | 0x16 | 不支持 MS–MS 全双工（**7.2.8.2 散文有，Table 7.43 表体未列**） | 7.2.8.2 b；6.6.10 |
| Refused_Reason_Unknown | `0001 1111₂` | 0x1F | MS 侧拒绝原因未知 | 7.2.8.2 |

`0000 0001₂`…`0001 0000₂`、`0001 0111₂`…`0001 1110₂` 未分配。

---

## 4. C_QACK / C_WACK（Table 7.44 / 7.45）

引用：7.2.8.3。仅 TS→MS（`d=1`）。非最终：后面还有信令。

### 4.1 C_QACK — 排队（`tt=10`）

| Alias | Value | Hex | 含义 | 表 |
|-------|-------|-----|------|----|
| Queued-for-resource（如业务信道） | `1010 0000₂` | 0xA0 | 已接受，等资源，后续还有信令 | 7.44 |
| Queued-for-busy | `1010 0001₂` | 0xA1 | 被叫正忙于其它呼叫 | 7.44 |

### 4.2 C_WACK — 中间确认（`tt=11`）

| Alias | Value | Hex | 含义 | 表 |
|-------|-------|-----|------|----|
| Wait | `1110 0000₂` | 0xE0 | 已接受，后续还有信令（登记/呼叫建立常见） | 7.45 |

---

## 5. 确认 PDU 字段布局（Reason 的载体）

### 5.1 C_ACKD 出站（Table 7.23）CSBKO=`10 0000₂`（32）

引用：7.1.1.1.7。单块 CSBK，LB=`1`。同一 Opcode 承载 ACK/NACK/QACK/WACK，**靠 Reason 的 tt 区分**。

```text
Octet0: LB(1)=1 | PF(1) | CSBKO(6)=10 0000
Octet1: FID(8)=0000 0000
Octet2: Response_Info(7) | Reason[7]
Octet3: Reason[6:0] | Reserved(1)=0
Octet4–6: Target address (24)     = 原请求 MS
Octet7–9: Additional Info / Source (24) = 请求目的或网关
```

| IE | Len | 含义 | 条款 |
|----|-----|------|------|
| LB / PF / CSBKO / FID | 1+1+6+8 | CSBKO=`100000₂` | 7.1.1.1.7 |
| Response_Info | 7 | 随 Reason 变化，见 §6 | 7.2.7 |
| **Reason Code** | 8 | 本文 §1–§4 | 7.2.8 |
| Reserved | 1 | `0` | |
| Target address | 24 | 原请求 MS | |
| Additional Information (Source Address) | 24 | 请求目的/网关 | |

类别别名（同一外壳）：`C_ACKD` / `C_NACKD` / `C_QACKD` / `C_WACKD`。

### 5.2 C_ACKU 入站（Table 7.27）CSBKO=`10 0001₂`（33）

引用：7.1.1.2.3。MS→TS。类别：`C_ACKU` / `C_NACKU`（入站无 QACK/WACK）。

| IE | Len | 含义 | 条款 |
|----|-----|------|------|
| LB / PF / CSBKO / FID | 1+1+6+8 | CSBKO=`100001₂` | 7.1.1.2.3 |
| Response_Info | 7 | | 7.2.7 |
| **Reason Code** | 8 | | 7.2.8 |
| Reserved | 1 | `0` | |
| Target address 或 Authentication | 24 | 对应 TS PDU 的 Source；鉴权时为挑战响应 | Table 6.18 |
| Additional Information (Source Address) | 24 | 发确认的 MS 个号 | |

### 5.3 业务信道 P_ACK（结构同 TSCC）

| 别名 | CSBKO | 方向 | 表 / 条款 |
|------|-------|------|-----------|
| P_ACKD / P_NACKD | `10 0010₂`（34） | TS→MS 业务信道 | Table 7.3；7.1.1.3.5 |
| P_ACKU / P_NACKU | `10 0011₂`（35） | MS→TS 业务信道 | Table 7.4；7.1.1.4.2 |

7.1.1.4.2：**结构与 TSCC 确认相同**，Reason 表仍是 7.42–7.45。过程中常见 `P_ACKU(Reason = MS_Accepted / Message_Accepted)`。

---

## 6. Response_Info（Table 7.41）— 与 Reason 成对

引用：7.2.7。7 bit，含义**依赖 Reason**。

| 当 Reason = | Response_Info 内容 | 备注 |
|-------------|-------------------|------|
| Reg_Accepted `0110 0010₂` | PowerSave_Offset（7） | 省电偏移；目标为 MS 个号。6.4.7 |
| Accepted for Status Polling `0110 0011₂` / `0100 0111₂` | Status（7） | 状态值 |
| Reg_Subscription/Attachment `0110 0101₂` | Index pattern（7） | 7 个组地址各 1 校验位，见 Table **6.10** |
| **其它所有 Reason** | G/I（1）+ Response_Check（6） | G/I：`0` 个号/网关，`1` 组；Response_Check = C_SYScode 的 NET+SITE 中 6 个 LSB（figure 6.19 bit 8…3） |

**Table 6.10 Index Pattern**（登记+组列表）：

| 列表项 | Response_Info 位 |
|--------|------------------|
| ADDRESS1 | `x------` |
| ADDRESS2 | `-x-----` |
| … | … |
| ADDRESS7 | `------x` |

`1111111₂` = 全部接受；`0000000₂` = 登记可接受但本组列表全拒（6.4.4.1.13）。

---

## 7. 登记拒绝 / 过程 Reason（非独立枚举表）

登记 **没有** 另一张独立 reject 码表。clause **6.4.4** 使用的就是 Table 7.42/7.43：

| 过程结果 | PDU + Reason | 学习口径 |
|----------|--------------|----------|
| 成功 | `C_ACKD(Reg_Accepted 0110 0010₂)` | 可带 PowerSave_Offset |
| 成功+组附着明细 | `C_ACK(Reg_Subscription/Attachment 0110 0101₂)` + Index | Table 6.10 |
| 忙/稍后 | `C_WACKD(Wait 1110 0000₂)` | 后续还有信令 |
| 拒绝（可再猎站） | `C_NACKD(Reg_Refused 0010 1010₂)` Source=REGI | 6.4.4 |
| 否决（离开本 TSCC） | `C_NACKD(Reg_Denied 0010 1011₂)` Source=REGI | 规范称 Denied 是把 MS 从该 TSCC 赶走的首选终答 |
| 未先登记就做业务 | `C_NACKD(MS_Not_Registered 0010 1101₂)` | |
| 注销 | 仅 `C_ACKD(Reg_Accepted)` 为合法终答 | 6.4.5 |
| IP 通告失败 | `C_NACKD(IP_Connection_failed)` Source=IPI | 6.4.11 |

Ahoy 驱动的登记/组列表：C_AHOY 字段见 Table **6.11 / 6.23** 等过程表；**Reason 仍在随后的 ACK**。

---

## 8. 其它带 Reason 的过程表（非 7.2.8 主表）

### 8.1 呼叫改向终答（Table 6.60）

引用：6.6.7.1.1.2。码值仍属 7.42/7.43。

| 确认 | Reason | 含义 |
|------|--------|------|
| C_ACK | `0110 0000₂` Message_Accepted | 改向被 TS 接受 |
| C_NACK | `0010 0000₂` Not_Supported | 系统不支持改向（对**初始** C_RAND） |
| C_NACK | `0010 0011₂` Transient_Sys_Refused | 不能改向到该目的（对**上行改向地址**终答） |

### 8.2 鉴权 / 无线检查过程中的固定 Reason

| 场景 | PDU | Reason | 表 |
|------|-----|--------|----|
| MS 鉴权响应 | C_ACKU | `0100 1000₂` Authentication Response；Target=24-bit 结果 | 6.18 |
| TS 鉴权响应 | C_ACKD | `0110 0100₂` | 6.20 / 6.24 |
| 无线检查 OK | C_ACKU | `0100 0100₂`（Table 6.28 写作 Message_Accepted 编码） | 6.28 |
| ALS 不支持 | C_NACKU | `0000 0000₂` MSNot_Supported | 6.47 |
| Stun/Revive 拒绝 | C_NACKU | Recipient_Refused | 6.4.8 |
| FOACSU 被叫拒接 | C_NACKD | `0001 0100₂` Recipient_Refused（镜像给主叫） | 6.6.1.4.2 |

Table 6.18 把 Reason 长度误写为 7；**以 7.2.8 的 8 bit 为准**。

### 8.3 LIP「Reason for Sending」（Table 6.80）— **不是** ACK Reason

引用：6.6.11.3.3。USBD 轮询响应里 3-bit 场，与 7.2.8 **无关**。

| IE | Len | Value | 含义 |
|----|-----|-------|------|
| Reason for Sending | 3 | `000₂` | 对立即请求的响应（LIP value = 3） |
| | | `001₂`…`111₂` | 保留 |

---

## 9. 与 Aloha / Ahoy / RAND 的交叉

| PDU | 有无 Reason | 相关场 | 如何接到 Reason |
|-----|-------------|--------|-----------------|
| **C_ALOHA** Table 7.19 | 无 | Mask / Service Function / Reg / Backoff / NRand_Wait | Reg=`1` 时未登记业务会被 `MS_Not_Registered` 拒绝 |
| **C_AHOY** Table 7.22 | 无 | Service_Kind(4) + Service_Kind_Flag(1) + Service_Options_Mirror(7) | MS 必须 `C_ACKU/C_NACKU`；TS 可镜像给主叫 |
| **C_RAND** Table 7.25 | 无 | Service_Kind + Service_Options | 终答是 ACK/NACK/QACK/WACK 或直接 Grant |
| **C_ACKVIT** Table 7.26 | 无 | 鉴权挑战路径 | 随后 C_ACKU Reason=`0100 1000₂` |
| **C_GRANT 族** | 无 | 见 §10 | 成功则**不**再靠 ACK Reason 表示“已接通” |
| **C_BCAST** | 无 | Announcement_type | 见 [`Announcement与其余枚举.md`](./Announcement与其余枚举.md) |

**C_AHOY 外壳（Table 7.22）** CSBKO=`01 1100₂`（28）— 便于对照 ACK：

| IE | Len | 摘要 |
|----|-----|------|
| LB / PF / CSBKO / FID | 1+1+6+8 | LB=`1` |
| Service_Options_Mirror | 7 | 常镜像 C_RAND 的 Service_Options；鉴权/Stun/Kill 见 Table 7.61–7.63 |
| Service_Kind_Flag | 1 | 依 Service_Kind：OACSU/FOACSU、Stun/Revive 等 |
| Ambient Listening Service | 1 | 仅个呼语音 ALS |
| G/I | 1 | 个号 / 组 |
| Appended_Blocks (STATUS(2)) | 2 | UDT 块数；状态业务时为 Status 低 2 位 |
| Service_Kind | 4 | 见 Announcement 文件 Table 7.49 |
| Target / Source | 24+24 | 被叫或组；主叫/网关/鉴权挑战/TSI |

---

## 10. Grant 变体总览

引用：7.1.1.1.1；Tables **7.1 / 7.9–7.16 / 7.29**；Annex **B.1**。  
出站、不征求响应。CSBK（逻辑信道号）或 MBC 头+**CG_AP**（绝对频率）。

### 10.1 变体对照

| 别名 | CSBKO (6) | Opcode | 用途 | 第 16 信息比特附近差异 | 绝对频率 | 表 |
|------|-----------|--------|------|------------------------|----------|----|
| **PV_GRANT** | `11 0000₂` | 48 | 个呼语音（半双工） | Reserved(1)+Emergency+**Offset** | 信道=`0xFFF`→CG_AP | 7.9 |
| **TV_GRANT** | `11 0001₂` | 49 | 组呼语音 | **Late_Entry**(1)+Emergency+Offset | 同上 | 7.11 |
| **BTV_GRANT** | `11 0010₂` | 50 | 广播组呼语音 | Late_Entry+Emergency_Flag+Offset | 同上 | 7.12 |
| **PD_GRANT** | `11 0011₂` SI / `11 0111₂` MI | 51 / 55 | 个呼数据 | **HI_RATE**(1)+Emergency+Offset | 同上 | 7.13 |
| **TD_GRANT** | `11 0100₂` SI / `11 1000₂` MI | 52 / 56 | 组呼数据 | HI_RATE+Emergency+Offset | 同上 | 7.15 |
| **PV_GRANT_DX** | `11 0101₂` | 53 | 个呼语音**双工** | Reserved+Emergency+**Call Direction**；**总是 offset timing** | 同上 | 7.10 |
| **PD_GRANT_DX** | `11 0110₂` | 54 | 个呼数据**双工** | HI_RATE 固定 `0`（单时隙）+Emergency+**Call Direction**；总是 offset | 同上 | 7.14 |
| **P_GRANT** | **沿用**当初 TSCC Grant 的 CSBKO | — | 业务信道上换信道 / 呼叫前公告 / 新呼叫公告 | 布局同对应 Grant；只改信道号（及可选绝对频率） | 可附 CG_AP | 7.29 |
| **CG_AP** | **与头块相同** | — | Grant MBC 续块：绝对 Tx/Rx | Cdeftype+CdefParms | 本身即绝对参数 | 7.16 |

**Logical Physical Channel Number（12 bit，所有 Grant 相同规则）**：

| 值 | 含义 |
|----|------|
| `0000 0000 0000₂` (0) | **无效** |
| `0000 0000 0001₂` … `1111 1111 1110₂` (1…0xFFE) | 逻辑信道号 → 单块 CSBK |
| `1111 1111 1111₂` (0xFFF / 4095) | 绝对频率在后续 **CG_AP**（7.1.1.1.2） |

**Logical Channel Number（1）**：`0` TDMA ch1；`1` ch2。

**SI / MI（数据）**：Single Item = 单条目数据；Multi-Item = 多条目。由 **CSBKO** 区分，不是单独 1-bit 场（C_RAND 的 Service_Options 里另有 SIMI 位，见 Announcement 文件 Table 7.53）。

**DX Call Direction**：`0` Target/Destination = 被叫；`1` = 主叫。规范：TSCC 可为一次双工呼叫发 **两条** DX Grant，每条 Target 填该参与者自己的 MS ID。

---

## 11. Grant 共用比特骨架（Octet 2–9，64 bit）

所有 TSCC Grant 的 Octet 0–1 相同：`LB | PF | CSBKO | FID=0`。Octet 2–9：

```text
  12 bit  Logical Physical Channel Number
   1 bit  Logical Channel Number (TDMA ch1/ch2)
   1 bit  变体位 A   ← Reserved / Late_Entry / HI_RATE
   1 bit  Emergency（BTV 称 Emergency_Flag）
   1 bit  变体位 B   ← Offset / Call Direction
  24 bit  Target / Destination Address
  24 bit  Source Address
```

| 变体 | 位 A | 位 B | 地址语义 |
|------|------|------|----------|
| PV_GRANT | Reserved=`0` | Offset：`0` aligned / `1` offset | Target=被叫个号/网关；Source=主叫/网关 |
| PV_GRANT_DX | Reserved=`0` | **Call Direction**（无 Offset 场；NOTE：总是 offset） | Target=本 Grant 对象；Source=对端 |
| TV_GRANT | **Late_Entry**：`0` 建链授予；`1` 建链后迟后进入 | Offset | Target=**Talkgroup**（ALLMSID* 按广播解释） |
| BTV_GRANT | Late_Entry | Offset | Destination=组；All Call 地址见 A.4 |
| PD_GRANT | **HI_RATE**：`0` 单时隙数据；`1` 双时隙 | Offset | Destination=个号/网关 |
| PD_GRANT_DX | HI_RATE **固定 0** | **Call Direction**（总是 offset） | 同 PV_GRANT_DX |
| TD_GRANT | HI_RATE | Offset | Destination=Talkgroup |

FID 标准业务均为 `0000 0000₂`。LB：单块 CSBK=`1`；MBC 头=`0`。

---

## 12. 各 Grant 字段表

### 12.1 PV_GRANT — Table 7.9（7.1.1.1.1.1.1）

| IE | Len | 编码 / 含义 |
|----|-----|-------------|
| LB | 1 | `1` 单块；`0` MBC 头 |
| PF | 1 | |
| CSBKO | 6 | `110000₂` |
| FID | 8 | `00000000₂` |
| Logical Physical Channel Number | 12 | 见 §10.1 |
| Logical Channel Number | 1 | `0` ch1；`1` ch2 |
| Reserved | 1 | `0` |
| Emergency | 1 | `1`=紧急 |
| Offset | 1 | `0` aligned；`1` offset |
| Target Address | 24 | 被叫个号/网关 |
| Source Address | 24 | 主叫/网关 |

### 12.2 PV_GRANT_DX — Table 7.10（7.1.1.1.1.1.2）

相对 PV_GRANT：**CSBKO=`110101₂`**；Reserved 仍为 `0`；**Offset → Call Direction**；NOTE：双工业务信道**总是 offset timing**。地址：Target=本端，Source=对端。

### 12.3 TV_GRANT — Table 7.11（7.1.1.1.1.2）

CSBKO=`110001₂`。Reserved → **Late_Entry**。Target=组地址；若为 ALLMSIDL / ALLMSIDZ / ALLMSID 则按广播解释（A.4）。

迟后进入：建链后 TSCC 继续发 `Late_Entry=1` 的 TV/BTV Grant，新上线的组员可被拉入（6.6.1.6）。

### 12.4 BTV_GRANT — Table 7.12（7.1.1.1.1.3）

CSBKO=`110010₂`。场名：Late Entry、Emergency_Flag、Destination_Address、Source_address。NOTE：All Call 地址为 ALLMSID / ALLMSIDZ / ALLMSIDL。

### 12.5 PD_GRANT — Table 7.13（7.1.1.1.1.4.1）

CSBKO：单条目 `110011₂`；多条目 `110111₂`。Reserved → **HI_RATE**。其余同个呼骨架。

### 12.6 PD_GRANT_DX — Table 7.14（7.1.1.1.1.4.2）

CSBKO=`110110₂`。HI_RATE 固定 `0`（双工数据总是单时隙）。Offset → Call Direction。总是 offset timing。

### 12.7 TD_GRANT — Table 7.15（7.1.1.1.1.5）

CSBKO：单条目 `110100₂`；多条目 `111000₂`。HI_RATE + Emergency + Offset。Destination=组。

> Annex B.1 中 Opcode **56** `111000₂` 亦被 Part 2 用作 BS_Dwn_Act；上下文靠 FID/场景区分。

### 12.8 P_GRANT — Table 7.29（7.1.1.3.1）

业务信道出站。**CSBKO 必须等于**当初把该 MS 拉到业务信道的那条 TSCC Grant。

用途（7.1.1.3.1）：

1. **换信道（swap）**：除逻辑信道号（及可选绝对频率）外，其余 IE 保持原 TSCC Grant；
2. **本呼叫首次发射前公告**：IE 与原 TSCC Grant 相同；
3. **公告新呼叫**：IE 用该新呼叫在 TSCC 上的值（MS 可跟随或忽略，厂商策略，6.6.1.6）。

| IE | Len | 备注 |
|----|-----|------|
| LB / PF | 1+1 | |
| CSBKO | 6 | **复制**原 TSCC Grant |
| FID | 8 | 0 |
| Logical Physical Channel Number | 12 | 新/当前业务信道或 `0xFFF` |
| Logical Channel Number | 1 | |
| HI_RATE / Emergency / Offset | 3 | **按原 Grant 类型解释**（数据才有 HI_RATE；DX 的第 3 位是 Call Direction） |
| Destination_Address | 24 | 个号 / 网关 / 组 |
| Source_address | 24 | |

---

## 13. 绝对频率附块：CG_AP / 与 Grant 的衔接

### 13.1 相对 vs 绝对

| 模式 | 头块信道号 | 续块 | Data Type（Table 7.1） |
|------|------------|------|------------------------|
| 逻辑/相对 | 1…0xFFE | 无（单块 CSBK） | CSBK `0011₂` |
| 绝对 | `0xFFF` | **CG_AP** MBC continuation | MBC Header `0100₂` + Continuation |

C_MOVE 的 MV_AP、C_BCAST 的 BC_AP、Vote Now 的 VN_AP 是**同一 CdefParms 机制**，不是 Grant，但比特骨架几乎相同。

### 13.2 CG_AP — Table 7.16（7.1.1.1.2）

```text
Octet0: LB=1 | PF | CSBKO = 头块 CSBKO（PV/TV/PD/… 原值）
随后:   Reserved(4)=0000 | Colour Code(4)
        Cdeftype(4) | Reserved(2)=00
        CdefParms(58)
```

| IE | Len | 含义 |
|----|-----|------|
| LB | 1 | 续块，置 `1` |
| PF | 1 | |
| CSBKO | 6 | **与 Grant 头块一致** |
| Reserved | 4 | `0000₂` |
| Colour Code | 4 | 目的物理信道色码 |
| Cdeftype | 4 | CdefParms 释义，7.2.42 |
| Reserved | 2 | `00₂` |
| CdefParms | 58 | 逻辑/物理频率关系 |

### 13.3 CdefParms（Table 7.103，Cdeftype=`0000₂`）

| 子场 | Len | Alias | 含义 |
|------|-----|-------|------|
| Logical Physical Channel Number | 12 | CHAN | |
| Absolute Tx 整数 MHz | 10 | TXMHz | |
| Absolute Tx 分数（125 Hz 步） | 13 | TXKHz | |
| Absolute Rx 整数 MHz | 10 | RXMHz | |
| Absolute Rx 分数（125 Hz 步） | 13 | RXKHz | |
| **合计** | **58** | | |

`Cdeftype = 0001₂`…`1111₂`：58 bit 保留。频率换算公式与 Table C.1–C.7：[`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md)。  
**VN_AP** Table 7.72 与 CG_AP 同构（含 Colour Code）。**BC_AP** Table 7.21：Reserved 为 8 bit（无独立 Colour Code 场），其余 Cdeftype+CdefParms 相同。

---

## 14. Opcode 速查（Grant / ACK 相关，Table B.1 / 7.1）

| OPCODE | OPCODE₂ | 别名 |
|--------|---------|------|
| 48 | `110000₂` | PV_GRANT |
| 49 | `110001₂` | TV_GRANT |
| 50 | `110010₂` | BTV_GRANT |
| 51 | `110011₂` | PD_GRANT（SI） |
| 52 | `110100₂` | TD_GRANT（SI） |
| 53 | `110101₂` | PV_GRANT_DX |
| 54 | `110110₂` | PD_GRANT_DX |
| 55 | `110111₂` | PD_GRANT_MI |
| 56 | `111000₂` | TD_GRANT_MI（亦见 Part 2 BS_Dwn_Act） |
| 57 | `111001₂` | C_MOVE（非 Grant，迁移 TSCC） |
| 32 | `100000₂` | C_ACKD 族 |
| 33 | `100001₂` | C_ACKU 族 |
| 34 | `100010₂` | P_ACKD 族 |
| 35 | `100011₂` | P_ACKU 族 |
| 28 | `011100₂` | C_AHOY / P_AHOY |
| 25 | `011001₂` | C_ALOHA |
| 31 | `011111₂` | C_RAND |

C_MOVE / MV_AP 字段见速览缺口列表；完整公告枚举见 [`Announcement与其余枚举.md`](./Announcement与其余枚举.md)。

---

## 15. 覆盖与缺口

### 已覆盖（本文件）

| 条款 / 表 | 内容 |
|-----------|------|
| 7.2.8.0–7.2.8.3；Tables **7.42–7.45** | 全部 ACK/NACK/QACK/WACK Reason 行 |
| 7.2.7 Table **7.41**；Table **6.10** | Response_Info / 组附着 Index |
| 7.1.1.1.7 Table **7.23**；7.1.1.2.3 Table **7.27** | ACK 外壳 |
| 6.4.4 / 6.4.8 / 6.6.1.4.2 / 6.6.7 Table **6.60** / 6.6.11 Table **6.80** | 登记/鉴权/FOACSU/改向/LIP 交叉 |
| 7.1.1.1.1.1–5 Tables **7.9–7.15** | 全部 TSCC Grant 变体字段 |
| 7.1.1.1.2 Table **7.16**；7.2.42 Table **7.103** | CG_AP + CdefParms(`0000₂`) |
| 7.1.1.3.1 Table **7.29** | P_GRANT |
| 7.1 Table **7.1–7.4**；Annex **B.1** | Opcode |
| 7.1.1.1.6 Table **7.22** | AHOY 外壳（交叉） |

### 未展开 / 仅在图或过程中

| 项 | 说明 |
|----|------|
| MSC 时序图（figure 6.x / 7.x Structure Highlight） | 未描图，只保留文字关系 |
| Annex C 频率换算公式 | 已迁出 → [`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md)；Cdeftype≠0 仍为保留 |
| C_MOVE / MV_AP 全表 | 非 Grant；Table 7.17–7.18 指针见 Announcement 文件 |
| Stun/Kill/DGNA 完整状态机 | Reason 已收录，过程 IE 见 clause 6.4.8–6.4.9 |
| 厂商 Reason（Custom_Refused）及 `0011 0010₂`–`0011 1110₂` 空洞 | 规范未定义 |
| Table 7.43 未列但散文有的 **MS_Duplex_Not_Supported** | 已按 7.2.8.2 补入并标注 |

---

*学习向整理。实现与互操作请核对 ETSI TS 102 361-4 V1.12.1 原文。*
