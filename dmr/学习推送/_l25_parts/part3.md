（第25课 · 推送 part 3/3）

## 8. 数字账本

| 数字 / 编码 | 含义 | 别记成 |
|-------------|------|--------|
| **30 ms** | 一时隙一突发时长 | ≠ 一列超帧 |
| **60 ms** | 一个 TDMA frame（TS1+TS2） | ≠ 超帧 |
| **360 ms** | 一列语音超帧 A–F | ≠ Hangtime 默认值 |
| **264 bit** | 一突发 | ≠ Full LC 72 |
| **Data Type `0001`** | Voice LC Header | ≠ Terminator |
| **Data Type `0010`** | Terminator with LC | ≠ Idle；≠ CSBK |
| **FLCO `000000`** | Grp_V_Ch_Usr 组呼门牌 | ≠ CSBKO |
| **FLCO `000011`** | UU_V_Ch_Usr 个呼门牌 | ≠ SLCO |
| **CSBKO `111000`** | BS_Dwn_Act | ≠ Header |
| **CSBKO `000100` / `000101`** | UU_V_Req / UU_Ans_Rsp | ≠ 已在语音 |
| **CSBKO `100110`** | NACK_Rsp | ≠ Terminator |
| **CSBKO `111101`** | Pre_CSBK | ≠ Full LC |
| **SLCO `0001`** | Act_Updt（CACH） | ≠ FLCO |
| **Answer Proceed / Deny** | `00100000` / `00100001` | 见资料库 §6.2 |
| **Activity ID `1000` / `1001`** | Group / Individual voice（Act_Updt） | 见资料库 §5.2 |

Hangtime / TxHang 的**具体秒数**是系统/中继配置，不是本课背诵表；岗位记层次，不记「全球统一 3 秒」。

---

## 9. 常见误区（10 则）

1. **「按住 PTT = 立刻语音突发，没有 Header。」**  
   → 常规语音常见先（或伴随）**Voice LC Header** 再进超帧；分析仪上先认 Data Type。

2. **「Terminator 可有可无，反正松键就结束。」**  
   → 规范路径用 Terminator with LC 宣告 EOT；漏收时靠 Hangtime/超时收尾，现象会「拖尾」。

3. **「Hangtime 是中继坏了、载波卡死。」**  
   → 多数是**正常保留**，方便同组回一句；先分 Hangtime vs TxHang vs 真故障。

4. **「迟后进入靠每个 30 ms 重传完整门牌大海报。」**  
   → 靠 **A 的 Voice SYNC + B–E 嵌入拼装**；不是每突发整包 Header。

5. **「Header CRC 失败 = 这通呼叫彻底没了。」**  
   → 嵌入路径仍可能 late entry；分层看（第 22/24 课）。

6. **「组呼和个呼只是地址数字不同，FLCO 无所谓。」**  
   → **FLCO 先分流**（`000000` vs `000011`），地址场语义才跟着变。

7. **「看见 CSBK 就一定是集群 Grant。」**  
   → Tier II 也有唤醒/个呼检查/前导/NACK 等 CSBK；**Grant 叙事留给阶段 E**。

8. **「Voice LC Header 中间也是 Voice SYNC。」**  
   → Header 是**数据壳**，中心是 **Data SYNC** + Slot Type；Voice SYNC 在超帧 **A**。

9. **「Short LC（CACH）就是通话门牌的缩小版。」**  
   → Short LC 是另一套 PDU（第 22 课）；`Act_Updt` 广播活动，不替代 Full LC。

10. **「数据终止 TD_LC（FLCO=110000）就是语音 Terminator。」**  
    → 语音结束是 **Terminator with LC**（Data Type=`0010` + Voice Channel User LC）；TD_LC 属 Part 3 数据挂起。

---

## 10. 自测（8 题）

**题 1.** 用一句话写出「一次语音呼叫」的时间线口诀（含可选 CSBK、Header、超帧、Terminator、Hangtime、Idle）。

<details><summary>参考答案</summary>

一次语音呼叫 =（可选）唤醒/个呼检查 CSBK → Voice LC Header（门牌）→ 超帧 A–F 语音+嵌入 LC（迟到也能上车）→ Terminator with LC（下车）→（中继）Hangtime 保留 → Idle。

</details>

**题 2.** Voice LC Header 与 Terminator with LC 的 Data Type 各是多少？它们通常是否携带同一类 Full LC？

<details><summary>参考答案</summary>

Header = `0001`，Terminator = `0010`。通常携带**同一类** Voice Channel User Full LC（同 FLCO/地址），分别承担发车与下车。

</details>

**题 3.** 组呼与个呼的 FLCO 各是什么别名？

<details><summary>参考答案</summary>

组呼：`000000` = Grp_V_Ch_Usr；个呼：`000011` = UU_V_Ch_Usr。

</details>

**题 4.** BOT/BOC/EOT/EOC 四个缩写各指哪一层边界？为什么「松 PTT」更接近 EOT 而不是 EOC？

<details><summary>参考答案</summary>

