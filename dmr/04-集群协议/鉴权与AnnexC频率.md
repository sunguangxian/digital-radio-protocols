# DMR Part 4：鉴权与 Annex C 频率

> **学习用整理，冲突以 ETSI TS 102 361-4 V1.12.1 (2023-07) 为准；非全文复制。**  
> 源 PDF：同目录 `TS102361-4_V1.12.1.pdf`（`pdftotext -layout` 归纳）。  
> 总览：[`集群协议字段速览.md`](./集群协议字段速览.md)  
> Reason / Grant / CG_AP 骨架：[`ReasonCode与Grant变体.md`](./ReasonCode与Grant变体.md)  
> Service_Kind / Announcement：[`Announcement与其余枚举.md`](./Announcement与其余枚举.md)  
> Stun / Kill 带鉴权时序：[`Stun_DGNA_UDT与定时器.md`](./Stun_DGNA_UDT与定时器.md)
> Annex D 猎站：[`AnnexD猎站Hunt.md`](./AnnexD猎站Hunt.md)

本文件补：**鉴权**（K / PSN / 挑战–响应 PDU 与过程）和 **Annex C 物理信道/频率编码**（相对逻辑号 + 绝对 CdefParms）。不抄 MSC 长图、FEC 矩阵、SYNC hex、RC4 内部状态机。

---

## 0. 两件事怎么接到空口

```text
鉴权（clause 6.4.8）
  TS --C_AHOY(Service_Kind=1110₂, Source=24-bit RAND)--> MS
  MS --C_ACKU(Reason=Authentication_Response, Target=24-bit 响应)--> TS
  （Stun/Kill 反向：MS --C_ACKVIT(Target=RAND)--> TS --C_ACKD(Reason=Auth Resp)--> MS）

频率（4.7.1 / 7.2.42 / Annex C）
  信道号 1…4094 = 逻辑 CHAN → 预置相对计划（fbase / 间隔 / 双工分裂）
  信道号 0xFFF  = 绝对：Grant/MOVE/BCAST/VoteNow 续块里的 CdefParms
```

---

# 第一部分 鉴权

## 1. 本 TS 写了什么、没写什么（算法边界）

引用：6.4.8.0–6.4.8.1.2；Tables **6.15 / 6.16**。

| 主题 | 本 TS 的口径 |
|------|-------------|
| **过程与 PDU** | **规范**。挑战在 C_AHOY（或业务信道 P_AHOY），响应在 C_ACKU / C_ACKD；Stun/Kill 反向用 C_ACKVIT。 |
| **K（128 bit）** | **只定义长度与存放**。写入每台 MS，并同步到 TS。**密钥如何生成不在本文件**，厂商自定（6.4.8.1.1）。被攻破只影响该台，厂商可重写 K。 |
| **PSN（≥3 字节）** | **只定义规则**。出厂固化、不可改、每台唯一；用厂商工具读出后录入基础设施。算法细节厂商自定（6.4.8.1.2）。 |
| **挑战–响应计算** | **本 TS 点名 RC4 密钥流发生器**（6.4.8.0）：用 `RAND ‖ K` 作密钥，产生 259 字节伪随机流，**弃前 256、取末 3 字节**为 24-bit 响应。可选再与 PSN **逐字节 XOR**。 |
| **RC4 本体** | **不展开**。本 TS 只引用该发生器；S-box / 密钥调度细节不在 Part 4。实现应对齐通行 RC4 与 Table **6.15 / 6.16** 测试向量，而不是本文。 |
| **Privacy / 空口加密** | Service_Options 的 Privacy 位在 7.2.13 **注明未定义**。鉴权 ≠ 话音/数据加密。 |

**结论**：互操作所需的 **字段、Opcode、Reason、挑战范围、K/PSN 角色、RC4 用法一句话** 在本 TS；**K 生成、PSN 工厂编码、RC4 内部、测试向量逐字节** 不在此复述。Fig **6.30** 是挑战–响应框图（RAND+K → 24-bit 响应，可选 XOR PSN；TS 用同一 K/RAND 算期望值比较），不描图。

兼容：不支持 PSN 的 MS，TS 可把 PSN 当全 0（6.4.8.0）。

---

## 2. 字段：K / PSN / 挑战 / 响应

