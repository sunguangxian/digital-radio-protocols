# Part 1：Annex C 时序例 · D Idle/Null · E 发射比特序

> **学习用整理，冲突以 ETSI 原文为准；非全文复制。**  
> 源：ETSI **TS 102 361-1 V2.7.1** Annex **C**（informative）、**D/E**（normative）。  
> **不抄**：Idle 96-bit 逐位表、编码后矩阵、Annex E 全符号表 E.1–E.12。  
> 覆盖清单：[`../附录覆盖清单.md`](../附录覆盖清单.md)  
> **原则加厚（B/D/E，无矩阵/无全比特）**：[`跳过项原则说明.md`](./跳过项原则说明.md)

---

## Annex C — Example timing diagrams

### C.1 Direct mode（发 Normal Burst 后听 RC）
- 时隙中心间隔 **30 ms**。
- 本站发完 Normal Burst 后准备收对端 **RC**；对端可能因传播最多晚约 **1 ms**。
- 关键数字直觉：发后约 **9,75 ms** 起可听 RC；下一 Normal Burst 前至少留约 **8,75 ms** → **合成器锁定时间宜 ≤ 8,75 ms**。

### C.2 Reverse Channel timing
- MS 插在对端（BS 或 MS）Normal Burst 之间发 RC；**锁定对端时序**，无额外传播偏置。
- 同样：**合成器锁定 ≤ 8,75 ms** 量级。

图见 PDF Fig C.1 / C.2；实现以 clause 5 时隙结构为准。

---

## Annex D — Idle / Null（概念）

### D.1 Null embedded message
- 嵌入 Null 的 **11 个信息位全 0** → BPTC 校验位亦全 0 → 发送的 **32-bit 嵌入场全 0**。
- 用途：占位/无有效嵌入信令（与 EMB 配合，见 clause 7/9）。

### D.2 Idle message
- Idle **不是**全 0：规范给出固定 **96 bit 伪随机信息位**（Table D.2），再经 **BPTC (196,96)** + 数据突发交织。
- 学习口径：Idle = **规定图案**的占空/保活类数据突发；逐位表回 PDF，本库不复制。

---

## Annex E — Transmit bit order（原则）

- 突发按 **dibit 符号**串行调制；突发中心左右各 66 符号：**先发 L66 → … → L1，再 R1 → … → R66**。
- 各信息场内比特编号：LSB 一般为 **0**，且 **通常最后发送**；图示上 LSB 在右侧。
- 校验场同理（如 EMB 的 QR：`qr(x)`，x 从高到 0）。
- **完整 L/R 符号映射表 E.1–E.12 → SKIP**（实现查 PDF）。

与 FEC 名称索引：[`帧结构与字段定义.md`](./帧结构与字段定义.md) · [`CSBK与LC字段详表.md`](./CSBK与LC字段详表.md)。  
原则详解（含 Table B.1 挂法、Idle/Null、4FSK）：[`跳过项原则说明.md`](./跳过项原则说明.md)。
