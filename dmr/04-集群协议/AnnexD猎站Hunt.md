# DMR Part 4：Annex D 猎站（Control Channel Hunting）

> **学习用整理，冲突以 ETSI TS 102 361-4 V1.12.1 (2023-07) 为准；非全文复制。**  
> 源 PDF：同目录 `TS102361-4_V1.12.1.pdf`（`pdftotext -layout` 归纳）。  
> 总览：[`集群协议字段速览.md`](./集群协议字段速览.md)  
> C_MOVE / Ann_WD 猎列表：[`Announcement与其余枚举.md`](./Announcement与其余枚举.md)  
> 相关定时器 / Nmax_Ch 等：[`Stun_DGNA_UDT与定时器.md`](./Stun_DGNA_UDT与定时器.md)  
> 频率信道号：[`鉴权与AnnexC频率.md`](./鉴权与AnnexC频率.md)

本文件补：**Annex D（informative）控制信道猎站框架**——Short Hunt / Comprehensive Hunt、Resume / Commanded 单信道猎、与 TSCC 确认 / 登记 / C_MOVE 的衔接。不抄 Fig D.1 图像 OCR、SYNC hex、FEC。

**性质**：Annex D **信息性**；给出 MS 猎站策略**框架**。厂商可增删步骤，但须仍满足正文 **clause 6.3** 的验证与确认。

---

## 0. 猎站在系统里干什么

目标：在候选**物理信道**上找到并**确认**一条可用 **TSCC**（Trunked Station Control Channel），然后才可在该控制信道上发射（登记、业务请求等）。

- 一个物理信道承载两个 TDMA 逻辑时隙；采样时 MS 可**同时评估**两路逻辑信道。
- 验证素材：CACH 或含 **C_SYScode** 的 PDU → 按 **6.3.2.2.1** 做验证；确认测试见 **6.3**。
- 正文入口：clause **5.x / 6.3**（TSCC 获取）；猎站细节框架 → **Annex D**。

```text
候选物理信道列表
  → 采样 / 测电平或质量
  → C_SYScode 等验证（6.3.2.2.1）
  → TSCC 确认（6.3）
  →（需要时）登记 → 在 TSCC 上活跃
```

---

## 1. 四段猎站阶段（D.1.0）

| 阶段 | 英文 | 何时用 | 一句话 |
|------|------|--------|--------|
| **a** | Resuming a TSCC Hunt Channel | 刚从业务信道回来 | 直接回到**上次确认过的**那条 TSCC |
| **b** | Commanded TSCC Hunt Channel | C_MOVE / P_CLEAR 点名，或开机/换网且仍记得信道 | **单信道**直调到指定/记忆的 CONT |
| **c** | Short Hunt Sequence | 无有效记忆，或单信道猎失败后 | 只扫**短列表**里“最可能当 TSCC”的信道 |
| **d** | Comprehensive Hunt Sequence | Short Hunt 失败（且未抑制） | 扫网络个性化给出的 **Low…High** 全范围 |

顺序直觉（失败则进下一段）：

```text
Resume（若适用）
  → Commanded / 单信道（若适用）
  → Short Hunt
  → Comprehensive Hunt（可被 Comp_Flag 关掉；关掉则一直待在 Short）
```

Resume / Commanded 完成条件：已调谐到目标物理信道并完成 **6.3** 验证+确认（D.1.0）。

任一**猎站序列**完成条件（D.1.0）：

- **成功**：找到满足 6.3 验证与确认的物理信道；或  
- **失败**：范围内信道都试过仍无一通过确认。

失败则进入**下一**序列；最后一段是 Comprehensive。若 Comprehensive 仍找不到，MS **留在**该序列直到确认成功（可被个性化放宽，见下）。

放宽（D.1.0）：

- Comprehensive 可由 MS **网络个性化**抑制（`Comp_Flag`）；
- 处于 Comprehensive 时，可**插播**一整轮其他类型猎站，失败再回来；
- 随时可额外采样“看起来可能成功”的物理信道。

多信道采样**顺序不规定**；为防偏置，建议：顺序扫但从随机起点开始，或完全随机（D.1.0）。

NOTE 2：框架可替换/扩展，只要仍满足 6.3 验证与确认。例：已找到合格 TSCC 仍可继续找更好的；也可在规定门限外再猎一轮。

---

## 2. Short Hunt vs Comprehensive Hunt

### 2.1 Short Hunt（短猎）— D.1.2.3

