## 4. 机制拆解：查表路径

### 4.1 总索引怎么进（30 秒 + 关键词 + 角色）

打开 `dmr/总索引.md`，先看三块（编号以库内为准）：

| 节 | 用途 | 本课怎么用 |
|----|------|------------|
| **§0** 30 秒怎么用 | 新人/墙上速查/附录覆盖/关键词入口 | 迷路时先回这里 |
| **§1** 文档目录 | 按文件夹列 md + PDF | 确认「语音速览在 02/」「数据速览在 03/」 |
| **§2** 关键词 → 文档 | 物理/语音/数据/集群/TR 五张检索表 | **日常主入口** |
| **§3** 官方 PDF 版本 | Part1 V2.7.1、Part2 V2.5.1、Part3 V1.3.1… | 报版本号、对争议 |
| **§4** 角色最小打开集 | 新人 / 空口 / 语音 / 数据 / 集群 | 岗位培训起点 |
| **§5** 刻意不收入 | FEC 矩阵、Idle 转储等 | 提醒本课硬禁令 |

**语音侧**关键词（总索引 §2「语音 / 补充业务」摘要）：个呼、组呼、迟后进入、主叫识别、FLCO、CSBKO、Service Options → **语音业务字段速览**。  
**数据侧**关键词：PDP、确认/非确认、C_HEAD、U_HEAD、DPF、SAP、短数据、UDP/IPv4 头压缩 → **数据协议字段速览**。

### 4.2 Part2 字段文怎么查（走一遍 TOC）

文件：`02-语音业务/语音业务字段速览.md`  
源声明：ETSI **TS 102 361-2 V2.5.1 (2023-05)**；公共外壳见 Part1 与 `01-空中接口/CSBK与LC字段详表.md`。

| 速览节 | 标题（库内） | 什么时候进 |
|--------|--------------|------------|
| **§1** | Opcode 速查（Annex B） | 手里有 FLCO/CSBKO/SLCO **数值** |
| **§1.1** | FLCO Table B.1 | Grp/UU Voice User、Talker Alias、GPS、TD_LC 指针 |
| **§1.2** | CSBKO Table B.2 | UU_V_Req/Ans、NACK、BS_Dwn_Act、Pre_CSBK、CT_CSBK |
| **§1.3** | SLCO Table B.3 | Nul_Msg / Act_Updt |
| **§2** | 语音呼叫过程与空口 PDU 对照 | **只有现象**（个呼检查、语音开始/结束、扫描前导） |
| **§3** | Full LC 业务 PDU | 已知 PDU 名：Grp_V_Ch_Usr / UU_V_Ch_Usr / GPS / Talker Alias |
| **§4** | CSBK 业务 PDU | 已知 CSBK 名：UU_V_Req、NACK_Rsp… |
| **§5** | Short LC（CACH） | 时隙活动、哈希地址、紧急活动 ID |
| **§6** | Service Options 与相关 IE | Emergency / Broadcast / Priority / Answer / Reason |
| **§7** | 补充业务相关字段 | Late Entry、Talker Alias、Emergency…概念→字段落点 |
| **§8** | 语音 Terminator 要点 | Data Type=`0010`；与 TD_LC 分家 |
| **§9** | 缺口 | CT_CSBK 全状态机、Privacy、Tier III 建链等——**停** |

**三种入口（必背）**：

```text
  A. 按 Opcode 值
     分析仪：FLCO=000100 → §1.1 → Talker_Alias_hdr → 需要字段细节再 §3.4
     分析仪：CSBKO=000100 → §1.2 → UU_V_Req → §4.2

  B. 按现象 / 过程阶段
     「个呼存在性检查没应答」→ §2 表「个呼存在性检查」行
       → UU_V_Req / UU_Ans_Rsp / NACK → 再进 §4.2–§4.4

  C. 按 PDU 名
     同事说「看一下 Pre_CSBK」→ §4.5；「Service Options Emergency」→ §6.1
```

**Part2 边界提醒（写进纪律）**：

- EMB / SLOT / Data Type / 突发壳 → **Part1**（`帧结构与字段定义.md`、`CSBK与LC字段详表.md`），不是 Part2 速览主战场。  
- FLCO=`110000` **TD_LC** 在 Part2 §1.1 只是对照指针——数据终止细节在 **Part3 §6**。  
- Tier III 控制信道语音建立（C_GRANT 等）→ **Part4** 集群速览；Part2 §9 已写缺口。

