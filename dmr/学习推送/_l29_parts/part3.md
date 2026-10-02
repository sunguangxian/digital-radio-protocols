## 8. 数字与符号账本（本课够用的量）

| 项 | 值 / 符号 | 用途 |
|----|-----------|------|
| Part2 官方版本 | **TS 102 361-2 V2.5.1 (2023-05)** | 语音业务硬出处 |
| Part3 官方版本 | **TS 102 361-3 V1.3.1 (2017-10)** | 数据协议硬出处 |
| Part1 官方版本 | **TS 102 361-1 V2.7.1 (2026-05)** | 外壳 / DPF/SAP / 三头位宽 |
| 总索引关键节 | §0–§5 | 门牌；本课用 §2/§4 最多 |
| Part2 速览节 | §1–§9 | Opcode→过程→LC→CSBK→Short LC→SO→补充→Terminator→缺口 |
| Part3 速览节 | §1–§9 | 衔接→C/U头→续块→响应→短数据→TD_LC→HC→Data Type→缺口 |
| FLCO 例 | `000000` Grp · `000011` UU · `000100–000111` Alias · `001000` GPS · `110000` TD_LC 指针 | §1.1 入口 |
| CSBKO 例 | `000100` UU_V_Req · `000101` UU_Ans · `100110` NACK · `111000` BS_Dwn_Act · `111101` Pre_CSBK | §1.2 入口 |
| SLCO 例 | `0000` Nul · `0001` Act_Updt | §1.3 |
| DPF 例 | `0010`/`0011` U/C 数据 · `1110`/`1101` 短数据 · `0001` 响应 · `0000` UDT | Part3 §1 |
| SAP 例 | `1010` Short Data · `0011` UDP HC · `0100` IP · `0010` TCP HC 预留 | Part3 §1 |
| Voice Terminator Data Type | `0010` | Part2 §8 |
| Data Header Data Type | `0110` | Part3 §1 / §8 |
| 冲突规则 | **TS > TR > 博客/幻灯/课文** | 全书通用 |
| RF / 调制提醒 | 12.5 kHz · 4FSK · 2-slot · 30 ms | 查表不改射频 |

---

## 9. 十则误区（看见就打回）

1. **「字段文 = 把 PDF 从头读到尾。」** → 先总索引门牌，再速览货架，最后 PDF 库房。  
2. **「FLCO 和 CSBKO 是一张 Opcode 表。」** → Part2 §1.1 / §1.2 分家；外壳还在 Part1。  
3. **「Part2 里找得到 EMB/SLOT 详解。」** → 外壳回 Part1；Part2 是业务 PDU。  
4. **「Part3 短数据 = Part4 UDT。」** → 信道与 Tier 不同；§5.4 只是指针。  
5. **「缺口节可以自行补表。」** → 缺口 = 停；回 PDF 或后课。  
6. **「DPF 和 SAP 哪个都能当唯一入口。」** → 常要两个一起看；再分流 §2/§5/§7。  
7. **「确认无 ACK 先查头压缩。」** → 先 §2/§4 车次与响应，再 §7。  
8. **「总索引 §4 最小打开集 = 只需那几页永远够。」** → 起步集；争议与认证仍回 PDF。  
9. **「代码仓库/幻灯条款号可覆盖速览。」** → 实现≠规范；TS 优先。  
10. **「翻错书说明射频一定有问题。」** → 错架是文档路径问题；12.5 kHz/4FSK 先别背锅。

---

## 10. 自测题（含答案）

**题 1.** 用三句话说明「三层书架」各层做什么。

<details><summary>答案</summary>

第一层总索引：按「我想查什么」给出打开哪篇。第二层 Part2/Part3 字段速览：结构化 Opcode/PDU/字段表，按节跳转。第三层官方 PDF：硬出处与认证；与笔记冲突时以 TS 为准。

</details>

**题 2.** 分析仪显示 CSBKO=`000101`。写出查表路径（文件 + 节）。

<details><summary>答案</summary>

打开 `02-语音业务/语音业务字段速览.md` **§1.2** → UU_Ans_Rsp；需要 Answer Response 等字段再进 **§4.3**（及 §6.2）。

