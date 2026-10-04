## 10. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| C_ALOHA CSBKO | **`011001`** | 告示牌（Table 7.19） |
| C_RAND CSBKO | **`011111`** | 入站按铃（含登记） |
| C_AHOY CSBKO | **`011100`** | 点名 / 登记后续等 |
| C_ACKD 族 CSBKO | **`100000`** 等 | 确认/拒绝外壳 |
| C_BCAST CSBKO | **`101000`** | 含 MassReg 公告 |
| Service_Kind 登记类 | **`1110₂`** | 登记/鉴权/注销/MS check（Table 7.49） |
| Reg | **1 bit**：`1`=须登记后活跃 | Aloha/CACH/BCAST |
| Mask | **5 bit** | 争用人口细分 |
| Backoff | **4 bit** | 退避号 |
| NRand_Wait | **4 bit** | 随机等待 |
| Service Function | **2 bit** | 允许的业务功能类 |
| System Identity Code | **16 bit** | 系统身份 |
| MS Address（Aloha） | **24 bit** | 可点名单台（配合 Mask） |
| MassReg Reg_Window | Table **7.77**；`0`=取消 | 大规模登记窗 |
| MS_Not_Registered | Reason 指针 `0010 1101₂`（0x2D） | **全表第 34 课** |
| Part4 官方版本 | **TS 102 361-4 V1.12.1 (2023-07)** | 集群硬出处 |
| 速览主节 | **§4 Aloha / §8 RAND / §9 登记 / §12 分工** | 本课入口 |
| Announcement 主节 | **§3.5 MassReg / §6 Kind / §10 共享位** | 枚举加深 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 换手续不换射频 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |

---

## 11. 十则误区（看见就打回）

1. **「看见 Aloha = 已经登记。」** → Aloha 是告示牌，不是入住回执。  
2. **「Reg=0 表示禁止入网。」** → 学习口径：MS **不应主动寻求登记**；不是「永久封站」口号。  
3. **「Reg=1 只是建议，PTT 一样能叫。」** → Reg=1 站未登记常被挡；典型路标 `MS_Not_Registered`。  
4. **「Aloha 可以当 Grant 读。」** → CSBKO 与语义都不同；告示 ≠ 房间小票。  
5. **「Mask 是 Colour Code。」** → Mask 细分随机接入人口；CC 是另一套同频区分故事。  
6. **「Backoff 就是 Hangtime。」** → 一个管随机接入再试节奏；一个管通话后保持——别混房间。  
7. **「Service Function = Service_Kind。」** → 前者在 Aloha 收窄大门；后者在 RAND/AHOY 写清要办的事。  
8. **「MassReg 等于控制信道故障。」** → 常是策略性大规模重登记；先看 Reg_Window/Mask。  
9. **「登记失败就要学鉴权/RC4。」** → 边界：登记地图本课；鉴权挑战 → 第 35；别抢跑。  
10. **「PTT 无声说明 4FSK/12.5 kHz 坏了。」** → 先读 Reg/登记 RAND/ACK；调制账本最后背锅。

---

## 12. 自测题（含答案）

**题 1.** 用旅馆比喻各一句话解释：登记、Aloha、Grant。

<details><summary>答案</summary>

登记 = 入住登记（系统知道你在哪站/是否允许活跃）。Aloha = 前台排队规则告示牌（Reg/Mask/Backoff…）。Grant = 房间号小票（第 31 课）。先读告示、办入住，再拿小票进客房。

</details>

**题 2.** Reg=0 与 Reg=1 各用速览口径写一句；并写一个现场分诊问题。

<details><summary>答案</summary>

Reg=0：MS **不应主动寻求登记**。Reg=1：须登记后才在该 TSCC 上活跃。分诊问题：「当前 Aloha/CACH/BCAST 的 Reg 是几？有没有登记类 C_RAND + ACK？」

</details>

**题 3.** 写出 C_ALOHA 与 C_RAND 的代表 CSBKO；登记类 Service_Kind 取值。

<details><summary>答案</summary>

C_ALOHA=`011001`；C_RAND=`011111`；登记类 Service_Kind=`1110₂`（登记/鉴权/注销/MS check，Table 7.49）。

</details>

**题 4.** 为什么说「Aloha 没有 Reason Code」？未登记却发业务，常见空口路标是什么？

<details><summary>答案</summary>

Announcement §10：Aloha 不承载 Reason。未登记却要业务 → TS 常用 `C_NACKD(MS_Not_Registered)`。Reason 全表见第 34 课。

</details>

**题 5.** Mask、Backoff、NRand_Wait 各管什么直觉？碰撞后下一步是什么（一句话）？

<details><summary>答案</summary>

Mask：细分谁可参与争用。Backoff：退避节奏。NRand_Wait：随机等待/选隙参数。碰撞或无应答后：按告示参数退避再试（不在本课背完整 SDL）。