| 名 | 宽度 | 谁持有 | 空口是否出现 | 条款 |
|----|------|--------|--------------|------|
| **K** | 128 bit | MS 与 TS 各存一份 | **不**上空气口 | 6.4.8.1.1 |
| **PSN** | ≥3 字节（计算用 3 字节） | MS 出厂；TS 配置库 | **不**单独上场；只影响响应 XOR | 6.4.8.1.2 |
| **RAND（Challenge）** | 24 bit | 挑战方当场产生 | **上空气口**（见下） | 6.4.8.2；Table **6.17** |
| **Response** | 24 bit | 被挑战方算出 | **上空气口** | 6.4.8.3；Table **6.18** |

**挑战取值范围**（Table **6.17 / 6.21 / 6.25**）：`00 0000₁₆` … `FF FCDF₁₆`。  
上界卡在网关号之前（Table **A.8** 从 `FF FEC0₁₆` 起：REGI / STUNI / **AUTHI**=`FF FECD₁₆` / KILLI …），避免把 RAND 读成网关。

测试向量（Table **6.15 / 6.16**，仅结构）：同一组 RAND / K，无 PSN 与有 PSN 各一行期望响应；有 PSN 行 = 无 PSN 响应 **XOR** PSN。逐字节以 PDF 为准。

---

## 3. 相关 PDU / Opcode / Service_Kind

外壳均为 Part 1 CSBK（LB|PF|CSBKO|FID|…）；FID 标准业务全 0。Opcode：Annex **B.1**。

| 别名 | CSBKO | 方向 | 鉴权角色 | 条款 / 表 |
|------|-------|------|----------|-----------|
| **C_AHOY** | `01 1100₂`（28） | TS→MS | **挑战**：Source=RAND | 7.1.1.1.6 Table **7.22**；6.4.8.2 Table **6.17** |
| **P_AHOY** | 同 28 | TS→MS（业务信道） | 同上，过程同 6.4.8.2 | 6.6.2.3.1.2 / 6.6.3.3.1.2 |
| **C_ACKU** | `10 0001₂`（33） | MS→TS | **响应**：Reason=`0100 1000₂`，Target=响应 | 7.1.1.2.3 Table **7.27**；Table **6.18** |
| **P_ACKU** | `10 0011₂`（35） | MS→TS（业务信道） | 替代 C_ACKU | 6.6.2.3.2.2 / 6.6.3.3.2.2 |
| **C_ACKD** | `10 0000₂`（32） | TS→MS | **TS 被挑战时的响应**：Reason=`0110 0100₂`，AddInfo=响应 | 7.1.1.1.7 Table **7.23**；Table **6.20 / 6.24** |
| **C_ACKVIT** | `01 1110₂`（30） | MS→TS | **MS 挑战 TS**（Stun/Kill）：Target=RAND | 7.1.1.2.2 Table **7.26**；Table **6.21 / 6.25** |
| **C_RAND** | `01 1111₂`（31） | MS→TS | 登记/业务请求；**不带**挑战。可触发后续鉴权 | 7.1.1.2.1 |

**Service_Kind**（Table **7.49**，4 bit）鉴权与登记、无线检查**共用** `1110₂`（Registration/Authentication Service / MS Radio Check）。靠 **Source / Gateway + Flag** 区分，不是单独 Opcode。

| 场景 | Service_Kind | Service_Kind_Flag | Source / Gateway | 条款 |
|------|--------------|-------------------|------------------|------|
| TS 挑战 MS（登记中或独立轮询） | `1110₂` | `0`（Table **7.50**：鉴权挑战/无线检查不适用） | **24-bit RAND**（Table **6.17**） | 6.4.8.2 |
| 登记请求 | `1110₂` | 视是否带组订阅 | Target=**REG_ADDR**（C_SYScode） | 6.4.4；Table **6.7** |
| 组订阅数据（与鉴权可拼接） | `1110₂` | `1` = Talk Group Subscription Data | — | Table **7.50**；6.4.4.1.13 |
| Stun/Revive / Kill 反向鉴权 | `1101₂` 补充业务 | Stun=`0` / Revive=`1`；Kill=`0` | 首包网关 **STUNI / KILLI**；Ackvitation 的 Target=RAND | 6.4.9.2 / 6.4.10 |
| 呼叫建立中的鉴权检查 | 随原业务 或 `1110₂` | — | 过程句 6.6.2.1.1 (d) 写 Source=**Challenge**；同款 NOTE 又写网关 **AUTHI**（`FF FECD₁₆`）。**字段以 Table 6.17 为准**（Source=RAND） | 6.6.2.1.1；A.4 |

