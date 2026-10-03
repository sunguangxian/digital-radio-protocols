## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| 时隙尺子 | **30 ms** · **2-slot** | 进房后仍用；Grant 指定 ch1/ch2 |
| 超帧 | **A–F ≈ 360 ms** | **Payload** 上（第 17/30） |
| PV_GRANT CSBKO | **`110000`** | 个呼语音小票（速览 §3.1） |
| TV_GRANT CSBKO | **`110001`** | 组呼语音小票（速览 §3.2） |
| C_ALOHA CSBKO | **`011001`** | 排队告示（过程 → 第 32） |
| C_RAND CSBKO | **`011111`** | 入站按铃 |
| C_AHOY CSBKO | **`011100`** | 点名（速览 §6） |
| C_ACKD 族 CSBKO | **`100000`** 等 | 确认/拒绝外壳（Reason → 第 34） |
| C_BCAST CSBKO | **`101000`** | 系统公告（指针） |
| Logical Physical Ch | **12 bit**；`0` 无效；`0xFFF`→附绝对块 | 房间逻辑号 |
| Logical Channel Number | **1 bit**：`0`=ch1，`1`=ch2 | 时隙门 |
| Voice LC Header DT | **`0001`** | **进 Payload 之后**才找（第 30） |
| Part4 官方版本 | **TS 102 361-4 V1.12.1 (2023-07)** | 集群硬出处 |
| 速览主节 | **§1 概念 / §2 PDU 地图 / §3 Grant 代表 / §12 分工** | 本课入口 |
| 总索引 | **集群 / Tier III** | 门牌：TSCC/Grant → 速览 → Part4 PDF |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 换故事不换射频 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |

---

## 9. 十则误区（看见就打回）

1. **「集群组呼也该在控制信道上先看到 Voice LC Header。」** → Header 在 Payload；控制上看 Grant。  
2. **「看见 Grant = 已经在通话。」** → 小票 ≠ 超帧；还要改频进房。  
3. **「C_RAND 就是常规个呼 UU_V_Req。」** → 都是「先问/先请求」味道，但 Opcode 地图与故事轴在 Part4。  
4. **「分析仪钉一个频点就能跟完集群呼叫。」** → 通常要跟 TSCC→Payload；小票指向哪跟到哪。  
5. **「Dedicated / Non-Dedicated 不用问，都一样。」** → 录波策略与「控制是否常在」味道不同。  
6. **「Grant 没 ACK 就是协议坏了。」** → 规范学习口径：Grant **不要求确认**，故常重复。  
7. **「进了业务信道就用不上第 30 课。」** → 相反：进房后正是第 30 课战场。  
8. **「P_GRANT 出现说明又回到控制信道。」** → 可能是业务信道上的再授予/换房。  
9. **「Logical Physical Channel Number 就是 MHz。」** → 先是逻辑号；`0xFFF`/绝对参数深挖留给第 36 课。  
10. **「听不见说明 4FSK/12.5 kHz 坏了。」** → 先定房间与阶段；调制账本最后背锅。

---

## 10. 自测题（含答案）

**题 1.** 用三句话说明：为什么「在 TSCC 上找 Voice LC Header」常常找错柜台？

<details><summary>答案</summary>

TSCC 是前台：跑 RAND/AHOY/ACK/Grant 等叫号信令。Voice LC Header 是客房（Payload）里语音开始的门牌。人还没拿 Grant 改频时，控制录波上本来就不该以 DT=`0001` 当第一期望。

</details>

**题 2.** 画出（文字版即可）MS 从空闲到说话的五步骨架，并标明哪一步离开 TSCC。

<details><summary>答案</summary>

①守 TSCC → ②C_RAND → ③可选 AHOY/ACK → ④Channel Grant → ⑤改频到 Payload 再 Header/超帧。**离开 TSCC 发生在拿到 Grant 之后、进入 Payload 之时。**

</details>

**题 3.** Dedicated TSCC 与 Non-Dedicated TSCC 各用一句现场话说清；并写一个分诊问题。

<details><summary>答案</summary>

Dedicated：专职前台，控制逻辑信道主要干管理。Non-Dedicated：控制与业务共享形态，更省资源但「控制是否一直在」要问清。分诊问题：「本站控制是专用还是共享？」

</details>

**题 4.** 为什么说 Channel Grant「不要求 ACK」却还常在空口重复？对弱场有什么含义？

<details><summary>答案</summary>

学习口径（速览 §1）：Grant 不要求确认，为提高听到概率而常重复发送。弱场含义：漏听小票 → MS 不改频 → 业务侧已有人说话、漏听方却静音；分诊先回放控制下行是否连发、MS 是否跟票。

</details>

**题 5.** 填写：PV_GRANT 与 TV_GRANT 的代表 CSBKO；并各用四字说明业务味道。

