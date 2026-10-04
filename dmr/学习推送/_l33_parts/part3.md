## 10. 术语账本 / 口袋速查

### 10.1 白话术语表

| 术语 | 一句话 | 别和谁混 |
|------|--------|----------|
| **Channel Grant** | TS 发给 MS 的「去哪间业务房」小票 | ≠ Aloha 告示；≠ Reason 判决书 |
| **CSBKO / Opcode** | 6 bit 票样编号；Grant 族约 48–56 | ≠ Colour Code；≠ Service_Kind |
| **Logical Physical Channel Number** | 12 bit 逻辑房号 | ≠ TDMA ch 位；0 / 1…FFE / FFF 三态 |
| **Logical Channel Number** | 1 bit：TDMA ch1/ch2 | ≠ 逻辑物理信道号 |
| **位 A** | Reserved / Late_Entry / HI_RATE（随票样） | ≠ Emergency |
| **位 B** | Offset / Call Direction（随票样） | ≠「双工开关」口号（DX 用 Call Direction） |
| **Late_Entry** | 组呼建链后迟后进入授予 | ≠ Emergency；≠ 单纯重发 |
| **Offset** | aligned / offset timing | DX 半双工票上的 Offset；DX 票无此场 |
| **Call Direction** | DX 票：Target 填哪一端 | ≠ Offset 的别名 |
| **HI_RATE** | 数据占单时隙/双时隙 | ≠ 换 4FSK；DX 数据固定 0 |
| **Emergency** | 紧急标志 | 别跟 Late_Entry/HI_RATE 抢名字 |
| **SI / MI** | 数据单条目/多条目；用 CSBKO 分开 | ≠ Service Function |
| **CG_AP** | 绝对频率 MBC 续块；头块信道号=0xFFF | ≠ 自己就是一种新 CSBKO 号码 |
| **P_GRANT** | 业务信道上的再授予；CSBKO 沿用原 TSCC Grant | ≠ 「新的 Opcode」 |
| **Reason Code** | 在 ACK/NACK/QACK/WACK 里 | **不在 Grant 里**（第 34 课） |

### 10.2 口袋速查：CSBKO 48–56

| Dec | 二进制 | 别名 |
|-----|--------|------|
| 48 | `110000` | PV_GRANT |
| 49 | `110001` | TV_GRANT |
| 50 | `110010` | BTV_GRANT |
| 51 | `110011` | PD_GRANT（SI） |
| 52 | `110100` | TD_GRANT（SI） |
| 53 | `110101` | PV_GRANT_DX |
| 54 | `110110` | PD_GRANT_DX |
| 55 | `110111` | PD_GRANT（MI） |
| 56 | `111000` | TD_GRANT（MI）／兼 Part2 语境注意 |

相关非 Grant（别误收进本课口袋当小票）：

| Dec | 别名 | 备注 |
|-----|------|------|
| 25 | C_ALOHA | 第 32 课告示牌 |
| 28 | C_AHOY | 点名 |
| 31 | C_RAND | 按铃 |
| 32/33 | C_ACKD/U 族 | Reason 载体 → 第 34 |
| 57 | C_MOVE | 迁 TSCC；非 Grant |

### 10.3 数字与符号账本

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| Grant 共用载荷 | Octet 2–9 **64 bit** | 信道+ch+A+E+B+地址 |
| 信道号无效 | **0** | 停 |
| 信道号逻辑 | **1…0xFFE** | 单块 CSBK 常见 |
| 信道号绝对指针 | **0xFFF** | → CG_AP |
| FID（标准） | `00000000` | SFID |
| Part4 官方版本 | **TS 102 361-4 V1.12.1 (2023-07)** | 硬出处 |
| 库内 canonical | `ReasonCode与Grant变体.md` **§10–§14** | 本课主入口 |
| 速览入口 | `集群协议字段速览.md` **§1 / §3** | 代表表 + 指针 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 换票样不换射频 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |

---

## 11. 十则误区（看见就打回）

