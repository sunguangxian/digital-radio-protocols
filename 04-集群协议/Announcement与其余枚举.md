# DMR Part 4：Announcement_type 与其余枚举

> **学习用整理，冲突以 ETSI TS 102 361-4 V1.12.1 (2023-07) 为准；非全文复制。**  
> Reason Code / Grant 变体（含 ACK 外壳、CG_AP）：[`ReasonCode与Grant变体.md`](./ReasonCode与Grant变体.md)  
> 总览：[`集群协议字段速览.md`](./集群协议字段速览.md)  
> Stun / DGNA / USBD / UDT / 定时器：[`Stun_DGNA_UDT与定时器.md`](./Stun_DGNA_UDT与定时器.md)  
> 鉴权 / Annex C 频率：[`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md)

本文件补速览未展开的：**C_BCAST / Announcement_type 参数比特**、**Service_Kind / Service_Options**、Protect/Maint、Version，以及与 Grant 相邻的 C_MOVE。

---

## 1. C_BCAST 外壳（Table 7.20）

引用：7.1.1.1.5；CSBKO=`10 1000₂`（40）。单块 CSBK 或 MBC 头。

```text
Octet0: LB | PF | CSBKO=101000
Octet1: FID=0
随后:   Announcement_type(5) | Broadcast Parms 1(14)
        Reg(1) | Backoff(4) | System Identity Code(16)
        Broadcast Parms 2(24)
```

| IE | Len | 含义 | 条款 |
|----|-----|------|------|
| LB / PF / CSBKO / FID | 1+1+6+8 | CSBKO=`101000₂`；LB 视单块/MBC | 7.1.1.1.5 |
| **Announcement_type** | 5 | 公告类别，Table **7.68** | 7.2.19 |
| Broadcast Parms 1 | 14 | **依 type 重定义** | 7.2.19.1–8 |
| Reg | 1 | 与 C_ALOHA 的 Reg 应一致（6.4） | 7.2.4 |
| Backoff | 4 | 退避号 | 7.2.5 |
| System Identity Code | 16 | | 7.2.6 |
| Broadcast Parms 2 | 24 | **依 type 重定义** | |

Reg 亦出现在 CACH / C_ALOHA；三者应一致。

---

## 2. Announcement_type 枚举（Table 7.68）

引用：7.2.19.0。5 bit（规范写作 `0 xxxx₂`）。

| Value | Alias | 含义 | 参数表 | 绝对频率附块 |
|-------|-------|------|--------|--------------|
| `0 0000₂` | Ann_WD_TSCC | 宣布/撤销 TSCC | 7.69 | 需要绝对频率时 + **BC_AP** |
| `0 0001₂` | CallTimer_Parms | 呼叫定时器 | 7.70 | — |
| `0 0010₂` | Vote_Now | 立即评估（Vote Now） | 7.71 | CH_VOTE=`0xFFF` → **VN_AP** |
| `0 0011₂` | Local_Time | 本地时间 | 7.73–7.75 | — |
| `0 0100₂` | MassReg | 大规模登记 | 7.76–7.77 | — |
| `0 0101₂` | Chan_Freq | 逻辑信道↔频率关系 | 7.78 | **必须** MBC + BC_AP |
| `0 0110₂` | Adjacent_Site | 邻站信息 | 7.79 | — |
| `0 0111₂` | Gen_Site_Params | 一般站点参数 | 7.80 | — |
| `0 1000₂`…`1 1101₂` | — | 保留 | | |
| `1 1110₂` / `1 1111₂` | — | 厂商专用 | | |

过程概述：clause **6.7.1**。

---

## 3. 各类公告的 Broadcast Parms

### 3.1 Ann_WD_TSCC — Table 7.69（7.2.19.1）

逻辑信道号形式：单块 CSBK，最多宣布/撤销 **两个** TSCC。只处理一个时：`BCAST_CH2=CHNULL`，CH_2 色码=`0000₂`。

| 段 | 子场 | Len | 含义 |
|----|------|-----|------|
| Parms 1（14） | Reserved | 4 | `0` |
| | Colour code CH_1 | 4 | 宣布时用；撤销默认 `0000₂` |
| | Colour code CH_2 | 4 | |
| | AW_FLAG1 | 1 | `0` 加入猎站列表；`1` 从列表撤销 |
| | AW_FLAG2 | 1 | 同上，针对 CH_2 |
| Parms 2（24） | BCAST_CH1 | 12 | CHNULL 或逻辑信道号 1…4095 |
| | BCAST_CH2 | 12 | 同上 |

绝对频率形式：MBC 头 + **BC_AP**；此时只处理 **一个** TSCC，频率在续块（7.2.42）。

### 3.2 CallTimer_Parms — Table 7.70（7.2.19.2）

| 段 | 子场 | Len | 取值 |
|----|------|-----|------|
| Parms 1 | T_EMERG_TIMER | 9 | `0` 用 MS 内部紧急定时器；1…510 秒；`511`=∞ |
| | T_PACKET_TIMER | 5 | `0` 内部分组定时器；1…30 秒；`31`=∞ |
| Parms 2 | T_MS-MS_TIMER | 12 | `0` 内部；1…4094 秒；`4095`=∞ |
| | T_MS-LINE_TIMER | 12 | 线路连接呼叫，同上 |

单位与范围见 Annex **A.1**。迟后进入前可先发本公告告知剩余通话时长（6.6.1.6）。

### 3.3 Vote_Now — Table 7.71（7.2.19.3）

| 段 | 子场 | Len | 含义 |
|----|------|-----|------|
| Parms 1 | （无名称） | 14 | 被评估 TSCC 的 System Identity Code **高 14 位** |
| Parms 2 | 可用性 | 1 | `1`=随后 Active_connection 有效 |
| | Active_connection | 1 | 该站是否连网 |
| | Confirmed channel priority | 3 | 已确认信道优先级 |
| | Adjacent channel priority | 3 | 邻信道优先级 |
| | Reserved | 4 | `0000₂` |
| | **CH_VOTE** | 12 | 待评估物理信道号 |

CH_VOTE 规则与 Grant 信道号相同：`0` 无效；`1…0xFFE` 逻辑号（单块）；`0xFFF` → **VN_AP**（Table 7.72，布局同 CG_AP：CC + Cdeftype + CdefParms）。

### 3.4 Local_Time — Table 7.73（7.2.19.4）

| 段 | 子场 | Len | 含义 |
|----|------|-----|------|
| Parms 1 | B_DAY | 5 | 日 1…31；`0`=不广播日期 |
| | B_MONTH | 4 | Table **7.74** |
| | UTC_OFFSET | 4 | 本地与 UTC 小时差 0…14；`1111₂`=不广播 |
| | UTC_OFFSET_SIGN | 1 | `0` 本地超前 UTC；`1` 落后 |
| Parms 2 | B_HOURS | 5 | 0…23 |
| | B_MINS | 6 | 0…59 |
| | B_SECS | 6 | 0…59 |
| | DAYOF_WEEK | 3 | Table **7.75** |
| | UTC_OFFSET_FRACTION | 2 | `00` 无；`01` +15 min；`10` +30；`11` +45 |
| | Reserved | 2 | `00₂` |

UTC 计算：clause **6.7.1.4**。

**B_MONTH（Table 7.74）**

| Value | 含义 |
|-------|------|
| `0000₂` | 不广播月 |
| `0001₂`…`1100₂` | 1 月…12 月 |

**DAYSOF_WEEK（Table 7.75）**

| Value | 含义 |
|-------|------|
| `000₂` | 不广播星期 |
| `001₂` | 星期日 |
| `010₂` | 一 |
| `011₂` | 二 |
| `100₂` | 三 |
| `101₂` | 四 |
| `110₂` | 五 |
| `111₂` | 六 |

### 3.5 MassReg — Table 7.76 / 7.77（7.2.19.5）

| 段 | 子场 | Len | 含义 |
|----|------|-----|------|
| Parms 1 | Reserved | 5 | `00000₂` |
| | **Reg_Window** | 4 | Table 7.77；`0`=取消大规模登记 |
| | Aloha Mask | 5 | 人口细分（与 C_ALOHA Mask 同类） |
| Parms 2 | 地址 | 24 | ADRNULL 或指定 MS 个号 |

**Reg_Window（Table 7.77）** — Treg_Window 秒：

| Value | 秒 | Value | 秒 |
|-------|----|-------|----|
| 0 | 取消 Mass Registration | 8 | 100 |
| 1 | 0.5 | 9 | 300 |
| 2 | 1 | 10 | 1 000 |
| 3 | 2 | 11 | 3 000 |
| 4 | 5 | 12 | 10 000 |
| 5 | 10 | 13 | 30 000 |
| 6 | 20 | 14 | 100 000 |
| 7 | 30 | 15 | 200 000 |

过程：6.4.6 / 6.7.1.5；MS 用 Reg_Window + Mask 决定何时重登记。

### 3.6 Chan_Freq — Table 7.78（7.2.19.6）

**必须** MBC 头 + BC_AP。

| 段 | 子场 | Len | 含义 |
|----|------|-----|------|
| Parms 1 | Reserved | 14 | `0` |
| Parms 2 | Reserved | 12 | `0` |
| | CH_ADJ | 12 | 被宣布信道的物理信道号 1…4095 |

续块 BC_AP 给绝对 Tx/Rx。

### 3.7 Adjacent_Site — Table 7.79（7.2.19.7）

布局与 Vote_Now 几乎相同（Parms 1 = 邻站 SYScode 高 14 位；Parms 2 = 连网标志 + 两级优先级 + CH_ADJ）。用于优化猎站（6.7.1.7）。

### 3.8 Gen_Site_Params — Table 7.80（7.2.19.8）

| 段 | 子场 | Len | 指向 |
|----|------|-----|------|
| Parms 1 | Reserved | 14 | |
| Parms 2 | Current (Confirmed) Site Information | 8 | Table **7.101**（含 Hibernating_Flag） |
| | Reserved | 8 | |
| | Network Information | 8 | Table **7.102**（含“登记是否带组订阅”位） |

**Table 7.101**（节选）：Hibernating_Flag(1) `1`=本 TSCC 即将休眠。  
**Table 7.102**（节选）：Reg and TG Subscription(1) `0`=登记过程带组订阅列表；`1`=登记不带（上电首次仍应带，NOTE）。

---

## 4. 绝对频率附块（公告侧）

与 Grant 的 CG_AP 对照（细节与 CdefParms 见 Reason/Grant 文件 §13）：

| 附块 | 表 | 用于 | 与 CG_AP 差异 |
|------|----|------|---------------|
| **BC_AP** | 7.21 | Ann_WD_TSCC 绝对形式；Chan_Freq | Reserved **8** bit（无独立 CC 场）+ Cdeftype(4)+Reserved(2)+CdefParms(58) |
| **VN_AP** | 7.72 | Vote_Now 当 CH_VOTE=`0xFFF` | 与 **CG_AP 同构**（Reserved4 + CC4 + Cdeftype + CdefParms） |
| **MV_AP** | 7.18 | C_MOVE 绝对形式 | 同 CG_AP 骨架 |
| **CG_AP** | 7.16 | 任意 Grant 绝对形式 | 见 Reason/Grant §13 |

Cdeftype=`0000₂`：CHAN(12)+TXMHz(10)+TXKHz(13)+RXMHz(10)+RXKHz(13)=58。换算公式：[`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md)。

