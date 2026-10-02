## 4. 机制拆解：三姐妹 + SARQ + UDP HC

Canonical 来源：`03-数据协议/数据协议字段速览.md` **§1、§4.3–§5、§7–§9**；第 13 课 **§7**；第 27 课承载回唤；手册 **§5.3**。下列**故意不画完整 SDL**，也**不重讲**确认/非确认全时间线。

### 4.1 短数据 ≠ IP：先分家

| 问题 | 短数据路径 | IP / HC 路径 |
|------|-----------|--------------|
| 用户要什么 | 状态码、短报文、约定字符集载荷 | IP 包（定位 LIP、文本 UDP、厂商应用…） |
| 头长什么样 | SP / R / DD_HEAD | C_HEAD 或 U_HEAD（+ 可选压缩头在续块） |
| DPF 家族 | `1110` / `1101`（另：UDT=`0000` 指针） | `0011` / `0010`（确认/非确认） |
| SAP | 常 `1010` Short Data | `0011` HC 或 `0100` IP based |
| 省字节手法 | 状态直接塞进头；载荷本来就短 | **HC** 去掉重复的 IP/UDP 常量与可推导地址 |

现场仲裁句：

> 「状态码先找 SP_HEAD；自由短字节找 R/DD；说『上网传定位』才进 IP/HC——三张票，别撕成一张。」

### 4.2 短数据三姐妹字段表（必背）

引用：Part1 Tables **9.17A–C**；资料库速览 **§5.1–§5.3**。

#### 4.2.1 SP_HEAD — Status/Precoded（Table 9.17A）

| IE | Len | 岗位备注 |
|----|-----|----------|
| G/I, A | 1+1 | 目的组/个；是否请求响应 |
| AB | 2+4 | **Status/Precoded 时置 `0`**（状态在头内，通常无续块） |
| DPF / SAP | 4+4 | DPF 常为 `1110`；SAP Short Data `1010` |
| LLID Dest/Src | 24+24 | |
| Source Port (SP) | 3 | 短数据源端口 |
| Destination Port (DP) | 3 | 短数据目的端口 |
| Status/Precoded | **10** | **状态码本体** |
| Header CRC | 16 | |

```text
  幸福路径（状态 ping）：
  [SP_HEAD] 里面已经带着 10-bit 状态
       → 若 A=0：发完即结束（像非确认）
       → 若 A=1：等短数据响应（Table 6.6 子集）
```

#### 4.2.2 R_HEAD — Raw（Table 9.17B）

| IE | Len | 岗位备注 |
|----|-----|----------|
| G/I, A | 1+1 | |
| AB MSBs/LSBs | 2+4 | **后续块数** |
| DPF / SAP | 4+4 | 常 DPF=`1110`；SAP Short Data |
| LLID Dest/Src | 24+24 | |
| SP / DP | 3+3 | |
| SARQ | 1 | 是否按块选择重传 |
| Full Message Flag (F) | 1 | 有 SARQ：首次 `1`、重试 `0`；无 SARQ 置约定值 |
| Bit Padding | 8 | |
| Header CRC | 16 | |

#### 4.2.3 DD_HEAD — Defined Data（Table 9.17C）

与 R_HEAD **类似骨架**，但用 **Defined Data（DD）6 bit** 字符集选择（Binary / BCD / UTF…，Part1 **9.3.38**）**替代** SP/DP 那一对端口字段；同样含 SARQ、F、Bit Padding。

口诀：

- **SP**：码在头里，AB=0。  
- **R**：原始字节跟在后面，靠 SP/DP 找应用。  
- **DD**：跟在后面，但先靠 **DD 字符集**约定「怎么读这些字节」。

### 4.3 A + SARQ + stop-and-wait + 响应子集（回唤第 27 课）

短数据确认响应 Class/Type/Status 见 Part3 Table **6.6**（资料库 §4.3）——与第 27 课同一张实用子集：

