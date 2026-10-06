### 7.5 C_MOVE：直接命令你去（7.1.1.1.3；Table 7.17）

字段（Table 7.17）：LB / PF / CSBKO（`11 1001₂` = 57）/ FID ｜ Reserved 9 ｜ **Mask** 5（与 Aloha 同类，可点名一部分手台）｜ Reserved 5 ｜ **Reg** 1（置 1 = 新 TSCC **要求**变为活跃前登记）｜ Backoff 4 ｜ Reserved 4 ｜ **Physical Channel Number** 12（0 无效；1…4094 单块；4095 → MV_AP）｜ MS address 24。

收到适用的 C_MOVE → 记下 CONT → 离开当前 TSCC（6.3.3.1 e）→ **Commanded 单信道猎**（3 个时隙内能收）→ 确认 → 看 Reg 决定要不要登记。

### 7.6 一句话收拢

**Ann_WD 改「地图」（手台应照办）；Adjacent_Site 给「提示」（怎么用不规定）；Vote_Now 发「邀请」（优先级怎么用厂商定）；C_MOVE 下「命令」（离开并单信道猎）。**

---

## 8. 丢了怎么办、找到以后怎么办：离开 TSCC 与登记分岔

### 8.1 什么时候离开 TSCC、重新猎（6.3.3.1）

手台在 TSCC 上「活跃但空闲」时，出现下面任何一条就回到猎站：

| # | 情况 | 回到哪一段 |
|---|------|-----------|
| a | 确认后误码率**劣于**驻留门限（§5.1） | 重新猎 |
| b | C_SYScode 与验证过的值**连续 NSYSerr 次**不同（Table A.6：1…3）；**只变了 PAR** 时，仅当本类手台不再被允许才必须走 | 重新猎 |
| c | **T_Nosig** 秒内收不到任何可解码 TSCC PDU（Table A.1：1…15 s） | 重新猎 |
| d | 用户换网 | 有记录走 Commanded，否则 Short |
| e | 收到适用于本手台的 **C_MOVE**，记下 CONT | Commanded |
| f | 登记收到 **C_NACKD(Reg_Denied)**（0x2B） | **登记前所处的那一段** |
| g | 确认后登记收到 **C_NACKD(Reg_Refused)**（0x2A） | **登记前所处的那一段** |
| h | 确认后登记随机接入超时（NRand_NR 次或 TRand_TC，2…60 s） | **登记前所处的那一段** |
| i | 确认后**非登记**业务的随机接入超时 | 离开 TSCC |

**f/g/h 那句「回到登记前所处的那一段」**是本课最容易被忽略的一点：如果手台是在 **Comprehensive 扫到第 80 号**时找到这个 TSCC、登记被拒，它就接着从全范围猎继续，**不是**回到 Resume 重新来。

**正在等信令时**（6.3.3.2，比如已经发了呼叫请求在等回音）：只有 **b、c、e** 三种情况才离开；而且在猎站和重新确认期间，**保持「等信令」状态和相关定时器**——换了个 TSCC，那次呼叫请求的「等待」还算数。

### 8.2 确认之后：三条岔路（6.4.3）

手台**确认 TSCC 之前不得做任何随机接入**。确认以后三条岔路：

| 岔路 | 条件 | 动作 |
|------|------|------|
| a | **Reg = 0**（C_ALOHA 和 CACH 里的 Reg 必须一致） | 不登记、不改登记记录，可直接发起呼叫 |
| b | 本片区 SYS_AREA 在**被拒登记名单**里 | 无权接入，继续猎 |
| c | 没有本片区的**成功登记记录** | 随机接入登记（第 32 课，可能带鉴权，第 35 课） |

c 的四种结局：

| 结局 | 手台怎么做 | 出处 |
|------|-----------|------|
| **Reg_Accepted** 0x62 | 记下 SYS_AREA，替换旧记录 ✔ | 6.4.4.1.2 |
| **Reg_Refused** 0x2A | 继续猎；确认 TSCC、收到合适 C_ALOHA 后重新登记 | 6.4.4.1.3 |
| **Reg_Denied** 0x2B | SYS_AREA 记入被拒名单，进入 TSCC 获取流程 | 6.4.4.1.4 |
| 等不到回音（TNP_Timer 到期） | 进入 TSCC 获取流程 | 6.4.4.1.6 |