---

## 5. C_MOVE / MV_AP（与 Grant 相邻，非 Grant）

引用：7.1.1.1.3；Tables **7.17 / 7.18**。CSBKO=`11 1001₂`（57）。把 MS 迁到另一 TSCC。

猎站衔接（Commanded Hunt）：[`AnnexD猎站Hunt.md`](./AnnexD猎站Hunt.md)。

| IE | Len | 含义 |
|----|-----|------|
| LB / PF / CSBKO / FID | 1+1+6+8 | CSBKO=`111001₂` |
| Reserved | 9 | 0 |
| Mask | 5 | 与 Aloha 同类，可点名子集 |
| Reserved | 5 | 0 |
| Reg | 1 | 新 TSCC 是否要求登记 |
| Backoff | 4 | |
| Reserved | 4 | 0 |
| Physical Channel Number | 12 | 新 TSCC；`0` 无效；`0xFFF`→MV_AP |
| MS address | 24 | 个号（可配合 Mask） |

---

## 6. Service_Kind（Table 7.49）

引用：7.2.12.0。4 bit。C_RAND / C_AHOY / C_ACKVIT 共用。

| Value | 含义 |
|-------|------|
| `0000₂` | 个呼语音（业务信道上亦可为 Include 个呼） |
| `0001₂` | 组呼语音（业务信道上亦可为 Include 组呼） |
| `0010₂` | 个呼分组数据 |
| `0011₂` | 组呼分组数据 |
| `0100₂` | 个呼 UDT 短数据 |
| `0101₂` | 组呼 UDT 短数据 |
| `0110₂` | UDT 短数据轮询 |
| `0111₂` | 状态传送 |
| `1000₂` | 呼叫改向 |
| `1001₂` | 呼叫应答（Answer Call / FOACSU） |
| `1010₂` | 全双工 MS–MS 语音 |
| `1011₂` | 全双工 MS–MS 分组数据 |
| `1100₂` | 保留 |
| `1101₂` | 补充业务（Stun/Revive/Kill/DGNA 等，靠网关 ID 细分） |
| `1110₂` | 登记/鉴权（及注销）/ MS 无线检查 |
| `1111₂` | 取消呼叫 |