1. **「看见 Grant = 知道业务类型。」** → 必须先读 CSBKO；Grant 是一大族，不是一种。  
2. **「Late_Entry 就是紧急。」** → Late_Entry 管迟后进入；Emergency 是另一 bit。  
3. **「Offset 等于双工。」** → Offset 是 aligned/offset timing；双工票是 DX + Call Direction，且总是 offset。  
4. **「HI_RATE 表示换了高速调制。」** → 管数据占几个时隙资源；调制仍是 4FSK。  
5. **「信道号 0xFFF 是坏值。」** → 常是「请看 CG_AP 附页」的合法写法。  
6. **「CG_AP 有自己的新 Opcode。」** → 续块 CSBKO **与头块相同**。  
7. **「P_GRANT 是 Opcode 新号码。」** → 沿用原 TSCC Grant 的 CSBKO；差在所在信道与用途。  
8. **「Grant 里一定有 Reason Code。」** → Grant **无 Reason**；失败看 NACK（第 34 课）。  
9. **「Opcode 56 永远是 TD_GRANT_MI。」** → Part2 也可能用同码；看 FID/场景。  
10. **「小票种类看不懂说明 12.5 kHz/4FSK 坏了。」** → 先完成票样分诊链；调制账本最后背锅。

---

## 12. 自测题（含答案）

**题 1.** 用旅馆比喻各一句话：Grant、CSBKO、CG_AP、P_GRANT。

<details><summary>答案</summary>

Grant = 房间小票。CSBKO = 票样编号（个呼/组呼/数据/双工等）。CG_AP = 房号栏写「见附页」时的绝对坐标附页。P_GRANT = 进客房之后的换房/再广播/新呼叫公告（票样编号通常沿用）。

</details>

**题 2.** 写出 Grant 共用 64-bit 骨架从前往后的七段名称。

<details><summary>答案</summary>

Logical Physical Channel Number(12) → Logical Channel Number(1) → 位 A(1) → Emergency(1) → 位 B(1) → Target(24) → Source(24)。

</details>

**题 3.** 给出 PV_GRANT / TV_GRANT / BTV_GRANT / PV_GRANT_DX 的 Opcode（十进制）与 CSBKO 二进制。

<details><summary>答案</summary>

48=`110000`；49=`110001`；50=`110010`；53=`110101`。

</details>

**题 4.** TV_GRANT 的位 A 叫什么？`0` 与 `1` 各表示什么（学习口径）？

<details><summary>答案</summary>

Late_Entry。`0`=建链授予；`1`=建链后的迟后进入授予。

</details>

**题 5.** PD_GRANT 的 SI/MI 如何区分？HI_RATE=`1` 表示什么？PD_GRANT_DX 的 HI_RATE 呢？

<details><summary>答案</summary>

SI=Opcode 51（`110011`），MI=Opcode 55（`110111`）。HI_RATE=`1`=双时隙数据。PD_GRANT_DX 的 HI_RATE **固定 0**。

</details>

**题 6.** 信道号 0、1…0xFFE、0xFFF 各怎么处理？

<details><summary>答案</summary>

0=无效。1…0xFFE=逻辑信道号（常单块 CSBK）。0xFFF=绝对参数在后续 CG_AP。

</details>

**题 7.** 为什么说「Grant 不要求确认」？分析仪上常见什么现象？

<details><summary>答案</summary>

规范学习口径：Channel Grant 不征求响应，故常重复发送。分析仪上同一张 Grant 连喊多遍很正常，不等于协议死锁。

</details>

**题 8.** P_GRANT 的 CSBKO 从哪来？列出三种用途关键词。

<details><summary>答案</summary>

必须等于当初 TSCC Grant 的 CSBKO。用途：换信道（swap）；本呼叫首次发射前公告；公告新呼叫。

</details>

**题 9.（加分）** 判断：失败呼叫应在 Grant 比特里找 Reason Code。（对/错）并改写正确路径。

<details><summary>答案</summary>

**错。** 成功路径是 Grant（无 Reason）；失败路径是 C_NACKD 等确认族里的 Reason Code（第 34 课）。

</details>

**题 10.（加分）** 现场分诊顺序（五步）写出来；并指出 Opcode 56 的额外陷阱。

<details><summary>答案</summary>

①读 CSBKO 定票样 → ②读位 A/B → ③读信道号（FFF→CG_AP）→ ④判断所在信道是否 Payload 上的 P_GRANT → ⑤失败才查 NACK Reason。Opcode 56：Part4 为 TD_GRANT_MI，亦可能在 Part2 BS_Dwn_Act 语境出现，需靠 FID/场景区分。