| 项 | 内容 |
|----|------|
| **目的** | 优先扫本网**最可能用作 TSCC** 的物理信道，尽快恢复服务 |
| **何时进入** | ① 开机且**无**该网既往有效记录；② 用户换网且新网**无**有效记录；③ Commanded 失败后；④ Resume 时 C_SYScode 验证失败后；⑤ Comprehensive 过程中 MS **自愿**插播 |
| **列表来源** | 出厂/外设写入的固定非易失短列表（容量建议至多 **64** 个逻辑物理信道号；未用槽位标记忽略）；同一信道可重复写入以**偏置**偏好 TSCC |
| **动态改列表** | 收到本网 **C_BCAST（Announce/Withdraw）** 时，按 AW_FLAG **加入/撤出**猎站列表（见 Announcement 文件 Ann_WD） |
| **步摘要** | 从短列表采样候选 →（可选）先一轮要求电平/质量 **> L_Short / L_SigShort**，再一轮放宽 → 对候选做 6.3 验证/确认 → 成功则停；全失败 → Comprehensive（除非被抑制） |
| **发射** | 短猎中发现的候选，**确认前不得发射** |

两种策略示例（D.1.2.3.0，非强制）：

1. **Fig D.1 类**：短列表顺序扫（随机起点），**扫两遍**——第一遍只要 Sig **> L_short**；第二遍放宽。  
2. **测完再选**：整表扫一遍，记录电平/BER，再选最合适的 TSCC。

`Nmax_Ch`（Table **A.6**）= **50**：短猎列表**最少**信道数（学习口径：设计短列表时至少覆盖这么多槽位容量约定）。

### 2.2 Comprehensive Hunt（全猎）— D.1.2.4

| 项 | 内容 |
|----|------|
| **目的** | 兜底：即使 TSCC 落在“非常用”信道号上也能搜到 |
| **何时进入** | Short Hunt **失败**之后（D.1.2.4.1） |
| **范围** | 个性化固定存储的 **Low_Comp_Ch … High_Comp_Ch**（逻辑信道，1…4095） |
| **步摘要** | 在 [Low, High] 内采样 → 6.3 确认 → 失败可**重复**全猎直到成功；过程中可插播 Short 或单点采样，失败再回全猎 |
| **抑制** | `Comp_Flag` = True → **不做**全猎；MS **留在 Short**，采集门限改用 **L_Squelch**，直到确认成功 |
| **发射** | 确认前不得发射 |

### 2.3 对照一览

| | Short Hunt | Comprehensive Hunt |
|--|------------|---------------------|
| 范围 | 短列表（≤64 槽；BCAST 可增删） | Low_Comp_Ch…High_Comp_Ch |
| 速度意图 | 快、先试“像 TSCC 的” | 慢、穷尽网络信道区间 |
| 失败后 | → Comprehensive（除非抑制） | 重复自身，或插播 Short |
| 可抑制 | — | `Comp_Flag` |
| 门限 | 常用 `L_Short`（落在 Upper…Lower 之间） | 抑制后 Short 用 `L_Squelch` |

---

## 3. Resume / Commanded（单信道猎）

### 3.1 Resuming（D.1.1）

业务信道活动结束后，**直接回到** Channel Grant 之前最后确认过的那条 TSCC。

应在下列时刻起 **2 个 TDMA-frame** 内能收到该 TSCC 出站：

- 收到要求离开业务信道的 **P_CLEAR** 结束；
- MS 在业务信道发出最后一条 **P_MAINT（Maint_Kind=DISCON）** 结束；
- 收到 **P_AUTH** 且其中地址**不匹配**当初 Grant 地址之一（未授权留在业务信道）；
- 组呼中非主叫用户发起的“结束呼叫”操作。

确认前须按 **6.3.2.2.1** 验证 C_SYScode；验证失败 → 本段失败 → 进入 **Short Hunt**。

### 3.2 Commanded / Single Channel Hunt（D.1.2.1–D.1.2.2）

适用：被指向**另一条** TSCC，或开机/换网时仍持有有效信道记忆。

应在下列时刻起 **3 个 TDMA slot** 内收到被提名信道：

- 适用于本 MS 的 **C_MOVE** 结束；
- 开机，且存有“最近确认 TSCC”有效记录；
- 用户换网，且新网有最近确认信道记录。

**提名信道来源**（CONT）：

| 来源 | CONT 含义 |
|------|-----------|
| **P_CLEAR** | CONT IE = 要回的控制信道 |
| **C_MOVE** | CONT IE = 新 TSCC（可为逻辑号；`0xFFF`→MV_AP 绝对，见 Announcement） |
| MS 读写存储 | 本网最近确认过的 TSCC 号 |

确认前不得发射；确认失败 → **Short Hunt**。

---

