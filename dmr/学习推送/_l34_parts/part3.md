
---

## 11. 现场分诊表（五步）

| 步 | 问题 | 怎么看 | 看错的典型后果 |
|----|------|--------|----------------|
| ① | 这是不是回条？ | CSBKO = 32/33（TSCC）或 34/35（Payload），FID=0 | 在 Grant/Aloha/Ahoy 里找理由栏，找不到就说「没原因」 |
| ② | 拼对 8 位了吗？ | 软件已拼好就直接用；只有原始字节时按 §3.3：`(Oct2&1)<<7 \| (Oct3>>1)` | `2A 4E` 念成 Reg_Refused（其实是 SYSbusy） |
| ③ | 完了没？ | tt：`01/00` 最终；`10/11` 中间 | 把 QACK 当失败，让用户狂按 PTT |
| ④ | 谁的意见？ | d=1 网络；d=0 手台（CSBKO 32 + d=0 = **转述**） | 把被叫拒接报成「系统故障」 |
| ⑤ | 具体为什么、角落写了啥？ | 查 §6–§9；按 Reason 读 Response_Info（§10） | 把省电偏移当校验码 |

**按「下一步找谁」再归一次**：

| 首位 / 值 | 找谁 |
|-----------|------|
| `0x20 0x21 0x22 0x2F` | 写频/开户/权限配置 |
| `0x24 0x25 0x26 0x2E` + 手台侧 `0x0_ 0x1_` | 被叫本人 / 被叫终端 |
| `0x23 0x27 0x28 0x2C 0x31` | 网管 / 容量 / 链路 |
| `0x2A 0x2B 0x2D` | 登记与站点配置（第 32 课） |
| `0x30` | 上行信号质量（少数真要看射频的） |
| `0xA_ 0xE_` | 谁都别找——**等** |

---

## 12. 现场对照：控制器设置怎么变成 Reason

协议规定的是「回条长什么样」；**什么时候回哪种条**，很多是控制器（TSC）的配置。拿一份公开的厂商应用说明——JVCKENWOOD《DMR Tier III · KAIROS Tier III Trunking》（AN-19-0001，见 §18）——里的几项控制器设置来对照（以下为对该文档设置说明的学习向转述，具体行为以厂商为准）：

| 控制器设置（英文原名） | 文档里的意思（转述） | 你在空口上可能看到 |
|------------------------|----------------------|--------------------|
| **Timeout Audio Call Setup QACK** | 收到呼叫请求后，系统最多等多久（没收到应答）就把呼叫转入排队 | 等待超时后出现 **QACK**（排队） |
| **Audio Call Group Mode · All Start** | 多站组呼：只要有一个目的站没空信道，就整体排队，等所有站都有信道才建立 | 一段时间的 **QACK `0xA0`**，然后才 Grant |
| **Audio Call Group Mode · Fast Start** | 有信道的站先建立，忙的站有信道后再加入 | 先 Grant；晚到的站靠迟后进入（第 33 课 Late_Entry） |
| **Talkgroup Call Collision · Deny** | 两台手台几乎同时发起同一组呼，晚一点的那台收到 NACK，再靠迟后进入进入业务信道 | 一条 **NACK**，随后靠迟后进入（可能看到 Late_Entry=1 的 TV_GRANT） |
| **Talkgroup Call Collision · Wait Late Entry** | 同样碰撞，但 TSCC 不给晚到者回 NACK，让它直接靠迟后进入 | 没有 NACK，只有 Late_Entry Grant |
| **Flooding Filter** | 同一呼叫过于频繁时，控制「回 NACK」的力度 | 用户狂按 PTT 后出现 **NACK** |

**这张表想让你记住的一件事**：同一个现场现象，「回 NACK 还是排队」「碰撞时给不给 NACK」，可以是**配置选择**。所以看见 NACK，别第一时间说「协议有问题」——先问：**控制器是怎么配的？**