</details>

---

## 13. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `04-集群协议/ReasonCode与Grant变体.md` **§10** | Grant 变体总览表（本课 canonical） |
| 2 | 同上 **§11** | 共用 64-bit 骨架与位 A/B 释义 |
| 3 | 同上 **§12** | 各 Grant 字段表（PV/TV/BTV/PD/TD/DX/P_GRANT） |
| 4 | 同上 **§13** | CG_AP / CdefParms 指针（公式不深挖） |
| 5 | 同上 **§14** | Opcode 速查 48–56 |
| 6 | 同上 **§0** | Reason 与 Grant 怎么配合：成功 Grant / 失败 NACK |
| 7 | `04-集群协议/集群协议字段速览.md` **§1** | TSCC / Payload / Grant 概念回唤 |
| 8 | 同上 **§3** | PV/TV 代表表 + 其余变体指针 + CG_AP 摘记 |
| 9 | `学习推送/第31课.md` | TSCC vs Payload + Grant 小票总名 |
| 10 | `学习推送/第32课.md` | 登记 + Aloha（本课前置；勿重 dump） |
| 11 | `总索引.md` **集群 / Tier III** | 门牌导航 |
| 12 | `04-集群协议/TS102361-4_V1.12.1.pdf` | 官方原文 Tables 7.9–7.16 / 7.29 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「票样分不清」当成调制故障 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。Reason 全表、鉴权/RC4、绝对频率公式、Hunt/拨号/Stun：**永远回对应课 / PDF**，本课不补第二份。

---

## 14. 下一课预告

**第 34 课 · Reason Code 怎么读**

本课把门钉在「成功就发哪种 Grant 小票」。下一课专攻 **失败与中间态**：C_ACK / C_NACK / C_QACK / C_WACK 里的 **Reason Code** 怎么拆（tt / d / aaaaa）、登记拒绝与呼叫拒绝常见码、Mirrored_Reason、Response_Info 成对读法。仍然少公式；**不回头把本课 Grant 变体再 dump 一遍**，也不抢第 35 课鉴权。

记住边界：**Grant 本身无 Reason；看见拒绝，去 ACK 族找。**

---

## 15. 推荐阅读与视频

