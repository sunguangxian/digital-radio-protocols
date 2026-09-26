# DMR Part 4：Annex G 本地编址 / 原生寻址（MS Native Addressing Plan）

> **学习用整理，冲突以 ETSI TS 102 361-4 V1.12.1 (2023-07) 为准；非全文复制。**  
> 源 PDF：同目录 `TS102361-4_V1.12.1.pdf`（`pdftotext -layout` 归纳）。  
> 总览：[`集群协议字段速览.md`](./集群协议字段速览.md)  
> 拨号 / 车队编号（用户域）：[`AnnexE拨号.md`](./AnnexE拨号.md)  
> 网关 / ALLMSID* 数值：Annex **A.4** Table A.8（本注收录摘要）；Stun 等业务侧见 [`Stun_DGNA_UDT与定时器.md`](./Stun_DGNA_UDT与定时器.md)  
> 空口通用地址分区：Part 1 **Annex A** Table A.1（交叉引用）

本文件补：**Annex G（normative）MS Native Addressing Plan**——互操作要求下的**空口 24-bit 原生地址**能力边界。G 正文极短（仅 **G.1**），无独立 NAI/SSI/SGI 表；车队拨号与 NAI‖SSI 拆分在 **Annex E（informative）**。

**性质**：Annex G **规范性**；Annex E **信息性**（MMI/拨号建议）。互操作以 G + clause **4.3** + **A.4** + Part 1 Annex A 为准。

---

## 0. 「本地编址 / 原生寻址」在说什么

| 术语 | 含义（学习口径） |
|------|------------------|
| **Native / 本地编址** | 终端与网络直接使用 **24-bit DMR ID** 作为 Source/Target，不依赖十进制拨号串 |
| **Dialling / 拨号（Annex E）** | 用户键盘串 → 可逆算法 → 同一套 24-bit 地址（及呼叫修饰） |
| **关系** | 拨号只是 MMI 映射；空口始终是 24-bit。G 要求：无论 MMI 如何，MS **须能**对合法原生地址个性化与发起呼叫 |

```text
用户域（可选）              空口域（强制）
  拨号串 (Annex E)  ──►  24-bit MS / TG / Gateway / ALLMS*
  通讯录 / 直写 ID  ──►  同一 24-bit 空间（Annex G 能力范围）
```

---

## 1. Annex G.1 三条互操作要求（全文要点）

为确保不同厂商 MS 互操作，每台 MS **应当**能呼叫 DMR 寻址范围内的全部有效 ID。完整要求（G.1）：

| # | 能力 | 数值范围（十进制） | 十六进制（演算） | 条款 |
|---|------|-------------------|------------------|------|
| 1 | **个性化**本机 MS 地址（见 clause **4.3**）可落在可寻址范围内任意值 | `000 001` … `16 776 415` | `000001₁₆` … `FFFCDF₁₆` | G.1 (1)；Part 1 Table A.1 |
| 2 | 对 MS 支持的全部呼叫业务，能把被叫（**个体或 talkgroup**）编址到可寻址范围 | `00 000 001` … `16 776 415` | 同上 | G.1 (2) |
| 3 | 若 MS 支持，能编址三类全呼 | ALLMSIDL `16 777 213`；ALLMSIDZ `16 777 214`；ALLMSID `16 777 215` | `FFFFFD₁₆` / `FFFFFE₁₆` / `FFFFFF₁₆` | G.1 (3)；A.4 |

要点：

- 范围上界 **`FFFCDF₁₆`** 与 Part 1 Annex A 个号/组号区一致；其后为保留区与网关/全呼特殊 ID（见 §3）。
- G **不**规定车队号、NAI、拨号键位；那些属 Annex E。
- 「本地编址」≠「只能编本站地址」：此处 *Native* 指相对拨号计划的**原生 24-bit 地址**。

---

## 2. 与 clause 4.3 / Annex E 的分工

### 2.1 Device Addresses（4.3）

| 子条款 | 内容 |
|--------|------|
| **4.3.1 MS Addresses** | Tier III MS 至少个性化 **一个个体身份**；可加入一个或多个 talkgroup |
| NOTE | 个体地址与 talkgroup **分属独立地址空间**（Part 1 Annex A）。数值可相同，但 PDU 用个呼/组呼业务类型区分，无歧义 |
| **4.3.2 Services and Gateway Addresses** | Tier III 另定义服务/网关地址；规定值见 **A.4** Table A.8 |

