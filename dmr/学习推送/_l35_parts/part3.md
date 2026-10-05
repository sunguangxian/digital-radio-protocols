---

## 9. 现场分诊表：「鉴权没过」先查什么

按顺序走，**越靠前越常见、越便宜**：

| 步 | 问题 | 怎么看 | 指向 |
|----|------|--------|------|
| ① | **真的是鉴权问题吗？** | NACK（`0x2A/0x2B`）前面有没有 C_AHOY（1110₂，Source 是题）+ C_ACKU（0x48）？ | 没有 → 不是鉴权，回第 32/34 课查登记/开户 |
| ② | **手台交卷了吗？** | 出题之后有没有 C_ACKU 0x48？ | 没有 → 手台不支持/未开启鉴权，或入站没收到 → 这时才查覆盖与射频 |
| ③ | **这台的 K 在网管里吗、对吗？** | 网管里这个个号有没有 K 记录；是不是刚写频改过 K 而网管没同步 | 一机一钥：**个号 ↔ K** 必须一一对上 |
| ④ | **PSN 两边用法一致吗？** | 网络启用了 PSN？这台手台支持 PSN 吗？录的是不是这台机器现在的 PSN？ | **返厂换板、借机调号**最常踩 |
| ⑤ | **是不是个号写错/串号？** | 手台自报的个号对应的 K，是不是另一台机器的 | 两台机器共用一个个号时，至少有一台永远过不了 |
| ⑥ | **网络侧算法/工具链对吗？** | 用 §5.3 的测试向量喂网管/测试仪：`7A17C0` + `01…10` 应出 `E8CA1D` | 新上线的第三方网管、自研测试工具先过这关 |
| ⑦ | **反向场景（Stun/Kill）** | 手台回 `0x14` Recipient_Refused？ | 手台不认网络的答案：网络侧那台手台的 K 是否正确 |

**口诀**：**先确认有题有答，再查钥匙，再查钢印，最后才查射频。**

---

## 10. 现场对照：日常工作里它长什么样

### 10.1 开通鉴权的工作流（概念版，具体菜单以厂商为准）

```text
  采购/入库 ──► 用厂商工具读出每台手台的 PSN（若启用）
       │
       ▼
  写频 ──► 为每台手台写入 K（128 bit）+ 个号
       │
       ▼
  网管 ──► 为每个个号录入同一 K（+ PSN）；打开「需要鉴权」开关
       │
       ▼
  试点 ──► 先拿几台手台在一个站登记；分析仪确认看到「题—答—Reg_Accepted」
       │
       ▼
  推广 ──► 分批开；每批先抽查；保留「个号 ↔ K ↔ PSN ↔ 机身序列号」对照表（妥善保管！）
```

开源控制器 dmrtc 的配置就是这个思路的极简版：配置文件里为每个个号存一把 K，打开「需要鉴权」后，**没存 K 的个号直接回登记 Denied**，存了的就出题、比答案。

### 10.2 工作例子（8 则）

1. **新站开鉴权，B 批 40 台全部登记不上**：分析仪看到每台都有题有答（0x48），随后 `0x2B`。→ 第③步：B 批的 K 导入文件格式错位（例如十六进制大小写/字节序问题），网管存的 K 不对。修导入后恢复。  
2. **一台返厂机回来就登记不上，其余正常**：有题有答，随后拒绝。→ 第④步：维修换了主板，PSN 变了；用工具重新读 PSN、更新网管。  
3. **一台老型号手台开鉴权后登记不上**：分析仪看到网络出题，**手台始终不回 C_ACKU**，TNP_Timer 到期后它去找别的 TSCC。→ 第②步：这款不支持鉴权（或固件没开），不是射频问题；处理方式是升级固件或给它豁免。  
4. **监听软件把 C_ACKU 的 Target 显示成「呼叫 15780125」**：新人以为 1001 在个呼一个不存在的号。→ 那是答案 `0xF0C91D`（举例数值）被当成地址显示了；看 Reason=0x48 就知道是交卷。  
5. **没人按 PTT，分析仪上却周期性出现「C_AHOY → C_ACKU」**：Mirror=0。→ §6.3 独立鉴权轮询，网络在抽查，正常现象。  
6. **遥毙下发后，手台回 `0x14`**：→ §6.4 反向鉴权失败：手台不认网络的答案。查网络侧这台的 K；**千万别反复重发 Kill 去「碰运气」**，先把钥匙对上。  
7. **Stun 下发后，手台回 `0x00`**：→ MSNot_Supported，这款不支持 Stun/Revive，和鉴权无关。  
8. **安全审计问「你们空口传不传密钥」**：→ 不传。空口只有 24 bit 题和 24 bit 答；K 与 PSN 只在手台和网管里（§3）。但要补一句：**鉴权不加密话音**（§8.3）。

