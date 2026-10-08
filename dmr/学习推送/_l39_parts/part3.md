
---

## 9. DGNA：空中给手台「发一张新的组号清单」

### 9.1 是什么（6.6.8.0）

> MS 可以持有一个或多个组号，这些组号可以**预先写频**，也可以**用 DMR UDT 动态增加 / 删除**。**一台 MS 最多可被分配 16 个 DGNA 地址。**DGNA 业务**只能指向个人 MS**。过程可以由 **MS 或网关**发起。

翻成现场话：**写频写死的组不动；在它之外，网络还可以临时给手台最多 16 个「动态组」。**典型用途是 DMR 协会资料（外链 2）里举的：**用一个临时组替换当前组**（抢险、大型活动临时编组），或者**一次加多个组**（资料说有的厂商用在交通行业）。

### 9.2 两种模式，一共 16 个

| | **DGNA_Address 模式** | **DGNA_Alias 模式** |
|---|---|---|
| UDT_Format | `0001`（地址） | `1010`（混合：1 地址 + 文字） |
| 一次能给 | 最多 **15 个**组号 | **1 个**组号 + 最多 **21 个字**的名字（UTF-16BE） |
| 存在手台哪 | 动态组清单 ADDRESS1~15 | 第 16 个（只有 Alias 模式能写） |
| 另一个用途 | — | 给 ADDRESS1~15 里**已下发的某个组补一个名字** |
| Pad Nibble | 固定 0 | 查 Table B.9（第 1 节放完 OK + 地址后只剩 3 个字的位置：3 / 9 / 15 / 21 字对应 1~4 节） |

6.6.8.1.2 的结论：**15 个（Address 模式）+ 1 个（Alias 模式）= 16 个动态组，每个都可以配一个最多 21 个字的名字。**

Address 模式的车厢数和组数（Table 6.67、B.3.2）：

| UAB | 车厢 | 能装的组号 | 怎么排 |
|---|---|---|---|
| `00` | 1 | ADDRESS1~3 | 第 1 节：`RSVD(7) OK(1)` + 3 个 24 位地址 = 10 字节 |
| `01` | 2 | ADDRESS1~7 | 第 1 节 12 字节，**ADDRESS4 跨节**（前 16 bit 在第 1 节，后 8 bit 在第 2 节，Fig B.7） |
| `10` | 3 | ADDRESS1~11 | 依此类推 |
| `11` | 4 | ADDRESS1~15 | 依此类推 |

规范还提醒：如果发送方用了不到 4 节，**动态组清单里不是每一格都「够得着」**（6.6.8.1.1）。比如只发 1 节，就只写了 ADDRESS1~3。

### 9.3 三条最容易踩的规则

1. **整表替换，不是追加。**原文：*the existing list of talkgroups ADDRESS1 to ADDRESS15 held by the MS shall be deleted and replaced*。手台收到一次成功的 Address 模式下发，**先清空原来的 15 格**，再写新的；没用到的格填 **ADRNULL `000000`**。→ §1 里「巡逻 3 组不见了」就是这么来的。想「追加」，就要**把旧组和新组一起重发**。  
2. **一键组（One-key_talkgroup）。**一台手台最多一个一键组，特点是「**按快捷键、甚至直接按 PTT 就能呼叫**」（6.6.8.0）。第 1 节车厢第一个字节的最低位 **OK = 1** 时，**ADDRESS1**（Address 模式）或 **ADDRESS**（Alias 模式）成为一键组；Alias 模式下 **OK = 0 不改变原来的一键组**（6.6.8.1.2）。临时编组时把临时组设成一键组，队员拿起来一按 PTT 就是它——这是 DGNA 在现场最实用的一点。  
3. **怎么删。**清空全部 15 个：发 1 节、OK = 0、ADDRESS1~3 = ADRNULL（6.6.8.1.1 最后一句）。删第 16 个：用 Alias 模式发 ADDRESS = ADRNULL、OK = 0、Pad Nibble = 0、UAB = `00`、文字全 0（6.6.8.1.2）。

### 9.4 流程：手台发起 vs 网关发起（Fig 6.67）

