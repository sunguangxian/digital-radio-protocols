# Part 1：Annex A 编址 + Annex H FID

> **学习用整理，冲突以 ETSI 原文为准；非全文复制。**  
> 源：ETSI **TS 102 361-1 V2.7.1** Annex **A**（normative）、**H**（normative）。  
> 覆盖清单：[`../附录覆盖清单.md`](../附录覆盖清单.md)  
> Tier III 网关/ALLMS*：[`../04-集群协议/AnnexG本地编址.md`](../04-集群协议/AnnexG本地编址.md) · Part 2 拨号：[`../02-语音业务/AnnexC拨号.md`](../02-语音业务/AnnexC拨号.md)

---

## Annex A — Numbering and addressing

### 规则要点
- Full LC **必须**带 **Source ID**（发送方个体）与 **Destination ID**（接收方/多方）。
- Source / Destination **恒为 24 bit**。
- 个号空间与组号空间**分立**（数值可相同，靠业务类型区分）。

### Table A.1 分区（学习摘要）

**Talkgroup 空间**

| DMR ID（hex） | 名称 | 备注 |
|---------------|------|------|
| `000000` | Null | **非法**源/目的 |
| `000001`–`FFFCDF` | Talkgroup ID | >16M 组地址 |
| `FFFCE0`–`FFFFDF` | Reserved | 768 |
| `FFFFE0`–`FFFFEF` | Unaddressed Id*n* | 16 个特殊未寻址组 |
| `FFFFF0`–`FFFFFF` | All talkgroup Id*n* | 16 个“全体组”分区 |

**Individual 空间**

| DMR ID（hex） | 名称 | 备注 |
|---------------|------|------|
| `000000` | Null | **非法**源/目的 |
| `000001`–`FFFCDF` | Unit ID | >16M 个体 |
| `FFFCE0`–`FFFEDF` | Reserved | 512 |
| `FFFEE0`–`FFFEEF` | System gateway Id*n* | 系统网关（中继、PABX/PSTN/SMS 路由等） |
| `FFFEF0`–`FFFFEF` | Custom | 256，可定制 |
| `FFFFF0`–`FFFFFF` | All unit Id*n* | 16 个“全体个体”分区 |

### 全体呼叫约定
- **未**采用分区“All * Idn”方案的系统：用 **`FFFFFF`** 呼叫系统上所有人。
- **采用**分区方案：用 `FFFFF0`…`FFFFFF` 分别呼叫各分区全体。
- 同一系统内**只允许一种**方案。

Tier III 另有 **ALLMSIDL / ALLMSIDZ / ALLMSID** 等网关区赋值（Part 4 Annex A.4），与上表网关/全呼区衔接。

---

## Annex H — Feature interoperability（FID）

### 模型
```text
FID（8 bit）= 特性集
FLCO（在给定 FID 下）= 空口功能码
```

- 标准 Part 2 业务：**仅**允许 **SFID（默认特性集）+ 对应 FLCO** 访问，以保证互通。
- **非** Part 2 标准化特性：走 **MFID**（厂商特性集）。

### Table H.1（摘要）

| FID 值 | 含义 |
|--------|------|
| `00000000` | **SFID** — TS 102 361-2 标准业务 |
| `00000001`…`00000011` | 保留，未来标准化 |
| `00000100`…`01111111` | **MFID** 厂商区 |
| `1xxxxxxx` | 保留，未来 MFID 扩展 |

- 一家厂商可持有多个 MFID；多家也可共用同一 MFID（厂商策略）。
- MFID **向 ETSI 申请**（见规范 H.2 / clause 9.3.13 链接）。

与 CSBK/LC 外壳中的 **FID 八位组**对照：[`CSBK与LC字段详表.md`](./CSBK与LC字段详表.md)。

---

## Annex I / J
- **I Void**、**J Change requests** → 覆盖清单 **SKIP**。