| Class | Type | Status | Message | 含义摘要 |
|-------|------|--------|---------|----------|
| 00 | 001 | 000 | ACK | 全部块成功 |
| 01 | 000 | 000 | NACK | Illegal format |
| 01 | 001 | 000 | NACK | Packet CRC failed |
| 01 | 010 | 000 | NACK | Memory full |
| 01 | 100 | 000 | NACK | Undeliverable |
| 10 | 000 | 000 | SACK | 按 C_RDATA 位图选择重传 |

**A + SARQ**（Table **6.5**）：

| A | SARQ | 含义 |
|---|------|------|
| 0 | 0 | 非确认（无响应） |
| 0 | 1 | 保留 |
| 1 | 0 | 确认（整消息） |
| 1 | 1 | 确认 + 按块 SARQ |

岗位节奏（短数据侧规范强调）：

```text
  stop-and-wait：
  发完本趟短数据（头 ± 续块）→ 若 A=1 则站岗等 ACK/NACK/SACK
       → 若 SACK：按位图补块（F 置重试语义）→ 再等
       → 成功或失败后再考虑发下一趟
  （不要幻想无限大窗口滑窗——本课记节奏即可）
```

R_HEAD / DD_HEAD：**无 SARQ** 时 F 置约定值；**有 SARQ** 时首次 F=`1`、重试 F=`0`（Part3 正文，资料库 §4.4）。

> 回唤一句第 27 课：C_RHEAD / C_RDATA、TD_LC 留窗、T_RspnsWait 量级——机制相同家族；本课不重画列车时刻表。

### 4.4 DPF 与 SAP 速查（短数据/HC 相关）

**DPF**（Part1 Table **9.30**，摘与本课相关行）：

| Value | Meaning | 本课角色 |
|-------|---------|----------|
| 0000 | UDT | 仅指针 → Part4 / 后课 |
| 0001 | Response | 短数据确认时的响应壳 |
| 0010 / 0011 | Unconfirmed / Confirmed | IP/HC 乘客的车次 |
| **1101** | Short Data: **Defined** | DD_HEAD |
| **1110** | Short Data: **Raw or Status/Precoded** | R_HEAD / SP_HEAD |
| 1111 | Proprietary | P_HEAD 门口 |

**SAP**（Part1 Table **9.31**，摘与本课相关行）：

| Value | Meaning | 本课角色 |
|-------|---------|----------|
| 0000 | UDT | 指针 |
| **0010** | TCP/IP header compression | **仅预留；无完整表** |
| **0011** | UDP/IP header compression | **本课 HC 主菜** |
| 0100 | IP based Packet data | 未压缩 IP 门口 |
| **1010** | Short Data | **三姐妹** |

### 4.5 UDP/IPv4 头压缩（Part3 clause 7.2 / Table 7.14）

压缩头位于**第一个数据续块**；Data Header 上 **SAP = `0011`**。

为什么值得压？IPv4 头 20 字节 + UDP 头 8 字节 = 28 字节常量/半常量——在 Rate ½/¾ 块里非常贵。HC 留下真正会变的 Identification 与端口索引，地址用 **SAID/DAID + LLID** 推导，长度/校验和在接收侧重算。

#### 4.5.1 压缩头字段（资料库 §7.1）

| IE | Len | 备注 |
|----|-----|------|
| IPv4 Identification | 16 | 原样传送 |
| SAID | 4 | 源网段索引 |
| DAID | 4 | 目的网段索引 |
| HC Opcode bit1 | 1 | Opcode MSB |
| SPID | 7 | 源端口索引；`0000000` → 扩展头带真端口 |
| HC Opcode bit2 | 1 | Opcode LSB |
| DPID | 7 | 目的端口索引 |
| Extended Header 1 | 16 | 可选 UDP 端口 |
| Extended Header 2 | 16 | 可选 UDP 端口 |