独立鉴权轮询（与登记无关）：`Service_Options_Mirror = 000 0000₂`（6.4.8.2；Table **7.61** 拆成 Reserved|Privacy|Reserved，Privacy 未定义）。  
登记/呼叫建立中的 C_AHOY：Mirror **回拷** 对应 C_RAND 的 Service_Options（6.4.8.2）。

**AUTHI**（Table **A.8**）=`FF FECD₁₆`：鉴权网关名。Table **6.7** 的鉴权行把挑战放在 C_AHOY 的 Source，响应放在 ACK 的 Target。Stun 文件已列该 ID。

---

## 4. PDU 字段表

### 4.1 C_AHOY 鉴权挑战 — Table 6.17（钉死于 6.4.8.2）

通用外壳 Table **7.22**，CSBKO=`01 1100₂`，LB=`1`。鉴权时：

| IE | Len | 取值 | 条款 |
|----|-----|------|------|
| Service_Options_Mirror | 7 | 登记/呼叫：回拷 C_RAND；独立轮询：`000 0000₂` | 6.4.8.2；7.2.14.1 Table **7.61** |
| **Service_Kind_Flag** | 1 | `0` | Table **7.50** |
| Ambient Listening Service | 1 | `0` 不适用 | |
| G/I | 1 | `0` **个号** | |
| Appended_Blocks | 2 | `00₂` | |
| **Service_Kind** | 4 | `1110₂` Authentication Service | Table **7.49** |
| Target address | 24 | 被挑战 MS 个号 | |
| **Source Address or Gateway** | 24 | **RAND**，`00 0000₁₆`…`FF FCDF₁₆` | |

业务信道：同一 IE，PDU 换 **P_AHOY**（6.6.2.3.1.2）。

### 4.2 C_ACKU 鉴权响应 — Table 6.18（MS→TS）

外壳 Table **7.27**，CSBKO=`10 0001₂`。Table 6.18 把 Reason 写成 7 bit，**以 7.2.8 / Table 7.27 的 8 bit 为准**。

| IE | Len | 取值 | 条款 |
|----|-----|------|------|
| Response_Info | 7 | 普通值（非登记特例） | 7.2.7 |
| **Reason Code** | 8 | **`0100 1000₂`（0x48）Authentication Response** | 7.2.8.1 Table **7.42** |
| Reserved | 1 | `0` | |
| **Target address** | 24 | **24-bit 挑战响应** | 7.1.1.2.3 明文：鉴权时本场改放响应 |
| Additional Information (Source Address) | 24 | 发 ACK 的 MS 个号 | |

### 4.3 C_ACKD 鉴权响应 — Table 6.20 / 6.24（TS→MS，反向）

Stun/Kill 时 TS 被 MS 挑战。外壳 Table **7.23**。Reason 交叉：[`ReasonCode与Grant变体.md`](./ReasonCode与Grant变体.md) §2.1。

| IE | Len | 取值 |
|----|-----|------|
| Response_Info | 7 | 普通值 |
| **Reason Code** | 8 | **`0110 0100₂`（0x64）Authentication Response** |
| Reserved | 1 | `0` |
| Target address | 24 | 被 Stun/Kill 的 MS |
| **Additional Information (Source Address)** | 24 | **TS 算出的 24-bit 响应** |

与 4.2 对称：MS→TS 把响应放在 **Target**；TS→MS 把响应放在 **AddInfo/Source**。

### 4.4 C_ACKVIT — Table 7.26 + Table 6.21 / 6.25

CSBKO=`01 1110₂`（30），单块，MS 发。通用场：

| IE | Len | 含义 |
|----|-----|------|
| LB / PF / CSBKO / FID | 1+1+6+8 | LB=`1`；CSBKO=`011110₂`；FID=0 |
| Service_Options_Mirror | 7 | Stun/Kill：`000 0000₂` |
| Service_Kind_Flag | 1 | 随 Kind：Stun=`0` / Revive=`1` |
| Reserved | 2 | `00₂` |
| Appended_Blocks | 2 | `00₂` |
| Service_Kind | 4 | Stun/Kill：`1101₂` |
| **Target address** | 24 | **MS 产生的 RAND**（同范围） |
| Source Address | 24 | MS 个号 |