```text
手台发起（例：班长手台 S 给队员手台 M 派组）
  S ──① C_RAND  Target=DGNAI  SK=1101  SUPED_VAL=节数−1 ───────────► TSCC   （被叫 M 此时还不出现！）
  S ◄─② C_AHOY  Source=DGNAI  Target=S  AB=同 SUPED_VAL ─────────── TSCC   （请交货）
  S ──③ C_DGNAHU 头（Target=M, Source=S）+ 附加块（组号清单）───────► TSCC   上传段
  M ◄─④ C_DGNAHD 头（Target=M, Source=S）+ 附加块（照抄上传的清单）── TSCC   下载段
  M ──⑤ C_ACKU  Reason=0x44 MS_Accepted ─────────────────────────► TSCC
  S ◄─⑥ C_ACKD  Mirrored_Reason=0x44 ───────────────────────────── TSCC   （可重复发以提高可靠性）

网关 / 调度台发起：只有 ④⑤（6.6.8.0：*only the UDT outbound phase is applicable*）
```

和短信比，最大的不同在 ①：**短信的 C_RAND 里直接写被叫；DGNA 的 C_RAND 里 Target 是 DGNAI，被叫 M 要等上传段的 UDT 头才告诉 TSCC**（6.6.8.3.1）。另外 DGNA 用 **SUPED_VAL** 报节数（Table 6.70：SDATA_VAL 固定 `00`），短信用 **SDATA_VAL**。TSCC 对 ① 的合法回应还包括 C_NACKD / C_QACKD / C_WACKD 和**鉴权用的 C_AHOY（Source = 题目）**（6.6.8.2.1）。主叫等待用 **TNP_Timer**（Table A.1：2…60 s），超时就放弃（6.6.8.3.5）。

### 9.5 手拼一次 DGNA：给 M 派 4 个组，第一个设为一键组

S = `40125312`（`0x348E1D`），M = `40125318`（`0x348E23`）。要派的 4 个组（按第 38 课 §6 公式算，Python 核对）：`40125934` = `0x348217`（设为一键组）、`40125935` = `0x348218`、`40125936` = `0x348219`、`40126900` = `0x348259`。4 个组 > 3，**要 2 节**（能装 7 个，剩 3 格填 ADRNULL）→ UAB = SUPED_VAL = `01`。

```text
① C_RAND   9F 00 00 4D FF FE D6 34 8E 1D
                    └ SUPED_VAL=01 SDATA_VAL=00 SK=1101 → 0100 1101 = 0x4D；Target=DGNAI
② C_AHOY   9C 00 00 1D 34 8E 1D FF FE D6
                    └ ALS=0 G/I=0 AB=01 SK=1101 → 0001 1101 = 0x1D；Source=DGNAI
③ C_DGNAHU 头：40 01 34 8E 23 34 8E 1D 01 25
               │  │  └Target=M┘ └Source=S┘ │  └ SF=0 PF=0 Opcode=100101 → 0x25
               │  │                         └ Pad=00000 | 0 | UAB=01 → 0x01
               │  └ SAP=0000 | UDT_Format=0001（地址）→ 0x01
               └ G/I=0 A=1 Rsvd=0 UDT_DIV=0 | DPF=0000 → 0x40
   第 1 节（12 字节）：01 | 34 82 17 | 34 82 18 | 34 82 19 | 34 82
                       └ RSVD=0000000 OK=1   └ADDRESS1~3┘        └ADDRESS4 前 16 bit
   第 2 节（10 字节）：59 | 00 00 00 | 00 00 00 | 00 00 00
                       └ADDRESS4 后 8 bit └── ADDRESS5~7 = ADRNULL ──┘
④ C_DGNAHD 头：40 01 34 8E 23 34 8E 1D 01 24   ← 只有 Opcode 变成 100100（0x24）；两节车厢照抄
⑤ C_ACKU   A1 00 00 88 34 8E 1D 34 8E 23        （M 回 0x44）
⑥ C_ACKD   A0 00 00 88 34 8E 1D ·· ·· ··        （镜像给 S；AddInfo 按 Table 7.23 是「请求的目的地或网关」，
                                                  DGNA 请求的 Target 是 DGNAI、实际被叫是 M，规范没逐字规定填哪个，以抓包为准）
```

M 收到后：**原来的动态组 ADDRESS1~15 全部清掉**，写入这 4 个，`40125934` 成为一键组。想给它起名「抢险1组」（4 个字），再发一次 **Alias 模式**：UDT_Format = `1010`，ADDRESS = `0x348217`，OK = 1，4 个字 → Table B.9：UAB = 1、Pad = 20。

---