---

## 7. Service_Kind_Flag（Table 7.50）

引用：7.2.12.1。1 bit，**随 Service_Kind + 所在 PDU** 变义。

### 7.1 TSCC / C_AHOY

| Kind | 消息 | Flag=`0` | Flag=`1` |
|------|------|----------|----------|
| `0000₂` | 个呼语音无线检查 | OACSU：能否立即接听 | FOACSU：是否准备好接听 |
| `0000₂` | 个呼到线路目的（上传号码） | 适用 | — |
| `0001₂` | 组呼无线检查 | 组内是否至少一台在无线覆盖 | — |
| `0010₂` / `0011₂` | 个/组数据检查 | 是否在覆盖 | — |
| `0100₂`…`1000₂` / `0111₂` 等短数据、改向 | 不适用 | 置 `0` | — |
| `1001₂` | P_AHOY 无线检查 | 个号：与业务无关的存在检查 | 组：存在检查 |
| `1010₂` | 全双工语音检查 | OACSU | FOACSU |
| `1011₂` | 全双工数据检查 | 是否在覆盖 | — |
| `1101₂` | Stun/Revive | **Stun** | **Revive** |
| `1101₂` | Kill / DGNA | 不适用 | — |
| `1110₂` | 登记/鉴权/无线检查 | 不适用 | Talk Group Subscription Data |
| `1111₂` | 取消呼叫 | 不适用 | — |

