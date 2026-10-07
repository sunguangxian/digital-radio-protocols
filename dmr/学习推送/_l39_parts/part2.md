## 5. UDT：控制信道上的「小货车」

### 5.1 为什么需要 UDT（6.5.0）

控制信道的 CSBK 一块只有 **8 个字节的信息区**（64 bit），而且几乎都被「两个 24 位地址 + 业务比特」占满了。可网络里有大量「要捎带一点数据」的场合——第 38 课的外线号码就是一例。如果每种业务都自己发明一套多块格式，Tier III 会乱成一锅粥。所以规范说（6.5.0 原文大意）：**为了降低复杂度，所有经过 TSCC 的数据运输共用一种方法——统一数据传送机制（Unified Data Transport，UDT）**。

UDT 拉的货分三大类（6.5.0 a/b/c，逐条核对过）：

| 类别 | 头里 SF 位 | 典型货物 |
|---|---|---|
| **a) 补充数据传送业务**（为别的业务服务） | **`1`** | 外线 PSTN / PABX 拨号数字（第 38 课）；经网关的目的地址；IPv4/IPv6 地址；NMEA 定位；来电号码 CLI（下行）；随某次呼叫附带的用户数据；呼叫转移的地址；**组订阅（附着）的组号上传** |
| **b) UDT 短数据投递业务**（数据本身就是目的） | **`0`** | **UDT 短信**；NMEA / LIP 定位；**DGNA 的组号** |
| **c) UDT 短数据轮询业务** | **`0`** | 网络或手台去「问」另一方要一份数据 |

记住 **SF（Supplementary_Flag）**这一位：**`1` = 这车货是给别的业务打下手的；`0` = 这车货就是用户要的东西**（6.5.0 NOTE）。

### 5.2 车的样子：1 个头 + 最多 4 节车厢

```text
  ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │  UDT 头块   │ │ 附块 #1   │ │ 附块 #2   │ │ 附块 #3   │ │ 附块 #4   │
  │ 10 字节信息  │ │ 12 字节   │ │ 12 字节   │ │ 12 字节   │ │ 10 字节   │
  │ + 2 字节 CRC │ │ （非末块） │ │ （非末块） │ │ （非末块） │ │ + 2 字节CRC│
  └────────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
     每一块 = 一个 30 ms 突发，BPTC(196,96) 1/2 码率；所有块必须连续发送（6.5.0）
```

- 每块 **12 个字节**（96 bit），用 **1/2 码率 BPTC(196,96)** 保护（Part 1 8.2.2.5）。  
- **最后一块**要留出 **2 个字节放 CRC**，所以末块用户数据只有 **10 字节 = 80 bit**（Part 1 8.2.2.5：*The last block shall contain a data CRC in the last two octets*）。  
- 头块也有自己的 2 字节头 CRC（Part 1 Figure 8.10），信息区 10 字节。  
- 所以总容量：**3 × 96 + 80 = 368 bit**——和 6.6.4.0 原文「*Up to 368 bits of data may be transported*」完全对上。

| 附块数 | UAB 字段 | 用户数据容量 |
|---|---|---|
| 1 | `00` | 80 bit |
| 2 | `01` | 96 + 80 = 176 bit |
| 3 | `10` | 96 + 96 + 80 = 272 bit |
| 4 | `11` | 96 × 3 + 80 = **368 bit** |

**UAB = 附块数 − 1**。这是最容易算错的地方：UAB = `00` 不是「没有附块」，而是「1 个附块」。UDT 头后面至少跟 1 个附块。

### 5.3 头块的 10 个字节（Figure 6.42 / Table 7.24 / 7.28）