（该文档没有逐条写出每种情况用哪个 Reason 值，所以上表「可能看到」只写到类别；具体值以现场抓包为准，**不要**替厂商补数字。）

### 12.1 工作例子（10 则）

**例 1 · 嘟一声就没了。** 抓到 `C_ACKD`，Reason `0x2F`。→ 首位 2 = 网络拒；`0x2F` = Called_Group_Not_Allowed。→ 这个组在本站没授权，找配置，不找射频。

**例 2 · 一直「排队中」。** Reason `0xA0`。→ 首位 A = 排队；Queued-for-resource。→ 业务信道不够或多站组呼在等（All Start）。告诉用户**别重按**；网管看话务高峰。

**例 3 · 新站一半手台登记不上。** 一部分 `0x2A`，一部分 `0x2B`。→ `2A` 可换站重试，`2B` 被本站否决、进拒绝名单。→ 重点查 `2B` 的那批：号段/授权是否没开到本站。

**例 4 · 对方开着机却「不在」。** Reason `0x25`。→ MSaway_Refused：**登记了但点名没回**。→ 对方在覆盖边缘？电量低？正在别的业务里？（若是 `0x24` 则查登记。）

**例 5 · 个呼被拒，同事说是系统故障。** 载体 CSBKO 32，Reason `0x14`。→ 首位 1 = d=0 手台意见，是**转述**；Recipient_Refused = 对方拒接。→ 不是系统故障。

**例 6 · 双工打不通、半双工能通。** 看 Reason：`0x31` → 网络双工资源不够（Duplex_Congestion，可改半双工）；`0x16` → 对方手台不支持全双工。→ 前者找网管扩资源，后者是终端能力。

**例 7 · 短消息「发成功了」但对方说没收到。** Reason `0x61` Store_Forward。→ 网络先存着，对方没登记。等对方开机登记后才投递。

**例 8 · 登记成功却收不到某些组呼。** Reason `0x65`，Response_Info `0000000₂`。→ 登记本身接受，但组列表全被拒。→ 查组附着授权（若是 `1101000₂`，则只有第 1、2、4 组被收下）。

**例 9 · 原始字节 `0B C0`。** 拼接：`(0x0B&1)<<7 = 0x80`，`0xC0>>1 = 0x60`，Reason = `0xE0` Wait。→ 中间态，还没完；**不是**「Message_Accepted 已成功」。

**例 10 · 未登记就按铃。** Aloha 的 Reg=1（第 32 课），手台跳过了登记，回条 `0x2D` MS_Not_Registered。→ 先查手台为什么没登记（开机登记被关？登记失败没处理？）。

---

## 13. 术语账本 / 口袋速查

### 13.1 白话术语表

| 术语 | 白话 | 别和谁混 |
|------|------|----------|
| **Reason Code** | 回条上的 8 位理由码 | ≠ Grant 里的任何字段（Grant 没有理由栏） |
| **tt（ACK type）** | 回条类别：NACK/ACK/QACK/WACK | ≠ CSBKO（四类共用 CSBKO 32） |
| **d（direction）** | 理由是谁的意见：1 网络，0 手台 | ≠ 这条 CSBK 本身的发送方向 |
| **aaaaa** | 5 位具体原因 | 同样的 aaaaa 在不同 tt 下意思不同 |
| **C_ACKD / C_NACKD / C_QACKD / C_WACKD** | 网络在 TSCC 上发的回条（同一 CSBKO 32） | ≠ Part2 的 NACK_Rsp（CSBKO 38，第 25 课） |
| **C_ACKU / C_NACKU** | 手台在 TSCC 上发的回条（CSBKO 33） | 入站没有排队/稍等 |
| **P_ACKD / P_ACKU** | 业务信道上的回条（34/35） | 结构与 Reason 表同 TSCC |
| **最终 / 中间** | ACK·NACK 是结论；QACK·WACK 是「还在办」 | 别把排队当失败 |
| **Mirrored_Reason** | 网络原样转述手台的理由，d 保持 0 | ≠ 系统拒绝 |
| **Response_Info** | 7 位角落备注，含义随 Reason 变 | 别脱离 Reason 单独解 |
| **Response_Check** | 6 位站点校验（系统码网号+站号部分的低 6 位） | ≠ CRC |
| **Index pattern** | 组附着结果，每位一个组 | `0000000` ≠ 登记失败 |
| **Refused vs Denied** | 拒绝（换站可试）vs 否决（别来本站） | `0x2A` vs `0x2B` |
| **Store_Forward** | 先存后投 | ≠ 对方已收到 |