<details><summary>答案</summary>

PV_GRANT = `110000`（个呼语音）；TV_GRANT = `110001`（组呼语音）。细字段差异见第 33 课，本课认名+认码即可。

</details>

**题 6.** 判断：分析仪在 TSCC 上看见 TV_GRANT，即可按第 30 课 CP2 开始数超帧 A–F。（对 / 错）并改写正确动作。

<details><summary>答案</summary>

**错。** 正确动作：记录 Grant 中的逻辑物理信道 + 时隙 + 地址 → 改守 Payload → 再按第 30 课认 Header/超帧。

</details>

**题 7.** Part1/2/3/4：下列问题各去哪本？①CSBK 外壳 bit 布局②组呼 Voice Channel User LC③业务信道确认数据④TSCC 上的 Aloha/Grant。

<details><summary>答案</summary>

①Part1 ②Part2 ③Part3 ④Part4（速览 §12）。

</details>

**题 8.** 现场：「同事把 Grant 时间戳和 Voice LC Header 画在同一条常规中继轴上」——你如何纠偏？再补一句调制提醒。

<details><summary>答案</summary>

纠偏：常规轴是 Tier II「固定房间直接 Header」；集群轴是「TSCC 小票 → Payload 再 Header」。两套发车故事不要对齐成一条。调制提醒：选错故事轴不改变 12.5 kHz/4FSK/双时隙——先纠房间与阶段，再查射频。

</details>

**题 9.（加分）** P_GRANT 与 TSCC 上的 PV/TV_GRANT 差在哪一个「房间」？为何本课只给一句指针？

<details><summary>答案</summary>

P_GRANT 出现在**业务信道**（客房内再授予/换房）；PV/TV_GRANT 典型是 **TSCC 前台**发的首张进房小票。本课目标是钉控制 vs 业务，不展开全部 Grant 变体（第 33 课）。

</details>

**题 10.（加分）** 写出 Logical Physical Channel Number 与 Logical Channel Number 各管什么；`0xFFF` 对本课意味着什么（不写公式）？

<details><summary>答案</summary>

前者：12-bit 房间逻辑号（哪条业务逻辑信道）；后者：1-bit 时隙门（ch1/ch2）。`0xFFF` 常表示「逻辑号不够，看绝对频率附块 CG_AP」——公式与 Annex C 留给第 36 课，本课只认「有附块这条岔路」。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `04-集群协议/集群协议字段速览.md` **§1** | TSCC / Dedicated / Payload / Grant 概念总图（本课 canonical） |
| 2 | 同上 **§2** | 控制 PDU 地图（出站 Grant/Aloha/Ahoy…；入站 RAND…） |
| 3 | 同上 **§3** | Grant 代表表（PV/TV 字段骨架；变体指针） |
| 4 | 同上 **§4** | C_ALOHA 代表表（**只扫一眼**；过程 → 第 32 课） |
| 5 | 同上 **§12** | Part1/2/3/4 分工（防串读） |
| 6 | `总索引.md` **集群 / Tier III** | 门牌：TSCC/Grant → 速览 → Reason/Grant 加厚 → Part4 PDF |
| 7 | `04-集群协议/ReasonCode与Grant变体.md` | **仅地图指针**：下节课才深挖；本课别整文件通读 |
| 8 | `学习推送/第9课.md` | Tier I/II/III 全貌回唤 |
| 9 | `学习推送/第25课.md` / `第30课.md` | 常规语音时间线（进 Payload 后接着用） |
| 10 | `学习推送/第11课.md` | 文档地图：Part4 管集群 |
| 11 | `04-集群协议/TS102361-4_V1.12.1.pdf` | 官方集群原文（硬冲突以 TS 为准） |
| 12 | `DMR整合学习手册.md` | 全貌与 Tier 边界 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「停错控制/业务」当成调制故障 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。登记/Aloha 过程、Grant 全变体、Reason 全表、鉴权、绝对频率、Hunt/拨号/Stun：**永远回对应课 / PDF**，本课不补第二份。

---

## 12. 下一课预告

**第 32 课 · 登记与 Aloha**