NOTE：`1101₂` 为补充数据业务，具体靠该 PDU 的 Gateway ID。

### 7.2 业务信道 P_AHOY

| Kind | Flag | 含义 |
|------|------|------|
| `0000₂`/`0001₂`/`0010₂`/`0011₂` | `0` | 语音/数据个或组检查 |
| `1001₂` | `0`/`1` | 个号 / 组 存在检查 |
| `1111₂` | `0` | 从语音业务信道清除**个号** |
| `1111₂` | `1` | 从语音业务信道清除**组** |

**UDT_Option_Flag（Table 7.51）**：UDT 下载带补充数据、用来替代 Ahoy 检查时，与 Flag 同义（`0` OACSU / `1` FOACSU）。其它业务保留为 `0`。

---

## 8. Service_Options（7 bit，按业务重定义）

引用：7.2.13。出现在 **C_RAND**；C_AHOY 用 **Service_Options_Mirror** 回映。

### 8.1 语音请求 — Table 7.52

| 子场 | Len | 编码 |
|------|-----|------|
| Emergency | 1 | `1`=紧急 |
| Privacy | 1 | 本 Part 未定义 |
| Supplementary Data | 1 | `1`=本呼叫要补充数据 |
| Broadcast | 1 | `1`=广播（适用于组） |
| Reserved | 1 | `0` |
| Priority level | 2 | `00` 普通；`01` P1；`10` P2；`11` **P3 最高** |