```text
            7     6      5        4         3   2   1   0
Octet 0:   G/I    A    EMERG/   UDT_Opt/       DPF(4) = 0000
                       RSVD     UDT_DIV
Octet 1:   SAP(4) = 0000（UDT）    |   UDT_Format(4)      ← 装的是什么货
Octet 2–4: Target address or Gateway (24)
Octet 5–7: Source address or Gateway (24)
Octet 8:   Pad Nibble(5)     |  0  |  UAB(2)            ← 空了几格 / 几节车厢
Octet 9:   SF | PF | Opcode(6)                          ← 货的性质 / 哪种头
（Octet 10–11：头 CRC，Part 1 定义）
```

字段逐个讲：

| 字段 | 位 | 下行 C_UDTHD | 上行 C_UDTHU | 白话 |
|---|---|---|---|---|
| G/I | 1 | `0` 个号 / `1` 组（不指望回应） | 同左 | 发给一个人还是一个组 |
| A | 1 | `1` = 要求回应 | 同左 | 个号时要不要对方回 ACK |
| 第 3 位 | 1 | **Emergency**：`1` 紧急 | **Reserved** `0` | 下行可标紧急 |
| 第 4 位 | 1 | **UDT_Option_Flag**（Table 7.51） | **UDT_DIV**：`1` = 这车装的是呼叫转移目的地 | 下行：OACSU/FOACSU；上行：转移 |
| DPF | 4 | `0000` | `0000` | 数据包格式，UDT 固定 0 |
| SAP | 4 | `0000` | `0000` | 业务接入点，UDT 固定 0 |
| **UDT_Format** | 4 | 见 §5.4 | 同左 | **货物格式** |
| Target / Source | 24+24 | | | 谁发给谁（可以是网关） |
| **Pad Nibble** | 5 | 填了几个 4 bit「空格」 | 同左 | 让数据正好填满最后一块 |
| UAB | 2 | 附块数 − 1 | 同左 | 几节车厢 |
| **SF** | 1 | `1` 补充数据 / `0` 用户数据 | 同左 | §5.1 |
| PF | 1 | 保留 `0` | 同左 | |
| Opcode | 6 | `011010` C_UDTHD（DGNA 用 `100100`） | `011011` C_UDTHU（DGNA 用 `100101`） | 哪种头 |

### 5.4 货物格式 UDT_Format（Table 7.88，B.3）

| 值 | 格式 | 最大装载 | 典型用途 |
|---|---|---|---|
| `0000` | Binary 二进制 | **367 bit**（留 1 bit 作结束标记） | 厂商自定数据、遥测 |
| `0001` | MS / TG Address 地址 | **15 个 24 位地址** | **DGNA_Address**、经网关的地址 |
| `0010` | 4-bit BCD | **92 位数字** | **外线号码**（第 38 课）、CLI |
| `0011` | ISO 7-bit（ISO/IEC 646） | 52 个字符 | 英文短信 |
| `0100` | ISO 8-bit（ISO/IEC 8859） | 46 个字符 | 西文短信 |
| `0101` | NMEA（IEC 61162-1） | 1 或 2 附块 | GPS 位置 |
| `0110` | IP 地址 | IPv4 1 块 / IPv6 2 块 | IP 连接通告 |
| `0111` | **UTF-16BE** | **23 个字符** | **中文短信** |
| `1000` / `1001` | 厂商自定 | | |
| `1010` | Mixed 混合（1 个地址 + UTF-16BE） | 1 地址 + 21 字符 | **DGNA_Alias** |
| `1011` | LIP | ≤ 46 字节 | 定位（格式在 TS 100 392-18-1） |
| `1100`–`1111` | 保留 | | |

**这张表里对中国现场最重要的一个数：控制信道 UDT 短信最多 23 个汉字**（UTF-16BE 一个汉字 16 bit，23 × 16 = 368 bit，正好塞满 4 个附块）。要发更长的内容，就得走业务信道上的分组数据（第 27 课 PDP），那是另一回事了。

### 5.5 Pad Nibble 怎么算：让最后一块「正好装满」

UDT 的每一块都要发满，数据不够就补「空格」。补多少，写在 Pad Nibble 里，单位是 **4 bit（一个 nibble）**，填充值是 `1111`（DigitNULL）。

