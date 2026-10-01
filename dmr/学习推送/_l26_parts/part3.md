## 6. 现场岗位对照

| 现场现象 | 补充业务 / 过程解释 | 先查什么 |
|----------|---------------------|----------|
| 中途开机：先静音，约零点几秒后进会 | **Late Entry** 正常：等 Burst A + 拼嵌入 | 组/时隙/色码是否本就对；再看弱场是否导致嵌入连续失败 |
| 分析仪有语音突发，终端一直不开声 | 可能嵌入拼不出、组不匹配、CC 不对；或实现要求「两次一致」未满足 | 抓嵌入 LC / EMB CC；对照本机监听列表；别先换天线 |
| Header CRC/RS 失败，稍后仍听到声音 | 头没赶上，**嵌入路径 late entry** 仍可能上车 | 第 22/24：两条门牌路；不必断言「没 Header 就绝不可能听」 |
| 有声但屏幕无组号/无源 | 语音壳锁了，门牌未拼齐或显示策略滞后 | 等下一两个超帧；查是否只开了「听音频、不解码 LC」类模式 |
| 屏幕突然出现主叫中文/英文名 | **Talker Alias** 嵌入拼齐 | FLCO `000100`–`000111`；与源地址数字对照；别去找「第二路模拟音」 |
| 语音中地图点更新 | **GPS_Info** 嵌入或其它定位路径 | FLCO=`001000`；完整 LIP/轮询细节不在本课死磕 |
| 「没人说话了」却占着组 | **Hangtime**，不是 late entry | 同组回传？CallHang 配置？礼貌/不礼貌？ |
| 把 Hangtime 当成「迟后进入失败」 | 概念反了：Hangtime 在 EOT 后；late entry 在通话中 | 看时间线：还有没有 A–F 语音？还是只剩 Terminator？ |
| CACH 刷 Group voice=`1000` | **Act_Updt** 看板 | 用它感知占用；进组仍靠 Full LC |
| 中继刚睡醒第一通晚半拍 | 可能先走了 **BS_Dwn_Act**；或扫描命中靠 **Pre_CSBK** | 空口开头有没有 CSBK；与「超帧内 late entry」分层看 |
| 紧急键红了仍像普通组呼波形 | Emergency 常是 **Service Options 位** + 过程，不是另调一个载波 | 读门牌贴纸；Act_Updt 是否变 `1100`/`1101` |
| 同事把 Tier III「grant update」教程套到常规中继 | 边界混了 | 问清有没有控制信道；本课主线是嵌入 LC |

写频 / 监听台 30 秒话术：

> 「组呼不是只在开头喊一次『这是 1001 组』。火车开了以后，每隔一列超帧还会把『谁呼谁』撕成四片贴纸贴在车厢上。你晚到，先等车头大标签（Voice SYNC）跳上车，再拼贴纸确认是不是咱们组——拼对了才给你出声。屏幕上的名字是另一叠贴纸（Talker Alias），不是第二根天线。」

---

## 7. 工作例子（6 则）

### 例子 A · 幸福路径：准时听到 Header（对照用）

```text
[Header Grp] → A B C D E F → A B C D E F → … → [Terminator] → Hangtime → Idle
     ↑你在这里开机：门牌整包已到手，超帧直接听
```

要点：迟后进入机制仍在后台重复贴门牌，只是你用不上。

### 例子 B · 经典迟后进入：错过 Header，从第二列超帧上车

```text
真实空口：
  [Header] A B C D E F | A B C D E F | A B C D E F | [Term]
你的接收：              ↑从这里醒
  1) 锁定 Voice SYNC@A
  2) B–E 拼出 Grp=1001, Src=2002, FLCO=组呼
  3) CC/时隙匹配 → 开声（可能已丢掉开头半句语义）
```

### 例子 C · 弱场：Header 坏了，嵌入两次一致后才开声（实现策略示意）

```text
Header RS/CRC 失败
超帧1 嵌入 LC：Grp=1001（先当候选，有的实现仍静音）
超帧2 嵌入 LC：再次 Grp=1001 且一致 → 开声
```

要点：第二次确认是**常见工程策略**；教学上理解「为什么要稳」，不要背成虚构条款。

### 例子 D · Talker Alias：进会之后屏幕才跳出名字

```text
… 超帧中穿插：
  嵌入 Voice Channel User LC   ← 先解决「能不能进」
  嵌入 Talker_Alias_hdr/blk… ← 再拼显示名「张三」
```