### 13.2 口袋速查：最常用的 20 个值

| Hex | 名称 | 类别 · 谁 |
|-----|------|-----------|
| `0x00` | MSNot_Supported | NACK · 手台 |
| `0x14` | Recipient_Refused | NACK · 手台 |
| `0x16` | MS_Duplex_Not_Supported | NACK · 手台 |
| `0x20` | Not_Supported | NACK · 网络 |
| `0x21` | Perm_User_Refused | NACK · 网络 |
| `0x23` | Transient_Sys_Refused | NACK · 网络 |
| `0x24` | NoregMSaway_Refused | NACK · 网络 |
| `0x25` | MSaway_Refused | NACK · 网络 |
| `0x27` | SYSbusy_Refused | NACK · 网络 |
| `0x2A` | Reg_Refused | NACK · 网络 |
| `0x2B` | Reg_Denied | NACK · 网络 |
| `0x2D` | MS_Not_Registered | NACK · 网络 |
| `0x2E` | Called_Party_Busy | NACK · 网络 |
| `0x2F` | Called_Group_Not_Allowed | NACK · 网络 |
| `0x31` | Duplex_Congestion | NACK · 网络 |
| `0x44` | MS_Accepted | ACK · 手台 |
| `0x60` | Message_Accepted | ACK · 网络 |
| `0x62` | Reg_Accepted | ACK · 网络 |
| `0xA0` | Queued-for-resource | QACK · 网络 |
| `0xE0` | Wait | WACK · 网络 |

### 13.3 数字与符号账本

| 数字 | 含义 |
|------|------|
| **32 / 33 / 34 / 35** | C_ACKD / C_ACKU / P_ACKD / P_ACKU 的 CSBKO |
| **7 + 8 + 1** | Response_Info + Reason + Reserved，横跨 Octet 2–3 |
| **2 + 1 + 5** | tt + d + aaaaa |
| **38** | Part2 的 NACK_Rsp（Tier II 个呼），**不是** Tier III C_NACKD |
| **7.42 / 7.43 / 7.44 / 7.45** | ACK / NACK / QACK / WACK 表号 |
| **7.41** | Response_Info 表号 |

---

## 14. 十则误区（看见就打回）

1. 「C_ACKD 就是成功。」——**错**。CSBKO 32 装四类回条，要看 tt。  
2. 「在 Grant 里找拒绝原因。」——**错**。Grant 没有 Reason；拒绝在确认族。  
3. 「QACK 是失败。」——**错**。排队是中间态，后面多半是 Grant。  
4. 「只记后 5 位就行。」——**错**。`00000` 在四类里分别是 Not_Supported / Message_Accepted / Queued / Wait。  
5. 「Octet 3 就是 Reason。」——**错**。Reason 跨字节，最高位在 Octet 2 的最低位。  
6. 「网络发的条子，理由一定是网络的。」——**错**。d=0 是转述手台的意见（Mirrored_Reason）。  
7. 「Reason = 0x00 是空值。」——**错**。是 MSNot_Supported。  
8. 「`0x2A` 和 `0x2B` 一回事。」——**错**。Refused 可换站试；Denied 是被本站赶走。  
9. 「看见 NACK 先查天线。」——**错**。能解出清晰 Reason 说明解调没问题；先查业务/配置/容量/对方（`0x30` UDT CRC 错是少数例外）。  
10. 「Tier III 拒绝 = 第 25 课的 NACK_Rsp。」——**错**。那是 Part2 的 CSBKO 38；Tier III 是 Part4 的 CSBKO 32 + Reason。有的实现参考表把 `0x26`（=38）标成 C_NACK，读外部资料时要留意这种混写，**以 ETSI 为准**。