通用算法（对 UTF-16、BCD 这类「按 nibble 对齐」的格式都成立）：

$$
\text{容量(bit)} = 80 + 96 \times \text{UAB} \qquad \text{Pad Nibble} = \frac{\text{容量} - \text{用户数据位数}}{4}
$$

先选能装下的最少块数，再算剩下几格。拿 UTF-16BE 中文短信练一下（结果与 Table B.8 逐行核对过）：

| 汉字数 | 用户 bit | 选 UAB | 容量 | Pad Nibble |
|---|---|---|---|---|
| 1 | 16 | 0 | 80 | (80−16)/4 = **16** |
| 5 | 80 | 0 | 80 | **0**（正好一块） |
| 6 | 96 | 1 | 176 | (176−96)/4 = **20** |
| 11 | 176 | 1 | 176 | **0** |
| 12 | 192 | 2 | 272 | **20** |
| 17 | 272 | 2 | 272 | **0** |
| 23 | 368 | 3 | 368 | **0**（满载） |
| 24 | 384 | — | — | **装不下** |

再拿第 38 课的 BCD 外线号码对一下：BCD 一位 4 bit，容量 = 20 + 24 × UAB **位数字**（80/4 = 20，96/4 = 24），所以 1–20 位用 1 块、21–44 位用 2 块……和第 38 课 §10 的「20 / 44 位门槛」是同一件事。

两个例外要记住：

- **Binary 不用 Pad Nibble**（固定 `00000`）：它在用户数据后面加一个 `0`，后面全填 `1`；收端从块尾往回找第一个 `0`，它前面就是最后一个用户比特（B.3.1）。所以 1 块最多 79 bit，4 块最多 **367** bit。  
- **Address 格式的 Pad Nibble 固定 `00000`**：空位用 **ADRNULL `000000`** 填（B.3.2）。

### 5.6 一条 UDT 短信的完整旅程（Fig 6.57，6.6.4）

UDT 短信用的是「**多段式呼叫建立**」（multi-part call set-up）。按 Fig 6.57 的字母：

```text
  A  MS(A) ──C_RAND(Target=对方或组, SK=0100/0101, SDATA_VAL=要几块)──────────► TSCC
  B  TSCC  ──C_AHOY(Source=SDMI, Target=MS(A), SK=0100)───────────────────────► MS(A)   「把短信交上来」
  C  MS(A) ──C_UDTHU 头 + 附块…（上行阶段 UDT Upload Phase）──────────────────► TSCC
          （个号时，TSCC 可先 C_AHOY 被叫做「在不在」检查，6.6.4.1.3）
  D  TSCC  ──C_UDTHD 头 + 附块…（下行阶段 UDT Download Phase）─────────────────► MS(B) / 组
  E  MS(B) ──C_ACKU(MS_Accepted 0x44)─────────────────────────────────────────► TSCC    （组：没有这一步）
  F  TSCC  ──C_ACKD(Mirrored_Reason=0x44)  或  组：Message_Accepted 0x60──────► MS(A)   （可重复发以提高可靠性）
```

几个关键点（6.6.4.0 / 6.6.4.1，逐条核对过）：

1. **C_RAND 里先报「要几块」**：Table 6.55 的 `SDATA_VAL`（2 bit）告诉网络「我这条短信需要几个附块」，网络据此预留上行时隙。它和 UAB 一样按「块数 − 1」编码（规范 6.6.8.0 的 DGNA 例子：2 个附块写 `01₂`）。  
2. **网络回 C_AHOY「要货」**：Source = **SDMI**（`FFFEC5`，短数据网关）。如果这次还带了补充数据，先由 **SUPLI**（`FFFEC4`）要补充数据，再由 SDMI 要短信（6.6.4.1.2：若发了 c 则 b 必须跟在 c 后）。  
3. **合法的即时响应**：C_NACKD / C_QACKD / C_WACKD、C_AHOY 鉴权题、C_AHOY(SDMI/SUPLI)，或者「被叫已设置呼叫转移」时直接下发一个 UDT（6.6.4.1.1）。  
4. **存储转发**：TSCC 可以「收一块转一块」（时延小，但上行有错时下行等于白发），也可以「整条收完再转」（出错可以先重收，但时延大）。**规范不规定选哪种**（6.6.4.0、Fig 6.58）。  
5. **主叫最多等 TNP_Timer**：网络每发一次进度消息就刷新它；超时则主叫放弃（6.6.4.1.0 / 6.6.4.6，§8）。

