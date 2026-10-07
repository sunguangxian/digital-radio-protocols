# 第 39 课 · Stun / DGNA / UDT

> DMR 深入学习 · **阶段 E · 集群 Tier III 第 9 课（约 10 课之九）**（接第 38 课「拨号与本地编址」）  
> 适合：已经知道手台怎么找网、登记、发 C_RAND、被 C_AHOY 点名，也会把 `40125318` 换成 `0x348E23`，但一被问到「**网管说『把那台丢了的手台遥晕』，空口上到底发了什么？手台晕了以后还能干什么？**」「**遥晕和遥毙在字节上差在哪？为什么遥毙必须鉴权，遥晕可以不鉴权？**」「**调度台一点『动态重组』，现场几十台手台怎么就多出一个组？原来的组去哪了？**」「**控制信道上发一条『三号门集合』短信，要占几个时隙、为什么组短信的『已送达』其实不保证送到？**」「**上一课外线号码用 UDT 交上去，UDT 到底是个什么东西？**」就答不上来——说不出**这三件事都跑在控制信道上，都靠『C_AHOY 点名 + 网关地址』开头，Stun/Kill 是单块 CSBK 的『命令 + 反向鉴权』，DGNA 和短信是多块 UDT 的『先上传、再下发、最后回执』**——的人  
> 阅读量：约 **30–40 分钟** · **只讲字段、比特落点和流程，不贴 FEC、不画完整 MSC** · 要把「**Stun = 冻结用户业务（还能猎站、登记、鉴权、被定位、被 Revive）；Kill = 永久废掉、空口救不回来、必须鉴权；三者的 C_AHOY 只差 Service_Kind_Flag 一位和 Source 网关的最后一个字节（STUNI `FFFECC` / KILLI `FFFECF`）；UDT = 一个 10 字节头 + 最多 4 个附块、最多 368 bit 的『控制信道小货车』，头里的 UDT_Format 说明货是什么、UAB 说明几节车厢、Pad Nibble 说明空了几格；DGNA = 用 UDT 把最多 15 个组号（或 1 个组号 + 21 个字的别名）塞进手台，Address 模式是**整表替换**，OK 位指定一键组**」钉牢  
> **频谱 / 调制提醒**：RF 仍是 **12.5 kHz** 一条车道，调制仍是 **4FSK**（一个符号 2 bit，**4800 符号/秒 = 9600 bit/s**），时隙 **30 ms**。本课所有动作都发生在**控制信道 TSCC** 上：一条 Stun 命令是 **1 个 CSBK 突发**（96 bit 信息，BPTC(196,96) 编码后占一个时隙）；一条短信最多是 **1 个头 + 4 个附块 = 5 个突发**。每个突发都是同一个 12.5 kHz 车道上的一个 30 ms 时隙——**短信多一节车厢，就多占控制信道一个时隙**，这一个时隙本来可以给别人做随机接入或发 Grant。这就是为什么规范把 UDT 限在 4 个附块：控制信道是全网共享的「调度大厅」，不能被一条长消息堵住。四句话原文见 `学习推送/加餐_频率带宽与调制解调.md`。

---

## 1. 为什么本课重要（动机）

第 38 课结尾我们说：**外线号码就是用 UDT 交上去的。**其实 UDT 远不止交号码。到这一课，阶段 E 的最后几块拼图是**网络对手台的「管理权」**——网络不只是给手台分配信道，它还能：

- **冻住**一台手台（Stun），等找回来再**解冻**（Revive）；
- **永久废掉**一台被盗的手台（Kill）；
- **在空中给手台改组**（DGNA），不用把几十台手台收回来重新写频；
- **在控制信道上捎带小数据**（UDT）：短信、定位、外线号码、IP 地址、动态组号……

现场遇到的问题往往就卡在这里：