---

## 11. 术语账本 / 口袋速查

### 11.1 白话术语表

| 术语 | 英文 | 白话 |
|------|------|------|
| 鉴权 | Authentication | 验证「你手里有没有这台设备的钥匙」 |
| 挑战 | Challenge（RAND） | 出题方当场生成的 24 bit 随机题 |
| 响应 | Response | 用钥匙把题算出来的 24 bit 答案 |
| 鉴权钥匙 | Authentication Key（K） | 每台 128 bit，手台和网络各一份，永不上空口 |
| 物理序列号 | PSN | 出厂固化、改不掉的 ≥3 字节钢印号；可选地 XOR 进答案 |
| 密钥流发生器 | Keystream generator | 本课里就是 RC4：吃进钥匙、吐出一串伪随机字节 |
| 重放 | Replay | 把偷听到的旧答案拿来再用；靠「每次换题」防住 |
| 克隆 | Cloning | 把别人的个号/钥匙复制到另一台机器；PSN 专门防它 |
| 反向鉴权 | MS authenticates TS | 手台出题验网络；只在 Stun/Revive/Kill 出现 |
| 确认+邀请 | Ackvitation（C_ACKVIT） | 手台对 Stun/Kill 命令的「收到，但请先答题」 |
| AUTHI | Authentication Identifier | 鉴权网关号 `FF FECD₁₆`（Table A.8） |
| 独立轮询 | Authentication poll | 不依附登记/呼叫的抽查；Mirror=`000 0000₂` |

### 11.2 口袋速查：本课最常用的值

| 值 | 是什么 | 在哪 |
|----|--------|------|
| CSBKO **28** `011100₂` | C_AHOY（网络出题） | Oct0 = `0x9C` |
| CSBKO **33** `100001₂` | C_ACKU（手台交卷） | Oct0 = `0xA1` |
| CSBKO **32** `100000₂` | C_ACKD（网络交卷 / 判卷） | Oct0 = `0xA0` |
| CSBKO **30** `011110₂` | C_ACKVIT（手台出题） | Oct0 = `0x9E` |
| Service_Kind **`1110₂`** | 登记 / 鉴权 / 无线检查 | C_AHOY 的 Oct3 低 4 位 |
| Service_Kind **`1101₂`** | Stun/Revive/Kill（补充业务） | C_ACKVIT |
| Reason **0x48** | 手台交卷 Authentication Response（ACK · d=0） | C_ACKU，原始 Oct3 = `0x90` |
| Reason **0x64** | 网络交卷 Authentication Response（ACK · d=1） | C_ACKD，原始 Oct3 = `0xC8` |
| Reason **0x62** | Reg_Accepted（鉴权通过后的登记成功） | C_ACKD |
| Reason **0x2A / 0x2B** | Reg_Refused / Reg_Denied（鉴权失败也走这里） | C_NACKD |
| Reason **0x44** | MS_Accepted（反向鉴权通过并执行） | C_ACKU |
| Reason **0x14** | Recipient_Refused（反向鉴权失败，不执行） | C_NACKU |
| Reason **0x00** | MSNot_Supported（不支持 Stun/Revive） | C_NACKU |
| 题的范围 | `00 0000₁₆ … FF FCDF₁₆` | Table 6.17 |
| AUTHI | `FF FECD₁₆` | Table A.8 |

### 11.3 数字与符号账本