---

## 15. 自测题（含答案）

**题 1.** 用旅馆比喻各一句话：ACK、NACK、QACK、WACK、Mirrored_Reason。

<details><summary>答案</summary>

ACK = 「办好了」条；NACK = 「不行」条（必附理由）；QACK = 「排上队了」条；WACK = 「在办，稍等」条；Mirrored_Reason = 前台把被叫客人的原话原样转给你。

</details>

**题 2.** 哪几个 CSBKO 带 Reason？C_RAND、C_AHOY、C_ALOHA、Grant 带不带？

<details><summary>答案</summary>

32 C_ACKD、33 C_ACKU、34 P_ACKD、35 P_ACKU 带。C_RAND、C_AHOY、C_ALOHA、Grant 族都**不带**。

</details>

**题 3.** 把 `0x2D` 拆成 tt / d / aaaaa，并说出名字。

<details><summary>答案</summary>

`0010 1101` → tt=`00` NACK，d=`1` 网络，aaaaa=`01101`。MS_Not_Registered（要求先登记而你没登记）。

</details>

**题 4.** 只看首位十六进制：`0x46`、`0xA1`、`0x13`、`0x65` 各属于哪类、谁的意见？

<details><summary>答案</summary>

`0x46`：ACK · 手台（MS_ALERTING）。`0xA1`：QACK · 网络（Queued-for-busy）。`0x13`：NACK · 手台（EquipBusy_Refused）。`0x65`：ACK · 网络（Reg_Subscription/Attachment）。

</details>

**题 5.** 原始字节 `Oct2=0x2A, Oct3=0x4E`，Reason 是多少？为什么不是 `0x2A`？

<details><summary>答案</summary>

`(0x2A&1)<<7 = 0`，`0x4E>>1 = 0x27` → SYSbusy_Refused。因为 Octet 2 的高 7 位是 Response_Info，只有最低位属于 Reason。

</details>

**题 6.** `0x24` 和 `0x25` 的区别？各自先查什么？

<details><summary>答案</summary>

`0x24` NoregMSaway_Refused：被叫没登记 → 查对方是否开机/登记。`0x25` MSaway_Refused：被叫登记了但无线检查没回 → 查对方覆盖、电量、是否在别的业务里。

</details>

**题 7.** 载体是 CSBKO 32，Reason 是 `0x14`。是谁拒的？

<details><summary>答案</summary>

被叫手台拒的（Recipient_Refused），网络只是转述（Mirrored_Reason，d=0）。

</details>

**题 8.** Reason=`0x62` 和 Reason=`0x65` 时，Response_Info 分别装什么？`0x65` 配 `0000000₂` 是什么意思？

<details><summary>答案</summary>

`0x62`：PowerSave_Offset。`0x65`：Index pattern（7 个组各 1 位）。`0000000₂` = 登记可接受，但这批组列表全被拒。

</details>

**题 9.（加分）** 双工个呼失败，`0x31` 与 `0x16` 怎么区分处理？

<details><summary>答案</summary>

`0x31` Duplex_Congestion：网络双工资源不够，MS 可改半双工；找网管看资源。`0x16` MS_Duplex_Not_Supported：对方手台不支持全双工；是终端能力问题。

</details>

**题 10.（加分）** 写出现场五步分诊；并说说为什么「看见清晰的 NACK 先别查天线」。

<details><summary>答案</summary>

①认载体 CSBKO 32–35 → ②拼对 8 位 → ③判最终/中间 → ④判 d（网络/手台/转述）→ ⑤查表 + 按 Reason 读 Response_Info。能干净解出一条 Reason，说明这条下行 CSBK 解调正常；拒因是业务结论，应先查配置/权限/容量/对方状态（`0x30` UDT 上行 CRC 错是少数与信号质量有关的例外）。