几个必须记住的细节：

- **登记之前只许发两样**：登记随机接入请求，或对鉴权挑战的应答（6.4.3）。所以「手台在 TSCC 上、却打不出电话」，先看它是不是还没登记成功（网络会回 `MS_Not_Registered`，第 34 课）。  
- **Refused 会乒乓，Denied 才稳**：6.4.4.1.0 原意——终答是 Refused 时手台继续猎；**找不到别的允许接入的 TSCC，就回到这个 TSCC 重复登记**；系统负载高时这会造成**大量登记业务**。终答是 Denied 时，片区记入被拒名单，6.4.3 b) 禁止手台再向这个 TSCC 登记。所以规范说：**Registration Denied 是把手台从某个 TSCC 拒掉的首选终答。**  
- **登记记录关机保留，被拒名单关机清空**（Table 6.8）。另外 6.4.4.1.9：TSCC 要求登记时，手台在**开机或换网**时要登记。

---

## 9. 把整套流程走一遍（教学虚构情景）

**写频（虚构）**：短名单 = [37, 37, 52, 101, 空…]（37 写两遍＝偏置）；Low…High = 1…160，Comp_Flag = False；Large、NET 5、ContCAT A、站点授权表为空、DMRLA 6；门牌表用第 36 课的固定计划；「最近确认 TSCC」记录 = **52**。

| 步 | 发生了什么 | 对应 |
|----|-----------|------|
| 1 | 开机，有记录 52 → 3 个时隙内调到 CHAN 52 | Commanded（D.1.2.1 b） |
| 2 | 52 上有 TSCC 同步 → 候选；CACH 高 14 位 = `10 1010 0010 0100₂`（0x2A24）→ MODEL Large、NET `1010₂` = 10 ≠ 5 | 验证 b 不过 → **马上走** |
| 3 | Commanded 失败 → Short；随机起点落在第 4 格（101），第一遍只要「够强」 | D.1.2.3 |
| 4 | 101 低于 L_Short，第一遍跳过；绕回第 1 格 37：够强，CACH = 0x2513 | Fig D.1 |
| 5 | 等到 C_ALOHA：完整 C_SYScode 0x944F → a b c d 全过；SYS_AREA 4 不在被拒名单 | §4.6 |
| 6 | 质量过猎站门限 → **确认**；读色码 5；记「最近确认 = 37」 | 6.3.2.3 / 6.3.2.4 |
| 7 | Reg = 1、无片区 4 记录 → 登记 → Reg_Accepted → 记下 SYS_AREA 4 | 6.4.3 c |
| 8 | 收到 Ann_WD_TSCC：撤 52（AW_FLAG1 = 1），加 101（AW_FLAG2 = 0，色码 3）——就是自测题 5 那条 | §7.1 |
| 9 | 进地下车库，T_Nosig 内无可解码 PDU → 离开 TSCC 进入猎站 | 6.3.3.1 c |
| 10 | 出车库：短名单在 37 / 101 间转，37 先够强 → 确认；片区 4 已登记，**不用再登记** | 6.4.3 |

> 第 2 步的纪律：CACH 只有 **14 位**（去掉了 PAR），别把它当 16 位拆；读到 NET 就够判了。「**先确认位数再拆**」和第 34 课的跨字节坑是同一类错。

---

## 10. 现场分诊表：「找网慢 / 找不到网 / 来回跳」