### 4.3 Part3 字段文怎么查（走一遍 TOC）

文件：`03-数据协议/数据协议字段速览.md`  
源声明：ETSI **TS 102 361-3 V1.3.1 (2017-10)**；头/块位宽硬表多在 **Part1 clause 8–9**。

| 速览节 | 标题（库内） | 什么时候进 |
|--------|--------------|------------|
| **§1** | 与 Part1 的衔接 | 手里有 **DPF / SAP**；或要确认 Data Type 角色 |
| **§2** | C_HEAD / U_HEAD 逐比特 | 确认 vs 非确认头字段差（A/FMF/S/N(S)…） |
| **§3** | 续块 / 末块载荷 | Rate ½·¾·1；DBSN / MsgCRC 差别 |
| **§4** | 确认响应（C_RHEAD / C_RDATA） | 无 ACK、NACK、SACK、Class/Type/Status |
| **§5** | 短数据头 | SP / R / DD_HEAD（+ UDT/P 指针）——第 28 课货架 |
| **§6** | TD_LC | 数据 hangtime Terminator |
| **§7** | UDP/IPv4 压缩头 | SAID/DAID/SPID/DPID / EH——第 28 课货架 |
| **§8** | 数据呼叫与 Data Type 速查 | **只有现象**时的总表入口 |
| **§9** | 缺口 | TCP HC 无完整表、UDT Opcode→Part4、ARP 未展开——**停** |

**三种入口（必背）**：

```text
  A. 按 DPF / SAP
     DPF=0011 → 确认数据 → §2 C_HEAD + §3 续块 +（要回执）§4
     DPF=1110 + 无续块 → §5.1 SP_HEAD（别先骂丢包）
     SAP=0011 → §7 UDP HC；SAP=0010 → §9 诚实：仅预留，不编造 TCP 表

  B. 按现象
     丢包 / 无 ACK / 解不出 IP / 状态码
       → §8 总表定 PDU 家族 → 再进 §2/§4/§5/§7

  C. 硬出处何时回 Part1
     三头位宽、DPF/SAP 枚举争议 → Part1 Tables **9.17A–C** / **9.30–9.31**
     （速览 §1/§5 已指向；实现认证以 PDF 为准）
```

**Part3 边界提醒（写进纪律）**：

- 业务信道短数据（三姐妹）≠ **Part4 UDT/控制信道**短数据过程。  
- TCP HC：SAP 有编码，Part3 V1.3.1 **无**与 UDP 对等完整八位组表 → **不编造**（§9）。  
- C_HEAD/U_HEAD 外壳 Data Type=`0110` 的定义在 Part1；Part3 讲业务语义与过程字段。

### 4.4 边界对照一张表（防串架）

| 问题 | 正确书架 | 常见错架 |
|------|----------|----------|
| EMB / Colour Code / Data Type 枚举 | Part1 帧结构 / CSBK详表 | 在 Part2 里找「突发壳」 |
| FLCO / 语音 Service Options / UU_V_Req | Part2 速览 | 在 Part3 里找个呼 CSBK |
| C_HEAD / DPF / 短数据三姐妹 / UDP HC | Part3 速览（+ Part1 硬表） | 在 Part2 里找 Data Header |
| Tier III 控制信道 UDT Opcode | Part4 | 在 Part3 §5.4 指针处硬编 UDTO 表 |
| TD_LC（数据终止） | Part3 §6（Part2 §1 仅对照） | 当成 Grp_V_Ch_Usr Terminator |
| 缺口节写「未展开」 | 回 PDF / 后课 | 自己补一张「看起来合理」的表 |

### 4.5 总索引实操：查表操练（8 题，含答案）

做题时请真的打开文件路径；答案只作对拍。

**操练 1.** 关键词「迟后进入」——总索引 §2 指向哪？再进 Part2 哪一节概念落点？

<details><summary>答案</summary>

总索引 §2「语音 / 补充业务」→ **语音业务字段速览**。概念落点在 Part2 速览 **§7**（Late Entry → Voice SYNC + 地址 LC）；过程对照见 **§2**；空口细节回 Part1（速览已注 Part1 5.1.2）。

</details>

**操练 2.** 手里 CSBKO=`100110`，第一步开 Part2 哪一小节？PDU 别名是什么？

<details><summary>答案</summary>