要点：别名拼齐可能比进会更晚几个超帧；「先进会、后显示名」是正常现象。

### 例子 E · Hangtime 误判成「迟后进入失败」

```text
已出现 Terminator with LC，BS 仍在 Hangtime 留灯
新来的用户拧到该组：礼貌接入显示忙 / 无法新开
用户说：「我 late entry 不进去！」
其实：车已到站在留灯，不是「车开着拼不出门牌」
```

### 例子 F · Act_Updt 有活动，但本机组列表没有该组

```text
CACH Act_Updt：TS1 Activity=Group voice，hashed 地址某某
本机未编程该组 → 不会因看板自动「进会」
真正进会仍需：本机监听该组 + 嵌入/头中 Full LC 匹配
```

---

## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| 超帧 | 6 burst ≈ **360 ms** | 嵌入门牌重复周期量级 |
| Burst A 中心 | Voice SYNC（48 bit 场） | 上车点 |
| B–E | 嵌入碎片 + EMB | 拼 Full LC |
| Header Data Type | `0001` | 整包门牌壳 |
| Terminator Data Type | `0010` | 下车壳 |
| 组呼 FLCO | `000000` | Grp_V_Ch_Usr |
| 个呼 FLCO | `000011` | UU_V_Ch_Usr |
| Talker Alias FLCO | `000100`–`000111` | 头 + 三块 |
| GPS_Info FLCO | `001000` | 嵌入位置 |
| Act_Updt SLCO | `0001` | CACH 活动看板 |
| BS_Dwn_Act CSBKO | `111000` | 唤醒出站 |
| Pre_CSBK CSBKO | `111101` | 前导 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 不换频不改调 |

---

## 9. 十则误区（看见就打回）

1. **「补充业务是第三种能单独拨打的电话。」** → 多数是主呼叫上的加料。  
2. **「迟后进入=永远听不见。」** → 恰恰相反：设计就是让你半路听得见。  
3. **「必须听到 Voice LC Header 才能进组。」** → Header 最好，但嵌入路径就是为错过头准备的。  
4. **「每个 30 ms 都会重贴一份完整地址。」** → 完整拼装节奏跟超帧/嵌入碎片走，不是每时隙一份新门牌。  
5. **「Hangtime 就是迟后进入。」** → 一个在通话中上车，一个在 EOT 后留灯。  
6. **「Talker Alias 是另开一路模拟音。」** → 嵌在语音超帧的 Full LC 乘客。  
7. **「Act_Updt 有组呼活动=我已经进组。」** → 看板≠门牌匹配。  
8. **「迟后进入失败一定是天线坏了。」** → 先查组/CC/时隙/嵌入是否可读，再查 L1。  
9. **「实现里『确认两次嵌入』=规范新 PDU。」** → 工程策略，不是另发明单据。  
10. **「集群 Grant 更新教程可以直接当 Tier II 迟后进入讲义。」** → 边界不同；本课主线是嵌入 LC。

---

## 10. 自测题（含答案）

**题 1.** 用一句话区分：基本语音呼叫（Tele-service）vs 补充业务（Supplementary）。

<details><summary>答案</summary>

基本语音呼叫是用户点的主菜（组呼/个呼等时间线）；补充业务是贴在主菜上的加料（迟后进入、别名、紧急位等），多数不能脱离主呼叫单独「另打一通补充电话」。

</details>

**题 2.** 迟后进入的「两步上车」分别等什么？为什么听感常常是「先静半拍再进会」？

<details><summary>答案</summary>

步骤 1：等到 Burst **A** 的 **Voice SYNC**，对齐超帧；步骤 2：用 **B–E 嵌入**拼出地址 Full LC，并做色码/组（或个号）/时隙匹配。静半拍，是因为最多大约要等一个超帧量级的 SYNC 机会，且门牌拼齐前接收机可能先不开声——不是永远听不到。

</details>

**题 3.** 判断：错过 Voice LC Header 就绝对不可能听到正在进行的组呼。（对 / 错）并说明为什么。

<details><summary>答案</summary>

**错。** 嵌入路径会周期性重复贴同类门牌；这正是 Late Entry 的设计意图。Header 是最干净的整包，但不是唯一门票。

</details>

**题 4.** Talker Alias 的 FLCO 范围是什么？它和 Late Entry 用的 Voice Channel User LC 有何分工？

<details><summary>答案</summary>