## 10. 邻居们：同在控制信道上的其他「小数据」，以及三种搬数据方式

控制信道上还有几位「邻居」经常和本课内容一起出现：

| 业务 | 条款 | 怎么认 | 和 UDT 的关系 | 一句话 |
|---|---|---|---|---|
| **UDT 短数据轮询** | 6.6.5 | Service_Kind `0110` | 用 UDT 运回答（同样 ≤368 bit） | 「请把你的某份数据发给我」 |
| **状态消息** | 6.6.6 | Service_Kind `0111` | **不用 UDT**：7 位状态值塞在 C_AHOY 的 Service_Options_Mirror（高 5 位）+ Appended_Blocks（低 2 位）里（Table 7.22 NOTE 2） | 0~99 由用户自定义含义（「我到了」「请回电」），100 以上有保留和系统用途 |
| **补充用户数据** | 6.4.13 | UDT 头 SF = `1`，网关 **SUPLI** | 就是 UDT | 随一次呼叫捎带的数据（§7.3） |
| **USBD 定位轮询** | 6.6.11 | 独立单块 PDU：Poll Request / Poll Response | **不是 UDT，也不在 CSBK Opcode 表（Table B.1）里** | 一问一答各一个突发，专门批量拿位置 |

USBD 和 Stun 是一对搭档（§4.1：被 Stun 的手台必须保留定位）：网络发 **Poll Request**（最多 48 bit 参数；Service Type `0000` = Short Location Request），手台在约定的延迟后回 **Poll Response**（最多 68 bit：经纬度、速度、方向、误差……）（6.6.11.0）。应答延迟由 2 bit 的 RD 决定：aligned 时序 30 / 90 / 150 / 210 ms，offset 时序 60 / 120 / 180 / 240 ms（Table 6.76）；在 TSCC 上，TSCC 要把应答那个时隙从随机接入里**收回**（6.6.11.1）。轮询可以在 TSCC，也可以在它的**另一个时隙 TSCCAS** 上进行。DMR 协会的介绍（外链 2）说一个 30 ms 突发就能装下一份位置报告、用另一个时隙轮询每站每分钟可达约 1000 次（协会资料数据，非 ETSI 条款）。

**三种「搬数据」的方式对比**：

| | **UDT**（本课） | **USBD** | **分组数据呼叫** |
|---|---|---|---|
| 走哪 | 控制信道 TSCC | TSCC 或 TSCCAS | **业务信道**（要 Grant：PD_GRANT / TD_GRANT，第 33 课） |
| 一次多少 | 头 + 1~4 节，≤368 bit | 问 ≤48 bit / 答 ≤68 bit | 持续传，直到挂断 |
| 占多少空口 | 上传 + 下载两段，每段 2~5 个突发 | 一问一答各 1 个突发 | 占住一条业务信道 |
| 主叫等待定时器 | TNP_Timer（只用控制信道） | — | TP_Timer（需要业务信道）（Table A.1） |
| 典型 | 短信、外线号码、DGNA、NMEA | 大批量 LIP 位置 | 大数据量、IP 应用 |

一句话：**小而偶发用 UDT；小而海量（定位）用 USBD；大而连续用分组数据。**

---

## 11. 现场对照与分诊