- 网管：「我对 3444259 发了遥晕，平台显示『成功』，可用户说手台还能听到组呼。」——**Stun 本来就不保证『变哑巴』**。规范只说被晕的手台「不能请求、也不能接收该网上**用户发起的**业务」，但**猎站、登记、鉴权、Stun/Revive 必须保持可用，定位业务必须保留**（6.4.9.0）。手台具体怎么表现（屏幕提示、听不听得到）要看厂商实现（§4.1）。  
- 网管：「遥毙下去，手台回了 NACK，Reason 是 `0x14`。」——那是 **Recipient_Refused**：手台出了一道题考网络，网络答错了，手台拒绝执行（§4.4，第 35 课反向鉴权）。**别反复重发去碰运气，先查网络侧这台手台的密钥 K。**  
- 网管：「遥毙第一次没收到回执，再发一次，手台完全不理了。」——**很可能第一次已经成功了**。规范 NOTE 明说：手台发完最终 ACK 就关掉全部 DMR 功能，如果这个 ACK 丢了，网络再发 Kill 不会有任何回应（6.4.10.0 NOTE）。  
- 调度：「我给 20 台手台做了动态重组，加了 2 个临时组，结果有 3 台原来动态加过的组全没了。」——**DGNA_Address 模式是整表替换**：收到新的一次传送，手台要删掉原来全部 15 个动态组，换成这次带来的（6.6.8.0）。你只带了 2 个，那原来的就被清掉了（§6.3）。  
- 用户：「组里发短信，平台显示『已送达』，可我们队有人没收到。」——**组短信没有逐台回执**：被叫组成员不回 ACK，TSCC 可以重复下发提高成功率，但给主叫的最终确认是「我发了」而不是「他们都收到了」（6.6.4.0）（§5.7）。  
- 解码器：「控制信道上看到 Target = `FFFED6` 的 C_RAND，这是什么？」——**DGNAI**，有人在发起动态组号分配（§6.4）。  
- 写频：「我写的组别名有 25 个汉字，DGNA 下发后被截断了。」——DGNA_Alias 模式别名**最多 21 个 UTF-16BE 字符**（6.6.8.0）（§6.7）。

所以本课要把一句话钉牢：

> **Stun / Kill：单块命令，网络从网关 STUNI / KILLI 点名手台，手台确认（必要时先反向鉴权）。**  
> **UDT：多块运输，头说明「谁发给谁、装的什么、几节车厢」，附块装货，最多 368 bit。**  
> **DGNA：用 UDT 运送「组号清单」的一项具体业务，网关 DGNAI，专用 Opcode C_DGNAHD / C_DGNAHU。**

本课目标：画出三件事的总图；复习它们共用的「C_AHOY + 网关地址 + Service_Kind」骨架；**手拼** Stun / Revive / Kill 三条 C_AHOY，看清只差哪几个比特；讲清 Stun 后哪些还能用、Kill 的「不归路」；讲清 UDT 的 10 字节头、4 种车厢数、10 种货物格式和 Pad Nibble 的算法；**手拼**一条组短信「三号门集合」从 C_RAND 到最终确认的每个 PDU；讲清 DGNA 两种模式、整表替换、一键组、删除；**手拼**一条 DGNA；会读定时器 TNP_Timer；能做现场分诊；为第 40 课「总复习 + 岗位深挖路线」收好尾。

**本课硬禁令（写进脑子）**：不 dump FEC/CRC/BPTC 矩阵、不贴完整 MSC/SDL、不发明 ETSI 条款号（入口锚点以资料库 `04-集群协议/Stun_DGNA_UDT与定时器.md` **§0–§7**、`ReasonCode与Grant变体.md`、`鉴权与AnnexC频率.md`、`集群协议字段速览.md`、`总索引.md` **集群 / Tier III** 已有编号为准；本课新引用的条款——6.4.9、6.4.10、6.5、6.6.4、6.6.8、7.1.1.1.6–8、7.1.1.2.1–4、7.2.8、7.2.12、Table 6.19–6.26、6.33、6.55、6.66–6.71、7.22–7.28、7.41、7.49、7.50、B.1、B.8、Part 1 8.2.1.8 / 8.2.2.5——都已在 PDF `TS102361-4_V1.12.1.pdf` 和 `TS102361-1_V2.7.1.pdf` 原文里逐条核对过）。**鉴权算法本身（RC4、K、PSN）第 35 课已讲透，本课只回唤流程**。**厂商菜单名（「遥晕」「遥毙」「动态重组」）和平台显示以厂商说明书为准**。

---

## 2. 总图：控制信道上的三件「管理工具」

先把三件事放在一张图上。它们都发生在 **TSCC（控制信道）** 上，都不需要业务信道：