| 数 | 含义 |
|----|------|
| **128** | K 的位数（16 字节） |
| **≥3** | PSN 的字节数（计算用 3 字节） |
| **24** | 题、答、地址的位数（所以题和答能借住在地址栏） |
| **19** | RC4 的密钥长度：3 字节题 + 16 字节 K |
| **259 / 256 / 3** | RC4 吐 259 字节，丢前 256，取末 3 |
| **16 776 416** | 合法题的个数（`0xFFFCDF + 1`） |
| **1 / 16 777 216** | 瞎猜一次答案猜中的概率（\(1/2^{24}\)） |
| `7A17C0` / `01…10` / `E8CA1D` / `E9C81E` | 官方测试向量（无 PSN / PSN=`010203`） |
| `‖` | 拼接（前后接起来） |
| `XOR` / `⊕` | 异或：同为 0、异为 1；任何数 XOR 0 不变 |

---

## 12. 十则误区（看见就打回）

1. **「鉴权就是把密码发给网络核对。」** ✗ 密码（K）从不上空口；上空口的是**题和答**。  
2. **「Colour Code 对了就说明手台合法。」** ✗ Colour Code 只说明「同一个站」，任何写频的人都能设。  
3. **「看见 `0x2A/0x2B` 就是鉴权失败。」** ✗ 那是登记拒绝的通用理由；**往前翻有没有题和答**才能下结论。  
4. **「C_ACKU 的 Target 就是被叫号码。」** ✗ Reason=0x48 时，Target 栏装的是**答案**。  
5. **「C_AHOY 就是点名被叫。」** ✗ Service_Kind=1110₂、Source 是题时，它是**出题**。  
6. **「0x48 和 0x64 是两个不同的东西。」** 半对：名字都叫 Authentication Response，**d 位不同**——0x48 是手台交卷，0x64 是网络交卷。  
7. **「开了 PSN 就更安全，所以先开了再说。」** ✗ 没先把每台的 PSN 录全，一开就是一片登记不上。  
8. **「RC4 被淘汰了，所以 DMR 鉴权等于没有。」** ✗ 用法不同（§8.2）；真正要盯的是 K 的生成与保管、题的随机性。  
9. **「鉴权过了，通话就加密了。」** ✗ 鉴权不派生会话密钥；加密是另一套规范、另一把钥匙（§8.3）。  
10. **「遥毙被拒就多发几次。」** ✗ `0x14` 是手台不认网络的答案，重发同一个错答案没用；先查钥匙。

---

## 13. 自测题（含答案）

**题 1.** 用旅馆比喻各一句话：K、PSN、RAND、Response。

<details><summary>答案</summary>

K = 只有你和前台有的密码本；PSN = 机器身上改不掉的钢印号；RAND = 前台每次新印的题卡；Response = 你用密码本把题算出来、念给前台的答案。

</details>

**题 2.** 四个量里，哪两个上空口、哪两个不上？各多宽？

<details><summary>答案</summary>

上空口：RAND（24 bit）、Response（24 bit）。不上：K（128 bit）、PSN（≥3 字节，计算用 3 字节）。

</details>

**题 3.** 登记 + 鉴权的四步 PDU 依次是什么？题和答分别在哪个栏？

<details><summary>答案</summary>

C_RAND（登记请求）→ C_AHOY（Service_Kind=1110₂，**Source = 题**）→ C_ACKU（Reason=0x48，**Target = 答**）→ C_ACKD Reg_Accepted 或 C_NACKD Reg_Refused/Denied。

</details>

**题 4.** 用一句话复述答案的算法。

<details><summary>答案</summary>

把 RAND（3 字节）和 K（16 字节）按「RAND 在前、K 在后」拼成 19 字节作为 RC4 的密钥，生成 259 字节密钥流，丢掉前 256 字节，最后 3 字节就是答案；若启用 PSN，再与 PSN 逐字节 XOR。

</details>

**题 5.** 无 PSN 时答案是 `E8 CA 1D`，PSN = `01 02 03`，有 PSN 的答案是多少？

<details><summary>答案</summary>

`E9 C8 1E`（E8⊕01、CA⊕02、1D⊕03），与 Table 6.16 一致。

</details>

**题 6.** 原始字节 `A1 00 00 90 F0 C9 1D 00 03 E9`，这是什么 PDU？谁发的？交卷了没有？答案是多少？

<details><summary>答案</summary>

Oct0 = `0xA1` → LB=1、CSBKO=33 → C_ACKU（手台发）。Reason = `((0x00&1)<<7) | (0x90>>1)` = 0x48 → 鉴权交卷。答案在 Target：`F0C91D`；交卷手台个号 `0x0003E9` = 1001。