| 现象 | 先怀疑 | 怎么查 | 涉及章节 |
|---|---|---|---|
| 远程禁用提示「终端不支持」 | 手台回 C_NACKU `0x00` MSNot_Supported | 查机型 / 固件 / 写频是否开启 Stun | §4.3 |
| Stun / Kill 回「拒绝」（Octet 3 = `0x28`） | `0x14` Recipient_Refused：手台没验证通过网络 | 核对网络侧这台终端的鉴权钥匙 K 是否与终端一致（换机、重写频后最常见）；**别反复重发** | §5.2、§5.3 |
| Stun 一直无应答 | 终端关机 / 不在覆盖 / 在业务信道上 | 查登记状态和最后位置；等它回到控制信道 | §5.5 |
| Kill 后一直「等待应答」 | 可能已经执行成功，最后的 ACK 丢了（6.4.10.0 NOTE） | 查它是否还在登记；不要当失败处理 | §5.4 |
| 已 Stun 的终端仍在登记、上报位置 | **正常设计** | — | §4.1 |
| 被 Stun 的终端重启后仍不能用 | 正常：重启不恢复（厂商资料） | 发 Revive，或厂商有线编程 | §4.2 |
| 短信失败，收到 C_NACKD | 看 Reason（第 34 课）：`0x30` 上传 CRC 错、`0x24` 被叫未登记、`0x25` 被叫无响应 | 抓控制信道，看卡在上传段还是下载段 | §8 |
| 组短信「已送达」，有人没收到 | `0x60` Message_Accepted 只代表网络已发出 | 确认那台当时是否在控制信道上 | §8.4 |
| 中文短信发不出 / 被截断 | 超过 23 个字（4 节上限） | 缩短或改用状态码 | §7.2 |
| DGNA 后原来的动态组没了 | Address 模式整表替换 | 新旧组一起重发 | §9.3 |
| DGNA 只出现了前 3 个组 | 发送端只发了 1 节（UAB = 00） | 看 UDT 头 Octet 8 的 UAB | §9.2 |
| DGNA 超时失败 | TNP_Timer 到期；中间某段没回 | 按 ①~⑥ 逐步看卡在哪 | §9.4 |
| 解码器看到 C_AHOY Source = `FFFECC` / `FFFECF` / `FFFED6` / `FFFEC5` | 分别是 Stun/Revive、Kill、DGNA、短信要货 | 再看 Octet 3 低 4 位和 Octet 2 最低位 | §3.1、§4.4 |

---

## 12. 术语表

| 术语 | 一句话 |
|---|---|
| Stun / Revive | 远程禁用 / 恢复：停用户业务，保留登记、鉴权、定位；C_AHOY(STUNI)，Flag 0/1 |
| Kill | 永久禁用：失去全部 DMR 功能，空口不可恢复；C_AHOY(KILLI)，必须鉴权 |
| STUNI / KILLI / DGNAI | `FFFECC` / `FFFECF` / `FFFED6`，Stun、Kill、DGNA 的业务标识 |
| SDMI / SUPLI | `FFFEC5` 短数据 / `FFFEC4` 补充数据，TSCC 以它们的名义「要货」 |
| C_ACKVIT | Ackvitation，手台出题验证网络（Target = 题），兼作确认 |
| Authentication Response | `0x64`（网络交卷）/ `0x48`（手台交卷） |
| MS_Accepted / Message_Accepted | `0x44` 手台收妥（或网络镜像）/ `0x60` 网络已接受 |
| Recipient_Refused / MSNot_Supported | `0x14` 拒绝（Stun/Kill 中 = 鉴权没过）/ `0x00` 不支持 |
| UDT | 统一数据传输：头 + 1~4 附加块，≤368 bit，先上传后下载 |
| C_UDTHD / C_UDTHU | UDT 下行头（26）/ 上行头（27） |
| C_DGNAHD / C_DGNAHU | DGNA 下行头（36）/ 上行头（37） |
| UAB / Pad Nibble | 附加块数 − 1 / 最后填了几个 `1111` 半字节 |
| SF | 1 = 补充数据（打下手）；0 = 用户业务本身 |
| UDT_Format | 车厢里装什么：地址 `0001`、BCD `0010`、UTF-16BE `0111`、混合 `1010`… |
| DGNA_Address / DGNA_Alias | 最多 15 个组 / 1 个组 + 21 字名字，合计 16 |
| One-key_talkgroup | 一键组，OK = 1 时 ADDRESS1（或 ADDRESS）当选，按 PTT 即呼 |
| ADRNULL | `000000`，空地址 |
| USBD | 单块数据轮询：问 48 bit / 答 68 bit，批量定位 |
| TNP_Timer / TP_Timer | 主叫等「只用控制信道」/「要业务信道」业务的定时器 |

---

## 13. 自测题（先自己做，答案在后面）