```text
                          ┌──────────────────── 控制信道 TSCC（一个 30 ms 时隙接一个） ────────────────────┐
                          │                                                                               │
  ① Stun / Revive / Kill  │  TSCC ──C_AHOY(Source=STUNI/KILLI, Flag)──► MS                                 │
     单块命令              │  MS   ──C_ACKU / C_NACKU──────────────────► TSCC        （无鉴权：2 步）        │
     （网关发起）           │       或 C_ACKVIT 出题 → C_ACKD 交卷 → C_ACKU/C_NACKU 判卷（带鉴权：4 步）       │
                          │                                                                               │
  ② UDT 统一数据传送        │  MS(A) ──C_RAND(Target=对方/网关, 要几块)──► TSCC                              │
     多块运输              │  TSCC  ──C_AHOY(Source=SDMI/SUPLI/PSTNI…)──► MS(A)   「把货交上来」             │
     （短信/定位/号码/IP…）  │  MS(A) ──UDT 头 + 附块 ×1…4（上行）────────► TSCC                              │
                          │  TSCC  ──UDT 头 + 附块 ×1…4（下行）────────► MS(B) / 组                         │
                          │  MS(B) ──C_ACKU──► TSCC ──C_ACKD（镜像）──► MS(A)     （组呼没有 MS(B) 回执）     │
                          │                                                                               │
  ③ DGNA 动态组号分配        │  MS(A) ──C_RAND(Target=DGNAI)──► TSCC ──C_AHOY(Source=DGNAI)──► MS(A)          │
     UDT 的一项专门业务      │  MS(A) ──C_DGNAHU + 组号附块──► TSCC ──C_DGNAHD + 组号附块──► MS(B)              │
     （网关发起时只有下行）    │  MS(B) ──C_ACKU(MS_Accepted)──► TSCC ──C_ACKD(镜像)──► MS(A)                   │
                          └───────────────────────────────────────────────────────────────────────────────┘
```

再用一张表把三者的「身份证」并排放：

| | **Stun / Revive** | **Kill** | **UDT 短数据** | **DGNA** |
|---|---|---|---|---|
| 条款 | 6.4.9 | 6.4.10 | 6.5、6.6.4 | 6.6.8 |
| 网关地址 | **STUNI** `FFFECC` | **KILLI** `FFFECF` | **SDMI** `FFFEC5`（补充数据用 **SUPLI** `FFFEC4`） | **DGNAI** `FFFED6` |
| Service_Kind | `1101` 补充业务 | `1101` 补充业务 | `0100` 个号短数据 / `0101` 组短数据 | `1101` 补充业务 |
| 谁发起 | 只能从 TSCC 网关 | 只能从 TSCC 网关 | MS 或网关 | MS 或网关 |
| 对象 | 只对个号 | 只对个号 | 个号、组、网关、全呼 | 只对个号 |
| PDU 形态 | 单块 CSBK | 单块 CSBK | 多块 UDT（1 头 + 1…4 附块） | 多块 UDT（专用 Opcode） |
| 鉴权 | 可选（手台决定挑不挑战） | **必须** | 可在 C_RAND 后被网络鉴权 | 可在 C_RAND 后被网络鉴权 |
| 可逆吗 | Revive 可逆 | **空口不可逆** | — | 下次 DGNA 可改 / 可删 |

一个记忆窍门：**Service_Kind = `1101`（补充业务）本身不说明是什么业务，真正说明「这是 Stun 还是 Kill 还是 DGNA」的是那个网关地址**（Table 7.49 NOTE：*The purpose is further defined by the Gateway ID defined in that PDU*）。所以解码器上看补充业务，**先看 Source / Target 里那个 `FFFExx`**。

把它放回整个阶段 E 的大图里：

```text
开机 → 猎站（第37课）→ 登记（第32课）→ 守控制信道
   │
   ├── 用户发起：拨号（第38课）→ C_RAND → Grant（第33课）→ 业务信道（第36课 CHAN）
   │                       └→ 短信 / 定位 / 外线号码：UDT（本课 §5）
   │
   └── 网络发起（本课）：
         · C_AHOY(STUNI/KILLI) → 冻结 / 解冻 / 永久废掉（§4）
         · C_DGNAHD → 空中改组（§6）
         · C_UDTHD  → 下发短信、来电号码 CLI、系统消息（§5）
         以上都可能夹一段鉴权（第35课）、都用 Reason 回执（第34课）
```