</details>

**题 3.** 为什么说 Part2 ≠ Part1 shell？举两个仍应回 Part1 的例子。

<details><summary>答案</summary>

Part2 展开语音业务 PDU/Opcode/Service Options；突发壳、EMB/SLOT、Data Type 枚举、许多 IE 位宽在 Part1。例子：Voice SYNC 与 Late Entry 外壳；Data Type=`0010` Terminator with LC 的空口定义。

</details>

**题 4.** DPF=`0011` 的包「无 ACK」——Part3 建议的两步入口是什么？何时才进 §7？

<details><summary>答案</summary>

先 **§2** 核对 C_HEAD 是否像确认头 + **§4** 查响应；仅当 SAP 指向 UDP HC、或解 IP/端口失败时再进 **§7**。

</details>

**题 5.** 总索引 §4「数据业务」最小打开集是什么？若还要 DPF 枚举硬表呢？

<details><summary>答案</summary>

**数据字段速览 → Part3 PDF**。DPF/SAP 硬枚举争议再加 **Part1** Tables 9.30–9.31（速览 §1 已桥接）。

</details>

**题 6.** 判断：Part3 速览 §9 写了 TCP HC 无完整表，因此可以根据 UDP 表「改两个字段」自造 TCP 表。（对 / 错）

<details><summary>答案</summary>

**错。** 缺口纪律：不编造；SAP=`0010` 仅预留；产品宣称以厂商文档为准，规范侧停在诚实边界。

</details>

**题 7.** 写出从「屏上无 Talker Alias」到字段表的完整路径（含 Opcode）。

<details><summary>答案</summary>

总索引「主叫识别」→ Part2 速览 → §1.1 FLCO `000100`–`000111` → §3.4/§3.5 头与块字段；并确认嵌入在语音超帧（§2/§7）。

</details>

**题 8.** 现场：「同事用 Part4 查 Tier II 中继上的 SP 状态」——你如何用总索引 + Part3 纠偏？再补一句调制提醒。

<details><summary>答案</summary>

总索引 §2「短数据」→ 数据协议字段速览 §5（SP_HEAD）；Part4 留给控制信道/UDT。调制提醒：选错书不改变 12.5 kHz/4FSK/双时隙——先纠路径，再查射频。

</details>

**题 9.（加分）** Part2 §8 语音 Terminator 与 Part3 §6 TD_LC 如何用 FLCO/Data Type 一眼分开？

<details><summary>答案</summary>

两者都可以走 Data Type = Terminator with LC（`0010`），但语音终止 LC 通常是 Grp/UU_V_Ch_Usr 的 FLCO；数据 hangtime 用 **TD_LC，FLCO=`110000`**（Part3 §6；Part2 §1.1 仅对照指针）。

</details>

---

## 11. 资料库加深

| 顺序 | 路径 | 看什么 |
|------|------|--------|
| 1 | `总索引.md` **§0 / §2 / §4** | 门牌、关键词、角色最小打开集（本课 canonical） |
| 2 | `02-语音业务/语音业务字段速览.md` **§1–§9** | Part2 全 TOC 入口（本课主书架） |
| 3 | `03-数据协议/数据协议字段速览.md` **§1–§9** | Part3 全 TOC 入口（本课主书架） |
| 4 | `01-空中接口/帧结构与字段定义.md` | 外壳 / Data Type；Late Entry SYNC |
| 5 | `01-空中接口/CSBK与LC字段详表.md` | EMB/SLOT/LC/CSBK 公共外壳 |
| 6 | `学习推送/第25课.md` / `第26课.md` | 补充业务与 Late Entry 内容回唤 |
| 7 | `学习推送/第27课.md` | 确认/非确认车次（查 §2/§4 时回唤） |
| 8 | `学习推送/第28课.md` | 三姐妹与 HC（查 §5/§7 时回唤） |
| 9 | `00-入门/DMR术语与帧结构速查卡.md` | 墙上 Data Type / 时隙 |
| 10 | `DMR整合学习手册.md` | 全貌；版本与能力 Tier |
| 11 | 官方 **TS 102 361-2 V2.5.1**（`02-语音业务/TS102361-2_V2.5.1.pdf`） | 语音过程与 PDU 原文 |
| 12 | 官方 **TS 102 361-3 V1.3.1**（`03-数据协议/TS102361-3_V1.3.1.pdf`） | PDP / 短数据 / HC 原文 |
| 13 | 官方 **TS 102 361-1 V2.7.1** | Tables 9.17A–C、9.30–9.31 等硬表 |
| 14 | `学习推送/加餐_频率带宽与调制解调.md` | 若仍把「翻错书」当成调制故障 |