1. 解码记录里看到 `9C 00 01 0D 34 8E 1D FF FE CC`，这是什么？如果最后一个字节换成 `CF`（其余不变），合不合规范？  
2. Stun 之后终端还能做哪些事？为什么规范要保留定位？  
3. 下发 Kill 后收到 C_ACKU，Octet 3 = `0x28`。Reason 是什么？终端状态变了吗？先查什么？  
4. 6.4.9 正文写手台回 Message_Accepted，Table 6.22 写 MS_Accepted。手台的成功应答该按哪个码认？为什么？  
5. Kill 发出后一直等不到最终 ACK，可能是什么情况？依据哪一条？  
6. 一条 9 个汉字的 UTF-16BE 短信：几节车厢、UAB、Pad Nibble 各是多少？一条最多几个字？  
7. A（`0x348E1D`）给组 `0x348217` 发 1 节短数据，写出 C_RAND 的 10 个字节。主叫最后收到的 Reason 是什么，说明了什么？  
8. Address 模式要下发 5 个组：几节、UAB、Pad Nibble 各是多少？ADDRESS6、7 填什么？C_RAND 的 SUPED_VAL 填几？  
9. 一台手台已有动态组 X、Y，现在用 Address 模式只下发 Z，结果如何？想保留 X、Y 该怎么发？想一次清空全部 15 个又怎么发？  
10. 用 Alias 模式给一个组起 8 个字的名字：UAB 和 Pad Nibble 是多少？  
11. UDT、USBD、分组数据三种方式各适合什么？为什么批量定位不用 UDT？

---

### 自测答案

1. **Revive**（恢复）`40125312`：Source = STUNI、SK = `1101`、Octet 2 最低位 Flag = 1。换成 `CF` 就是 Source = KILLI 但 Flag = 1——Table 6.23 规定 Kill 的 Flag 只能是 0，**不合规范**，也说明 Kill 没有「撤销」一说。  
2. 能猎站、漫游、登记 / 注销、被鉴权、再收 Stun/Revive 命令、**提供定位**；不能发起或接收任何用户业务（6.4.9.0）。保留定位是为了让运营方能找回丢失的终端；保留登记和鉴权是为了之后还能 Revive。  
3. `0x28 >> 1` = **`0x14` Recipient_Refused**：终端没有验证通过网络的鉴权应答，**状态不变**（6.4.10.0 d)）。先核对网络侧这台终端的鉴权钥匙配置，不要反复重发。  
4. 按 **`0x44` MS_Accepted** 认。Table 7.42 里 Message_Accepted（`0x60`）属于「由 TS 发送」的一栏（d = 1），终端发出的确认在「由 MS 发送」一栏，对应 `0x44`；正文的叫法不统一，以码值为准。  
5. 终端可能已经发了 C_ACKU 并关闭了全部功能，只是 ACK 没被 TSCC 收到；此后重发不会有任何回应。依据 **6.4.10.0 的 NOTE**。  
6. 9 × 16 = 144 bit > 80 → **2 节，UAB = 1**，Pad = (176 − 144) ÷ 4 = **8**（Table B.8 ✓）。最多 **23 个字**（4 节 368 bit）。  
7. `9F 00 00 05 34 82 17 34 8E 1D`（SK = `0101` GRP_SD_SRV，SDATA_VAL = 00）。最后收到 **`0x60` Message_Accepted**：只说明网络已把短信发给这个组，**不知道有没有人收到**（6.6.4.5 c) 2)）。  
8. 1 节只能装 3 个，2 节能装 7 个 → **2 节，UAB = `01`**，Pad = **0**（地址格式固定 0）；ADDRESS6、7 填 **ADRNULL `000000`**；SUPED_VAL = **`01`**（SDATA_VAL = 00）。  
9. **X、Y 被删除**，清单只剩 Z（整表替换，6.6.8.1.1）。想保留就把 **X、Y、Z 一起发**（3 个组，1 节就够）。清空：发 1 节、**OK = 0、ADDRESS1~3 = ADRNULL**。  
10. 32 bit（RSVD + OK + 地址）+ 8 × 16 = 160 bit → **2 节，UAB = 1**，Pad = (176 − 160) ÷ 4 = **4**（Table B.9 ✓）。  
11. UDT：小而偶发（短信、外线号码、DGNA）；USBD：小而海量（批量定位，一问一答各 1 个突发）；分组数据：大而连续（要业务信道）。批量定位如果用 UDT，每次都要随机接入 + AHOY + 头 + 块的多次往返，控制信道很快被占满。

---

## 14. 加深阅读与视频

