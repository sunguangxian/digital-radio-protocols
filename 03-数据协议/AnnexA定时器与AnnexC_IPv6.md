# Part 3：Annex A PDP 定时器 · Annex C IPv6

> **学习用整理，冲突以 ETSI 原文为准；非全文复制。**  
> 源：ETSI **TS 102 361-3 V1.3.1** Annex **A**（normative）、**C**（informative）。  
> Annex **B** 仅 FLCO=`110000` **TD_LC** → 已写入 [`数据协议字段速览.md`](./数据协议字段速览.md)。  
> 覆盖清单：[`../附录覆盖清单.md`](../附录覆盖清单.md)

---

## Annex A — PDP timers / constants

### A.1 Layer 2 timers

| 定时器 | 用途 | 量级 |
|--------|------|------|
| **T_DataTxLmt** | 未确认发送、或确认发送并等回复的总尝试时长 | 建议 max **60 s** |
| **T_RspnsWait** | 等确认数据头响应 | 建议 **180 ms**；同播建议 min **2,0 s** |
| **T_Holdoff** | 信道变闲后排队数据的随机退避 | 实现范围；未确认/确认建议 max **2 s** |
| **T_DataHngtime** | BS 发 **TD_LC** 预留确认响应窗口 | 建议 **180 ms**（约 3 个业务突发） |

### A.2 Layer 2 constants

| 常数 | 用途 | 量级 |
|------|------|------|
| **N_RtryLmt** | DLL 确认数据空口重试上限 | 建议 max **8** |

---

## Annex B — Opcode（已覆盖）
Table B.1：**TD_LC** only（`110000₂`）。见数据速览 §TD_LC。

---

## Annex C — IPv6 transport over PDP（informative）

### 背景
- PDP 主设计面向 **IPv4**；本附录给 IPv6 承载**策略与 IETF 引用**，非完整 IPv6 栈规范。
- IPv6 地址 **128 bit**；本附录主要讨论 **Unicast**。

### 地址形态（摘要）
| 类型 | 结构直觉 |
|------|----------|
| IPv4-compatible IPv6 | 高 96 bit 为 0，低 32 bit = IPv4 |
| IPv4-mapped IPv6 | 高 80 bit 0 + `FFFF` + 32-bit IPv4 |

（另有 Global Unicast：global routing prefix | subnet ID | interface ID，见 RFC 8200。）

### 两条策略
1. **直接映射**：IPv6 包直接进确认/未确认承载（可用专用 SAP）；头开销多约 20 字节；IPv6 一般**不需 ARP**（地址含链路标识）。**本附录未展开该方案细节**。
2. **IPv6-over-IPv4 隧道**：在 IPv4 PDP 上跑双栈/配置隧道/自动隧道等（RFC 2529 / 3056 / 3142 / 4213）。

### 配置直觉（Fig C.1 / C.2）
- MS 接 **IPv4 LAN**：由主机做隧道；兼容地址时可走 ARP-over-DMR 路由。
- MS / 对端双栈或 IPv6 侧：隧道端点与路由由部署决定。

**学习结论**：标准互通数据面仍以 IPv4 PDP + Part 1 头压缩/ARP SAP 为主；IPv6 属部署扩展，细节回 RFC + 厂商。

---

## Annex D / E
Change requests / Bibliography → **SKIP**。