官方版本锚点：**Part2 V2.5.1**、**Part3 V1.3.1**、**Part1 V2.7.1**。冲突规则：**TS > TR > 实现博客/幻灯/课文笔记**。课文是学习整理，**实现与认证以 ETSI PDF 为准**。FEC 矩阵、Idle 比特、完整 SDL、缺口臆造表、Part4 UDTO 全表：**永远回 PDF / 后课**，本课不补第二份。

---

## 12. 下一课预告

**第 30 课 · 小综合：跟一次语音呼叫空口**

本课把「三层书架 + Part2/Part3 查表路径」钉进手指肌肉。下一课做阶段 D 小综合：跟着一次语音呼叫的空口时间线（从可选 BS 激活、Voice LC Header、超帧、嵌入补充、到 Terminator/hangtime），在关键节点**当场翻表**——仍然少公式；把第 11/25/26/29 课叠成一条可演示的跟读路径，为后续数据小综合留接口。

---

## 13. 推荐阅读与视频

本课外链为 **2026-10-02**（晚间推送）检索核验；真实打开过内容页/PDF（协会镜像 / ETSI deliver / Tait Academy / GitHub 等 HTTP 200；`www.dmrassociation.org/dmr-standards.html` 本环境失败时以 **`https://dmrassociation.org/dmr-standards.html`** 为准）。**不编造地址**。策略 = **Part2 协会镜像 + Part2 ETSI 官方链 + Part3 协会镜像 + Part1 协会镜像 + DMRA 标准目录页 + Benefits 白皮书（产品语感）+ Tait Intro to DMR 学习指南 PDF + Tait Radio Academy 课程页 + go-dmr（实现≠规范对照）**。另检索公开「如何查阅 DMR Part2/Part3 字段文档 / navigate ETSI TS 102 361 field tables」专题视频与长文：**未找到**达到本课「三层书架 + 速览 TOC 入口」深度的独立优质短片（Tait Academy 有入门视频课，但是 **DMR 概论**，不是字段文导航课；产品写频演示亦不适用）。**已弃用**易触发浏览器挑战的第三方 wiki 页。