所有链接都已打开核验可达、内容对口（2026-10-08）。**不编造地址。**另检索了「DMR Stun / Kill / DGNA / UDT」相关视频：**没有**找到专讲 Stun、DGNA 或 UDT 空口流程的公开技术视频；找到一个开源 Tier III 基站实测视频（第 6 条），可以帮你建立「控制信道 + 业务信道」的直观印象。**video_found=true（通用 Tier III 实测视频，非本课专项）**。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMR 协会镜像 PDF）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - 本课唯一的权威出处：6.4.9 Stun/Revive、6.4.10 Kill、6.5 UDT、6.6.4 短数据、6.6.8 DGNA、6.6.11 USBD、Annex A.8、Annex B.3。库内副本 `dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。**怎么用**：先读 6.4.9.0、6.4.10.0、6.6.8.0 三段引言，再拿本课 §4.4、§8、§9.5 的字节对照表格核一遍。

2. **[DMR Association · DMR Feature Evolution（PDF 幻灯片）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - DMR 协会的功能演进介绍：DGNA 两种用法（替换为临时组 / 一次加多个组）、USBD 定位轮询（一个突发装一份位置、另一个时隙上每站每分钟约 1000 次）。**怎么用**：看 DGNA 和 USBD 两页，对照本课 §9.1、§10。

3. **[Tait Communications · DMR Standards Update for Tait Solutions](https://www.taitcommunications.com/en/about-us/news/2021/04/22/dmr-standards-update-for-tait-solutions)**  
   - 厂商视角：DGNA Address 模式最多动态增删 15 个组、USBD 快速轮询、原生编址（第 38 课 Annex G 的呼应）。**怎么用**：体会「标准功能」如何变成厂商宣传里的卖点。

4. **[MOTOTRBO Wiki（DJ0WH）· Radio Disable/Enable](https://cwh050.mywikis.wiki/wiki/Radio_Disable/Enable)**  
   - Capacity Max 里 Stun/Revive 和 Kill 的厂商行为：Stun 是系统范围、被 Stun 仍上报位置、重启不能恢复；Kill 必须鉴权、钥匙属于机主、建议不要用默认钥匙。**怎么用**：对照本课 §4.2、§5.4 读，分清「ETSI 规定」和「厂商实现」。

5. **[QRadioLink · Implementation of a DMR Tier III trunked radio BTS in SDR](https://qradiolink.org/DMR-tier-3-trunked-radio-BTS-software-defined-radio.html)**  
   - 一个开源、面向教育和业余无线电的 Tier III 基站实现说明：短信 / 状态消息走控制信道、正在通话的手台会错过控制信道上的消息、UDT 头与重传、DGNA 的实现方式。**怎么用**：对照 §8.4「组短信没收到」读，理解「不在控制信道上就收不到」。

6. **[Adrian M · Testing amateur radio DMR tier III trunked radio BTS（YouTube 视频）](https://www.youtube.com/watch?v=BKQUbE32vl4)**  
   - 第 5 条项目作者的实测视频（业余无线电频段）。**讲的是 Tier III 基站整体运行，不专讲 Stun / DGNA / UDT**。

**资料库入口**：`dmr/04-集群协议/Stun_DGNA_UDT与定时器.md`（§0 业务识别、§1 Stun/Kill、§2 DGNA、§3 USBD、§4–§5 UDT 头与载荷、§6 定时器与网关表）、`ReasonCode与Grant变体.md`（Reason 全表）、`鉴权与AnnexC频率.md`（K / RC4）、`集群协议字段速览.md`、`总索引.md` 集群 / Tier III。

---

## 本课收束

阶段 E 第九站：**控制信道上的「管理」与「搬运」。**  
底座：Service_Kind 说大类（`1101` 补充业务 / `0100`·`0101` 短数据），网关地址说具体业务（STUNI `FFFECC`、KILLI `FFFECF`、DGNAI `FFFED6`、SDMI `FFFEC5`）。  
Stun / Revive：C_AHOY(STUNI) Flag 0/1；停用户业务，保留登记、鉴权、定位；只在执行它的网络上生效。  
Kill：C_AHOY(KILLI)，必须先过「手台考网络」（C_ACKVIT → C_ACKD `0x64` → `0x44` / `0x14`）；空口不可恢复；最后的 ACK 可能丢。  
UDT：头 + 1~4 节，80 / 176 / 272 / 368 bit；UDT_Format 说装什么，Pad Nibble 说填了几个 F；先上传再下载，个人回 ACK 并镜像，组不回。  
DGNA：Address 模式 15 个（整表替换）+ Alias 模式 1 个 = 16；OK 位定一键组；网关发起只有下载段。  
下一站：**第 40 课 · 总复习 + 岗位深挖路线**——把 39 课串成一张「从 4FSK 符号到集群业务」的总地图，按网优、运维、测试、开发等不同岗位，给出下一步该精读的规范章节、该练的工具和该做的实验。