兼作对首包 C_AHOY 的确认（6.4.9.2.1）。

---

## 5. Reason 交叉（只列鉴权用到的）

全表：[`ReasonCode与Grant变体.md`](./ReasonCode与Grant变体.md) Tables **7.42–7.45**。

| 名 | Value | Hex | 方向 | 用在 |
|----|-------|-----|------|------|
| **Authentication Response** | `0110 0100₂` | 0x64 | TS→MS（`d=1`） | C_ACKD：TS 回答 MS 的挑战 |
| **Authentication Response** | `0100 1000₂` | 0x48 | MS→TS（`d=0`，可镜像） | C_ACKU：MS 回答 TS 的挑战 |
| **Reg_Accepted** | `0110 0010₂` | 0x62 | TS→MS | 登记成功终 ACK（鉴权通过之后） |
| **Reg_Refused** / **Reg_Denied** | `0010 1010₂` / `0010 1011₂` | 0x2A / 0x2B | TS→MS | 登记失败（含鉴权失败后的拒绝路径，6.4.4） |
| **MS_Accepted** | `0100 0100₂` | 0x44 | MS→TS | Stun/Kill 反向鉴权**成功**终 ACK（Table **6.22 / 6.26**） |
| **Recipient_Refused** | `0001 0100₂` | 0x14 | MS→TS | 反向鉴权**失败**，不 Stun/Kill |
| **MSNot_Supported** | `0000 0000₂` | 0x00 | MS→TS | 不支持 Stun/Revive |
| **Wait**（WACK） | `1110 0000₂` | 0xE0 | TS→MS | 登记/建立中间态，后面还有鉴权或终 ACK |

登记拒绝没有单独 “Auth Fail” Reason：失败走 **Reg_Refused / Reg_Denied** 或过程超时（TNP_Timer → 猎站，6.4.4.1.6）。

---

## 6. 过程摘要（短列表，不描 MSC）

### 6.1 算法直觉（6.4.8.0；Fig 6.30 的文字等价）

1. 挑战方抽 24-bit RAND（范围内）。  
2. 被挑战方：`RC4(key = RAND ‖ K)` → 259 字节 → 弃 256 → 3 字节 `X`。  
3. 若用 PSN：空口响应 = `X XOR PSN`；否则 = `X`。TS 用同一 K（及已知 PSN 或 0）算期望值。  
4. 相等 → 成功。K / PSN **不上空气口**。

SDL 名 **AuthCalc(challenge, key, authresp)** 出现在 Fig **6.23**（登记+鉴权），语义即上式。

### 6.2 TS 挑战 MS（主路径，6.4.8.2–6.4.8.3）

可嵌在：**登记**（6.4.4.1.5 Fig **6.20**）、**呼叫建立**（6.6.2.1.1 (d) 等）、**独立轮询**、**业务信道**（P_AHOY/P_ACKU）。

```text
MS --C_RAND(Kind=登记或业务)--> TSCC          # 独立轮询则无此步
TS --C_AHOY(Kind=1110₂, Source=RAND)--> MS    # 兼作对 RAND 的确认；开 TNP_Timer
MS --C_ACKU(Reason=0x48, Target=响应)--> TS
TS 比较 → C_ACKD(Reg_Accepted / 业务继续) 或 C_NACKD(Reg_* / 拒绝)
```

- Fig **6.20** 槽位：aligned 与 offset 两行（A=RAND，B=AHOY 挑战，C=ACK 响应，D=终 ACK）。不描图。  
- 与组订阅可**先鉴权再附着**（Fig **6.27**）或**先附着再鉴权**（Fig **6.28**）：挑战 ACK 后立刻跟 UDT 列表，或反过来。  
- 业务信道：C_* 换成 P_*，其余 IE 同 6.4.8.2。

### 6.3 MS 挑战 TS（Stun/Revive / Kill，6.4.9.2 / 6.4.10）

Kill **必须**鉴权。Stun/Revive 可选（MS 是否发 Ackvitation 由实现定）。详序已在 Stun 文件 §1.3。

```text
TS --C_AHOY(STUNI|KILLI, Kind=1101₂)--> MS
MS --C_ACKVIT(Target=RAND)--> TS              # 兼确认 AHOY
TS --C_ACKD(Reason=0x64, AddInfo=响应)--> MS
MS 校验 → C_ACKU(MS_Accepted) 并执行  或  C_NACKU(Recipient_Refused)
```