| 症状 | 先怀疑 | 怎么核 | 本课 |
|------|--------|--------|------|
| 开机「搜索中」很久，别的机子几秒就好 | 没有「最近确认 TSCC」记录；短名单里没有当前 TSCC 号，一路扫到 Comprehensive | 读写频：短名单、Low/High、Comp_Flag；看手台上网后停在哪个号 | §6.2–§6.4 |
| **永远**上不去，扫频仪看到 TSCC 在发 | ① 号不在短名单且 Comp_Flag = True ② 门牌表把号算错了频率 ③ 验证不过：MODEL / NET / 站点授权表 / PAR 与 ContCAT ④ SYS_AREA 在被拒名单里 | 按 ①→④ 逐条；④ 关机重开即清 | §4、§6.4；第 36 课 |
| 只有**一部分**手台上不了某个 TSCC | **PAR 与 ContCAT**（双 TSCC 负载分担）；或这批手台站点授权表不含该站 | 读这批机的 ContCAT 和授权表 | §4.4 |
| 新加控制信道，老手台不去 | 短名单没有新号，网络没发 Ann_WD_TSCC 加号；或新号超出 Low…High | 分析仪看有没有 C_BCAST type `0 0000₂` 带这个号 | §7.1–§7.2 |
| 拆了旧控制信道，开机总先去旧频点 | 记着「最近确认 TSCC」= 旧号（Commanded），短名单也还留着 | 发 Ann_WD 撤号；让手台在新 TSCC 确认一次 | §6.2 |
| 两站交界，登记被拒后来回跳，控制信道登记请求暴增 | 网络用 **Reg_Refused**：找不到别的就回来再登记 | 看 C_NACKD Reason：0x2A 还是 0x2B；想赶走用 **Reg_Denied** | §8.2 |
| 被拒以后很久不再去那片 | Denied 名单 + T_DENREG | 看 T_DENREG；关机清空 | §4.5 |
| 出地下室 / 隧道后很久才恢复 | T_Nosig 到期后在别的号上转圈；短名单太长或起点随机落在远处 | 短名单精简、把本区 TSCC 多写几格做偏置 | §6.3、§8.1 |
| 手台在 TSCC 上，但打不出电话 | 还没登记成功（Reg = 1 时登记前只能发登记请求） | 看是否收到 `MS_Not_Registered` | §8.2 |

**分诊口诀**：**先问「它在试哪些号」（名单、范围、记录）→ 再问「号对应的频率对不对」（第 36 课门牌表）→ 再问「听到了为什么不认」（验证五步）→ 再问「认了为什么不留」（确认门限）→ 最后问「留了为什么不能用」（登记分岔）。**

**写频检查单（概念版，菜单名以厂商为准）**：短名单与重复次数｜Low / High｜Comp_Flag｜MODEL / NET｜ContCAT｜站点授权表｜DMRLA｜门牌表。**网络侧**：Ann_WD 是否随改造更新｜CH_ADJ 是否指向现役 TSCC｜Vote_Now 优先级「全带或全不带」｜拒登记用 Refused 还是 Denied｜T_DENREG。

---

## 11. 术语账本 / 口袋速查

| 速查项 | 值 / 出处 |
|--------|-----------|
| 四段顺序 | Resume → Commanded → Short → Comprehensive（D.1.0） |
| Resume / Commanded 时限 | 2 个 TDMA 帧 / 3 个时隙（D.1.1 / D.1.2.1） |
| 短名单 | Nmax_Ch = 50（最少）；建议存储 64；可重复；空槽可忽略 |
| 全范围 | Low_Comp_Ch 1…4 095；High_Comp_Ch Low…4 095；Comp_Flag = True 关闭 |
| 门限 | L_Upper_SHort / L_Lower_SHort / L_Squelch，单位数值厂商定（Table A.7） |
| C_SYScode | 16 bit = MODEL 2 + NET + SITE + PAR 2；CACH 只带高 14 位 |
| PAR | 00 保留 / 01 仅 A / 10 仅 B / 11 A+B |
| 离开 TSCC | NSYSerr 1…3；T_Nosig 1…15 s；TRand_TC 2…60 s |
| 被拒名单 | ≥ 8 条 FIFO；T_DENREG 0 或 1…1 000（× 10 s） |
| 广播 | C_BCAST CSBKO 40；Ann_WD `0 0000₂`、Vote_Now `0 0010₂`、Adjacent_Site `0 0110₂` |
| Vote_Now | VOTE_BLK 2…10 TDMA 帧；优先级 1 最高…7 最低，0 非优选；Ch_Pref 50 |
| C_MOVE | CSBKO 57；Reg 位；4095 → MV_AP |

---

## 12. 八则误区（看见就打回）