</details>

---

## 16. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `04-集群协议/ReasonCode与Grant变体.md` **§0** | Reason 与 Grant 怎么配合（本课总图来源） |
| 2 | 同上 **§1** | 8 bit 骨架 tt/d/aaaaa + Mirrored_Reason |
| 3 | 同上 **§2–§4** | ACK / NACK / QACK / WACK 全表（本课 canonical） |
| 4 | 同上 **§5** | C_ACKD / C_ACKU / P_ACK 字段布局 |
| 5 | 同上 **§6** | Response_Info + Index pattern |
| 6 | 同上 **§7** | 登记结论速查（接第 32 课） |
| 7 | 同上 **§8** | 改向、鉴权、无线检查等过程中的固定 Reason |
| 8 | 同上 **§9** | 与 Aloha / Ahoy / RAND / Grant 的交叉：谁有 Reason、谁没有 |
| 9 | `04-集群协议/集群协议字段速览.md` **§7 / §8** | 确认类外壳与入站 C_RAND / C_ACKU |
| 10 | `02-语音业务/语音业务字段速览.md` **§4.4** | Part2 NACK_Rsp（对照用，别混） |
| 11 | `学习推送/第32课.md` / `第33课.md` | 登记 + Aloha；Grant 变体 |
| 12 | `总索引.md` **集群 / Tier III** | 门牌导航 |
| 13 | `04-集群协议/TS102361-4_V1.12.1.pdf` | 官方原文 7.2.7、7.2.8、Tables 7.41–7.45 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 厂商文档 > 开源实现 > 课文笔记**。鉴权、绝对频率、Hunt、拨号、Stun 状态机：**回对应课 / PDF**，本课不补第二份。

---

## 17. 下一课预告

**第 35 课 · 鉴权挑战响应（边界：RC4）**

本课你已经认识了两个名字：`0x48`（手台的 Authentication Response）和 `0x64`（网络的 Authentication Response）。下一课讲它们背后的流程：网络为什么要「出题」（挑战）、手台怎么「交卷」（响应）、C_ACKVIT 与 C_ACKU 在这条路上各扮演什么角色、鉴权和加密（RC4 等）的边界在哪——**只讲流程与字段落点，不讲算法细节**。

记住边界：**本课的 Reason 告诉你「结论」；下一课的鉴权告诉你「凭什么相信你是你」。**

---

## 18. 推荐阅读与视频