---

## 3. 先打地基：三件事共用的骨架

三件事的 PDU 你其实都见过，只是这一课换了「填法」。先把四个零件复习到能手拼的程度。

### 3.1 CSBK 头两个字节：Octet 0 / Octet 1

所有控制信道 CSBK 的头两个字节都一样（Table 7.22 等，来自 Part 1 的 LC 结构）：

```text
Octet 0:  LB(1) | PF(1) | CSBKO(6)        LB=1 单块（或多块的最后一块）；PF=0
Octet 1:  FID(8)                          标准业务 = 0x00
```

本课用到的 Opcode（Table B.1，已核对）：

| CSBKO 十进制 | 二进制 | 名字 | 方向 | Octet 0（LB=1, PF=0） |
|---|---|---|---|---|
| 28 | `01 1100` | **C_AHOY** | TSCC → MS | `0x9C` |
| 30 | `01 1110` | **C_ACKVIT** | MS → TSCC | `0x9E` |
| 31 | `01 1111` | **C_RAND** | MS → TSCC | `0x9F` |
| 32 | `10 0000` | **C_ACKD**（含 NACKD / QACKD / WACKD） | TSCC → MS | `0xA0` |
| 33 | `10 0001` | **C_ACKU**（含 NACKU） | MS → TSCC | `0xA1` |
| 26 | `01 1010` | **C_UDTHD** UDT 下行头 | TSCC → MS | 见 §5（头块格式不同） |
| 27 | `01 1011` | **C_UDTHU** UDT 上行头 | MS → TSCC | 见 §5 |
| 36 | `10 0100` | **C_DGNAHD** DGNA 下行头 | TSCC → MS | 见 §6 |
| 37 | `10 0101` | **C_DGNAHU** DGNA 上行头 | MS → TSCC | 见 §6 |

注意第 34 课讲过：**ACK 和 NACK 用同一个 Opcode**，区别在 Reason 的最高两位 `tt`（`01`=ACK，`00`=NACK，`10`=QACK，`11`=WACK）。所以 C_NACKU 的 Octet 0 也是 `0xA1`。

### 3.2 C_AHOY 的 8 字节「信息区」（Table 7.22）

```text
Octet 2:  Service_Options_Mirror(7) | Service_Kind_Flag(1)
Octet 3:  ALS(1) | G/I(1) | Appended_Blocks(2) | Service_Kind(4)
Octet 4–6: Target address (24)        被点名的那一方
Octet 7–9: Source Address or Gateway (24)    谁在点名：主叫个号 / 网关 / 鉴权题目
```

C_AHOY 是网络的「点名」：**「Target 那位，Source 这位找你，事由是 Service_Kind」**。本课它出现在三个场合：

| 场合 | Source 填 | Service_Kind | 意思 |
|---|---|---|---|
| Stun / Revive | STUNI `FFFECC` | `1101` | 「我要晕你 / 解你」 |
| Kill | KILLI `FFFECF` | `1101` | 「我要废你」 |
| 要短信上传 | SDMI `FFFEC5` | `0100` | 「把你的短信交上来」 |
| 要补充数据上传 | SUPLI `FFFEC4` | `0100` | 「把附带数据交上来」 |
| 要外线号码（第 38 课） | PSTNI / PABXI / LINEI / DISPATI / IPI | `0100` | 「把号码 / IP 交上来」 |
| 要 DGNA 组号上传 | DGNAI `FFFED6` | `1101` | 「把你要分配的组号交上来」 |
| 鉴权（第 35 课） | **题目 RAND**（不是网关） | 依业务 | 「先答题」 |

### 3.3 Reason 码：8 bit = `tt d aaaaa`（7.2.8，第 34 课）

```text
tt  ACK 类型：00 NACK · 01 ACK · 10 QACK · 11 WACK
d   方向：1 = TS 发给 MS；0 = MS 发给 TS，或 TS 镜像 MS 的回执
aaaaa 原因
```

本课要用的 6 个码（全部在资料库 `ReasonCode与Grant变体.md` 里，已对过 PDF）：