### 5.7 个号短信 vs 组短信：「已送达」的含义不同

| | 个号短信（IND_SD_SRV `0100`） | 组短信（GRP_SD_SRV `0101`） |
|---|---|---|
| 被叫回不回 ACK | **回**：C_ACKU(MS_Accepted `0x44`) | **不回**（6.6.4.0：*the called party shall not send a response*） |
| 下发失败怎么办 | 没收到 ACK 可以重发头 + 附块 | TSCC **可以**重复下发提高成功概率 |
| 给主叫的最终确认 | C_ACKD(**Mirrored_Reason** = `0x44`)：「对方确实收到了」 | `Message_Accepted 0x60`：「网络已经发完了」 |
| 什么时候发最终确认 | 收到被叫 ACK 后 | **最后一次下发完成后**（不能提前） |
| 「已送达」真实含义 | **对方手台确认收妥** | **网络已经下发，不保证每台都收到** |

这就是 §1 里「组短信显示已送达但有人没收到」的根源。原文：*The TSCC shall send a final acknowledgement to the calling unit even though the receipt of the UDT Short Data message is not certain.*（6.6.4.0）

> 关于组短信那条最终确认：6.6.4.1.5 原文写作「C_ACKU(Reason = Message_Accepted [0110 0000₂])」。但 `0x60` 的 `d` 位是 1，表示「网络发给手台」，而组短信里没有任何手台需要回这个 ACK，所以按码值理解，它是**网络发给主叫的确认**（C_ACKD 外壳）。做解析工具时按 Reason 码值认就不会错。

### 5.8 手拼：班长给「3 号门组」发「三号门集合」

条件：MS(A) = 班长 `0x348E1D`，Target = 3 号门组 `0x348217`，内容「三号门集合」5 个汉字，UTF-16BE。

**第一步，算车厢**：5 × 16 = 80 bit → 1 个附块正好装满 → UAB = `00`、Pad Nibble = `0`、SDATA_VAL = `00`。

**第二步，UTF-16BE 编码**（Python 核对过）：

```text
三 U+4E09   号 U+53F7   门 U+95E8   集 U+96C6   合 U+5408
→ 4E 09 53 F7 95 E8 96 C6 54 08          （正好 10 字节 = 末块用户区 80 bit）
```

**第三步，逐个 PDU 拼出来**（CRC 不展开；Response_Info 假设为 0）：