Fig **6.32 / 6.33** 与 6.31（无鉴权）对照；aligned/offset 槽位以 PDF 为准。

### 6.4 Table 6.7 地址对照（鉴权行）

| 服务 | PDU | Source | Target |
|------|-----|--------|--------|
| MS 鉴权 / 登记中的鉴权 | C_AHOY | **Authentication Challenge** | MS ID |
| | ACK | MS ID | **Authentication Result** |
| Stun/Revive（MS 鉴 TS） | C_ACKVIT | MS ID | Challenge |
| | ACK（TS） | **Result** | MS ID |
| Kill（必鉴） | 同上，网关 **KILLI** | | |

---

# 第二部分 Annex C 频率

Annex **C 是 informative**（Physical Channel Plan）。规范性字段在 **7.2.42 / Table 7.103** 与各绝对续块（CG_AP / MV_AP / BC_AP / VN_AP）。绝对换算公式以 C.1.1.4 为准。

上层只看见 **12-bit 逻辑信道号 CHAN**；计划类型、间隔、双工分裂等在物理层预置或由绝对 PDU 当场给出（C.1.1.1；4.7.1）。

---

## 7. 相对 vs 绝对（空口怎么选）

引用：4.7.1；各 Grant 7.1.1.1.1.x；C_MOVE 7.1.1.1.3；Vote Now 7.2.19.3；C_BCAST Chan_Freq 7.2.19.6。

| 12-bit 信道号 | 含义 | 空口形态 |
|---------------|------|----------|
| `0000 0000 0000₂`（0，**CHNULL**） | 无效 / 未分配 | 单块里作“无信道” |
| `1` … `4094`（`0x001`…`0xFFE`） | **逻辑 CHAN** → 预置 Tx/Rx 对 | 单块 CSBK |
| `4095`（`0xFFF`） | **绝对频率在续块** | MBC 头 + CG_AP / MV_AP / VN_AP / BC_AP |

系统还可 **C_BCAST(Announcement_type = Chan_Freq = `0 0101₂`)** 广播“逻辑号 ↔ 绝对频率”（必须 MBC+**BC_AP**，Table **7.78**）。

Annex C 支持的四条策略（C.1.1.1）：

1. **固定计划**：CHAN + 预置 fbase / 间隔 / 双工分裂 / Tx 高低。  
2. **灵活计划**：每个 CHAN 单独预置一对 Tx/Rx（Table **C.6**）。  
3. **广播**逻辑/物理关系（C_BCAST）。  
4. **扩展 Grant** 当场给绝对 Tx/Rx（CdefParms）。

标称载波可落在 **50 MHz–999 MHz**（C.1.1.1）。国家管理可另限功率等。Annex C **无单独框图**；频率关系全是公式+表。

---

## 8. 固定计划公式（C.1.1.2）

符号：

| 符号 | 含义 | 单位 |
|------|------|------|
| `fMS_Tx` | MS 发频 | MHz |
| `fMS_Rx` | MS 收频 | MHz |
| `fbase` | 该频段 **CHAN=1** 的最低频率 | MHz |
| `fseparation` | 相邻信道间隔 | kHz |
| `fduplexsplit` | **MS Tx − MS Rx** 的差（可正可负） | MHz |
| `CHAN` | 逻辑号 1…4094 | — |

```text
fMS_Tx = fbase + ((CHAN − 1) × (fseparation / 1000))     [MHz]
fMS_Rx = fMS_Tx ± fduplexsplit                             [MHz]
```

`fduplexsplit` 幅度：0 … 50 MHz，步长 **2,5 kHz**（C.1.1.2）。符号由 **TXRX_SPLIT** 定（Table **C.2**）：

| TXRX_SPLIT | 含义 | 等价 |
|------------|------|------|
| `0` | MS Tx **高于** MS Rx | `fMS_Rx = fMS_Tx − |fduplexsplit|` |
| `1` | MS Tx **低于** MS Rx | `fMS_Rx = fMS_Tx + |fduplexsplit|` |

这些 SEP / BAND / DUPLEX_SPLIT 是 **物理层预置 SDU**，不在普通单块 Grant 里重传；Grant 只带 12-bit CHAN。

---

## 9. 参数表（从正文能还原的）

### 9.1 Table C.1 — 信道间隔 SEP（4 bit）