本课外链均为 **2026-10-05**（上午推送）检索并用 HTTP 请求核验可达（返回 200）。**不编造地址**。ETSI 官网直链对自动化抓取不稳定，Part4 以 DMR 协会镜像为准。另检索了「DMR Tier III acknowledgement / reason code / call queued rejected」相关公开视频：能找到 Tier III 概论与产品宣传片，**没有**找到按「tt/d/aaaaa + ACK/NACK/QACK/WACK + Response_Info」讲解的对口技术视频。**video_found=false**（诚实备注）。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMR 协会镜像 PDF）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - **为什么值得看**：7.2.7 Response_Info、7.2.8 Reason（Tables 7.41–7.45）的硬出处。  
   - **库内副本**：`dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。  
   - **怎么用**：先读 7.2.8.0 的一页引言（tt/d/aaaaa 与 Mirrored_Reason），再翻 7.2.8.2 的 NACK 散文——比表格更好懂每条「为什么」。

2. **[SDRTrunk · DMR Reason.java（开源解码器的 Reason 枚举）](https://github.com/DSheirer/sdrtrunk/blob/master/src/main/java/io/github/dsheirer/module/decode/dmr/message/type/Reason.java)**  
   - **为什么值得看**：一张屏幕就能看完全部 Reason 值和英文短标签，和本课 §13.2 口袋速查对读很顺手；也包含 `0x16 MS_DUPLEX_NOT_SUPPORTED`。  
   - **怎么用**：当「监听软件会显示成什么英文」的对照表；注意其中 Queued-for-busy 写成 `0xAa`，与 ETSI 表 7.44 的 `0xA1` 不一致——**以 ETSI 为准**（§9.1）。

3. **[IanWraith/DMRDecode · CSBK.java（开源解码器）](https://github.com/IanWraith/DMRDecode/blob/master/src/main/java/com/dmr/CSBK.java)**  
   - **为什么值得看**：C_ACKD 解析函数的注释直接写出「第 16–22 位 Response_Info、第 23–30 位 Reason、第 31 位保留」（从 CSBK 第 0 位起数），代码里用 `>>6` 取 tt、用 `&32` 取 d——就是本课 §3.2 和 §4.1 的代码版。  
   - **怎么用**：搜 `csbko32fid0`，对着本课 §3.3 的拼接公式看一遍。

4. **[JVCKENWOOD · DMR Tier III KAIROS Tier III Trunking 应用说明（AN-19-0001，PDF）](https://portal.au.jvckenwood.com/cdn/shop/files/AN-19-0001_DMR_Tier3_KAIROS_Trunking_V110.pdf?v=2051844276723892895)**  
   - **为什么值得看**：少见的公开厂商控制器设置说明，§4.5 里的 QACK 超时、多站组呼 All Start/Fast Start、组呼碰撞 Deny/Wait Late Entry、Flooding Filter 等，把「什么时候回 NACK、什么时候排队」落到了真实配置项上。  
   - **怎么用**：配合本课 §12 读；它是厂商实现，不是标准，**别拿它推断 Reason 具体值**。

5. **[GopherTrunk · DMR CSBK payloads](https://gophertrunk.org/reference/dmr-csbk-payloads/)**  
   - **为什么值得看**：一张表看全 Tier III 常见 CSBKO（Aloha/Ahoy/RAND/ACKD/ACKU/Grant/C_MOVE……），帮你把「回条」放回整张控制消息地图里。  
   - **怎么用**：认名认码；注意它把 `0x26` 列作 C_NACK，这与 Part4（C_NACKD 共用 CSBKO 32，靠 tt 区分）不同——练一次「外部资料冲突以 ETSI 为准」（§14 第 10 条）。

6. **[GopherTrunk · DMR Tier III（概念页）](https://gophertrunk.org/reference/dmr-tier-3/)**  
   - **为什么值得看**：白话复习「手台守控制信道 → 请求 → 被指派业务信道」，并点出 12.5 kHz、4FSK 9600 bps、双时隙这些射频账本——正好对上本课 §2.4。  
   - **怎么用**：当阶段 E 的英文复习页。

7. **[Tait Radio Academy · Channel Operation](https://www.taitradioacademy.com/topic/dmr-channel-operation-1/)**  
   - **为什么值得看**：白话讲控制信道如何分配业务信道，适合给新同事讲「为什么会排队」。

8. **[DMR Association · Standards 目录](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：Part1–4 官方下载总入口，找 PDF 不迷路。

**视频备注（诚实）**：本课所需的「读懂 Reason」能力，标准 PDF + 两份开源解码器源码 + 一份厂商控制器说明已经足够；公开视频里没有达到本课深度的专项讲解，所以本课不放视频。日后如果 DMR 协会或厂商学院上架相关技术片，再补进来。

---

## 本课收束

阶段 E 第四站就一件事：**读懂前台的回条。**  
看见回条，先认 CSBKO 32–35；拼对 8 位；首位十六进制定类别和方向。  
ACK、NACK 是结论；QACK、WACK 是「还在办」。  
d=0 的理由是对方的话，网络只是转述。  
角落备注跟着理由变。  
能读出清晰的理由，就先别怀疑调制——12.5 kHz / 4FSK / 双时隙一直没变。  
下一站：鉴权的挑战与响应。