**HC Opcode（2 bit）**：`00` = UDP/IPv4 Header Compression；其它保留。

#### 4.5.2 SAID / DAID / SPID / DPID 取值摘要（§7.2）

| IE | 关键值 |
|----|--------|
| SAID | `0000` Radio Network；`0001` USB(Ethernet)；`1100–1111` 厂商；其它保留 |
| DAID | 同上，另 `0010` Group Network |
| SPID/DPID | `0000000` → 真端口在 Extended Header；`0000001` → **5016** UTF-16BE Text；`0000010` → **5017** LIP；高值厂商可配 |

#### 4.5.3 Extended Header 选用（Tables 7.20 / 7.21）

| SPID | DPID | EH1 | EH2 |
|------|------|-----|-----|
| 0 | 任意 | 源 UDP 端口 | （若 DPID 也 0 → EH2=目的端口） |
| ≠0 | 0 | 目的 UDP 端口 | 不用 → 改放应用数据 |
| ≠0 | ≠0 | 不用 → 应用数据 | 不用 → 应用数据 |
| 0 | 0 | 源端口 | 目的端口 |

口诀：**索引能说清端口就别占 EH；两边都是 0 才双挂真端口。**

#### 4.5.4 解压侧常量 / 推导（§7.4 摘要）

| 字段 | 处理 |
|------|------|
| UDP Length | = 8 + User − 压缩头字节 |
| UDP Checksum | 接收侧重算（RFC 768） |
| IPv4 Version / IHL | 常量 `0100` / `0101`（IHL=5） |
| IPv4 TOS / Flags / FragOff | 规范默认（常 0） |
| IPv4 Total Length | = 20 + UDP Length |
| IPv4 TTL / Protocol | 默认；Protocol=UDP |
| IPv4 Header Checksum | 接收侧重算 |
| IPv4 Src/Dst Addr | **SAID/DAID + Data Header LLID** 推导（DLL derived IP） |

```text
  [C_HEAD/U_HEAD] SAP=0011 · LLID Dest/Src …
        │
        ▼
  [第一续块]  [IPv4 ID|SAID|DAID|Opcode/SPID|Opcode/DPID|(EH…)|应用数据…]
        │
        ▼ 接收侧拼回「像模像样的 UDP/IPv4 包」
  应用：LIP / 文本 / 厂商 UDP …
```

### 4.6 诚实边界三块（写进纪律）

**（1）TCP HC**  
SAP=`0010` 已预留；Part3 V1.3.1 **clause 7.2** 正文展开的是 **UDP/IPv4** 压缩头字段表。资料库 §9 写明：未见与 UDP 对等的完整 TCP 压缩八位组表 → **本课与资料库都不编造**。现场若产品声称 TCP HC，去问厂商实现说明书，别假装 ETSI 有一张你「记得」的表。

**（2）UDT**  
UDT_HEAD（Table 9.17D）本课**只做指针**：DPF=`0000`；含 UDT Format、Pad Nibble、AB/SF/PF、**UDT Opcode（UDTO）** 等；续/末块 UDT_LDATA。**控制信道 UDT 短数据过程 → Part4**；UDTO 取值**不在本课展开**（大纲后段 / 约第 39 课一带）。别把 UDT 和 SP/R/DD 三姐妹背成四种平行「日常短数据」。

**（3）Tier I/II vs Tier III（一行提醒，手册 §5.3 / 第 13 §7.5）**

| 能力 | Tier I / II | Tier III |
|------|-------------|----------|
| 短数据 | 多经 **业务信道 PDP（Part3）** 三姐妹 | **控制信道有自有短数据**（Part4）；业务信道仍可走 PDP |
| IP / HC | 业务信道 PDP | 业务信道 PDP（HC 故事同族） |

> 「集群控制信道短数据是 Part4；常规模式下短数据走 Part3 PDP。两边都对，路径不同。」——第 13 课原句，本课继续有效。