### 8.2 分组数据 — Table 7.53

Emergency(1) + Privacy(1) + Supplementary Data(1) + **Hi Rate**(1：`0` 单时隙 / `1` 双时隙) + **SIMI**(1：`0` 单条目 / `1` 多条目) + Priority(2)。  
Grant 侧 SI/MI 由 **CSBKO** 表达（PD/TD `_MI`），与这里的 SIMI 对应。

### 8.3 呼叫改向 — Table 7.54

| 子场 | Len | 编码 |
|------|-----|------|
| Emergency / Privacy | 1+1 | 不适用 / 未定义 |
| Divert On/Off | 1 | `0` 清除改向；`1` 设置 |
| Divert Kind | 4 | 各 1 bit：语音 / 分组数据 / UDT 短数据 / 状态（`1`=适用） |

终答 Reason 见 Reason 文件 Table 6.60。

### 8.4 登记 — Table 7.55

| 子场 | Len | 编码 |
|------|-----|------|
| Reserved / Privacy | 1+1 | |
| IP_Inform | 1 | `1`=通告 IP 连接 |
| PowerSave_RQ | 3 | `000` 不请求省电；`001`…`111` 请求 |
| Reg_Dereg | 1 | 与 IP_Inform 组合：登记/注销或加/删 IP |

登记失败 Reason：`Reg_Refused` / `Reg_Denied`（无独立码表）。

### 8.5 Include（仅业务信道）— Table 7.56

Reserved(1)+Privacy(1)+Reserved(5)。

### 8.6 状态传送 — Table 7.57

G/I(1) + Supplementary_user Data(1) + Status 高 5 位。低 2 位走 C_AHOY 的 Appended_Blocks（Table 7.22 NOTE 2）。

### 8.7 UDT 短数据 — Table 7.58

Emergency/Privacy/Supplementary Data + BCAST_SV=`0` + Reserved + PRIORITY=`00`（后几位不适用）。

### 8.8 补充数据 — Table 7.59

多数位置 `0` / 不适用。

### 8.9 UDT 短数据轮询 — Table 7.60

Emergency/Privacy/Supplementary=`0` + **Polling Format**(4)。

### 8.10 Service_Options_Mirror（鉴权 / Stun / Kill）

Table **7.61–7.63**：Reserved(1)+Privacy(1)+Reserved(5)。若 AHOY 是对 C_RAND 的立即（或延迟）确认，则 Mirror **复制**该 C_RAND 的 Service_Options（7.2.14.0）。

---

## 9. 其它短枚举

### 9.1 Protect_Kind — Table 7.82（P_PROTECT，7.2.21）

| Value | Alias | 含义 |
|-------|-------|------|
| `000₂` | DIS_PTT | 禁止目标 MS/组发射 |
| `001₂` | EN_PTT | 允许发射 |
| `010₂` | ILLEGALLY_PARKED | 清除地址不匹配 Source/Target 的 MS |
| `011₂` | EN_PTT_ONE_MS | 仅 Target 匹配的 MS 允许 PTT，其余禁止 |
| `100₂`…`111₂` | | 保留 |

### 9.2 Maint_Kind — Table 7.83（P_MAINT，7.2.22）

| Value | Alias | 含义 |
|-------|-------|------|
| `000₂` | DISCON | 断开，结束业务信道使用 |
| `001₂`…`111₂` | | 保留 |

### 9.3 Version（C_ALOHA）— Table 7.93（7.2.32）