| 名字 | 二进制 | 十六进制 | tt / d | 谁发 | 本课用在哪 |
|---|---|---|---|---|---|
| **MS_Accepted** | `0100 0100` | `0x44` | ACK / MS→TS | 手台 | Stun/Kill 鉴权通过后执行；个号短信、DGNA 收妥 |
| **Message_Accepted** | `0110 0000` | `0x60` | ACK / TS→MS | 网络 | 组短信的最终确认 |
| **Authentication Response** | `0110 0100` | `0x64` | ACK / TS→MS | 网络 | 反向鉴权：网络交卷 |
| **Recipient_Refused** | `0001 0100` | `0x14` | NACK / MS→TS | 手台 | 反向鉴权失败，拒绝执行 |
| **MSNot_Supported** | `0000 0000` | `0x00` | NACK / MS→TS | 手台 | 手台不支持 Stun/Kill |
| （镜像） | 同 MS 原码 | — | d=0 | 网络 | C_ACKD(Mirrored_Reason = MS_Accepted) 给主叫 |

> 读码小技巧：`0x44` 拆开是 `01 0 00100`——ACK、方向 MS→TS、原因 4；`0x60` 是 `01 1 00000`——ACK、方向 TS→MS、原因 0。**同样是「接受」，看 `d` 位就知道是手台说的还是网络说的。**

### 3.4 回执 PDU 的字节落点（Table 7.23 / 7.27）

```text
Octet 2:  Response_Info(7) | Reason 的最高位
Octet 3:  Reason 的低 7 位 | Reserved(1)=0
Octet 4–6: Target address (24)
Octet 7–9: Additional Information / Source Address (24)
```

因为 Reason 跨了两个字节，**Octet 3 = (Reason × 2) 的低 8 位**（Reserved 恰好在最低位）。所以：`0x44 → Octet 3 = 0x88`；`0x14 → 0x28`；`0x64 → 0xC8`；`0x60 → 0xC0`。Response_Info 对本课这些码是「G/I(1) + Response_Check(6)」（Table 7.41），Response_Check 取自 C_SYScode 的 NET+SITE 低 6 位。**下面手拼时为讲解方便假设 Response_Info = 0**（和第 35 课一样），真实抓包里 Octet 2 会随站点变化。

### 3.5 本课的示例人物（沿用第 38 课的 NP 401 网）

| 角色 | 用户号码 | 空口地址 | 十进制 |
|---|---|---|---|
| 班长手台 MS(A) | `40125312` | `0x348E1D` | 3 444 253 |
| 队员手台 MS(B)（就是那台「丢了」的） | `40125318` | `0x348E23` | 3 444 259 |
| 3 号门临时组 | `40125934` | `0x348217` | 3 441 175 |
| 4 号门临时组 | `40125935` | `0x348218` | 3 441 176 |

（组号 `40125934`：FGN 25、GN 934 → SGI = (25−20)×100 + (934−900) + 1 = 535 = `0x217`，NAI 105 → `0x348000 + 0x217 = 0x348217`；`40125935` 再加 1。算法见第 38 课 §6。）

---

## 4. Stun / Revive / Kill：网络对一台手台的「冻结」与「废除」

### 4.1 三个动作分别做了什么（6.4.9.0 / 6.4.10.0）

先用白话：

- **Stun（遥晕）**：像把员工的门禁卡**临时冻结**。人还在公司名册上，网络还认识他（还能登记、被定位），但**他不能叫别人，别人叫他也叫不到**——在执行 Stun 的这个网上。  
- **Revive（遥醒 / 解冻）**：把冻结撤销，一切照旧。  
- **Kill（遥毙）**：把门禁卡**剪碎**。手台**永久失去全部 DMR 功能**，**任何空口消息都不能把它救回来**。

规范原文要点（逐句核对过）：