## 4. 参数 / 门限 / 相关定时器

### 4.1 Annex A 常数（Table A.6，猎站相关）

| Mnemonic | 值 | 用途 |
|----------|----|------|
| **Nmax_Ch** | 50 | Short Hunt 列表最少信道数 |
| **Low_Comp_Ch** | 1…4095 | 全猎最低逻辑信道 |
| **High_Comp_Ch** | Low…4095 | 全猎最高逻辑信道 |
| **Comp_Flag** | True/False | True = 抑制 Comprehensive Hunt |
| **Ch_Pref** | 50 | Vote_Now 优选 TSCC 标记容量（邻站/优选相关，非 Annex D 核心） |
| **NSYSerr** | 1…3 | 与已验证 C_SYScode 连续不符次数 → 离开 TSCC 再猎（6.3.3.1） |

### 4.2 电平门限（Table A.7；单位厂商自定）

| Mnemonic | 含义（学习口径） |
|----------|------------------|
| **L_Upper_SHort** | Short Hunt **优先**采样的质量上沿（“先找够强的”） |
| **L_Lower_SHort** | 低于此则 MS **不得**在该信道活跃 |
| **L_SHort / L_Short / L_SigShort** | 文中混用书写；指 Short 采集门限，落在 Upper…Lower 之间（D.1.2.5 / Fig D.1 叙述） |
| **L_Squelch** | 厂商静噪/质量底线；Comprehensive **被抑制**时 Short 用此门限 |

D.1.2.5：低于规定采集门限的物理信道，MS **不应**试图在其上活跃。可用电平或等价质量（如 BER）。

### 4.3 与猎站衔接的定时器（正文 / Annex A.1）

| 名 | 典型范围 | 与猎站关系 |
|----|----------|------------|
| **T_Nosig** | 约 1…15 s | 收不到可解码 TSCC PDU 达此时长 → **离开控制信道、进入猎站**（6.3.3.1 c） |
| **TRand_TC** | 2…60 s | 随机接入（含登记）最长等待；超时可离开 TSCC 并**回到超时前的猎站阶段**（6.3.3.1 h/i） |

细节档位见 [`Stun_DGNA_UDT与定时器.md`](./Stun_DGNA_UDT与定时器.md)。

### 4.4 优先级 / 信道相关字段（正文旁路，猎站会用到）

| 字段 / PDU | 作用 |
|------------|------|
| **C_MOVE** Physical Channel / CONT | 命令式单信道猎目标；Reg 位=新 TSCC 是否要求登记 |
| **P_CLEAR** CONT | 清业务后指向的控制信道 |
| **C_BCAST Ann_WD** AW_FLAG + BCAST_CHx | 向 Short Hunt 列表 **加/撤**信道 |
| **C_BCAST Vote_Now / Adjacent_Site** | 邻站/优选提示，优化后续猎站（6.7.1；非 Annex D 状态机本身） |
| **C_SYScode** | 验证是否为本网/本区域合法控制信道 |

无单独“Hunt Priority” IE；优先级体现在：**Resume/Commanded → Short（强信号优先）→ Comprehensive**，以及短列表重复写入偏置、Vote_Now 优选。

---

## 5. 与 TSCC / 登记 / C_MOVE 的关系

### 5.1 TSCC 获取链（正文 6.3 + Annex D）

1. **猎站**（Annex D 框架）找到候选物理信道；  
2. **验证** C_SYScode 等（6.3.2.2.1）；  
3. **确认** TSCC（6.3）；  
4. 若 Reg 要求登记 → 随机接入 **C_RAND（Service_Kind=登记类）** 等；  
5. 收到合适 **C_ALOHA** 后才在该 TSCC 上正常活跃。

猎站阶段**本身不发射**；确认前禁止在候选 TSCC 上发。

### 5.2 离开 TSCC 再猎（6.3.3.1，与 Annex D 衔接）

活跃空闲时，下列情况回到猎站（摘要）：

| 条件 | 猎站阶段怎么接 |
|------|----------------|
| BER 劣于门限 / C_SYScode 连续不符（NSYSerr）/ T_Nosig | 重新猎 |
| 用户换网 | 按新网有无记忆 → Commanded 或 Short |
| **C_MOVE** 适用于本 MS | 记 CONT → **Commanded** 单信道猎 |
| 登记 **Reg_Denied / Reg_Refused**，或登记随机接入次数/TRand_TC 超时 | **回到登记尝试前**所处的猎站阶段 |
| 非登记业务随机接入次数/定时超时 | 离开 TSCC（等待信令时另有子集规则） |