Part2 速览 **§1.2** → **NACK_Rsp**；字段细节再进 **§4.4**。

</details>

**操练 3.** 现象「确认数据发出后对端无响应」——Part3 先看哪两节？

<details><summary>答案</summary>

先 **§2**（C_HEAD 上 A/FMF/S/N(S) 是否像确认头）+ **§4**（C_RHEAD Class/Type/Status、有无 C_RDATA/SACK）；§8 可作总表入口。不要一上来只查 §7 HC。

</details>

**操练 4.** DPF=`1110` 且 AB/后续块迹象为无——进 Part3 哪一小节？和「丢了 Rate 块」怎么分？

<details><summary>答案</summary>

**§5.1 SP_HEAD**：Status/Precoded 在头内，AB 常置 0。先认证件再谈丢包——这是第 28 课纪律，本课练的是**进 §5.1 的路径**。

</details>

**操练 5.** 新人岗位「只做语音业务」——总索引 §4 最小打开集是什么？

<details><summary>答案</summary>

**语音字段速览 → Part2 PDF**（总索引 §4「语音业务」行）。需要外壳时再补 Part1 帧结构/CSBK详表。

</details>

**操练 6.** 要查「UDP/IPv4 头压缩」——总索引关键词去哪？Part3 哪一节？TCP HC 呢？

<details><summary>答案</summary>

总索引 §2「数据 / PDP / IP」→ 数据协议字段速览；细表在 Part3 **§7**。TCP HC：SAP=`0010` 仅预留 → 看 **§9 缺口**，**不编造**表。

</details>

**操练 7.** Service Options 的 Emergency 比特——Part2 哪一节？和 Act_Updt 紧急活动 ID 是否同一张表？

<details><summary>答案</summary>

Emergency 比特在 Part2 **§6.1 Service Options**。Act_Updt 的紧急活动编码在 **§5.2** Activity ID 表——相关但**不是同一张表**；§7 补充业务表把两者都挂到「Emergency」概念下。

</details>

**操练 8.** 同事在 Part4 里找 Tier II 业务信道 SP_HEAD——错在哪一层书架？应回哪？

<details><summary>答案</summary>

错在**第一层选书**：业务信道 / Tier I·II 短数据 → Part3 速览 §5；Part4 是集群/控制信道 UDT 主战场。总索引 §2 已把「短数据、UDT（常规数据面）」指向数据速览，并注明集群 UDT 见 Stun_DGNA_UDT。

</details>

---

## 5. 对照表：先前各课 → 本课查表角色

| 主题 | 先前课（会什么） | 本课查表入口（怎么找） |
|------|------------------|------------------------|
| 组呼/个呼 Voice LC | 第 11 | Part2 §1.1 + §3.1/§3.2；过程 §2 |
| 个呼 OACSU / NACK | 第 11 / 25 | Part2 §2 + §4.2–§4.4 |
| Late Entry | 第 26 | Part2 §7 + §2；外壳 Part1 Voice SYNC |
| Talker Alias / GPS | 第 26 | Part2 §1.1 FLCO 000100–001000 → §3.3–§3.5 |
| Service Options | 第 11/26 | Part2 §6 |
| Pre_CSBK / BS_Dwn_Act / Act_Updt | 第 26 | Part2 §4.1/§4.5、§5 |
| 确认/非确认 PDP | 第 27 | Part3 §2/§3/§4/§8（不重画时间线） |
| 短数据三姐妹 | 第 28 | Part3 §5（路径课，不 dump 全字段） |
| UDP/IPv4 HC | 第 28 | Part3 §7；TCP→§9 |
| 「打开哪篇」 | （新） | **总索引 §2 / §4** |

咬合原则：**内容课负责「是什么」；本课负责「去哪翻」。** 两者都要，缺一不可。

---

## 6. 现场岗位对照 / 分诊