```text
A  C_RAND（MS(A)→TSCC）
   Octet 2 = Service_Options 0000000（无紧急、无补充数据、非广播、无优先级）| Proxy 0 = 0x00
   Octet 3 = SUPED_VAL 00 | SDATA_VAL 00 | Service_Kind 0101（组短数据）     = 0x05
   ⇒ 9F 00 00 05  34 82 17  34 8E 1D
                 Target=3号门组  Source=班长

B  C_AHOY（TSCC→MS(A)）「把短信交上来」
   Octet 2 = SOM 0000000 | SKF 0 = 0x00
   Octet 3 = ALS 0 | G/I 0 | AB 00 | SK 0100 = 0x04     （6.6.4.1.1 写明 Service_Kind = 0100₂）
   ⇒ 9C 00 00 04  34 8E 1D  FF FE C5
                 Target=班长  Source=SDMI

C  C_UDTHU 头（MS(A)→TSCC）
   Octet 0 = G/I 1 | A 0 | Rsvd 0 | UDT_DIV 0 | DPF 0000 = 1000 0000 = 0x80
   Octet 1 = SAP 0000 | UDT_Format 0111（UTF-16BE）     = 0x07
   Octet 8 = Pad 00000 | 0 | UAB 00                     = 0x00
   Octet 9 = SF 0 | PF 0 | Opcode 011011                = 0x1B
   ⇒ 80 07  34 82 17  34 8E 1D  00 1B  [头CRC]
   附块 #1（末块）⇒ 4E 09 53 F7 95 E8 96 C6 54 08  [CRC]

D  C_UDTHD 头（TSCC→3号门组）——和 C 几乎一样，只换 Opcode：
   Octet 0 = G/I 1 | A 0 | Emergency 0 | UDT_Option_Flag 0 | DPF 0000 = 0x80
   Octet 9 = SF 0 | PF 0 | Opcode 011010 = 0x1A
   ⇒ 80 07  34 82 17  34 8E 1D  00 1A  [头CRC]   + 同一个附块（TSCC 可重复下发）

E  （组短信：被叫不回 ACK）

F  最终确认（TSCC→MS(A)），Reason = Message_Accepted 0x60 → Octet 3 = 0xC0
   ⇒ A0 00 00 C0  34 8E 1D  34 82 17
                 Target=发起请求的班长  AddInfo=请求的目的地（3号门组）
```

**常见手拼错误**：把 Service_Kind 直接写进 Octet 2。记住 C_RAND 的 Octet 2 是「7 位 Service_Options + 1 位 Proxy」，Service_Kind 在 **Octet 3 的低 4 位**，Octet 3 的高 4 位是 SUPED_VAL 和 SDATA_VAL。

数一数这条短信占了控制信道多少时隙：A 1 个、B 1 个、C 2 个（头 + 1 附块）、D 2 个（可能重复多次）、F 1 个，**最少 7 个突发**，中间还夹着 Aloha 和等待。规范 Figure 6.43 的示例图上，标出的一段时长是 **540 ms（aligned 时序）/ 720 ms（offset 时序）**。短信越长、附块越多、组下发重复越多，占得就越多——**控制信道繁忙时，大量短信会和呼叫请求抢时隙**，这是网规里要考虑的。

如果是**个号短信**发给队员 `0x348E23`：C_RAND 的 Service_Kind 改 `0100`（Octet 3 = `0x04`）；C / D 的 G/I = 0、A = 1，Octet 0 = `0x40`；E 有了：

```text
E  C_ACKU（MS(B)→TSCC）  A1 00 00 88  34 8E 1D  34 8E 23     Reason 0x44；Target = TS PDU 的 Source（班长）
F  C_ACKD（TSCC→MS(A)）  A0 00 00 88  34 8E 1D  34 8E 23     Mirrored_Reason 0x44；Target=班长；AddInfo=队员
```

E 和 F 只差 Octet 0（`A1` 上行 / `A0` 下行），Reason 原样「镜像」——这就是 Mirrored_Reason 的字面意思。

### 5.9 外线拨号回头看：同一辆车，SF = 1

第 38 课的外线流程现在可以完整读懂了：

```text
C_RAND(Target=PSTNI, Proxy=0/1)               「我要打外线，号码 1–20 位 / 21–44 位」
C_AHOY(Source=PSTNI, SK=0100)                 「把号码交上来」
C_UDTHU：UDT_Format=0010（BCD）、SF=1（补充数据）、UAB=0/1、Pad Nibble=…
```

**SF = 1**，因为这车货（号码）是给「语音呼叫」这项业务打下手的，不是用户要传的数据本身（6.5.0 a-2）。

---

## 6. DGNA：在空中给手台「加组 / 改组」

### 6.1 是什么（6.6.8.0）