### 2.2 Native（G）vs Dialling（E）

| 维度 | Annex G | Annex E |
|------|---------|---------|
| 状态 | **normative** | informative |
| 对象 | 空口 24-bit 能力边界 | 用户拨号 ↔ 24-bit 映射 |
| NAI / SSI / SGI | **未定义**（交叉 E） | E.3.1 Tables E.1–E.2 |
| ALLMS* | 给出十进制强制可达（若支持） | E.3.4 拨号串 `*196*` / `*197*` / `*198*` |
| 网关 ID | 指向 A.4 | 拨号行为 E.3.7；数值 A.4 |

车队拆分速记（详表在 E）：

| 段 | 比特 | 角色 |
|----|------|------|
| **NAI** | 9 | Network Area Identity |
| **SSI** / **SGI** | 15 | Short Subscriber / Group Identity |
| NP | — | `NP = NAI + 296`（E.3.1.2） |

---

## 3. 地址空间总览（G + Part 1 A + Part 4 A.4）

### 3.1 通用分区（Part 1 Table A.1，G 范围对齐）

个号与组号**平行**各占一套数值；下列为两空间共用的数值带含义：

| 范围 (hex) | 个号空间 | 组号空间 | 备注 |
|------------|----------|----------|------|
| `000000₁₆` | ADRNULL / Null | 同左 | 无实体；A.4 / Part 1 NOTE |
| `000001₁₆` … `FFFCDF₁₆` | Unit ID（MS） | Talkgroup ID | **G.1 可个性化 / 可呼叫范围** |
| `FFFCE0₁₆` … `FFFEDF₁₆`（个） / `…FFFFDF₁₆`（组） | 保留等（Part 1） | 保留等 | Tier III 在邻近区叠 **A.8** 网关/服务 ID |
| `FFFFF0₁₆` … `FFFFFF₁₆` | All unit Idn | All talkgroup Idn | Part 1 分区全呼方案；Tier III 常用末三值见下 |

> 学习提示：Part 1 还划有 System gateway Idn（`FFFEE0…FFFEEF`）与 Custom（`FFFEF0…FFFFEF`）。**Tier III 实际业务网关以 Part 4 Table A.8 为准**（数值多落在 `FFFEC0…FFFED7`）。

### 3.2 Tier III 全呼三元组（G.1 + A.4 ≡ E.3.4）

| Alias | Dec | Hex | 语义（6.6.1.7 / A.4） |
|-------|-----|-----|----------------------|
| **ALLMSIDL** | 16 777 213 | `FFFFFD₁₆` | 本站全部 MS（发起呼叫所在站点）— 作 talkgroup 广播 |
| **ALLMSIDZ** | 16 777 214 | `FFFFFE₁₆` | 系统内**部分站点**子集 — 站点选择厂商相关 |
| **ALLMSID** | 16 777 215 | `FFFFFF₁₆` | 系统**全部站点**全部 MS（AllCall） |

发起全呼时，C_RAND 等应正确标明为 **talkgroup 广播**（6.6.1.7）。

另：Annex E 还有车队内全呼 **SGI = 32 767**（组空间特殊值），路由按车队登记站点；**不是**上述三类 ALLMS*。

### 3.3 网关 / 系统 / 服务标识 — Table A.8（摘要）

G 本身无表；互操作与呼叫建立依赖 A.4。按功能分组（完整 Remark 见 Stun 文件 §6.4 与原文）：

#### 线网 / 数据网关（aligned / offset 成对）

| Hex | Alias | 用途 |
|-----|-------|------|
| `FFFEC0₁₆` / `FFFED0₁₆` | PSTNI / PSTNDI | PSTN（payload aligned / offset） |
| `FFFEC1₁₆` / `FFFED1₁₆` | PABXI / PABXDI | PABX |
| `FFFEC2₁₆` / `FFFED2₁₆` | LINEI / LINEDI | 线路网关 |
| `FFFEC3₁₆` / `FFFED5₁₆` | IPI / IPDI | IP 网关 |
| `FFFECB₁₆` / `FFFED3₁₆` | DISPATI / DISPATDI | 系统调度台 |

#### 控制面服务标识