1. **「听到同步就上去。」**——那只是候选；要过验证和确认。  
2. **「找到 TSCC 就能发。」**——确认前绝不发射；Reg = 1 时登记成功前只能发登记请求。  
3. **「猎站失败就从头来。」**——登记失败回到**登记前那一段**；Resume / Commanded 失败进 Short。  
4. **「短名单越长越好。」**——越长扫一遍越慢；该做的是把本区 TSCC **多写几格**偏置。  
5. **「L_Short 是 −xx dBm。」**——规范只说单位数值厂商定。  
6. **「Adjacent_Site 是命令。」**——是提示；命令是 C_MOVE。  
7. **「Refused 和 Denied 差不多。」**——Refused 会让手台回来再试（可能乒乓），Denied 进黑名单。  
8. **「CACH 里就是完整系统码。」**——只有高 14 位，没有 PAR。

---

## 13. 自测题（含答案）

**题 1.** 手台刚开机，存有「最近确认 TSCC」记录。按顺序写出它可能经历的猎站段，以及每段失败去哪。

<details><summary>答案</summary>

Commanded（单信道猎记录的号）→ 失败进 Short → 失败进 Comprehensive（除非 Comp_Flag = True，则留在 Short、门限改 L_Squelch）→ 失败重复 Comprehensive，可插播 Short。

</details>

**题 2.** 「验证」五步各查什么？哪一步「没存就不查」？

<details><summary>答案</summary>

MODEL、NET、SITE（站点接入授权数据）、PAR（对 ContCAT）、SYS_AREA（不在被拒登记名单）。SITE 授权数据一条都没存时不查。

</details>

**题 3.** 拆 C_SYScode `0x5A6D`：模型、NET、SITE、PAR？若 DMRLA = 4，SYS_AREA 是多少？

<details><summary>答案</summary>

`0101 1010 0110 1101₂`：MODEL `01` = Small → NET 7 位 `0110 100` = 52，SITE 5 位 `11011` = 27，PAR `01` = 只允许 A 类。SYS_AREA = SITE 高 4 位 `1101₂` = 13。

</details>

**题 4.** Short Hunt 名单「至少多少、建议多少、能不能重复、怎么动态改」？

<details><summary>答案</summary>

Nmax_Ch = 50（Table A.6，最少数目）；D.1.0 建议存储最多 64 个值；同一号可重复写以偏置；收到本网 C_BCAST Ann_WD_TSCC 按 AW_FLAG 加入（0）或撤出（1），加入的号关机保留。

</details>

**题 5.** 拆这条单块 CSBK：`A8 00 00 01 D3 94 4F 03 40 65`。

<details><summary>答案</summary>

Oct0 `A8` → LB 1、CSBKO 40 → C_BCAST；Oct1 FID 0。Oct2–4 连起来 `00000 000 │ 0000 0001 │ 1101 0011`：type `0 0000₂` = Ann_WD_TSCC；Parms1 = Reserved `0000`、CC_CH1 `0000`、CC_CH2 `0011` = 3、AW_FLAG1 = **1（撤出）**、AW_FLAG2 = **0（加入）**；Reg = 1；Backoff = 3。系统码 0x944F。Oct7–9 `03 40 65` → BCAST_CH1 = 0x034 = **52**，BCAST_CH2 = 0x065 = **101**。意思：短名单撤掉 52、加入 101（色码 3）。

</details>

**题 6.** 手台在 Comprehensive 扫到某号，确认了 TSCC，登记收到 Reg_Refused。接下来呢？换成 Reg_Denied 呢？

<details><summary>答案</summary>

都回到登记前所处的那一段（Comprehensive）继续猎（6.3.3.1 f/g）。Refused：若找不到别的允许接入的 TSCC，会回来重新登记（负载高时可能造成大量登记）。Denied：该 SYS_AREA 记入被拒名单，之后验证第五步就把这个 TSCC 排除，直到关机或 T_DENREG 到期。

</details>

**题 7.** 正在等一次呼叫的回音，哪几种情况会让手台离开 TSCC？离开后那次「等待」怎么办？

<details><summary>答案</summary>

只有 6.3.3.1 的 b（C_SYScode 连续不符）、c（T_Nosig）、e（C_MOVE）。猎站和重新确认期间保持等信令状态和相关定时器（6.3.3.2）。

</details>

**题 8.** 一个站有两个 TSCC，PAR 分别是 `01₂` 和 `10₂`。某批手台只上第二个，另一批只上第一个，正常吗？若某批手台两个都上不去呢？

<details><summary>答案</summary>

正常：这是用 PAR + ContCAT 做负载分担，A 类上 PAR = 01 的、B 类上 PAR = 10 的。两个都上不去：先查这批手台的 ContCAT 写频（以及 MODEL / NET / 站点授权表），再查片区是否在被拒名单里。