平常手台的组是**写频时写死的**。现场临时组建一支跨部门队伍（比如大型活动的「3 号门安保组」），如果要把几十台手台收回来重新写频，根本来不及。**DGNA（Dynamic Group Number Assignment，动态组号分配）**就是：**用 UDT 在空中把临时组号塞进手台**。

规范要点（逐句核对过）：

| 规则 | 原文要点 |
|---|---|
| 手台可以持有的组 | 写频预置的，或用 UDT **动态增删**的 |
| 动态组上限 | **最多 16 个**：DGNA_Address 模式 **15 个** + DGNA_Alias 模式 **1 个** |
| 别名 | 每个动态组都可以挂一个**最多 21 个 UTF-16BE 字符**的别名（通过 Alias 模式） |
| 对象 | **只能发给个号**（*shall only be directed to an individual MS*）——要给 20 台手台加组，就是 20 次 DGNA |
| 发起方 | MS 或网关；**网关发起时只有下行阶段** |
| 一键组 | 手台可以有**一个** One-key_talkgroup：按快捷键甚至**只按 PTT** 就呼这个组 |

### 6.2 两种模式

| | **DGNA_Address** | **DGNA_Alias** |
|---|---|---|
| UDT_Format | `0001`（地址格式，B.3.2） | `1010`（混合格式，B.3.9） |
| 一次带什么 | 1…15 个 24 位组号 | **1 个**组号 + 最多 21 字别名 |
| 附块数 ↔ 容量 | 1 块 3 个、2 块 7 个、3 块 11 个、4 块 15 个 | 1 块 3 字、2 块 9 字、3 块 15 字、4 块 21 字 |
| Pad Nibble | 固定 `00000` | 按字数查 Table B.9 |
| 收到后 | **删掉原来全部 15 个，换成这次的（整表替换）** | 新增 / 改第 16 个组；或给已有的某个组挂别名 |

附块布局（B.3.2 / B.3.9）：

```text
DGNA_Address 附块 #1：  RSVD(7) | OK(1) | ADDRESS1(24) | ADDRESS2(24) | ADDRESS3(24)      = 80 bit
                       后续附块继续排 ADDRESS4…（地址可以跨块切开）

DGNA_Alias   附块 #1：  RSVD(7) | OK(1) | ADDRESS(24) | ALIAS1(16) | ALIAS2(16) | ALIAS3(16)  = 80 bit
                       后续附块继续排 ALIAS4…ALIAS21
```

容量怎么来的（自己验算一遍）：

- Address：总容量 80 + 96 × UAB bit，扣掉开头 8 bit（RSVD + OK），剩 72 + 96 × UAB，除以 24 → **3 + 4 × UAB** 个地址：3、7、11、15（Table 6.67）。地址可以跨块切开，所以不浪费。  
- Alias：总容量扣掉 8 + 24 = 32 bit（RSVD + OK + ADDRESS），剩 48 + 96 × UAB，除以 16 → **3 + 6 × UAB** 个字：3、9、15、21（Table 6.68 / B.9）。

### 6.3 最容易踩的坑：Address 模式是「整表替换」

原文（6.6.8.0 / 6.6.8.1.1）：*The recipient of the DGNA_Address mode transfer shall delete all fifteen previous DGNA addresses and replace them with the addresses conveyed in the new DGNA transfer.*

画出来：

```text
手台原有动态组：  [A] [B] [C] [D] [ ] [ ] … [ ]     （15 格）
调度只想「再加一个 E」，发了一条只含 E 的 DGNA_Address：
手台变成：        [E] [ ] [ ] [ ] [ ] [ ] … [ ]     ← A B C D 全没了！
正确做法：        发 [A] [B] [C] [D] [E]           ← 带上完整清单（需要 2 个附块）
```

**所以「加组」在协议上其实是「下发完整新清单」**。调度平台必须自己记住每台手台当前的动态组清单，每次下发都带全。这也解释了为什么规范说「如果主叫只用了不到 4 个附块，动态组表里就不是所有条目都能访问到」（6.6.8.1.1）——你只发了 1 块，那就只有 ADDRESS1…3 有效。