</details>

**题 6.** Service Function 与 Service_Kind 差在哪？举一个「大门收窄」的现场说法。

<details><summary>答案</summary>

Service Function 在 **C_ALOHA** 上允许哪类功能按铃；Service_Kind 在 **C_RAND/AHOY** 上声明这一枪具体服务。现场说法：告示暂时只开登记门，语音 RAND 会被挡，但登记 RAND 仍可能看见。

</details>

**题 7.** Mass Registration：哪个 PDU？Reg_Window=`0` 表示什么？为何常配 Mask？

<details><summary>答案</summary>

C_BCAST，Announcement_type=MassReg。Reg_Window=`0` = 取消大规模登记。Mask（Aloha Mask）用来把重登记人口切开、摊峰，避免同时挤爆。

</details>

**题 8.** 判断：分析仪在 TSCC 上持续解码 C_ALOHA，即可认为该 MS 已完成登记。（对 / 错）并改写正确证据链。

<details><summary>答案</summary>

**错。** 正确证据链：Reg 要求（若 Reg=1）→ 看见该 MS 的登记类 C_RAND → 看见成功 ACK（或完成 AHOY 驱动路径）→ 之后才谈语音 RAND/Grant。

</details>

**题 9.（加分）** 画出（文字版）Reg=1 时从空闲到「可以请求语音」的六步骨架。

<details><summary>答案</summary>

①守 TSCC → ②读 Aloha(Reg=1) → ③C_RAND(登记类) → ④ACK/AHOY 路径成功 → ⑤再 C_RAND(语音/数据) → ⑥Grant →（第 31 课）进 Payload。

</details>

**题 10.（加分）** Part1/2/3/4：下列问题各去哪本？①CSBK 外壳②组呼 Voice LC③业务信道确认数据④TSCC 上的 Aloha/登记。

<details><summary>答案</summary>

①Part1 ②Part2 ③Part3 ④Part4（速览 §12）。

</details>

---

## 13. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `04-集群协议/集群协议字段速览.md` **§4** | C_ALOHA Table 7.19 全字段（本课 canonical） |
| 2 | 同上 **§9** | 登记与编址要点：Reg=0/1、Denied List、Mass Reg、双路径 |
| 3 | 同上 **§8** | C_RAND 外壳与 Service_Kind 位置 |
| 4 | 同上 **§6** | C_AHOY：登记后续/点名指针 |
| 5 | 同上 **§1 / §12** | 概念回唤 + Part 分工 |
| 6 | `04-集群协议/Announcement与其余枚举.md` **§3.5** | MassReg / Reg_Window / Mask |
| 7 | 同上 **§6 / §8.4 / §10** | Service_Kind=`1110`；登记 Service_Options；Aloha 无 Reason |
| 8 | `00-入门/TR附录_省电接入功率.md` **B.1–B.2** | Mask/SF/Backoff 直觉（**冲突以 TS 为准**） |
| 9 | `04-集群协议/ReasonCode与Grant变体.md` | **仅路标**：`MS_Not_Registered` / `Reg_*`；全表 → 第 34 |
| 10 | `学习推送/第31课.md` | TSCC vs Payload + Grant（本课前置） |
| 11 | `学习推送/第9课.md` / `第11课.md` | Tier 全貌 / 文档地图 |
| 12 | `总索引.md` **集群 / Tier III** | 门牌导航 |
| 13 | `04-集群协议/TS102361-4_V1.12.1.pdf` | 官方原文（硬冲突以 TS 为准） |
| 14 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「未登记」当成调制故障 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。Grant 全变体、Reason 全表、鉴权/RC4、绝对频率、Hunt/拨号/Stun：**永远回对应课 / PDF**，本课不补第二份。

---

## 14. 下一课预告

**第 33 课 · Grant 变体地图**

本课把门钉在「前台入住 + Aloha 告示」。下一课把第 31 课只认了名字的 **PV / TV / BTV / PD / TD / DX / P_GRANT…** 摊成一张**变体地图**：各小票差在哪几个字段、什么时候会看到附块、业务信道上的再授予怎么认。仍然少公式；不抢第 34 课的 Reason 全表，也不回头把本课登记 MSC 再 dump 一遍。

---

## 15. 推荐阅读与视频