| SEP | 间隔 (kHz) |
|-----|------------|
| `0000₂` | 5 |
| `0001₂` | 6,25 |
| `0010₂` | 10 |
| `0011₂` | 12,5 |
| `0100₂` | 15 |
| `0101₂` | 20 |
| `0110₂` | 25 |
| `0111₂` | 30 |
| `1xxx₂` | 保留 |

### 9.2 Table C.2 — Tx/Rx 高低（1 bit）

见上节。

### 9.3 Table C.3 — 双工分裂 DUPLEX_SPLIT（15 bit）

步长 **2,5 kHz**。规范用省略号，可还原：

```text
fduplexsplit_kHz = N × 2,5
N = DUPLEX_SPLIT 无符号整数（0…20000 → 0…50 MHz）
```

规范举例（核对用）：

| DUPLEX_SPLIT | 分裂 |
|--------------|------|
| `000 0000 0000 0000₂` | 0 |
| `000 0000 0000 0001₂` | 2,5 kHz |
| `000 0111 0011 0000₂` | 4 600 kHz（4,6 MHz） |
| `000 1100 1000 0000₂` | 8 000 kHz（8 MHz） |
| `000 1111 1010 0000₂` | 10 000 kHz（10 MHz） |
| `100 0110 0101 0000₂` | 45 000 kHz（45 MHz） |

### 9.4 Table C.4 — 频段 BAND → fbase

7-bit BAND 与 fbase 的对应，正文给代表点（中间 `……`）。可还原关系：

```text
fbase_MHz = BAND × 10
```

| BAND | fbase (MHz) |
|------|-------------|
| `000 0011₂`（3） | 30 |
| `000 0100₂`（4） | 40 |
| `000 0101₂`（5） | 50 |
| `000 0110₂`（6） | 60 |
| `000 0111₂`（7） | 70 |
| `010 1101₂`（45） | 450 |
| `101 0000₂`（80） | 800 |
| `110 0100₂`（100） | 1 000 |

C.1.1.1 正文可用载波从 50 MHz 起；BAND=3→30 MHz 是表的下沿。中间每 10 MHz 一档，规范未逐行列完。

### 9.5 Table C.5 — 逻辑信道号 CHAN

| CHAN | SDU（12 bit） | 色码 |
|------|---------------|------|
| 1 | `0000 0000 0001₂` | 默认 `0000₂`（NOTE） |
| … | … | … |
| 4 094 | `1111 1111 1110₂` | 默认 `0000₂` |

**0** 与 **4095** 不在本表：0=CHNULL，4095=绝对续块指示。

### 9.6 Table C.6 — 灵活计划

每个 CHAN（1…4094）各自预置 Tx 频率、Rx 频率、色码。无通项公式；表体在规范里是空行模板。色码默认仍 `0000₂`。

---

## 10. 绝对频率：CdefParms（规范场 + Annex C 公式）

### 10.1 Cdeftype / CdefParms — Table 7.103（7.2.42）

| Cdeftype | CdefParms（58 bit） |
|----------|---------------------|
| **`0000₂`** | CHAN(12)+TXMHz(10)+TXKHz(13)+RXMHz(10)+RXKHz(13) |
| `0001₂`…`1111₂` | 58 bit **保留** |

`0000₂` 子场（与 Grant 文件 §13.3 同，此处加换算）：

| 子场 | Len | Alias | 含义 |
|------|-----|-------|------|
| Logical Physical Channel Number | 12 | CHAN | 同时宣告的逻辑号 |
| Absolute Tx 整数 MHz | 10 | TXMHz | 0–1023；有用约 50–999 |
| Absolute Tx 分数 | 13 | TXKHz | **125 Hz** 步 |
| Absolute Rx 整数 MHz | 10 | RXMHz | 同 Tx |
| Absolute Rx 分数 | 13 | RXKHz | 125 Hz 步 |

### 10.2 换算 — Table C.7 + C.1.1.4

```text
f_Tx_MHz = TXMHz + (TXKHz × 125) / 1 000 000
f_Rx_MHz = RXMHz + (RXKHz × 125) / 1 000 000
```

Table **C.7** 代表点（SDU 即该整数本身）：