**一键组 OK 位**：

- Address 模式：附块 #1 的 OK = `1` → **ADDRESS1** 成为一键组。  
- Alias 模式：OK = `1` → 这个 ADDRESS 成为新的一键组（原来的被替换）；OK = `0` → **原来的一键组保持不变**。

**删除**（原文核对过）：

| 要删什么 | 怎么发 |
|---|---|
| 清空 Address 模式的全部 15 个 | Address 模式，1 个附块（UAB `00`），OK = `0`，ADDRESS1…3 = ADRNULL |
| 删第 16 个（只有 Alias 模式能分配的那个） | Alias 模式，ADDRESS = ADRNULL，OK = `0`，Pad Nibble = 0，UAB = `00`，ALIAS = `0000` |

### 6.4 流程：和短信几乎一样，只是网关换成 DGNAI（Fig 6.67）

```text
  A  MS(A) ──C_RAND(Target=DGNAI, SK=1101, SUPED_VAL=要几块)──► TSCC     注意：被叫个号此时还不出现！
  B  TSCC  ──C_AHOY(Source=DGNAI, Target=MS(A), SK=1101, AB=请求的块数)──► MS(A)
  C  MS(A) ──C_DGNAHU 头(Target=MS(B)) + 组号附块──► TSCC                  上行阶段
  D  TSCC  ──C_DGNAHD 头(Target=MS(B), Source=MS(A)) + 组号附块──► MS(B)   下行阶段
  E  MS(B) ──C_ACKU(MS_Accepted 0x44)──► TSCC
  F  TSCC  ──C_ACKD(Mirrored_Reason=0x44)──► MS(A)                        可重复发
```

和短信的三点区别：

1. **C_RAND 的 Target 是 DGNAI，不是被叫**。6.6.8.3.1 原文：*the destination address is not provided to the TSCC until the UDT Inbound phase is complete*——被叫个号要等上行 UDT 头里才出现。  
2. **块数报在 SUPED_VAL**，不是 SDATA_VAL（Table 6.70：SDATA_VAL 固定 `00`）。Fig 6.67 的例子：2 个附块，SUPED_VAL = `01`，最多 7 个组。  
3. **专用 Opcode**：上行 C_DGNAHU（37）、下行 C_DGNAHD（36），不是普通的 C_UDTHU / C_UDTHD。解码器靠 Opcode 就能把 DGNA 和普通短信分开。

**网关（调度台）发起**时，A–C 都没有，直接从 D 开始（6.6.8.0）。现场最常见的就是这种：**调度台在平台上点「动态重组」，TSCC 直接对每台手台下发 C_DGNAHD**。

网络对 C_RAND 的合法即时响应（6.6.8.2.1）：C_NACKD / C_QACKD / C_WACKD；C_AHOY 鉴权题（网络先验主叫）；C_AHOY(DGNAI) 要货。

### 6.5 手拼：班长给队员分配「3 号门（一键）+ 4 号门」

条件：MS(A) 班长 `0x348E1D` → MS(B) 队员 `0x348E23`；组 `0x348217`（一键组）、`0x348218`。2 个组 → 1 个附块（可装 3 个，第 3 个填 ADRNULL）。