</details>

**题 7.** 题的范围为什么到 `FF FCDF₁₆` 就停了？

<details><summary>答案</summary>

题要借住在 C_AHOY 的 Source 地址栏里，上面 `FF FEC0₁₆` 起是网关号（REGI、STUNI、AUTHI、KILLI 等），题不能和网关号撞车，否则会被误读成来自某个网关。

</details>

**题 8.** 0x48 和 0x64 都叫 Authentication Response，怎么区分？各出现在什么场景？

<details><summary>答案</summary>

拆 d 位：0x48 = `01 0 01000`，d=0，手台交卷，出现在 C_ACKU（网络验手台：登记/呼叫/轮询）；0x64 = `01 1 00100`，d=1，网络交卷，出现在 C_ACKD（手台验网络：Stun/Revive/Kill）。

</details>

**题 9.** 画出 Kill 的反向鉴权四步，并说出成功和失败各回什么。

<details><summary>答案</summary>

C_AHOY（KILLI，命令）→ C_ACKVIT（手台出题，Target=题）→ C_ACKD（0x64，AddInfo=网络答案）→ 手台判卷：对上回 C_ACKU MS_Accepted（0x44）并执行；对不上回 C_NACKU Recipient_Refused（0x14），不执行。

</details>

**题 10.** 为什么 Kill 必须鉴权，Stun 却是可选的？

<details><summary>答案</summary>

Kill 是永久的，被 Kill 的手台丧失全部 DMR 功能，任何空口消息都救不回来；如果能被冒充的网络随便 Kill，后果不可逆。Stun 可以用 Revive 撤销，所以规范把它的鉴权留作可选。

</details>

**题 11.** 看见一条 `C_NACKD 0x2B`，怎么判断它是不是「鉴权失败」引起的？

<details><summary>答案</summary>

往前翻同一台手台的信令：如果紧挨着有 C_AHOY（1110₂，Source=题）+ C_ACKU（0x48），才是鉴权没过导致的登记拒绝；如果没有题和答，就是别的登记拒绝原因。规范没有专门的「鉴权失败」Reason。

</details>

**题 12.** 网络出了题，手台一直不回 C_ACKU，最后去找别的 TSCC。先怀疑什么？

<details><summary>答案</summary>

先怀疑手台不支持/未开启鉴权，其次才是入站覆盖或干扰（交卷没被收到）。手台离开是因为 TNP_Timer 到期，按 6.4.4.1.6 重新进入找 TSCC 的流程。

</details>

**题 13.** 一台返厂维修的手台回来后鉴权一直失败，其余手台正常。最可能的原因？

<details><summary>答案</summary>

维修换了主板，PSN 变了，而网络启用了 PSN、网管里还是旧 PSN。用厂商工具重新读 PSN 并更新网管。

</details>

**题 14.** 「独立鉴权轮询」的 C_AHOY 和「登记中的鉴权」C_AHOY，字段上怎么区分？

<details><summary>答案</summary>

看 Service_Options_Mirror：独立轮询为 `000 0000₂`；登记/呼叫建立中则回拷对应 C_RAND 的 Service_Options。

</details>

**题 15.** 同事说「我们用的是 RC4，RC4 被 RFC 禁了，所以鉴权没用」。你怎么回？

<details><summary>答案</summary>

RFC 7465 禁的是 TLS 里拿 RC4 加密大量数据；DMR 鉴权只拿它当搅拌机、丢掉开头 256 字节后取 3 字节，用法不同。真正要盯的是 K 是否随机生成并妥善保管、题是否足够随机、答案只有 24 bit、以及平时只有网络验手台。另外鉴权不等于话音加密。

</details>

**题 16.** 一个改题实验：K 不变，题从 `7A17C0` 改成 `7A17C1`，答案会是 `E8CA1C` 或 `E8CA1E` 这种「差一点」的值吗？

<details><summary>答案</summary>

不会。原料差一位，RC4 的输出就面目全非；本课实测为 `973F09`。这正是偷听者无法「从旧答案推新答案」的直觉原因。

</details>

---

