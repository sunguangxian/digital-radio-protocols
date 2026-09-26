# DMR 协议学习导航（最新版整理）

> 面向新用户：先建立整体认识，再按角色进入对应标准分册。  
> 整理日期：2026-09-13  
> 权威来源：ETSI（以 ETSI 官网 PDF 为准）；[DMR Association 标准页](https://www.dmrassociation.org/dmr-standards.html) 便于浏览，版本可能略滞后。

---

## 1. 一分钟认识 DMR

**DMR（Digital Mobile Radio）** 是由 ETSI 制定的数字集群/专业移动无线电标准，目标是在现有 **12.5 kHz** 信道上提供低复杂度、可负担的数字语音与数据，并满足 **6.25 kHz 等效** 频谱效率要求。

核心技术要点：

- **2 时隙 TDMA**（专业 Tier II / III）
- 载波带宽 **12.5 kHz**
- 覆盖语音、短消息、分组数据等业务
- 三层产品互不跨层互通（各自独立）

### 三层（Tier）怎么选

| 层级 | 场景 | 要点 |
|------|------|------|
| **Tier I** | 免执照 / 消费级 | 一体天线、直通；DMR Association 主要精力在 II/III |
| **Tier II** | 执照常规（常规对讲） | 直通或中继；专业市场主力 |
| **Tier III** | 执照集群 | 有控制器自动分配信道；支持更完整的语音/数据业务 |

---

**总索引（检索）：** [`总索引.md`](./总索引.md)

## 2. 新人推荐阅读顺序

1. **先读总览（必读）**  
   `ETSI TR 102 398`《DMR General System Design》——给采购、运营商、使用者看的系统设计导读，不是完整技术规范；与 TS 冲突时以 TS 为准。

2. **建立概念（可选但很友好）**  
   - [DMR Association：标准与 Tier 说明](https://www.dmrassociation.org/dmr-standards.html)  
   - [Tait Radio Academy：Introduction to DMR Study Guide](https://www.taitradioacademy.com/wp-content/uploads/2014/11/Introduction_to_DMR_Study_Guide-Tait_Radio_Academy.pdf)（入门概念清晰，部分版本号较旧，细节以最新 TS 为准）

3. **再啃正式协议（按需）**  
   - 做射频/空口/终端底层 → **Part 1**  
   - 做语音与通用业务 → **Part 2**  
   - 做短数据 / IP 分组数据 → **Part 3**  
   - 做集群（Tier III）→ **Part 4**

---

## 3. 最新官方标准清单（截至 2026-09）

| 文档 | 内容 | 最新公开版 | 官方 PDF |
|------|------|------------|----------|
| **TR 102 398** | 系统设计总览（新人入口） | **V1.5.1 (2023-11)** | [下载](https://www.etsi.org/deliver/etsi_tr/102300_102399/102398/01.05.01_60/tr_102398v010501p.pdf) |
| **TS 102 361-1** | Part 1：空中接口（AI）协议 | **V2.7.1 (2026-05)** ⭐ 最新大更新 | [下载](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf) |
| **TS 102 361-2** | Part 2：语音与通用业务 | **V2.5.1 (2023-05)** | [下载](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/02.05.01_60/ts_10236102v020501p.pdf) |
| **TS 102 361-3** | Part 3：数据协议 | **V1.3.1 (2017-10)** | [下载](https://www.etsi.org/deliver/etsi_TS/102300_102399/10236103/01.03.01_60/ts_10236103v010301p.pdf) |
| **TS 102 361-4** | Part 4：集群协议 | **V1.12.1 (2023-07)** | [下载](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236104/01.12.01_60/ts_10236104v011201p.pdf) |

### 版本提醒

- **Part 1 已从 V2.6.1（2023-05）升到 V2.7.1（2026-05）**。若资料库仍挂旧版，请优先替换。
- DMR Association 公开页有时滞后（例如仍列 Part 1 为 V2.6.1），**以 ETSI deliver 链接为准**。
- Part 4 / TR 102 398 在 ETSI 工作项中有后续修订草稿（截至整理时尚未形成可下载的更新发布版）；当前学习与实现仍以表中公开版为准。

### 镜像（可选）

DMR Association 也托管部分 PDF（便于备份）：  
https://www.dmrassociation.org/dmr-standards.html

---

## 4. 按角色的快速索引

| 你是谁 | 先看什么 |
|--------|----------|
| 产品经理 / 销售 / 新同事 | TR 102 398 → DMRA Tier 说明 |
| 射频 / 基带 / 空口实现 | Part 1（V2.7.1） |
| 语音业务 / 补充业务 | Part 2 |
| 短消息、IP 数据、头压缩 | Part 3 |
| 集群控制器 / Tier III | Part 4（再回看 Part 1/2） |
| 互操作与认证背景 | DMRA + 各厂商互操作说明（非本表范围） |

---

## 5. 学习时的小建议

1. **先图后文**：用 TR 102 398 搞清系统图、编号编址、业务分类，再进 TS。  
2. **一次只啃一本**：不要四本并行；按你的产品层级（II 或 III）选路径。  
3. **记版本号**：文档、代码注释、Wiki 里写清 `文档号 + 版本 + 发布年月`，避免混用旧空口规范。  
4. **冲突裁决**：导读（TR）与规范（TS）不一致时，**以 TS 为准**。

---

## 6. 建议的资料库目录结构（可直接复制）

```text
digital-radio-protocols/
├── dmr/                         # 本分册
│   ├── 00-入门/
│   ├── 01-空中接口/
│   ├── 02-语音业务/
│   ├── 03-数据协议/
│   ├── 04-集群协议/
│   ├── 学习推送/
│   └── README.md / 总索引.md …
├── shared/ dpmr/ nxdn/ pdt/ compare/   # 其他体制（占位）
├── codex/
└── scripts/
```

---

## 7. 快速链接汇总

- ETSI 标准搜索：https://www.etsi.org/standards-search  
- DMR Association 标准页：https://www.dmrassociation.org/dmr-standards.html  
- Part 1 最新：https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/02.07.01_60/ts_10236101v020701p.pdf  
- TR 总览：https://www.etsi.org/deliver/etsi_tr/102300_102399/102398/01.05.01_60/tr_102398v010501p.pdf  


---

## 字段速览（扩展）

| 文档 | 说明 |
|------|------|
| `01-空中接口/帧结构与字段定义.md` | 帧/时隙/CACH/SYNC 类型名/IE |
| `01-空中接口/CSBK与LC字段详表.md` | CSBK/LC/EMB 八位组 + FEC 名称 |
| `02-语音业务/语音业务字段速览.md` | FLCO/CSBK/Service Options/Terminator |
| `03-数据协议/数据协议字段速览.md` | C/U_HEAD、短数据、响应、UDP HC |
| `04-集群协议/集群协议字段速览.md` | TSCC、Grant、Aloha、登记、RC |
| `04-集群协议/ReasonCode与Grant变体.md` | Reason Code 全表 + Grant 变体/CG_AP |
| `04-集群协议/Announcement与其余枚举.md` | Announcement_type、Service_Kind/Options |
| `04-集群协议/Stun_DGNA_UDT与定时器.md` | Stun/Kill/Revive、DGNA、USBD、UDT Annex B、Annex A 定时器 |
| `04-集群协议/鉴权与AnnexC频率.md` | 鉴权 PDU/K/PSN/挑战–响应 + Annex C 频率/CdefParms |
| `04-集群协议/AnnexD猎站Hunt.md` | Annex D Short/Comprehensive 猎站、Resume/Commanded、C_MOVE/登记 |
| `04-集群协议/AnnexE拨号.md` | Annex E 车队拨号、个/组映射、ALLMSID*、PSTN/PABX |
| `04-集群协议/AnnexG本地编址.md` | Annex G 原生/本地编址互操作、4.3/A.4/ALLMS* |

| `附录覆盖清单.md` | 五册 Annex 覆盖矩阵（COVERED / NAMES ONLY / STUB / SKIP） |
| `00-入门/TR附录_省电接入功率.md` | TR Annex A–D：省电、随机接入、架构、闭环功率 |
| `01-空中接口/AnnexA编址与AnnexH_FID.md` | Part1 Annex A 24-bit 分区 + Annex H SFID/MFID |
| `01-空中接口/AnnexCDE_时序Idle比特序.md` | Part1 Annex C 时序例、D Idle/Null 概念、E 比特序原则 |
| `01-空中接口/跳过项原则说明.md` | Part1 Annex B/D/E 故意跳过表体的原则（无矩阵/无全比特/无 E.1–E.12） |
| `01-空中接口/AnnexF定时器与AnnexG状态.md` | Part1 Annex F L2 定时器、G MS/BS 高层状态 |
| `02-语音业务/AnnexA定时器.md` | Part2 Annex A L3 定时器/常数 |
| `02-语音业务/AnnexC拨号.md` | Part2 Annex C UI↔AI 拨号（常规） |
| `03-数据协议/AnnexA定时器与AnnexC_IPv6.md` | Part3 Annex A PDP 定时器 + Annex C IPv6 策略 |
| `04-集群协议/AnnexF_MSC图例说明.md` | Part4 Annex F MSC/SDL 图例 stub |
