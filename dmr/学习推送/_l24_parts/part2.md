（第24课 · 推送 part 2/3）

## 5. 对照表：先前各课字段 → FEC 名称

| 先前课 / 字段 | 校验名 | 块 FEC / 短码 | 备注 |
|---------------|--------|---------------|------|
| 第 18 · CACH TACT | （场内） | Hamming(7,4) | 中心短场 |
| 第 18/22 · Short LC | CRC-8 | 变长 BPTC for CACH | 经 4×CACH |
| 第 21 · EMB | （无额外 checksum） | QR(16,7,6) | 语音壳中缝 |
| 第 21 · SLOT | （无额外 checksum） | Golay(20,8) | 数据壳中缝；含 Data Type |
| 第 22 · Full LC Header/Term | RS(12,9) 24-bit | BPTC(196,96) | Data Type 头/终止 |
| 第 22 · 嵌入 Full LC | 5-bit CS | 变长 BPTC B.2.1 | 超帧 B–E |
| 第 23 · CSBK / MBC | CRC-CCITT 16 | BPTC(196,96) | Data Type 0011/0100/0101 |
| Idle | **无** | BPTC(196,96) | 无 Mask |
| Rate ½ 数据 | CRC-9 / 末 CRC-32（确认路径） | BPTC(196,96) | 先校验后 BPTC |
| Rate ¾ 数据 | （按业务） | Trellis ¾ | ≠ BPTC |
| Rate 1 数据 | CRC-9 / 末 CRC-32（确认路径） | 几乎无块 FEC | pad 凑 196 |
| RC | CRC-7 | 单突发变长 BPTC（奇校验） | 第 21 课 PI 相关预告 |

读表口诀：**中缝看短码；单据看 CRC/RS/CS；整舱看 BPTC/Trellis/Rate1。**

---

## 6. 现场岗位对照

| 现场现象 | 先查哪一层 | 别急着怪 |
|----------|------------|----------|
| 「CRC fail」红字 | ① SYNC/壳 ② CC ③ Data Type ④ 块 FEC ⑤ Mask/CRC | 天线（最后才查 RF） |
| Idle 突发「怎么没有 CRC」 | Table B.1：**Idle 无 checksum** | 「解码器坏了」 |
| Header 过、嵌入偶发不过 | Header 是 **RS24+BPTC**；嵌入是 **CS5+变长 BPTC** | 「同一条 LC 校验长度应一样」 |
| CSBK 解不出 | CRC16 → Mask → BPTC；再 FID/CSBKO | 去语音嵌入里找 CSBKO |
| 分析仪「BPTC fail」 | Data Type 是否解成了该走 Trellis/Rate1 的类型？ | 立刻背矩阵 |
| Rate ¾ 当 ½ 解 | 码型错了：¾≠BPTC | 「信道特别差」 |
| 同机房一台过一台不过 | 掩码/固件版本/Data Type 解释是否一致 | 先换天线 |

**CRC 分层分诊（建议贴工位）**：

```text
  L0 射频能量 / SNR          → 加餐与第 1–4 课
  L1 SYNC 认壳是否对          → 第 19 课
  L2 CC（色码门）是否过        → 第 20 课
  L3 中心短码：EMB QR / SLOT Golay / TACT Hamming
  L4 块 FEC：BPTC / Trellis / Rate1 是否选对类型
  L5 Mask + CRC/RS/CS 是否过
  L6 才轮到「天线 / 馈线 / 干扰」硬件大手术
```

---

## 7. 工作例子（6 则）

### 例子 A · CSBK：CRC16 → Mask → BPTC

```text
  [LB|PF|CSBKO|FID|Data64] --CRC16--> [+CRC] --Mask--> [加封签]
        --BPTC(196,96)--> 左右 Info --Data SYNC+SLOT(Golay)--> 突发
```

对照第 23 课：外壳先完整，再进保护链。CRC 失败时先确认 Data Type=`0011`，再查 Mask/CRC，不要先拆天线。

### 例子 B · Voice LC Header：RS24 + BPTC

```text
  Full LC 72 + RS(12,9)24  → 96 信息叙事
       →（Mask，若适用）→ BPTC(196,96) → 数据壳 Header 突发
```

晚入网主要靠嵌入路径（例子 C），Header 是「整包门牌」的高保护版本。

### 例子 C · 嵌入 Full LC：CS5 + 变长 BPTC → B–E

```text
  超帧：A(SYNC)  B(嵌入1)  C(嵌入2)  D(嵌入3)  E(嵌入4)  F
                      └──── 72+CS5 → 变长 BPTC → 4×32 ────┘
  每个语音突发中缝另有 EMB = QR(16,7,6)（护 CC/PI/LCSS，不是护整段 LC）
```

钉子：**Header 的 RS24 ≠ 嵌入的 CS5**——同一门牌正文，两条运载、两套校验预算。

### 例子 D · Idle：有 BPTC、无 CRC

```text
  规定 96-bit Idle 信息图案（不 dump）
       → BPTC(196,96) → Data Type=Idle
       → 无 checksum、无 Mask
```

现场：解出 Idle 是「占空/保活」，不是用户数据坏了。Null 嵌入（全 0 占位）≠ Idle 整突发——见原则说明 §2。

### 例子 E · 「BPTC fail」其实是 Data Type 解错

```text
  真：Data Type = Rate ¾  → 应走 Trellis
  错：分析仪按 BPTC(196,96) 解  → 报 BPTC fail
  分诊：先回 SLOT 的 Data Type（Golay 护着的那 4 bit），再换解码器档案
```

### 例子 F · Rate 1：几乎裸箱

```text
  192 用户 bit + 4 pad0 → 196 入突发（无块 FEC）
  确认路径仍可能：块内 CRC-9；消息末 CRC-32
```

信道差时 Rate1 更容易「上层重传忙」——这是设计取舍，不是「忘了加 FEC」。

---

## 8. 数字账本

| 名称 | 数字 | 别混成 |
|------|------|--------|
| 突发总长 | **264** bit | ≠ 196 Info |
| 左右 Info | **98+98** | 块 FEC 后的码字舱 |
| BPTC 信息/码字 | **96 / 196** | 控制与 ½ 数据主力 |
| Trellis 信息/码字 | **144 / 196** | ¾ 数据 |
| Rate1 用户/码字 | **192(+4 pad) / 196** | 几乎无块 FEC |
| EMB | **16** = 7+9 QR | ≠ 整段 48 中心 |
| SLOT | **20** = 8+12 Golay | 含 CC+Data Type |
| TACT | **7** = 4+3 Hamming | CACH 头 |
| Full LC 头/终止校验 | **24** RS | ≠ 嵌入 CS5 |
| 嵌入 CS | **5** | ≠ CRC16 |
| Short LC CRC | **8** | CACH 路径 |
| CSBK CRC | **16** CCITT | 先 CRC 后 BPTC |
| RC CRC | **7** | 与 RC BPTC 叠用 |
| 时隙 / 符号率 | **30 ms** / **4800** baud | 调制账本 |

串句：

```text
组 PDU → 校验(CRC/RS/CS) → Mask? → 块FEC → 交织 → 中缝短码
控制/½ …… BPTC(196,96)
¾ ……… Trellis
Rate1 …… 几乎不编
中缝 …… QR / Golay / Hamming
永不背 …… 生成矩阵
下一课 …… 语音呼叫过程直觉（阶段 D）
```

---