## 14. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `04-集群协议/鉴权与AnnexC频率.md` **§0–§1** | 鉴权怎么接到空口；本 TS 写了什么、没写什么（本课 §8.1 来源） |
| 2 | 同上 **§2** | K / PSN / 题 / 答四个量 |
| 3 | 同上 **§3–§4** | C_AHOY / C_ACKU / C_ACKD / C_ACKVIT 字段表（本课 canonical） |
| 4 | 同上 **§5** | 鉴权用到的 Reason 交叉 |
| 5 | 同上 **§6** | 过程摘要：算法直觉、TS 验 MS、MS 验 TS、Table 6.7 地址对照 |
| 6 | `04-集群协议/ReasonCode与Grant变体.md` **§8.2** | 鉴权 / 无线检查过程中的固定 Reason |
| 7 | `04-集群协议/Stun_DGNA_UDT与定时器.md` **§1.3–§1.4** | 带鉴权的 Stun/Kill 时序与字段（第 39 课再细讲） |
| 8 | `学习推送/第32课.md` / `第34课.md` | 登记；Reason 读法与跨字节坑 |
| 9 | `总索引.md` **集群 / Tier III** | 门牌导航（「鉴权、RAND、K、PSN、RC4 边界」一行） |
| 10 | `04-集群协议/TS102361-4_V1.12.1.pdf` | 官方原文 6.4.4.1.5、6.4.8、6.4.9.2、6.4.10；Tables 6.15–6.26；Fig 6.20 / 6.30 / 6.32 / 6.33 |

官方版本锚点：**Part4 V1.12.1 (2023-07)**。冲突规则：**TS > TR > 厂商文档 > 开源实现 > 课文笔记**。频率换算、Hunt、拨号、Stun 状态机：**回对应课 / PDF**，本课不补第二份。

---

## 15. 下一课预告

**第 36 课 · 频率 CHAN / 绝对频率**

第 33 课的 Grant 小票上写着「去几号房」——那个「几号」是 12 bit 的**逻辑信道号 CHAN**。下一课回答：**手台拿到 CHAN 之后，到底调到哪个频率上去？** 我们会讲固定信道计划（fbase、信道间隔、双工分裂）、灵活计划、以及 CHAN = `0xFFF` 时 Grant 后面跟着的那块「**绝对频率**」续块怎么读——也正好把你最弱的「频率与带宽」再巩固一遍。资料就在本课同一个文件 `鉴权与AnnexC频率.md` 的**第二部分**。

记住边界：**本课的鉴权决定「让不让你进门」；下一课的 CHAN 决定「进门后去哪个房间、那房间在哪个频率」。**

---

## 16. 推荐阅读与视频

本课外链均为 **2026-10-05**（晚间推送）检索并用 HTTP 请求核验可达（返回 200）。**不编造地址**。ETSI 官网直链对自动化抓取不稳定，Part4 以 DMR 协会镜像为准。另检索了「DMR Tier III authentication challenge response」相关公开视频：能找到 Tier III 概论与产品宣传片，**没有**找到专讲 DMR 鉴权流程的技术视频；找到一个讲同类思想（共享密钥 + 一次性计算）的优质通用视频，见第 6 条。**video_found=true（通用概念视频，非 DMR 专项）**。