</details>

**题 9.** Resume 和 Commanded 的时限各是多少？分别从什么时刻算起？

<details><summary>答案</summary>

Resume：从 P_CLEAR 结束、最后一条 P_MAINT(DISCON) 结束、地址不匹配的 P_AUTH 结束或非主叫按结束呼叫起，2 个 TDMA 帧内应能收到老 TSCC（D.1.1）。Commanded：从适用的 C_MOVE 结束、或带有效记录的开机 / 换网起，3 个时隙内应能收到被点名信道（D.1.2.1）。

</details>

**题 10（思考）.** 为什么规范要求随机起点？为什么要两个门限？

<details><summary>答案</summary>

随机起点：防止所有手台偏向同一个物理信道（例如全网重启后都挤到名单第一格的 TSCC 上登记）。两个门限：进门门槛高于离开门槛，留出回差，避免信号在门槛附近抖动时手台乒乓。

</details>

---

## 14. 资料库加深

| 路径 | 看什么 |
|------|--------|
| `04-集群协议/AnnexD猎站Hunt.md` | 四段猎站、Short vs Comprehensive、A.6/A.7、Fig D.1 文字流 |
| `04-集群协议/Announcement与其余枚举.md` §3.1 / §3.3 / §3.7 / §5 | Ann_WD_TSCC、Vote_Now、Adjacent_Site、C_MOVE |
| `04-集群协议/Stun_DGNA_UDT与定时器.md` | T_Nosig、TRand_TC、Nmax_Ch、Comp_Flag |
| `04-集群协议/ReasonCode与Grant变体.md` | Reg_Accepted / Refused / Denied |
| `学习推送/第32课.md` / `第34课.md` / `第36课.md`；`总索引.md` 集群 / Tier III | 登记、拒因、门牌表；「猎站、Hunt、Comp_Flag」一行 |
| `04-集群协议/TS102361-4_V1.12.1.pdf` | **Annex D 全部（约 5 页）**；5.1.0–5.1.2；6.3.0–6.3.3.2；6.4.2–6.4.4.1.9；6.7.1.1 / .3 / .7；Tables 6.4 / 6.5 / 6.8 / 6.81 / 7.17 / 7.20 / 7.69 / 7.71 / 7.79 / A.1 / A.6 / A.7 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 厂商文档 > 开源实现 > 课文笔记**。Annex D 是资料性附录，但它引用的验证与确认（clause 6.3）是**规范性**要求。

---

## 15. 下一课预告

**第 38 课 · 拨号与本地编址**

到这里，手台已经能**找到网、留在网上、丢了再找回来**。下一课回答：**用户在键盘上按的那串号码，怎么变成空口上的 24 bit 地址？**规范 Annex E（车队编号与拨号方案）和 Annex G（本地编址）都是资料性附录，我们会把「用户看到的号」和「空口跑的地址」分开讲。

记住边界：**本课决定「在哪个控制信道上」；下一课决定「在控制信道上叫谁」。**

---

## 16. 推荐阅读与视频