### 4.7 和确认/非确认列车如何叠乘（只回唤）

```text
  短数据：
    A=0 → 像「非确认」节奏（无响应）
    A=1 → 像「确认」节奏（等 Table 6.6 子集；可 SARQ）

  IP + HC：
    外层仍是 C_HEAD（DPF=0011）或 U_HEAD（DPF=0010）
    SAP=0011 只说明「第一续块有压缩登机牌」
    要不要 ACK，仍看确认/非确认车次 —— 不是「开了 HC 就自动确认」
```

---

## 5. 对照表：先前各课 → 本课角色

| 来源 | 本课用它做什么 |
|------|----------------|
| 第 13 §7.3–7.5 | 三姐妹门口、IP/HC 指针、Tier 分家 |
| 第 27 全文 | 车次（确认/非确认）、响应、TD_LC——乘客往上坐 |
| 速览 §1 | DPF/SAP 总表 |
| 速览 §4.3–4.4 | Table 6.6 子集；A+SARQ |
| 速览 §5 | SP/R/DD/UDT/P 头字段 |
| 速览 §7 | UDP/IPv4 HC 全表与解压常量 |
| 速览 §8–§9 | Data Type/DPF 速查；TCP HC / UDT 缺口声明 |
| 手册 §5.3 | Tier 数据能力一览 |
| 第 24 课 | Rate 保护权衡直觉（HC 省字节的背景） |
| 加餐 | 12.5 kHz / 4FSK / 双时隙提醒 |

---

## 6. 现场岗位对照 / 分诊

| 现场现象 | 本课解释 | 先查什么 |
|----------|----------|----------|
| 「发个到位」却去配 IP 通道 | 应用要的是 **Status/Precoded** | 写频/API 是否走 SP_HEAD；DPF 是否 `1110` 且头内 10-bit |
| 抓到 SP_HEAD 却抱怨「后面 Rate 块丢了」 | Status 常 **AB=0、无续块** | 先读 AB 与 Status 字段，再骂丢包 |
| 短报文对端乱码 | Raw vs Defined 路径混用；或 DD 字符集不一致 | DPF `1110` vs `1101`；DD 值；应用是否按约定解码 |
| 要回执的短报文却永无 ACK | A=0；或对端不支持；或 ID/CC 错 | 先读 **A / SARQ**，再查射频 |
| 开了 SARQ 仍整包重传 | 对端只回 NACK 不回 SACK；或实现未走选择重传 | 看响应 Class/Type；F 重试语义 |
| 「UDP 文本/定位失败」 | 可能 SAP 不是 `0011`；或 SPID/DPID≠5016/5017；或 EH 规则错 | Data Header SAP → 第一续块压缩头 → 端口索引 |
| 解压后 IP 地址怪异 | SAID/DAID / LLID 推导链断 | 对照 Radio Network / USB / Group Network 索引 |
| 产品说支持 TCP HC，规范里找不到表 | SAP 仅预留 | **不要编造**；问厂商说明书 |
| 集群网优与常规网优吵「短数据走哪」 | Tier 路径不同 | 问清 Tier；控制信道 → Part4；业务信道 PDP → 本课 |
| 把短数据 SP/DP（3 bit）当成 UDP SPID/DPID（7 bit） | 两套端口语义 | 先看 SAP：Short Data vs UDP HC |

写频 / 网优 30 秒话术：

> 「短数据先问要状态码还是短字节：状态码看 SP_HEAD，码在头里；短字节看 R 或 DD，DD 还多一个字符集约定。要回执就置 A，需要按块补洞再加 SARQ，短数据侧是发一趟等一趟。传 IP 定位/文本才进 UDP 头压缩：SAP=0011，第一块里是压缩登机牌，5017 是 LIP、5016 是 UTF-16BE 文本。车次还是第 27 课那两班——确认或非确认。集群控制信道短数据另翻 Part4。」

---