本课外链为 **2026-10-04**（上午推送）检索核验；真实用 HTTP 头/跳转核验过可达（协会镜像 / Tait Academy / GopherTrunk / 维基背景 / 产品页等，**ETSI deliver 直链对部分自动化抓取常返回 403，故 Part4 以 DMRA 协会镜像为准**）。**不编造地址**。策略 = **Part4 协会镜像 PDF + DMRA Tier III 现状讲稿 + Tait「Channel Operation」（明确写控制信道管 registration）+ Tait Study Guide + GopherTrunk Tier III 深潜（C_ALOHA 锁台/SystemID）+ GopherTrunk CSBK payload 参考 + DMRA 标准目录 + Benefits 白皮书 + Hytera Tier III 系统页 + 维基 ALOHAnet（仅随机接入背景，非 DMR 字段课）**。另检索公开「DMR registration + Aloha」专项技术视频：可见 Tier III 概论/营销短片，**未**找到按「Reg 位 + C_ALOHA 字段 + 登记类 C_RAND + MassReg」展开的独立优质技术课。**video_found=false**（诚实备注：有实现向博客与标准 PDF，无对口技术短片）。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMRA 协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - **为什么值得看**：登记过程、C_ALOHA、随机接入、Mass Reg 等硬出处；与速览 §4/§9 对照。  
   - **库内副本**：`dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。  
   - **怎么用**：先翻 C_ALOHA / Registration 相关叙述与 Table 7.19，再回本课总图；**不要**第一天啃完鉴权与全部 Annex。

2. **[State-of-the-art of ETSI DMR Tier III Standard（DMRA 讲稿 PDF）](https://dmrassociation.org/public-downloads/documents/State-of-the-art-of-ETSI-DMR-Tier-III-Standard-Critical-Comms-Russia-18Apr-2019.pdf)**  
   - **为什么值得看**：用幻灯节奏扫过控制信道能力与 Tier III 功能地图；适合阶段 E 建立「前台管什么」直觉。  
   - **怎么用**：当导游图；字段细节仍回 Part4 / 速览。

3. **[Tait Radio Academy · Channel Operation](https://www.taitradioacademy.com/topic/dmr-channel-operation-1/)**  
   - **为什么值得看**：白话列出控制信道主要功能，**明确包含 registration requests / location management by registration**——与本课「入住登记」同向。  
   - **怎么用**：读完立刻用本课分诊表问：Reg 位？登记 RAND？ACK？

4. **[Tait · Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：节点侧「receiving radio registrations, storing them in registration database」的经典叙述；帮助把「为什么要登记」说给领导听。  
   - **怎么用**：当英文版动机朗读；空口字段仍回 Part4。

5. **[GopherTrunk · DMR End to End Part 8：Tier III — C_ALOHA, Grants & LCNs](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-08-tier3-trunking/)**  
   - **为什么值得看**：实现向说明 C_ALOHA 作为控制信道信标、用 System Identity 锁台——与本课「告示牌 + System Identity」同向。  
   - **怎么用**：当监听/解码语感；**字段冲突仍以 ETSI / 速览为准**。

6. **[GopherTrunk · DMR CSBK payloads](https://gophertrunk.org/reference/dmr-csbk-payloads/)**  
   - **为什么值得看**：把 C_ALOHA / C_RAND / C_AHOY / C_BCAST 等 Opcode 放在一张实现参考表里，便于和本课账本对读。  
   - **怎么用**：认名 + 认码；细节以 Table 7.19 等为准。

7. **[DMR Association · Standards 目录](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：Part1–4 / TR 下载入口总台；阶段 E 找官方 PDF 少迷路。

8. **[DMR Association · Benefits and Features of DMR（白皮书）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：Tier 分层与容量语境；帮新人解释「为什么集群要控制面手续」。  
   - **怎么用**：背景阅读；不替代 Part4。

9. **[Hytera · DMR Tier 3 Trunking 系统页](https://www.hytera.us/systems/dmr-tier-3-trunking-systems/)**  
   - **为什么值得看**：厂商白话：控制信道上的注册与请求、其余为共享 traffic。  
   - **怎么用**：产品叙事；与标准术语对照时以 Part4 为准。

10. **[Wikipedia · ALOHAnet（随机接入背景）](https://en.wikipedia.org/wiki/ALOHAnet)**  
   - **为什么值得看**：理解「随机发、碰撞、再试」的历史直觉，帮助消化 Mask/Backoff 为什么存在。  
   - **怎么用**：**仅背景**；DMR 的 C_ALOHA 字段与 Reg 位以 ETSI 为准，勿把课堂 Aloha 吞吐公式硬套进机房分诊。

**视频备注（诚实）**：公开可核验资源里，登记 + Aloha 的**文字/PDF/实现博客**足够支撑本课；未找到达到本课深度的对口技术短片。故 **video_found=false**。若日后协会/学院上架专项片，再补进进度外链清单。

---

## 本课收束

阶段 E 第二站就一件事：**留在前台，先读告示、再办入住。**  
Aloha 告诉你谁能按铃、要不要登记、怎么退避；登记让系统知道你在哪、允不允许活跃。  
未登记却要业务，常撞 `MS_Not_Registered` 这类路标——Reason 全表下周细读。  
调制账本仍是 12.5 kHz / 4FSK / 双时隙。  
下一站：把 Grant 小票摊成变体地图。