本课外链均为 **2026-10-06**（晚间推送）检索，并用 HTTP 请求或页面抓取核验可达、内容对口。**不编造地址**。另检索了「DMR Tier III control channel hunting / roaming」公开视频：**没有**找到专讲 DMR 猎站的技术视频；找到一个讲**蜂窝网空闲态小区重选**（排序、门限、回差、定时器）的通用视频，概念和本课高度同构，见第 7 条。**video_found=true（通用概念视频，非 DMR 专项）**。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMR 协会镜像 PDF）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - Annex D（约 5 页）是猎站框架的唯一出处，6.3 的验证 / 确认 / 离开 TSCC 是硬要求。库内副本 `dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。**怎么用**：先读 Annex D，再读 6.3，再拿本课 §9 走一遍。

2. **[MPT 1327：A Signalling Standard for Trunked Private Land Mobile Radio Systems（1997 版，sigidwiki 存档 PDF）](https://www.sigidwiki.com/images/8/85/Mpt1327.pdf)**  
   - DMR Tier III 的「祖先」。它的 6.2.1.1「控制信道获取」与 Part 4 的 6.3.0 几乎逐句对应（可全面猎也可参考存储；收到合适系统码前不得活跃；明显得不到服务就尽快离开），还写了「离开业务信道先回上次的控制信道，除非 CLEAR 另有指示」——就是 Resume。**怎么用**：只读 6.2.1 和 adjacent site / vote now advice 两段广播。

3. **[GopherTrunk · Trunking Engine, Part 12: Control-Channel Hunting, the Call Watchdog & Testing With a Fake Bus](https://gophertrunk.org/blog/deep-dives/trunking-engine-12-cc-hunting-watchdog-testing/)**  
   - 开源扫描器的猎站：候选逐个驻留、首个锁定即停、**把上次锁定的频率排到最前**（带记忆的搜索）、全失败就退避。**怎么用**：读「Finding the control channel」「When nothing locks」。它**只收不发**，没有登记和确认门限。

4. **[GopherTrunk · DMR End to End, Part 8: Tier III Trunking — C_ALOHA, Grants & LCNs](https://gophertrunk.org/blog/deep-dives/dmr-end-to-end-08-tier3-trunking/)**  
   - 扫描器靠 **C_ALOHA 里的系统码**锁定 Tier III 控制信道，再从 **C_BCAST（Adjacent_Site 等）**收集邻站——对应本课 §4.2、§7.3。**怎么用**：读「Lock on C_ALOHA, learn from C_BCAST」。它的「锁定」比本课的验证 + 确认宽松得多。

5. **[QRadioLink · Implementation of a DMR Tier III trunked radio Base Station Transceiver in Software Defined Radio](https://www.qradiolink.org/DMR-tier-3-trunked-radio-BTS-software-defined-radio.html)**  
   - 开源 Tier III 控制器作者实测：「**猎站序列配置正确**时，手台开机会检测到控制信道并发起登记」；支持固定 / 灵活猎站信道计划；广播邻站信息，由**终端按自己的信号准则**决定漫游——即 §7.3「提示而非命令」。**怎么用**：读「DMR trunking controller」。页面顶部注明该软件已被新软件取代；业余概念验证，**不是标准**。

6. **[Telecommunications4dummies · Idle Mode Behavior in LTE – Part 1](https://telecommunications4dummies.com/2021/02/08/idle-mode/)**  
   - 手机找小区：**先试上次驻留的小区 → 再用存储信息 → 都没有才扫全部频段**，再用门限判断能否驻留——和 Resume → Short → Comprehensive + 确认门限几乎一一对应。**怎么用**：读「Cell Selection」两节，RSRP≈电平、RSRQ≈质量。**它是 LTE，不是 DMR。**

7. **[Uniinfo · Idle Mode Procedures: Cell Reselection (Part-1)（视频）](https://www.youtube.com/watch?v=7-g7ebh0b7A)**  
   - 空闲态手机怎么给小区**排序、加回差（Qhyst）、等 Treselection** 再决定换不换——帮你理解 §5.1 的「两个门限 / 回差」和 §7.4 的优先级。**怎么用**：只看排序、回差、定时器；5G 专有名词可跳过。**讲的是 5G 蜂窝网，不是 DMR。**

**视频备注（诚实）**：没有专讲 DMR Tier III 猎站的公开技术视频；第 7 条是蜂窝网选站的通用视频。标准 Annex D + 6.3 + MPT 1327 + 开源笔记已足够支撑本课。

---

## 本课收束

阶段 E 第七站：**手里一堆号码，怎么找到那个能用的控制信道。**  
顺序：Resume → Commanded → Short（≥ 50、建议 64 槽、可重复、广播可加减）→ Comprehensive（Low…High，可被 Comp_Flag 关掉）。  
两道关：验证（MODEL / NET / SITE / PAR / SYS_AREA）+ 确认（电平或误码过门限）；确认前绝不发射。  
网络帮忙：Ann_WD 改名单、Adjacent_Site 给提示、Vote_Now 请你去看、C_MOVE 命令你去。  
找到以后：Reg = 0 或已有记录就直接用，否则登记；Refused 会乒乓，Denied 进黑名单；失败回登记前那一段。  
每个号都要过第 36 课的门牌表——号码错了，猎得再勤也白跑。  
下一站：找到网之后，键盘上按的号码怎么变成地址——拨号与本地编址。