| 岗位 / 现象 | 先问 | 打开 | 别急着 |
|-------------|------|------|--------|
| 写频 / 产品 | 语音还是数据？Tier II 还是 III？ | 总索引 §4 → 对应速览 | 把白皮书当字段表 |
| 空口分析 | Data Type / SYNC 认出来了吗？ | Part1 帧结构 → 再分流 Part2/3 | 直接在 Part2 找 EMB |
| 个呼无应答 | 有没有 UU_V_Req？Ans 还是 NACK？ | Part2 §2 → §4.2–§4.4 | 先换天线 |
| 听半截才进组 | Late entry？有无 Voice SYNC@A + LC？ | Part2 §7 + Part1 | 当成 hangtime 配错唯一原因 |
| 屏上无主叫名 | Talker Alias FLCO 段有没有？ | Part2 §1.1 → §3.4–§3.5 | 怪显示驱动之前不查 Opcode |
| 确认数据无 ACK | C_HEAD.A？对端 C_RHEAD？ | Part3 §2 + §4 | 先查 §7 HC |
| 「短消息」失败 | 状态码 / Raw / Defined / UDP 文本？ | Part3 §5 vs §7（证件分家） | 三种证件当一种 |
| 解不出 IP | SAP 是不是 `0011`？SPID/DPID/EH？ | Part3 §7；对照第 28 课 | 当射频故障 |
| 集群台短状态 | 控制信道还是业务信道？ | 控制→Part4；业务→Part3 §5 | 两套书搅一锅 |
| 争议字段位宽 | 速览不够 | 同目录 PDF；Part1 9.17A–C / 9.30–9.31 | 用博客/代码覆盖 TS |

**分诊口诀**：证件/Opcode → 速览节 →（不够）PDF →（仍像射频）再测场强与天线。

---

## 7. 工作例子（7 则）

### 例子 A · 个呼无应答

```text
  现象：主叫按了个呼，对端不响；分析仪偶发 CSBK
  路径：总索引「个呼」→ Part2 速览
        §2「个呼存在性检查」→ UU_V_Req / UU_Ans_Rsp / NACK
        → §4.2–§4.4 看 Target、Answer Response、Reason Code
  结论线索：
    · 有 Req 无 Ans → 对端未听清/未开机/未在网
    · 有 NACK_Rsp → 读 Reason / Service Type（=被拒 CSBKO）
  别做：在 Part3 里找「语音应答码」
```

### 例子 B · Late entry

```text
  现象：组呼已打一会儿，后开机的人能听进后半段
  路径：总索引「迟后进入」→ Part2 §7
        提醒：靠超帧 A 的 Voice SYNC + 嵌入/头中地址 LC
        外壳细节 → Part1（速览已注）
  别做：只在 Part2 §3 找一个叫「Late_Entry_PDU」的独立表（没有这种单独 PDU 名当日常入口）
```

### 例子 C · Talker Alias

```text
  现象：屏上要显示主叫别名；抓到 FLCO=000100
  路径：Part2 §1.1 → Talker_Alias_hdr
        → §3.4 头字段；块 1/2/3 → §3.5（FLCO 000101–000111）
  别做：把 FLCO 表和 CSBKO 表对着找「Alias」
```

### 例子 D · 确认数据无 ACK

```text
  现象：确认 PDP 发出，对端无 ACK
  路径：Part3 §8 定家族 → §2 核对 C_HEAD（A、FMF、BF、N(S)…）
        → §4 看是否该出现 C_RHEAD；Class/Type/Status 是否 NACK/SACK
  短提醒（不重讲第 27 课）：确认要回执；SACK 才带 C_RDATA 位图
  别做：先打开 §7 怀疑头压缩
```

### 例子 E · SP 状态 vs UDP 文本

```text
  现象：产品说「发个短消息」
  路径：先问证件——
        状态/预编码 → Part3 §5.1 SP_HEAD（常无续块）
        UDP 5016 文本 → Part3 §7（SAP=0011，SPID/DPID 索引）
  这是第 28 课内容课 + 本课路径课的叠乘
  别做：在 Part2 Service Options 里找「短信 bit」
```

### 例子 F · Service Options Emergency

```text
  现象：紧急组呼；要确认 Emergency 比特位置
  路径：Part2 §6.1 Service Options 表 → Emergency 1 bit
        若还看 CACH 活动宣布 → §5.2 Act_Updt Activity ID（11xx 紧急类）
  别做：在 Part3 DPF 表里找 Emergency
```

### 例子 G · 错书：Part4 里找 Tier II 短数据

```text
  现象：Tier II 中继业务信道发状态，同事翻 Part4 UDT Opcode
  路径纠偏：总索引 §2 短数据 → 数据协议字段速览 §5
        Part3 §5.4 UDT_HEAD 只是指针；控制信道过程 → Part4
  口诀：先问 Tier 与信道种类，再选书（第 28 课例子 F 的书架版）
```

---