| Hex | Alias | 用途 |
|-----|-------|------|
| `FFFEC4₁₆` | SUPLI | 补充数据业务 |
| `FFFEC5₁₆` | SDMI | UDT 短数据 |
| `FFFEC6₁₆` | REGI | 登记业务 |
| `FFFEC7₁₆` | MSI | 呼叫转移至 MS |
| `FFFEC8₁₆` | — | **Reserved** |
| `FFFEC9₁₆` | DIVERTI | 取消呼叫转移 |
| `FFFECA₁₆` | TSI | Trunked Station（TS）地址 |
| `FFFECC₁₆` | STUNI | Stun / Revive |
| `FFFECD₁₆` | AUTHI | 鉴权 |
| `FFFECE₁₆` | GPI | 呼叫转移至 Talkgroup |
| `FFFECF₁₆` | KILLI | Kill |
| `FFFED4₁₆` | ALLMSI | 全部个体 MS **与** talkgroup 之总体 |
| `FFFED6₁₆` | DGNAI | 动态组号分配 |
| `FFFED7₁₆` | TATTSI | 组订阅 / 附着 |

#### 空 / 填充

| 值 | Alias | 用途 |
|----|-------|------|
| `000000₁₆` | ADRNULL | 未赋给任何实体 |
| `000₁₆`（信道） | CHNULL | 未分配逻辑物理信道 |
| `1111₂` | DigitNULL | 未用 BCD 填充 |

---

## 4. 与 MS / Talkgroup / All_MS 的关系

```text
24-bit 空口地址用法
├─ 个体 MS ID     …… 个号空间 000001…FFFCDF；个性化须落此（G.1/4.3.1）
├─ Talkgroup ID   …… 组号空间同数值带；与个号空间独立（4.3.1 NOTE）
├─ ALLMSIDL/Z/ID  …… 作 TG 广播全呼（G.1 可选支持；6.6.1.7）
├─ Gateway/Svc ID …… A.8；出现在 Source/Target 标识网关或补充业务
└─ ADRNULL        …… 列表空位、无效填充
```

| 场景 | 地址落点 | 规范锚点 |
|------|----------|----------|
| 个呼被叫 | 个号空间合法 Unit ID | G.1 (2)；4.3.1 |
| 组呼被叫 | 组号空间 Talkgroup ID | 同上 |
| 站/区/网全呼 | ALLMSIDL / Z / ID | G.1 (3)；A.4；6.6.1.7 |
| PSTN/PABX | Target = PSTNI 等 + UDT 号码 | A.4；E.3.7；6.6.x |
| Stun/Kill/鉴权/DGNA | Source/Target = STUNI/KILLI/AUTHI/DGNAI | A.4；对应过程条款 |

Voice 实体组合（Table **6.39**）：MS↔MS/TG；MS↔All MS；MS↔线网关；线网关↔MS/TG/All MS。

---

## 5. 学习对照表（条款索引）

| 主题 | 条款 / 表 |
|------|-----------|
| Native 能力三条 | **Annex G.1** |
| MS / TG 个性化规则 | **4.3.1** |
| 服务与网关地址指针 | **4.3.2** → **A.4** |
| 网关 / ALLMS* / ADRNULL | **Table A.8** |
| 全呼过程 | **6.6.1.7**；语音选项 **6.6.2** |
| 空口通用分区 | Part 1 **Annex A** Table A.1 |
| 拨号 ↔ 原生地址 | Annex **E**（[`AnnexE拨号.md`](./AnnexE拨号.md)） |
| NAI / SSI / SGI / NP | E.3.1（**不在 G**） |

---

## 6. 覆盖与缺口

**已覆盖**

- G.1 三条互操作要求与十进制 / hex 范围  
- Native vs Dialling（G ↔ E）概念对照  
- 与 4.3、Part 1 Annex A、A.4、6.6.1.7 的衔接  
- Table A.8 网关/服务/全呼摘要表  
- ALLMS* 与车队 SGI=32767 的区分（指向 E）

**本文件不展开 / 缺口**

- NAI/SSI/SGI 算法与拨号串 → [`AnnexE拨号.md`](./AnnexE拨号.md)  
- Stun/Kill/DGNA/UDT 过程 → [`Stun_DGNA_UDT与定时器.md`](./Stun_DGNA_UDT与定时器.md)  
- Part 1 分区 All-unit Idn（`FFFFF0…FFFFFF` 十六个）的完整分区方案（非 Tier III 常用三元组）  
- Annex **F**（MSC/SDL 图例说明，非寻址）  
- SYNC hex / FEC 矩阵（按任务不收录）

**Annex G 原文体量**：仅 **G.1 Introduction**（约 1 页）；无 G.2+、无独立地址赋值表。地址赋值表在 **A.4** 与 Part 1 **A**。