1. **[ETSI TS 102 361-4 V1.12.1｜DMR trunking protocol（DMR 协会镜像 PDF）](https://www.dmrassociation.org/public-downloads/standards/ts_10236104v011201p.pdf)**  
   - **为什么值得看**：6.4.8 鉴权（含 RC4 一句话与测试向量）、6.4.4.1.5 登记中鉴权、6.4.9.2 / 6.4.10 Stun/Kill 反向鉴权的硬出处。  
   - **库内副本**：`dmr/04-集群协议/TS102361-4_V1.12.1.pdf`。  
   - **怎么用**：6.4.8.0 只有两段话，**逐句读**；然后对着本课 §5.3 自己核一遍 Table 6.15 / 6.16。

2. **[qradiolink/dmrtc · rc4.cpp（开源 Tier III 控制器的鉴权实现）](https://github.com/qradiolink/dmrtc/blob/master/src/rc4.cpp)**  
   - **为什么值得看**：文件头注释直接引用 6.4.8.0，代码就是本课 §5.1 四步的 C++ 版：题和 K 拼成 19 字节、生成 259 字节、取第 256–258 下标的 3 字节；还把超范围的题钳到 `0xFFFCDF`。  
   - **怎么用**：再看同仓库的 [controller.cpp](https://github.com/qradiolink/dmrtc/blob/master/src/controller.cpp)，搜 `getCBF() == 0x90`（交卷识别，对应本课 §4.5）和 `createReplyRegistrationDenied`（答错时回登记 Denied，对应 §7）。它是业余爱好者的概念验证实现，**不是标准**，冲突以 ETSI 为准。

3. **[Wikipedia · Challenge–response authentication](https://en.wikipedia.org/wiki/Challenge%E2%80%93response_authentication)**  
   - **为什么值得看**：用通用语言讲清「出题—答题、秘密不上线、每次换题防重放、双向鉴权」——正好对应本课 §2 和 §6.4。  
   - **怎么用**：读开头几段和 mutual authentication 一段即可；把里面的 server/client 换成 TSCC/MS。

4. **[Wikipedia · RC4](https://en.wikipedia.org/wiki/RC4)**（也有 [中文版](https://zh.wikipedia.org/wiki/RC4)）  
   - **为什么值得看**：RC4 的密钥调度和输出过程只有十几行伪代码，和本课 §5.3 的 Python 一一对应；Security 部分解释了「开头字节有偏差」以及 RC4-drop[n]「先丢掉开头」的对策——这就是 DMR「弃 256」的背景。  
   - **怎么用**：只读算法伪代码和 Security 的前半部分；攻击论文细节不属于本课范围。

5. **[RFC 7465 · Prohibiting RC4 Cipher Suites](https://www.rfc-editor.org/rfc/rfc7465)**  
   - **为什么值得看**：「RC4 被淘汰」这句话的原始出处——它禁的是 **TLS 里的 RC4 加密套件**。读完你就能准确回答 §13 题 15。  
   - **怎么用**：只看 Introduction 一页。

6. **[Computerphile · 2FA: Two Factor Authentication（视频）](https://www.youtube.com/watch?v=ZXFYT-BG2So)**  
   - **为什么值得看**：讲手机验证码（HOTP/TOTP）怎么用**双方共享的秘密 + 一个每次都变的输入**算出一次性数字——和 DMR 鉴权「共享 K + 每次换的题」是同一类思想，画板讲解很直观。  
   - **怎么用**：把视频里的「时间计数器」换成「网络出的 RAND」，把「HMAC」换成「RC4 取 3 字节」，就是 DMR 鉴权。**注意它讲的不是 DMR**，只借它建立直觉。

7. **[GopherTrunk · DMR CSBK payloads](https://gophertrunk.org/reference/dmr-csbk-payloads/)**  
   - **为什么值得看**：一张表看全 Tier III 常见 CSBKO，帮你把 C_AHOY / C_ACKVIT / C_ACKU / C_ACKD 放回整张控制消息地图里。  
   - **怎么用**：认名认码；和 ETSI 有出入时以 ETSI 为准（第 34 课已练过一次）。

**视频备注（诚实）**：公开视频里没有专讲「DMR Tier III 挑战–响应鉴权 + RC4 用法」的技术片；第 6 条是通用概念视频。本课所需能力，标准 PDF + 一份开源实现 + 两篇百科 + 一份 RFC 已经足够。日后如果 DMR 协会或厂商学院上架相关技术片，再补进来。

---

## 本课收束

阶段 E 第五站就一件事：**前台凭什么相信你是你。**  
谁怀疑谁出题：平时网络出题（C_AHOY），手台交卷（C_ACKU 0x48）；遥晕遥毙时手台出题（C_ACKVIT），网络交卷（C_ACKD 0x64）。  
题和答各 24 bit，借住在地址栏；钥匙 K 和钢印 PSN 永不出门。  
答案 = RC4(题‖K) 的第 257–259 字节，可选再 XOR PSN——测试向量 `7A17C0 → E8CA1D` 你已经亲手核过。  
鉴权失败没有专门的 Reason，看见登记拒绝先往前翻有没有题和答。  
鉴权是入网门禁，不是话音加密；RC4 的边界，要分清「用在哪」。  
能看见完整的题和答，就先别怀疑调制——12.5 kHz / 4FSK / 双时隙一直没变。  
下一站：拿到房号（CHAN）之后，房间到底在哪个频率。