| 动作 | 原文要点 | 白话 |
|---|---|---|
| Stun | *the MS may not request nor receive any user initiated services on the network that performed the procedure* | 在**执行 Stun 的那个网**上，不能发起也不能接收**用户发起的**业务（个呼、组呼、短信……） |
| Stun | *However hunting and registration, authentication, stun/revive and registration services shall remain active* | 但**猎站、登记、鉴权、Stun/Revive** 必须继续工作 |
| Stun | *While an MS is stunned, it shall retain and provide access to MS location services* | **被晕期间必须保留定位业务**——这正是找回丢失手台的关键 |
| Stun/Revive | *MS shall only be stunned/revived from a TSCC gateway STUNI* | 只能从网关 STUNI 发起，不能由另一台手台直接晕 |
| Kill | *the MS shall lose all DMR functionality. An MS may not be revived from the kill state by any AI generated message* | 全部 DMR 功能丢失；**空口（AI = Air Interface）发什么都救不回来** |
| Kill | *MS shall only be killed from a TSCC gateway KILLI* | 只能从网关 KILLI 发起 |

为什么 Stun 要保留「猎站、登记、鉴权、定位」？想一想丢手台的场景就明白了：

```text
手台丢了 ──► 网管 Stun（不让捡到的人用它乱呼、偷听组呼）
          ──► 手台仍会猎站、登记 ──► 网络知道它在哪个站
          ──► 定位业务仍可用 ──► 调度轮询它的 GPS 位置（USBD / LIP，§7）
          ──► 找回来 ──► Revive，原样归还
          ──► 确认找不回 / 已落入不法之手 ──► Kill（不可逆）
```

如果 Stun 把手台变成「完全关机」，网络就再也找不到它，也没法对它发 Revive 或 Kill 了。**Stun 是「可控的冻结」，不是「关机」。**

两个规范**没写**、现场常问的问题，诚实说明：

- **手台被晕后屏幕显示什么、能不能听到组呼的声音**：规范只说「不能接收用户发起的业务」，界面表现**由厂商实现**。  
- **掉电重启后是否仍保持被晕状态**：6.4.9 没有写。看厂商说明书（本课第 6 条视频里讲的模拟手台「掉电后仍保持」是模拟信令时代的常见做法，**不能直接套到 DMR Tier III 上**）。

### 4.2 三条 C_AHOY 的字段（Table 6.19 / 6.23）

| 字段 | 长度 | Stun | Revive | Kill |
|---|---|---|---|---|
| Service_Options_Mirror | 7 | `000 0000` | `000 0000` | `000 0000` |
| **Service_Kind_Flag** | 1 | **`0`** | **`1`** | `0`（不适用） |
| Ambient Listening Service | 1 | `0` | `0` | `0` |
| G/I | 1 | `0` 个号 | `0` | `0` |
| Appended_Blocks | 2 | `00` | `00` | `00` |
| Service_Kind | 4 | `1101` | `1101` | `1101` |
| Target address | 24 | 被晕的个号 | 被解的个号 | 被毙的个号 |
| **Source Address or Gateway** | 24 | **STUNI** | **STUNI** | **KILLI** |

Service_Kind_Flag 的含义由 Service_Kind 决定（Table 7.50）：对 `1101` 的 Stun/Revive，`0` = Stun、`1` = Revive；对 Kill 和 DGNA，固定 `0`（不适用）。

### 4.3 手拼：对队员手台 `0x348E23` 发 Stun / Revive / Kill

逐字节拼：

```text
Octet 0  = LB 1 | PF 0 | CSBKO 011100        = 1001 1100 = 0x9C   （C_AHOY）
Octet 1  = FID                               = 0x00
Octet 2  = SOM 0000000 | Flag                = 0x00（Stun） / 0x01（Revive） / 0x00（Kill）
Octet 3  = ALS 0 | G/I 0 | AB 00 | SK 1101   = 0000 1101 = 0x0D
Octet 4–6 = Target                           = 34 8E 23
Octet 7–9 = Source（网关）                     = FF FE CC（STUNI） / FF FE CF（KILLI）
```

三条并排：

```text
Stun   : 9C 00 00 0D 34 8E 23 FF FE CC
Revive : 9C 00 01 0D 34 8E 23 FF FE CC
Kill   : 9C 00 00 0D 34 8E 23 FF FE CF
              ↑↑                    ↑↑
          Flag 位不同          网关最后一个字节不同
```