| Alias | 例 SDU | 频率 |
|-------|--------|------|
| TXMHz | `00 0011 0010₂`（50） | 50 MHz |
| RXMHz | `11 1110 0111₂`（999） | 999 MHz |
| TXKHz / RXKHz | `0 0000 0000 0000₂` | +0 Hz |
| | `0 0000 0000 0001₂` | +125 Hz |
| | `0 0000 0000 0010₂` | +250 Hz |
| | `1 1111 0011 1111₂`（7999） | +999 875 Hz |

分数场满幅 ≈ 0,999875 MHz，与整数 MHz 相加覆盖 Annex C 的 50–999 MHz 标称范围。

**MS 侧**：TX* 是 **MS 发**，RX* 是 **MS 收**（C.1.1.4 标题 “Transmitter and Receiver frequency from CdefParms”）。与固定计划的 `fMS_Tx` / `fMS_Rx` 同一视角。

### 10.3 续块外壳（谁携带 CdefParms）

骨架已在 Grant / Announcement 文件。对照：

| 续块 | 表 | 头块触发 | 与 CG_AP 差异 |
|------|----|----------|---------------|
| **CG_AP** | 7.16 | 任意 Grant 信道号=`0xFFF` | Reserved(4)+**Colour Code(4)**+Cdeftype+CdefParms |
| **MV_AP** | 7.18 | C_MOVE 信道号=`0xFFF` | 同 CG_AP |
| **VN_AP** | 7.72 | Vote_Now CH_VOTE=`0xFFF` | 同 CG_AP |
| **BC_AP** | 7.21 | Ann_WD_TSCC 绝对形式；**Chan_Freq 必须** | Reserved **8 bit**（无独立 CC 场）+Cdeftype+CdefParms |

C_BCAST Chan_Freq（Table **7.78**）：Parms1 全 0；Parms2 = Reserved(12)+CH_ADJ(12)，绝对频率在 BC_AP。

---

## 11. 覆盖与缺口

### 已覆盖（本文件）

| 条款 / 表 | 内容 |
|-----------|------|
| 6.4.8.0–6.4.8.3；Tables **6.15–6.18** | 鉴权引言、K/PSN、挑战/响应 IE、算法边界 |
| 6.4.4.1.5 / 6.4.4.1.11；Fig 6.20 / 6.23 / 6.27 / 6.28 | 登记+鉴权、与组订阅拼接（只留步骤） |
| 6.4.9.2 / 6.4.10；Tables **6.20–6.26** | 反向鉴权（指针到 Stun 文件） |
| 6.6.2.3.1.2 / 6.6.3.3.1.2 等 | 业务信道 P_AHOY/P_ACKU |
| 7.1.1.1.6 / 7.1.1.2.2–3 Tables **7.22 / 7.26 / 7.27** | AHOY / ACKVIT / ACKU 外壳 |
| 7.2.8 Tables **7.42–7.43**；7.2.12 / 7.2.14.1 Tables **7.49 / 7.50 / 7.61** | Reason、Kind、Mirror |
| 7.2.42 Table **7.103**；7.1.1.1.2/3/5 Tables **7.16 / 7.18 / 7.21 / 7.72** | CdefParms 与续块 |
| 4.7.1；Annex **C.1.1.1–C.1.1.4** Tables **C.1–C.7** | 相对公式、SEP/BAND/分裂、绝对 125 Hz |
| A.4 **AUTHI** | 网关号 |

### 未展开 / 仍缺

| 项 | 说明 |
|----|------|
| RC4 内部与 Table 6.15/6.16 逐字节 | 本 TS 只引用发生器并给向量；不对齐实现请对 PDF |
| K 生成 / PSN 工厂编码 | **明确不在本 TS** |
| Fig 6.30 / 6.20 / 6.23 / 6.27–6.28 / 6.32–6.33 槽位图 | 只留文字步骤 |
| **Annex D 猎站**（Short / Comprehensive Hunt、Fig D.1、L_short） | **仍开**；6.3 验证/确认被猎站引用 |
| 组订阅/附着（TATTSI）完整 PDU | 仅 Kind Flag 与 Fig 6.27/6.28 指针；过程 6.4.4.1.13 |
| Cdeftype≠0 | 58 bit 保留，无公式 |
| Table C.4 / C.3 省略号中间档 | 用公式补；以 PDF 代表点核对 |
| 国家/执照对具体频点的额外限制 | C.1.1.1 一句，不在本 TS |

---

*学习向整理。实现与互操作请核对 ETSI TS 102 361-4 V1.12.1 原文。*