FLCO **`000100`–`000111`**（头 + block1/2/3）。Voice Channel User LC 解决「这通是不是我的组/个呼」（进不进得去）；Talker Alias 解决「屏幕显示主叫什么名字」。二者都可走嵌入，职责不同。

</details>

**题 5.** 现场：「没人说话了却占着组」——更应先怀疑 Late Entry 还是 Hangtime？空口上可能看见什么？

<details><summary>答案</summary>

更应先怀疑 **Hangtime**（EOT 后保留）。空口常见 BS 继续下发 **Terminator with LC** 等保留指示；此时不是「车开着拼不出门牌」的 late entry 场景。

</details>

**题 6.** Act_Updt 在哪里走？它能不能替代嵌入 Full LC 完成进组判断？

<details><summary>答案</summary>

走 **CACH Short LC**（SLCO=`0001`）。**不能**替代：它是两槽活动类型 + hashed 地址的小看板；进组仍靠头/嵌入中的话务 Full LC 与本机监听匹配。

</details>

**题 7.** BS_Dwn_Act 与 Pre_CSBK 和迟后进入是什么关系？（各用一句话）

<details><summary>答案</summary>

**BS_Dwn_Act**：唤醒 BS 出站，让信道上「有车可收」——不是嵌入拼门牌本身。**Pre_CSBK**：给扫描/节电台垫前导提高命中——帮「赶上」后续块，不是 Voice SYNC 上车点。二者是边缘「帮你赶上」的手续；迟后进入是超帧内认门牌的机制。

</details>

**题 8.** 为什么本课要把 Tier III「grant update 式 late entry」划到边界外？

<details><summary>答案</summary>

因为那是**控制信道周期性重播业务信道分配**的集群叙事；本课主线是 **Tier II 常规**下语音超帧 **Voice SYNC + 嵌入 LC**。两套都可能被口语叫 late entry，但空口载体与阶段不同，混讲会把 Grant 故事错误塞进 Header/嵌入时间线。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `02-语音业务/语音业务字段速览.md` **§7** | **补充业务概念→字段** canonical 表 |
| 2 | 同上 **§2** | 过程阶段表；Late entry 一句指针 |
| 3 | 同上 **§3.3–3.5 / §5.2 / §6** | GPS / Talker Alias；Act_Updt；Service Options |
| 4 | `学习推送/第13课.md` §6 | 补充业务地图与三层分类 |
| 5 | `学习推送/第17课.md` §4.3 | 两步上车故事 |
| 6 | `学习推送/第22课.md` | Full LC 三路径；嵌入证明 late entry |
| 7 | `学习推送/第18课.md` / `第23课.md` | CACH Act_Updt；BS_Dwn_Act / Pre_CSBK |
| 8 | `学习推送/第25课.md` | 呼叫时间线；本课窗口的前文 |
| 9 | `00-入门/DMR术语与帧结构速查卡.md` | 超帧 / 264 / CACH 一页墙 |
| 10 | `DMR整合学习手册.md` §5 | 业务全景里对补充业务的总述 |
| 11 | 官方 **TS 102 361-2 V2.5.1**（库内 PDF：`02-语音业务/TS102361-2_V2.5.1.pdf`） | 组/个呼过程、补充与字段原文 |
| 12 | 官方 **TS 102 361-1 V2.7.1** **5.1.2** 一带 | 超帧与 late entry 空口指针 |
| 13 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「听不见」一律怪调制 |

官方版本锚点：**Part2 V2.5.1**、**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。FEC 矩阵、Idle 比特、符号表：**永远回 PDF**，本课不补第二份。

---

## 12. 下一课预告

**第 27 课 · PDP：确认与非确认数据**

语音主菜与补充加料（本课）告一段落。下一课进入 **Part 3 数据主战场**：分组数据协议（PDP）里确认数据与非确认数据怎么分、空口上大致长什么样、和语音时间线如何共用同一条 12.5 kHz / 双时隙载波——仍少公式，多现场对照，并提醒：短数据/头压缩细讲在第 28 课。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-01**（上午推送）检索核验；真实打开过内容页/PDF（HTTP 200 或协会镜像可用）；**不编造地址**。策略 = **Part2 协会镜像 + Feature Evolution 嵌入图 + Benefits 白皮书迟入句 + GopherTrunk 门牌/嵌入/迟入/别名深文 + Decoders 帧路径 + 一篇通俗 Late Entry 专文（意文，机制同向）**。