**这就是本课的第一个「顿悟点」：Stun 和 Revive 只差 1 个比特；Stun 和 Kill 只差 Source 的最后 2 个比特（`CC` → `CF`）。**一个是可逆的冻结，一个是不可逆的废除，在空口上却几乎长得一样。这正是为什么规范要求 **Kill 必须鉴权**——如果谁都能伪造这 10 个字节，假基站就能把一批手台变砖（第 35 课 §1 讲过这个风险）。

解码器上怎么一眼认出来：

| 你看到 | 判断 |
|---|---|
| CSBKO 28、Service_Kind `1101`、Source `FFFECC`、Octet 2 = `00` | Stun |
| 同上，Octet 2 = `01` | Revive |
| CSBKO 28、Service_Kind `1101`、Source `FFFECF` | **Kill**——立刻关注，看后面有没有 C_ACKVIT / C_ACKD 鉴权 |
| CSBKO 28、Service_Kind `1101`、Source `FFFED6` | DGNA 相关（§6） |

### 4.4 流程：无鉴权 2 步，带鉴权 4 步（Fig 6.31–6.33）

**无鉴权 Stun / Revive（Fig 6.31）**：

```text
  A：TSCC ──C_AHOY(Source=STUNI, Flag=0/1)──► MS
  B：MS   ──C_ACKU(Reason=0x44)──────────────► TSCC      支持并已执行
       或 ──C_NACKU(Reason=MSNot_Supported 0x00)──►       不支持 Stun/Revive
```

**带鉴权 Stun / Revive（Fig 6.32）和 Kill（Fig 6.33，Source=KILLI）**：

```text
  A：TSCC ──C_AHOY(STUNI 或 KILLI)──────────────────► MS
  B：MS   ──C_ACKVIT(Target=手台出的题, Source=本机)──► TSCC   既是「收到 A」，又是「请先答题」
  C：TSCC ──C_ACKD(Reason=0x64, AddInfo=网络的答案)──► MS
  D：MS   ──C_ACKU(Reason=MS_Accepted 0x44)─────────► TSCC   答对了，执行
       或 ──C_NACKU(Reason=Recipient_Refused 0x14)──►          答错了，不执行，状态不变
```

这就是第 35 课讲的「**反向鉴权**」：平常是网络考手台（登记时），这里是**手台考网络**——「你真有权冻我 / 废我吗？」。算法和第 35 课完全一样（RC4、K、可选 PSN），只是出题人和答题人对调了。

几条容易忽略的细节：

1. **C_ACKVIT 的 Target 是题目，不是地址。**题目范围 `00 0000`…`FF FCDF`（Table 6.21）。`FF FCDF` 是多少？**16 776 415**——正是第 38 课 Annex G 里个号的最大值。也就是说题目被限制在普通个号的数值范围内，不会落进 `FFFCE0` 以上的网关 / 特殊地址段（规范只给了范围，没写理由；可以理解为避免题目被误读成某个网关地址）。  
2. **Stun/Revive 的鉴权是可选的**：手台收到 STUNI 的 C_AHOY，**挑不挑战由手台实现决定**。**Kill 没有无鉴权变体。**  
3. **网络可以重发 C**：如果 D 没收到，TSCC 可以重复步骤 C（6.4.9.2.0）；Kill 场景下手台也可以重复步骤 B（6.4.10.0）。  
4. **支持不支持，一律先回答**：手台不支持该特性时回 `C_NACKU(MSNot_Supported 0x00)`，不做 Stun/Kill（6.4.9.1.2 / 6.4.10.2）。

### 4.5 手拼：带鉴权 Stun 的四个 PDU

沿用第 35 课的官方测试题 `7A17C0`，假设手台出的就是这道题（**示例**）。网络的答案记作 `RRRRRR`（24 bit，算法见第 35 课 §5；本课不重复计算）。Response_Info 假设为 0。

```text
A  C_AHOY  (TSCC→MS) : 9C 00 00 0D  34 8E 23  FF FE CC
                       AHOY  Stun  SK=1101  Target=队员  Source=STUNI

B  C_ACKVIT(MS→TSCC) : 9E 00 00 0D  7A 17 C0  34 8E 23
                       ACKVIT Flag=0(Stun) Res|AB|SK=1101  Target=题目  Source=队员本机

C  C_ACKD  (TSCC→MS) : A0 00 00 C8  34 8E 23  RR RR RR
                       ACKD  RI=0  Reason 0x64→Oct3=C8  Target=队员  AddInfo=网络的答案

D  C_ACKU  (MS→TSCC) : A1 00 00 88  FF FE CC  34 8E 23     ← 答对：MS_Accepted 0x44
   C_NACKU (MS→TSCC) : A1 00 00 28  FF FE CC  34 8E 23     ← 答错：Recipient_Refused 0x14
                       ACKU  RI=0  Reason       Target=STUNI  AddInfo=队员本机
```