| Value | 系统声称符合的 Part 4 版本 |
|-------|---------------------------|
| `000₂` | 直到 V1.5.1 |
| `001₂` | V1.6.1 |
| `010₂` | V1.7.1 / 1.8.1 / 1.9.1 / 1.9.2 |
| `011₂` | V1.10.1 |
| `100₂` | V1.11.1 |
| `101₂`…`111₂` | 保留 |

本资料库 PDF 为 **V1.12.1**；表中尚未单独列出 `1.12.1` 码点（以原文 Table 7.93 为准）。

### 9.4 HI_RATE — Table 7.48

`0` 单时隙数据；`1` 双时隙。DX 数据 Grant 固定 `0`。

### 9.5 G/I — Table 7.81

`0` 个号；`1` 组（定义在 Part 1，Part 4 重申）。

### 9.6 Opcode — Table 7.67

6 bit，取值见 Annex **B.1**（Reason/Grant 文件 §14 已列 Grant/ACK 子集）。其余：C_BCAST=`101000₂`，C_ALOHA=`011001₂`，C_MOVE=`111001₂`，P_CLEAR=`101110₂`，P_PROTECT=`101111₂`，P_MAINT=`101010₂`，C_RAND=`011111₂`，C_ACKVIT=`011110₂`。

### 9.7 Proxy Flag — Table 7.64（指针）

网关延伸 BCD：`0` → 1…20 位（1 块 UDT）；`1` → 21…44 位（2 块）。

---

## 10. C_ALOHA 场与公告的共享位（对照）

C_ALOHA Table **7.19**（速览已有字段表）。与 BCAST 重叠的 IE：

| IE | Aloha | BCAST |
|----|-------|-------|
| Reg | 有 | 有（应一致） |
| Backoff | 有 | 有 |
| System Identity Code | 16 | 16 |
| Mask | 5（争用细分） | MassReg 的 Aloha Mask |
| Offset | TSCC aligned/offset | Grant/Vote 的业务信道 Offset 是另一回事 |
| Version | Table 7.93 | — |
| TSCCAS / Site Timeslot Sync / Active_Connection | 仅 Aloha（Active_Connection 亦出现在 Vote/Adjacent Parms） | |

Aloha **没有** Reason Code；未登记却发业务 → TS 用 `C_NACKD(MS_Not_Registered)`。

---

## 11. 覆盖与缺口

### 已覆盖

| 条款 / 表 | 内容 |
|-----------|------|
| 7.1.1.1.5 Tables **7.20–7.21** | C_BCAST / BC_AP |
| 7.2.19 Tables **7.68–7.80** | 全部 8 类 Announcement_type + 子枚举 7.74/7.75/7.77 |
| 7.2.19.3.1 Table **7.72** | VN_AP |
| 7.1.1.1.3 Tables **7.17–7.18** | C_MOVE / MV_AP |
| 7.2.12 Tables **7.49–7.51** | Service_Kind / Flag / UDT_Option_Flag |
| 7.2.13–7.2.14 Tables **7.52–7.63** | Service_Options 及 Mirror |
| 7.2.21–7.2.22 Tables **7.82–7.83** | Protect_Kind / Maint_Kind |
| 7.2.32 / 7.2.40–7.2.41 | Version；Site / Network Info 要点 |

### 未展开

| 项 | 说明 |
|----|------|
| Annex C 频率公式与信道规划图 | 不抄 |
| UDT 附录 B 载荷 / Stun / DGNA / USBD / 定时器 | 已迁出 [`Stun_DGNA_UDT与定时器.md`](./Stun_DGNA_UDT与定时器.md) |
| 鉴权算法、Stun/Kill 完整 MSC | 枚举已收；过程场见上文件，算法以 6.4.8 PDF 为准 |
| Table 7.64–7.66、7.84–7.92 等单比特/格式 IE | 部分只作指针（Proxy、A、SAP、Privacy、STATUS） |
| 厂商 Announcement_type `11110₂/11111₂` | 无公开语义 |
| CACH 上 Short LC 的 SYScode 比特图 | figure 6.19，见 7.2.7 NOTE |

---

*学习向整理。实现与互操作请核对 ETSI TS 102 361-4 V1.12.1 原文。*