1. **[ETSI TS 102 361-2 V2.5.1｜Voice services（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：组呼/个呼过程、Voice Channel User LC、Talker Alias / GPS PDU、Service Options、补充相关叙述——本课字段硬出处。  
   - **库内副本**：`dmr/02-语音业务/TS102361-2_V2.5.1.pdf`。  
   - **适合哪一段**：第 4、6、8、11 节。  
   - **基础**：进阶；英文 PDF。

2. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：超帧 **5.1.2**、SYNC/嵌入总框架——给「上车点」钉空口原文。  
   - **适合哪一段**：第 2、4.3、11 节。  
   - **基础**：进阶；英文 PDF。

3. **[DMR Association｜DMR Feature Evolution（PDF）](https://dmrassociation.org/public-downloads/documents/DMR_Association_DMR_Feature_Evolution.pdf)**  
   - **为什么值得看**：「Embedding Data within Voice」一页画出 A=Voice SYNC、B–E=Embedded，并写明嵌入 initially 用于 **Late Entry**（呼叫类型、源/目的 ID、业务选项）；同材料亦讲 Talker Alias / 嵌入位置语感。  
   - **适合哪一段**：第 2、4.2–4.4 节。  
   - **基础**：入门～中级；英文幻灯 PDF。

4. **[DMR Association｜Benefits and Features of DMR（白皮书 PDF）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：用产品/用户语言写 Late Entry「持续提供 call-in-progress updates」——适合给领导/新同事的一句话语感。  
   - **注意**：白皮书不是 TS；冲突以 Part1/2 为准。  
   - **基础**：入门；英文 PDF。

5. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
   - **为什么值得看**：把门牌三条运载、B–E 拼装、header-less late entry、Talker Alias 拼装写成同一条故事线——本课例子 B/C/D 的加厚版。  
   - **适合哪一段**：第 4.3–4.4、7 节。  
   - **注意**：文中「确认两次嵌入 / ~720 ms」等是**工程策略**，**不以博客条款号替代 ETSI**。  
   - **基础**：中级～进阶；英文网页。

6. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - **为什么值得看**：EMB/LCSS、嵌入重装、FLCO 列表（含 Talker Alias / GPS）——防止把 Short LC 与 Full LC 搅乱。  
   - **适合哪一段**：第 4.3、4.5、5 节。  
   - **基础**：中级～进阶；英文网页。

7. **[D2ALP｜Late Entry nel DMR（通俗专文，意文）](https://www.d2alp.it/late-entry-nel-dmr-entrare-in-una-comunicazione-gia-iniziata/)**  
   - **为什么值得看**：专门解释「通话已开始仍能加入」、Header vs Embedded LC、与 Talker Alias 的分工；机制叙述与本课同向，适合非英语同事对照。  
   - **注意**：通俗博客；**硬条款以 ETSI PDF / 资料库为准**。  
   - **基础**：入门～中级；意大利文网页（浏览器翻译可用）。

8. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读，帮助把补充能力放回整网叙事。  
   - **注意**：TR **不是**规范。  
   - **基础**：入门～中级；英文 PDF。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 补充业务 + Tier II 迟后进入：Voice SYNC@A + 嵌入 Full LC 拼门牌 + Talker Alias/GPS 乘客分工 + Hangtime 对照」** 按课堂深度讲透的独立高质量中文/英文短片（多数视频只口播写频/双时隙/产品演示，或讲 P25/集群扫描器）。本课 **`video_found=false`**。建议用：**语音业务字段速览 §7 + Feature Evolution 嵌入图 + GopherTrunk E2E Part5 + 本课总图** 对照自学。

---

*推送说明：本课为阶段 D「补充业务（迟后进入等）」专课。频谱/调制仅保留短提醒（加料不换频、不改 4FSK/双时隙），不复述加餐全文。主文加厚覆盖动机、主菜加料总图与两步上车、术语、补充全景、迟后进入细讲、别名/GPS/Act_Updt/边缘 CSBK、Hangtime 对照、Tier III 边界、现场分诊、六则例子、账本、十则误区、八题自测、资料库路径与核验外链（诚实标明无合适公开专题视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle/符号表、不发明条款号、不把 Tier III Grant 更新冒充本课主线。读完应能向同事讲清「补充业务是加料不是第三道主菜、迟后进入两步怎么上车、别名与门牌如何分工、Hangtime 为何不是 late entry」，并进入第 27 课 PDP。*