本课把门钉在「前台 vs 客房 + Grant 小票」。下一课留在前台，把 **登记（我在哪个站/是否允许活跃）** 和 **Aloha（排队规则告示：Mask、Backoff、Reg 位…）** 讲清楚：为什么有的台「没登记就叫不动」、Aloha 广播到底在管什么。仍然少公式；不抢第 33 课的 Grant 全地图，也不抢第 34 课的 Reason 全表。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-03**（晚间推送）检索核验；真实用 HTTP 头/跳转核验过可达（协会镜像 / Tait Academy / GopherTrunk / 产品页等，**ETSI deliver 直链对部分自动化抓取返回 403，故 Part4 以 DMRA 协会镜像为准**）。**不编造地址**。策略 = **Part4 协会镜像 PDF + DMRA Tier III 现状讲稿 + Tait Academy「Channel Operation」+ Tait「Physical and Logical Channels」+ Tait Intro Study Guide + DMRA 标准目录 + Benefits 白皮书 + GopherTrunk CSBK 参考（控制信道 Grant 语感）+ Hytera Tier III 系统页（控制/业务白话）**。另检索公开「control channel vs traffic/payload channel」专题视频：Tait 有 **DMR Tier 3 Introduction** 营销向短片（YouTube 可打开），但是 **效用/行业卖点介绍**，**不是**「TSCC vs Payload + Grant 转台」技术对照课；未找到达到本课深度的独立优质技术短片。**video_found=false**（诚实备注：有 Tier III 概论片，无专门对照片）。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMRA 协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - **为什么值得看**：Tier III 控制/业务、Dedicated/Non-Dedicated、Grant/Aloha 等硬出处；与速览 §1–§3 对照。  
   - **库内副本**：`dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。  
   - **怎么用**：先读系统模型与控制信道模式章节，再回本课总图；**不要**第一天啃完所有 Annex。

2. **[State-of-the-art of ETSI DMR Tier III Standard（DMRA 讲稿 PDF）](https://dmrassociation.org/public-downloads/documents/State-of-the-art-of-ETSI-DMR-Tier-III-Standard-Critical-Comms-Russia-18Apr-2019.pdf)**  
   - **为什么值得看**：用幻灯节奏扫过 Dedicated/Non-Dedicated、控制信道能力、与 Part1–4 关系；适合阶段 E 开门建立「集群功能地图」。  
   - **怎么用**：当「导游图」，细节仍回 Part4 / 速览。

3. **[Tait Radio Academy · Channel Operation](https://www.taitradioacademy.com/topic/dmr-channel-operation-1/)**  
   - **为什么值得看**：白话解释站点上控制信道常落在哪条物理信道/时隙、控制信道主要管登记/呼叫请求/分配逻辑信道/广播系统信息——与本课「前台」比喻同向。  
   - **怎么用**：读完立刻用本课分诊表问自己：分析仪该钉控制还是跟业务。

4. **[Tait Radio Academy · Physical and Logical Channels](https://www.taitradioacademy.com/topic/dmr-physical-and-logical-channels-1/)**  
   - **为什么值得看**：明确 Tier III 上 control vs traffic（payload）逻辑信道分类；多站呼叫时每站业务信道的直觉。  
   - **怎么用**：对照本课术语表「Logical Physical Channel / slot」。

5. **[Tait · Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：Tier III 控制信道 + 业务信道、Channel Grant 建立语音的一段经典叙述（PTT→控制请求→Grant→改到 traffic 通话）。  
   - **怎么用**：当英文版「总图朗读」；与本课 §2 ASCII 对读。

6. **[DMR Association · Standards 目录](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：Part1–4 / TR 下载入口总台；阶段 E 以后找官方 PDF 少迷路。  

7. **[DMR Association · Benefits and Features of DMR（白皮书）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：Tier 分层与容量/双时隙语境；帮新人把「为什么要集群」说给领导听。  
   - **怎么用**：不替代 Part4；当背景阅读。

8. **[GopherTrunk · CSBK 参考](https://gophertrunk.org/reference/csbk/)**  
   - **为什么值得看**：强调 Tier III 控制信道上 CSBK 承载请求与 **channel grant**，解码器靠跟 Grant 跳到正确业务信道+时隙——与本课「分析仪要跟票走」同向。  
   - **怎么用**：当实现/监听语感；字段冲突仍以 ETSI / 速览为准。

9. **[Hytera · DMR Tier 3 Trunking 系统页](https://www.hytera.us/systems/dmr-tier-3-trunking-systems/)**  
   - **为什么值得看**：厂商白话：专用控制信道注册与请求，其余为共享 traffic channel。  
   - **怎么用**：产品叙事；与标准术语对照时以 Part4 为准。

**视频备注（诚实）**：公开可核验的 Tait「DMR Tier 3 Introduction」等短片偏行业价值介绍，**未**按「控制信道 vs 业务信道 + Grant 转台检查点」展开；故本课 **video_found=false**。若日后协会/学院上架专项技术片，再补进进度外链清单。

---

## 本课收束

阶段 E 开门就一件事：**分清前台与客房。**  
前台（TSCC）发号令、发小票；客房（Payload）才跑你已经会的第 30 课语音超帧。  
分析仪要跟票走；Grant 不是「已经在说话」；调制账本仍是 12.5 kHz / 4FSK / 双时隙。  
下一站留在前台：登记与 Aloha。