1. **[ETSI TS 102 361-2 V2.5.1｜Voice and generic services（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：Part2 官方正文——Opcode / 语音过程 / Full LC / CSBK 硬出处；与资料库语音速览对照。  
   - **库内副本**：`dmr/02-语音业务/TS102361-2_V2.5.1.pdf`。  
   - **适合哪一段**：第 4.2、7、8、11 节。  
   - **基础**：进阶；英文 PDF。

2. **[ETSI TS 102 361-2 V2.5.1｜ETSI 官方投递链](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/02.05.01_60/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：与协会镜像同文的官方入口；部分环境抓取异常时改用镜像或浏览器。  
   - **适合哪一段**：同上。  
   - **基础**：进阶；英文 PDF。

3. **[ETSI TS 102 361-3 V1.3.1｜Packet Data Protocol（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236103v010301p.pdf)**  
   - **为什么值得看**：Part3 硬出处——C/U_HEAD、响应、短数据、UDP HC；与数据速览 §1–§9 对照。  
   - **库内副本**：`dmr/03-数据协议/TS102361-3_V1.3.1.pdf`。  
   - **适合哪一段**：第 4.3、7、11 节。  
   - **基础**：进阶；英文 PDF。

4. **[ETSI TS 102 361-1 V2.7.1｜Air Interface（协会镜像）](https://dmrassociation.org/public-downloads/standards/ts_10236101v020701p.pdf)**  
   - **为什么值得看**：外壳与 Tables **9.17A–C / 9.30–9.31**——当速览不够时的第三层。  
   - **适合哪一段**：第 4.3、4.4、8、11 节。  
   - **基础**：进阶；英文 PDF。

5. **[DMR Association｜DMR Standards 目录页](https://dmrassociation.org/dmr-standards.html)**  
   - **为什么值得看**：协会标准下载门牌——Part1–4 / TR 入口一览，适合给新人「官方书架在哪」。  
   - **注意**：目录页≠字段表；版本以 PDF 封面与总索引 §3 为准。  
   - **适合哪一段**：第 2、4.1、11 节。  
   - **基础**：入门；英文网页。

6. **[DMR Association｜Benefits and Features of DMR（白皮书 PDF）](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：产品语言里的语音/数据能力量级——适合向领导解释「我们为什么要会查 Part2/Part3」。  
   - **注意**：白皮书不是 TS；冲突以 Part1/2/3 为准。  
   - **基础**：入门；英文 PDF。

7. **[Tait Radio Academy｜Introduction to DMR Study Guide（PDF）](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)**  
   - **为什么值得看**：厂商学院学习指南，帮助建立「标准分 Part、语音/数据/集群分家」的直觉——为本课选书铺垫。  
   - **注意**：导读≠字段速览；版本较旧时以现行 ETSI / 总索引 §3 为准。  
   - **适合哪一段**：第 1、2、4.1 节。  
   - **基础**：入门；英文 PDF。

8. **[Tait Radio Academy｜Introduction to DMR 课程页](https://www.taitradioacademy.com/courses/introduction-to-digital-mobile-radio/)**  
   - **为什么值得看**：有入门视频课与评估——适合弱基础同事补「DMR 是什么」；**不是**「字段文怎么查」专题课。  
   - **适合哪一段**：课前预习 / 第 1 节动机。  
   - **基础**：入门；英文网页/视频。

9. **[pd0mz/go-dmr｜dataheader.go（头字段解析代码）](https://github.com/pd0mz/go-dmr/blob/master/dataheader.go)**  
   - **为什么值得看**：实现侧可见 DPF/SAP/短数据头拆解——用来练习「代码枚举 vs 速览表 vs PDF」三层对照。  
   - **注意**：**代码不是规范**；冲突以 ETSI PDF 为准。  
   - **适合哪一段**：第 4.3、4.4、9 节误区。  
   - **基础**：中级～进阶；Go 源码。

**说明（视频）**：公开检索**未找到**专门把 **「DMR 资料库三层书架 + Part2/Part3 字段速览 TOC 入口（FLCO/CSBKO/DPF/SAP/现象分流）」** 按课堂深度讲透的独立高质量中文/英文短片。Tait Radio Academy 的 Introduction to DMR 是**概论视频课**，可作弱基础补课，但不能替代本课查表操练。本课 **`video_found=false`**。建议用：**总索引 §2/§4 + 语音速览 §1–§9 + 数据速览 §1–§9 + Part2/Part3 PDF + 本课决策树与 8 道操练** 对照自学。

---

*推送说明：本课为阶段 D「Part2/Part3 字段文怎么查」图书馆技能专课。频谱/调制仅保留短提醒（查表不换频、不改 4FSK/双时隙；翻错书≠射频故障），不复述加餐全文。主文加厚覆盖动机、三层书架与决策树、术语、总索引/Part2 TOC/Part3 TOC 入口、边界表、8 道查表操练、与第 11/13/25–28 课对照、现场分诊、七则例子、账本、十则误区、九题自测、资料库路径与核验外链（含 Part2 双链、DMRA 目录、Tait 指南与课程页；诚实标明无合适公开「字段文导航」专题视频）。硬禁令贯穿全文：不贴 FEC 矩阵、不 dump Idle、不发明条款号、不重讲第 27/28 课全文、不从缺口编造表、不把 Part4 当 Part3 日常入口。读完应能向同事演示「现象→总索引→速览节→（必要时）PDF」，并进入第 30 课语音呼叫空口小综合。*