C_ACKVIT 的 Octet 3 拆开：`Reserved 00 | Appended_Blocks 00 | Service_Kind 1101` = `0x0D`（Table 7.26）——和 C_AHOY 的 Octet 3 恰好同值，因为 ALS、G/I 这两位在 C_ACKVIT 里变成了 Reserved，都是 0。

看最终回执 D 的 **Target = STUNI**：Table 6.22 规定手台回执的 Target 填「对方 PDU 的 Source」（Table 7.27 也这么说），也就是网关 STUNI（Kill 时填 KILLI）。**所以在解码器上，看到「Target = FFFECC 的 C_ACKU」，就是某台手台在回应遥晕；它的 Additional Information 就是那台手台的个号。**

### 4.6 规范里一处用词不一致（诚实说明）

6.4.9 的散文里，无鉴权和带鉴权的最终回执都写作 `C_ACKU(Reason = Message_Accepted)`；可 Table 6.22 / 6.26 写的是 **`MS_Accepted = 0100 0100₂`**；6.4.9.2.0 第 c 步甚至写成 `C_ACKU(Reason = Authentication_Response)`，紧接着第 d 步又改回 Message_Accepted。**而 Message_Accepted 的码值是 `0x60`，`d` 位 = 1 表示「网络发给手台」，手台发 `0x60` 在方向上是矛盾的。**

实际怎么办：**以表格和码值为准——手台回 `0x44` MS_Accepted**（资料库 `Stun_DGNA_UDT与定时器.md` §1.3 也是这么处理的）。做测试仪或网管解析时，**两个值都要能认**，免得某家厂商按散文实现、你的工具就误报。

### 4.7 Kill 的「不归路」：最后一个 ACK 丢了怎么办

Kill 有一个 Stun 没有的坑（6.4.10.0 NOTE，原文核对过）：

```text
  D：MS ──C_ACKU(0x44)──X（丢了）       手台已经执行 Kill，关掉全部 DMR 功能
     TSCC：没收到 D，以为没成功
  A'：TSCC ──C_AHOY(KILLI)──► MS        重发
     MS：已经是砖了，没有任何回应
     TSCC：「手台不在线？」
```

规范的原话是 *The TSCC should be able to deal with this situation*——**网络要能处理这种情况**，但没规定怎么处理。现场的理解应该是：

- **Kill 后「再发无响应」不等于「Kill 失败」**，很可能恰恰说明成功了。  
- 网管平台应当把「已发 Kill、C 已发出、D 未收到、之后再无响应」标记为「**疑似已执行**」，而不是自动无限重发。  
- 想确认，可以看这台手台**之后是否再出现登记**（Kill 后它不会再猎站登记；Stun 后它会）。

### 4.8 Stun / Kill 的现场管理建议

这些不是规范条款，而是从规范的设计推出来的操作原则：

| 原则 | 原因（规范依据） |
|---|---|
| **先 Stun，后 Kill** | Stun 可逆、保留定位（6.4.9.0），可以先控制风险再找回；Kill 空口不可逆（6.4.10.0） |
| Kill 前**核对对象个号两遍** | 字节上 Stun/Kill 只差 2 bit，个号输错一位就废掉了别人的手台 |
| Kill 前**确认该手台的 K 在网络侧正确** | Kill 必须鉴权；K 不对只会得到 `0x14`，反复重发没有意义 |
| 平台记录每一步 PDU 的收发 | D 丢失时要靠记录判断「疑似已执行」（§4.7） |
| 不要把 Stun 当「禁言」长期使用 | Stun 期间手台不能接收用户业务，**紧急情况下也叫不到它**；限制个别业务应该用业务权限，而不是 Stun |
| 收到 `0x00` MSNot_Supported 就停 | 手台根本不支持，重发无用；换管理手段（收回、写频禁用） |

---