BOT=一次发射开始；BOC=整次呼叫开始；EOT=一次发射结束；EOC=整次呼叫结束。松 PTT 结束的是**本段发射**（EOT，常见 Terminator）；中继 Hangtime 过后才更接近 EOC/放空。

</details>

**题 5.** 用户中途开机，错过了 Header，为何仍可能听到后半段组呼？指出两个关键空口元素。

<details><summary>参考答案</summary>

迟后进入：① 超帧 Burst **A** 的 **Voice SYNC** 对齐；② **B–E 嵌入 Full LC**（或后续能拼出的地址 LC）识别组/源。细策略见第 26 课。

</details>

**题 6.** Hangtime 与 TxHang 在岗位上如何一句话区分？

<details><summary>参考答案</summary>

Hangtime：EOT 后**业务/组保留**（同组优先、异组常忙）；TxHang：保留结束后**载波还可再挂多久才关**（常见实现参数名）。先保留、再挂载波、再 Idle。

</details>

**题 7.** 空口上只看到 `UU_V_Req` 和 `NACK_Rsp`，没有 Voice LC Header——通话进入语音段了吗？

<details><summary>参考答案</summary>

没有。仍停在个呼检查/拒绝手续段；进入语音段的标志是 **Voice LC Header（UU_V_Ch_Usr）** 及后续超帧。

</details>

**题 8.** 为什么本课反复强调「不要把 Tier III Grant 当成这条时间线」？

<details><summary>参考答案</summary>

本课是 **Tier II 常规**叙事：门牌靠 Header/嵌入/Terminator，可选 CSBK 做唤醒与个呼检查。Tier III 用控制信道 **Grant** 等另一套状态机（阶段 E），混谈会把「门牌从哪来」讲错。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `02-语音业务/语音业务字段速览.md` **§2** | **本课 canonical 过程表**：阶段↔Data Type↔PDU↔FLCO/CSBKO |
| 2 | 同上 **§3 / §4 / §6 / §8** | Grp/UU Full LC；CSBK 手续；Service Options；Terminator 要点 |
| 3 | `学习推送/第17课.md` | 超帧 A–F、Voice SYNC、late entry 上车点 |
| 4 | `学习推送/第21课.md` | Data Type `0001`/`0010`；EMB/SLOT |
| 5 | `学习推送/第22课.md` | Full LC 三处运载；与 Short LC 边界 |
| 6 | `学习推送/第23课.md` | BS_Dwn_Act / UU_V_* / NACK / Pre_CSBK |
| 7 | `学习推送/第24课.md` | 头/终止 vs 嵌入的保护链原则（不背矩阵） |
| 8 | `01-空中接口/CSBK与LC字段详表.md` | 外壳与 Opcode 详表 |
| 9 | 官方 **TS 102 361-2 V2.5.1** clause **5.2** 等（库内 PDF：`02-语音业务/TS102361-2_V2.5.1.pdf`） | 组呼/个呼过程原文 |
| 10 | 官方 **TS 102 361-1 V2.7.1**（Data Type、late entry 指针 **5.1.2**、超帧图） | 空口壳与超帧 |
| 11 | **TR 102 398** | 系统设计导读，**不是**替代 TS |
| 12 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「听不见」一律怪调制 |

官方版本锚点：**Part2 V2.5.1**（语音业务过程/字段）、**Part1 V2.7.1**（空口/Data Type/超帧）。冲突规则：**TS > TR > 实现博客/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。FEC 矩阵、Idle 比特、符号表：**永远回 PDF**，本课不补第二份。

---

## 12. 下一课预告

**第 26 课 · 补充业务（迟后进入等）**

本课只把「一次语音呼叫」串成时间线，并为 **late entry** 开了一扇窗。下一课进入补充业务与迟后进入细讲：嵌入确认直觉、Talking Party / Talker Alias、紧急与优先级在过程中的位置、Broadcast/OVCM 等如何落在字段上——仍少 SDL、多现场对照。

---

## 13. 推荐阅读与视频

本课外链为 **2026-09-30**（晚间推送）检索核验；真实打开过内容页/PDF/Wiki（HTTP 200 或协会镜像可用）；**不编造地址**。策略 = **Part1/Part2 协会镜像 + TR 导读 + GopherTrunk 门牌/迟入/双时隙文 + MMDVM Hangtime 实现直觉 + Wavecom/hamgear 帧回顾 + 一条可选入门视频（诚实标明非呼叫时间线专题）**。

1. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：Data Type、超帧、late entry 指针（如 **5.1.2**）、SYNC/嵌入总框架——给本课「壳」与「上车点」钉原文。  
   - **适合哪一段**：第 2、4.4、4.5、8、11 节。  
   - **基础**：进阶；英文 PDF；**冲突以该 PDF 为准**。