本课外链为 **2026-10-04**（晚间推送）检索核验；真实用 HTTP 头/跳转核验过可达（协会镜像 / Tait Academy / GopherTrunk Grant·CSBK 参考 / DMRA 白皮书 / Hytera Tier III / 开源解码器对照等，**ETSI deliver 直链对部分自动化抓取常返回 403，故 Part4 以 DMRA 协会镜像为准**）。**不编造地址**。策略 = **Part4 协会镜像 PDF + DMRA Tier III 现状讲稿 + Tait Channel Operation + Tait Study Guide + GopherTrunk Tier III 深潜（Grants & LCNs）+ GopherTrunk Channel grant 概念页 + GopherTrunk CSBK payloads（含 PV/TV/BTV/PD/TD Opcode）+ DMRA 标准目录 + Benefits 白皮书 + Hytera Tier III 系统页 + IanWraith DMRDecode CSBK.java（开源侧 Opcode 48–52 命名对照）**。另检索公开「DMR Grant variants / PV_GRANT TV_GRANT CSBKO map」专项技术视频：可见 Tier III 概论/营销短片与实现向博客，**未**找到按「CSBKO 48–56 变体地图 + 位 A/B + CG_AP + P_GRANT」展开的独立优质技术课。**video_found=false**（诚实备注：有实现向博客、标准 PDF 与开源对照，无对口技术短片）。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMRA 协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - **为什么值得看**：Tables 7.9–7.16 / 7.29 等 Grant 硬出处；与本课 §4–§8 对照。  
   - **库内副本**：`dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。  
   - **怎么用**：先翻 Channel Grant 叙述与代表表，再回本课总表；**不要**第一天啃完 Reason 全表与 Annex C 公式。

2. **[State-of-the-art of ETSI DMR Tier III Standard（DMRA 讲稿 PDF）](https://dmrassociation.org/public-downloads/documents/State-of-the-art-of-ETSI-DMR-Tier-III-Standard-Critical-Comms-Russia-18Apr-2019.pdf)**  
   - **为什么值得看**：用幻灯节奏扫过控制信道能力与 Tier III 功能地图；适合阶段 E 建立「前台发什么票」直觉。  
   - **怎么用**：当导游图；字段细节仍回 Part4 / `ReasonCode与Grant变体.md`。

3. **[Tait Radio Academy · Channel Operation](https://www.taitradioacademy.com/topic/dmr-channel-operation-1/)**  
   - **为什么值得看**：白话讲控制信道如何分配业务信道——与「Grant = 房间小票」同向。  
   - **怎么用**：读完立刻用本课分诊表问：CSBKO？位 A/B？信道号是否 FFF？

4. **[Tait · Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：节点侧信道分配与集群效率的经典叙述；帮你把「为什么要发 Grant」说给领导听。  
   - **怎么用**：当英文版动机朗读；空口票样仍回 Part4。

5. **[GopherTrunk · DMR End to End Part 8：Tier III — C_ALOHA, Grants & LCNs](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-08-tier3-trunking/)**  
   - **为什么值得看**：实现向强调 TV/PV Grant 以 12-bit LPCN + 时隙位打头、逻辑信道需 band plan 映射——与本课信道号故事同向。  
   - **怎么用**：当监听/解码语感；**字段冲突仍以 ETSI / 库内整理为准**。

6. **[GopherTrunk · Channel grant（概念页）](https://gophertrunk.org/reference/channel-grant/)**  
   - **为什么值得看**：跨标准白话解释「grant = 呼叫落到具体语音信道的那一瞬间」；并提到 group 再公告与 late entry 直觉。  
   - **怎么用**：建立故事感；DMR 具体 CSBKO 地图仍回本课 §4。

7. **[GopherTrunk · DMR CSBK payloads](https://gophertrunk.org/reference/dmr-csbk-payloads/)**  
   - **为什么值得看**：把 PV_GRANT/TV_GRANT/BTV_GRANT/PD_GRANT/TD_GRANT 等 Opcode 放在一张实现参考表里，便于和本课口袋速查对读。  
   - **怎么用**：认名 + 认码；DX/MI 细表与位释义以 `ReasonCode与Grant变体.md` §10–§12 为准。

8. **[DMR Association · Standards 目录](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：Part1–4 / TR 下载入口总台；阶段 E 找官方 PDF 少迷路。

9. **[DMR Association · Benefits and Features of DMR（白皮书）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：Tier 分层与容量语境；帮新人解释「为什么要用动态 Grant 而不是写死频率」。  
   - **怎么用**：背景阅读；不替代 Part4。

10. **[Hytera · DMR Tier 3 Trunking 系统页](https://www.hytera.us/systems/dmr-tier-3-trunking-systems/)**  
    - **为什么值得看**：厂商白话：控制信道管请求与分配、其余为共享 traffic。  
    - **怎么用**：产品叙事；与标准术语对照时以 Part4 为准。

11. **[IanWraith/DMRDecode · CSBK.java（开源对照）](https://github.com/IanWraith/DMRDecode/blob/master/src/main/java/com/dmr/CSBK.java)**  
    - **为什么值得看**：开源解码器里对 CSBKO 48–52 等命名（PV/TV/BTV/PD/TD_GRANT）的直观分支，便于和本课 Opcode 表互证。  
    - **怎么用**：只作命名对照；完整变体与 DX/MI/CG_AP 仍以 ETSI / 库内 §10–§13 为准。

**视频备注（诚实）**：公开可核验资源里，Grant 变体的**文字/PDF/实现博客/开源对照**足够支撑本课；未找到达到本课深度的对口技术短片（无「CSBKO 48–56 地图」专项课）。故 **video_found=false**。若日后协会/学院上架专项片，再补进进度外链清单。

---

## 本课收束

阶段 E 第三站就一件事：**把房间小票摊成种类地图。**  
看见 Grant，先问哪种 CSBKO；再问位 A/B；再问信道号是不是 0xFFF；再问人在前台还是已在客房。  
成功路径是重复的小票；失败路径才去翻 Reason。  
调制账本仍是 12.5 kHz / 4FSK / 双时隙。  
下一站：学会读拒绝与排队的 Reason Code。