```text
A  C_RAND（班长→TSCC）
   Octet 2 = Service_Options 全 0 | Proxy 0                       = 0x00
   Octet 3 = SUPED_VAL 00 | SDATA_VAL 00 | SK 1101                = 0x0D
   ⇒ 9F 00 00 0D  FF FE D6  34 8E 1D
                 Target=DGNAI  Source=班长

B  C_AHOY（TSCC→班长）
   Octet 3 = ALS 0 | G/I 0 | AB 00 | SK 1101                      = 0x0D
   ⇒ 9C 00 00 0D  34 8E 1D  FF FE D6
                 Target=班长  Source=DGNAI

C  C_DGNAHU 头（班长→TSCC）
   Octet 0 = G/I 0 | A 1 | Rsvd 0 | UDT_DIV 0 | DPF 0000          = 0100 0000 = 0x40
   Octet 1 = SAP 0000 | UDT_Format 0001（地址）                    = 0x01
   Octet 8 = Pad 00000 | 0 | UAB 00                               = 0x00
   Octet 9 = SF 0 | PF 0 | Opcode 100101                          = 0010 0101 = 0x25
   ⇒ 40 01  34 8E 23  34 8E 1D  00 25  [头CRC]
             Target=队员  Source=班长
   附块 #1 = RSVD 0000000 | OK 1 → 0x01，ADDRESS1、2、3：
   ⇒ 01  34 82 17  34 82 18  00 00 00  [CRC]
        3号门(一键)  4号门     ADRNULL

D  C_DGNAHD 头（TSCC→队员）：Octet 0 = G/I 0 | A 1 | Emergency 0 | UDT_Option_Flag 0 | DPF → 0x40；Opcode 100100 → 0x24
   ⇒ 40 01  34 8E 23  34 8E 1D  00 24  [头CRC]  + 同一个附块（6.6.8.0：下行的 ADDRESS 从上行原样复制）

E  C_ACKU（队员→TSCC）   A1 00 00 88  34 8E 1D  34 8E 23
F  C_ACKD（TSCC→班长）   A0 00 00 88  34 8E 1D  34 8E 23     （Response_Info 假设为 0）
```

队员手台收到后：**原来的 15 个动态组全部清掉**，换成 [3 号门, 4 号门]；3 号门成为一键组，按 PTT 就呼它。

### 6.6 手拼：再给 3 号门挂个别名「三号门」

Alias 模式，ADDRESS = `0x348217`，OK = `1`（它本来就是一键组；若写 0 则一键组保持不变，这里写 1 也不改变结果），别名 3 个字。查 Table B.9：**3 字 → UAB 0、Pad Nibble 0**（验算：80 − 8 − 24 = 48 bit = 3 字，正好满）。

```text
C_DGNAHD 头：Octet 1 = SAP 0000 | UDT_Format 1010（混合）= 0x0A；Octet 8 = 0x00；Opcode 0x24
   ⇒ 40 0A  34 8E 23  [发起方地址]  00 24
附块 #1：RSVD|OK=1 → 01，ADDRESS 34 82 17，「三号门」4E 09 53 F7 95 E8
   ⇒ 01  34 82 17  4E 09  53 F7  95 E8
```

于是手台上 3 号门组的显示名就变成「三号门」。别名最多 21 字；第 22 个字起装不下（§1 的「25 个汉字被截断」就是这个原因——严格说是**根本发不出去**，被截断是平台或手台自己的处理）。

### 6.7 厂商实现和标准的差异（看说明书时别混）

ETSI 只定义了「手台持有动态组清单 + 一键组」。具体到手台界面，各家做法不同。以本课加深阅读里的两份厂商资料为例：

- **Motorola R7 用户指南（Capacity Max 系统）**：DGNA 由第三方调度台下发；收到后**当前信道进入 DGNA 模式**，响提示音、屏幕短暂显示 Assigned，按 PTT 只能呼当前 DGNA 组；调度台**移除** DGNA 后，手台**恢复原来的组**。  
- **TRBOnet 知识库**：DGNA 会**替换当前 personality 里的联系人和别名**，其他参数不变；扫描列表满了会挤掉一个非优先组；**可选鉴权**，开启后手台先验证系统再接受 DGNA 命令。

注意这些是**厂商在标准之上的产品行为**（「恢复原来的组」「挤掉扫描列表」），**不能拿来推断别家手台**。混合厂商组网做 DGNA，**先在测试手台上验证一遍**整表替换、一键组、别名、删除四种情况。

---