2. **[ETSI TS 102 361-2 V2.5.1｜Voice services（协会镜像）](https://www.dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：clause **5.2** 组呼/个呼过程、Voice Channel User LC、Terminator/Hangtime 叙述、Service Options——本课业务时间线的硬出处。  
   - **库内副本**：`dmr/02-语音业务/TS102361-2_V2.5.1.pdf`。  
   - **适合哪一段**：第 2、4、6、8、11 节。  
   - **注意**：部分网络对 etsi.org 直链可能 403，以协会镜像或库内 PDF 为准。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TR 102 398 V1.5.1｜General System Design（协会镜像）](https://dmrassociation.org/public-downloads/standards/tr_102398v010501p.pdf)**  
   - **为什么值得看**：系统设计导读，帮助把「呼叫过程」放回整网叙事。  
   - **注意**：TR **不是**规范；冲突以 TS 为准。  
   - **基础**：入门～中级；英文 PDF。

4. **[GopherTrunk｜DMR End to End Part 5：Link Control, Embedded LC & Late Entry](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-05-link-control-late-entry/)**  
   - **为什么值得看**：清楚写出门牌三条运载（Header / Terminator / 嵌入）与 late entry「为何能半路上车」——与本课口诀、例子 D/F 同向。  
   - **适合哪一段**：第 4.3、4.5、7 节。  
   - **注意**：文中实现确认次数等是工程策略，**不以博客条款号替代 ETSI**。  
   - **基础**：中级～进阶；英文网页。

5. **[GopherTrunk｜Operator Cookbook Part 3：Conventional DMR Two Slots](https://gophertrunk.org/blog/tutorials/operator-cookbook-03-conventional-dmr-two-slots/)**  
   - **为什么值得看**：Tier II 双时隙两路通话、Terminator 按目的释放、hangtime 作为收尾后门——帮你建立「时隙独立 + EOT/EOC」现场感。  
   - **适合哪一段**：第 2.4、4.6、6 节。  
   - **基础**：中级；英文网页。

6. **[N4IRS Wiki｜MMDVMHost timers（CallHang / TxHang）](https://github.com/N4IRS/MMDVM-Install/wiki/MMDVMHost-timers)**  
   - **为什么值得看**：用实现语言讲清「通话 Hangtime 保留同组、TxHang 再挂载波」——正好对照本课 §4.6 与例子 E（**不是** ETSI 条文）。  
   - **适合哪一段**：第 4.6、6、9 节。  
   - **基础**：入门～中级；英文 Wiki。

7. **[Wavecom｜Advanced Protocol DMR（PDF）](https://www.wavecom.ch/content/pdf/advanced_protocol_dmr.pdf)**  
   - 帧/突发/超帧图，把 Header→语音→Terminator 钉回 264 结构。厂商综述可能偏早；**硬条款以现行 Part1/2 为准**。

8. **[Alessandro Guido｜How DMR Works — primer PDF（hamgear）](https://hamgear.files.wordpress.com/2014/02/dmr-primer.pdf)**  
   - 培训幻灯式回顾呼叫/LC/时隙名称。年代偏早；以 V2.5.1/V2.7.1 与资料库为准。

9. **[GopherTrunk｜Protocol Decoders Part 5：Bursts, EMB & FLC](https://gophertrunk.org/blog/deep-dives/protocol-decoders-05-dmr-tier-2-3/)**  
   - Data Type 分支、Header vs 嵌入路径、Tier II/III 同线不同状态机——防止把 Grant 叙事塞进本课。

10. **（可选，非专题）[Scanner School｜What is DMR?（YouTube）](https://www.youtube.com/watch?v=aQX_JbTbXuY)**  
    - **为什么可以看**：对完全没听过 DMR 的同事做 10 分钟热身（时隙/色码/谈组口语）。  
    - **诚实标签**：**不是**「Voice Header → 超帧 → Terminator → Hangtime」呼叫时间线专题；看完必须回到本课 §2 / §4。  
    - **基础**：入门；英语视频。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 语音呼叫时间线：可选 CSBK → Voice LC Header → 超帧 A–F（嵌入 LC）→ Terminator with LC → Hangtime → Idle」** 按课堂深度讲透的独立高质量中文/英文短片（多数入门视频只口播双时隙/写频/产品演示）。本课 **`video_found=false`**（无合适的呼叫过程专题视频）；仅附一条可选入门视频并标明「非专题」。建议用：**语音业务字段速览 §2 + Part2 clause 5.2 + 本课总图 + GopherTrunk Part5（End-to-End / Decoders）** 对照自学。

---

*推送说明：本课为阶段 D「语音呼叫过程直觉」开篇课。频谱/调制仅保留短提醒（过程不换频、不改 4FSK/双时隙），不复述加餐全文。主文加厚覆盖动机、PTT 上下车总图与组/个分叉、术语、组呼/个呼/三份门牌/超帧/迟入开窗/Hangtime/Tier II 范围、第 7/15–24 课映射、现场对照、六则 ASCII 时间线例子、数字账本、十则误区、八题自测、资料库路径与核验外链（诚实标明无呼叫时间线专题视频，仅附可选入门视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle/符号表、不发明条款号、不把 Tier III Grant 冒充主线。读完应能向同事讲清「一次语音呼叫怎么上下车、Header/嵌入/Terminator 为何是同一门牌三形态、Hangtime 为何不是坏机」，并进入第 26 课补充业务（迟后进入等）。*