等待信令期间离开：仅对 6.3.3.1 的 b/c/e 等子集；猎站与再确认期间**保持等待状态与相关定时器**（6.3.3.2）。

### 5.3 C_MOVE（D.1.2 + 7.1.1.1.3）

- 出站 CSBK，把 MS **迁移到另一 TSCC**（字段见 Announcement §5）。  
- 触发 **Commanded TSCC Hunt**：CONT = 新信道号。  
- 新信道确认后，**Reg** 位指示是否必须再登记。  
- `0xFFF` 时跟 **MV_AP** 绝对频率（Annex C / 鉴权文件）。

### 5.4 登记失败与猎站

登记被拒/拒绝/超时 → **不**盲目从 Short 重开，而是**恢复登记前的猎站阶段**（可能仍在 Comprehensive 中途）。最终确认到新 TSCC 并收到合适 C_ALOHA 后，再按需登记。

Stun 状态：仍可猎站与登记（见 Stun 文件）；用户业务被限制。

---

## 6. Fig D.1 流程（文字等价，不描图）

引用：**Figure D.1: Physical Channel Hunting**（D.1.0）。规范说明这是 Short + Comprehensive 的**一种可能实现**，非唯一算法。

文字等价：

```text
START
  │
  ├─► Short Hunt 第 1 遍（列表可含：预置 Channel#、BCAST 加入的信道；空槽 Null 跳过）
  │      只接受 信号/质量 > L_short（图注亦作 L_SigShort）的候选
  │      对候选做 6.3 验证/确认 → 成功则结束猎站
  │
  ├─► Short Hunt 第 2 遍（同一短列表，起点宜随机以防偏置）
  │      接受 信号/质量 ≤ 上一门限、但仍高于活跃底线 的候选
  │      确认成功则结束；整表失败则 ↓
  │
  └─► Comprehensive Hunt
         按 Low_Comp_Ch … High_Comp_Ch（Channel #, #+1, #+2, …）扫描
         可随时暂停去再跑 Short 或抽测“像 TSCC”的信道，失败再回来
         直到 6.3 确认成功（或 Comp_Flag 抑制本段，则困在 Short + L_Squelch）
```

要点：

- **先短后全**；短猎内部示例为**两遍、先严后宽**；  
- 短列表可被 **C_BCAST** 动态加减；  
- Comprehensive 是列式穷尽，不是另一张独立“魔法表”。

---

## 7. 条款索引（便于回 PDF）

| 条款 / 图 / 表 | 内容 |
|----------------|------|
| **Annex D** D.1.0 | 总框架、四阶段、完成条件、Fig D.1 说明 |
| D.1.1 | Resume |
| D.1.2.1–D.1.2.2 | Commanded / 提名信道（C_MOVE、P_CLEAR、记忆） |
| D.1.2.3 / D.1.2.3.1 | Short Hunt 与进入条件 |
| D.1.2.4 / D.1.2.4.1 | Comprehensive 与进入/抑制 |
| D.1.2.5 | 采集门限 L_SHort / L_Squelch |
| **Fig D.1** | Short×2 + Comprehensive 示例 |
| clause **6.3** | 验证与确认（猎站成功判据） |
| clause **6.3.3** | 离开 TSCC 再猎；登记失败接回猎站阶段 |
| clause **7.1.1.1.3** | C_MOVE / MV_AP |
| C_BCAST Ann_WD | Short 列表加减（7.2.x / Announcement） |
| Tables **A.6 / A.7** | Nmax_Ch、Comp_*、L_* |

---

## 8. 覆盖与缺口

### 已覆盖

- Short vs Comprehensive：目的、进入条件、步骤摘要、抑制；  
- Resume / Commanded 与 C_MOVE、P_CLEAR、记忆信道；  
- Fig D.1 文字流；  
- A.6/A.7 猎站相关参数与 T_Nosig / TRand_TC 衔接；  
- 与 6.3 确认、登记失败回阶段、C_MOVE Reg 的关系。

### 仍未在本库展开（Part 4 其余缺口）

- **Annex E** 车队拨号/编号计划（informative）；  
- **组订阅/附着（TATTSI）** 完整 PDU 与 6.4.4.1.13 过程；  
- Stun/Kill **完整时序图**（步骤已在 Stun 文件；图以 PDF Fig 6.31–6.33 为准）；  
- Vote_Now / 邻站优选与猎站的**实现级**结合（字段在 Announcement；无单独状态机专章）；  
- RC4 内部与鉴权测试向量逐字节（刻意不抄）。

---

*学习向整理。实现与互操作请核对 ETSI TS 102 361-4 V1.12.1 原文 Annex D 与 clause 6.3。*
