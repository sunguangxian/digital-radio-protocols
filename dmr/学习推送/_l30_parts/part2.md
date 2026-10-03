## 4. 机制拆解：跟读时间线（检查点 + 查表路径）

Canonical 来源：`02-语音业务/语音业务字段速览.md` **§1–§2 / §3–§4 / §7–§8**；`01-空中接口/CSBK与LC字段详表.md` **§2 / §4 / §6 / §8**；`总索引.md` **§2（语音关键词）/ §4（语音业务最小打开集）**；第 25–26 / 29 课回唤。下列**故意不画完整 SDL**，每个检查点只给「认什么 → 翻哪」。

### 4.1 CP0 · 可选手续：Pre_CSBK / BS_Dwn_Act /（个呼）OACSU

**空口上你可能看见**：Data SYNC + Data Type = CSBK；CSBKO 落在速览 §1.2。

| 现象 | CSBKO | 白话 | 翻表路径 |
|------|-------|------|----------|
| 中继刚被叫醒出站 | `111000` BS_Dwn_Act | 敲门唤醒，**还不是语音** | 速览 **§1.2 → §4.1**；总索引「CSBK」 |
| 扫描/节电台前导 | `111101` Pre_CSBK | 帮你提高命中，**替代不了门牌** | 速览 **§4.5** |
| 个呼先问在不在 | `000100` UU_V_Req | 存在性检查请求 | 速览 **§4.2** |
| 对方同意/拒绝 | `000101` UU_Ans_Rsp | Proceed 才准进语音；Deny 停 | 速览 **§4.3** + §6.2 |
| 否定/不支持 | `100110` NACK_Rsp | 礼貌拒绝，**不进超帧** | 速览 **§4.4** |

**跟读口令**：

1. 先认壳：这是 **CSBK 数据壳**，不是 Voice Header。  
2. 读 CSBKO（不要误读成 FLCO——第 29 课已钉死两张 Opcode 表）。  
3. 只有「个呼 Proceed 之后」或「组呼直接进 Header」才进入 CP1。  
4. **不是每次呼叫都有 CP0**——直通组呼常常直接从 Header 开闸。

**一句对照（数据）**：确认/非确认 PDP、短数据三姐妹是第 27–28 课的「另一条车次」——本课跟读轴上**不要把 Data Header 当成 Voice LC Header**。

### 4.2 CP1 · Voice LC Header：发车门牌（当场翻 Full LC）

**空口上你应看见**：Data SYNC + **Data Type = `0001`（Voice LC Header）** + 整包 Full LC。

**跟读步骤（叠第 29 课肌肉）**：

```text
  分析仪：Data Type=0001
      │
      ▼
  总索引 §2「个呼/组呼」→ 语音业务字段速览
      │
      ▼
  §2 过程表确认阶段 =「语音开始」
      │
      ▼
  读 Full LC：FLCO（§1.1）→ FID → Service Options → 地址
      │
      ├─ FLCO=000000 → §3.1 Grp_V_Ch_Usr（组呼）
      └─ FLCO=000011 → §3.2 UU_V_Ch_Usr（个呼）
      │
      ▼
  外壳位宽有争议？→ 详表 §4 FULL LC / Part1 PDF（第三层）
```

岗位顺序口诀：**先 FLCO（组还是个）→ 再 Service Options 贴纸 → 最后读地址数字。**  
Broadcast 位**仅组呼**侧有广播/全呼语义；别在个呼 LC 上硬找 Broadcast 故事。

### 4.3 CP2 · 超帧 A–F + 嵌入 LC：火车在跑

一列超帧 = Burst **A–F** = **6 × 30 ms ≈ 360 ms**：

```text
  [Voice LC Header] → A B C D E F → A B C D E F → … → [Terminator]
                       │         │
                       │         └─ B–E：EMB + 嵌入 Full LC 碎片
                       └─ A：Voice SYNC（边界 + Late Entry 上车点）
```

| 突发 | 中心你先认什么 | 翻哪 |
|------|----------------|------|
| **A** | **Voice SYNC**（不是 Data SYNC） | 详表 **§8 SYNC 类型名**；总索引「语音超帧」 |
| **B–E** | EMB（16 bit）+ 嵌入 32 bit 碎片；LCSS 帮你拼 | 详表 **§2 EMB**；速览 §2 |
| **F** | 本超帧收尾；下一列再从 A | 第 17 课回唤 |

**跟读口令**：

1. 进入语音段后，**别再按「每个 30 ms 都有完整门牌」去找 Header**——门牌整包主要在 CP1；跑起来靠嵌入重复贴。  
2. 同一通话中，组呼就一直是 `Grp_V_Ch_Usr`；个呼就一直是 `UU_V_Ch_Usr`。  
3. 若嵌入里出现 FLCO=`000100`–`000111`（Talker Alias）或 `001000`（GPS_Info）——那是**加料乘客**（第 26 课），不是「换了一趟车」；翻速览 **§3.3–3.5 / §7**。  
4. Colour Code 在 EMB/SLOT 里当「同频系统色码门」——第 20–21 课眼镜继续戴着。

### 4.4 CP3 · Late Entry 窗口：半路上车（短回唤，不重讲第 26 课）

你太晚开机 / 扫描刚扫到 / 开头 Header CRC 失败时：

1. **步骤 1**：等到下一个 Burst **A**，认到 **Voice SYNC** → 对齐超帧相位；  
2. **步骤 2**：用 **B–E 嵌入**拼回 Full LC（FLCO + 地址 + Service Options）+ 比对 CC / 时隙 / 组；  
3. 匹配则开声；不匹配继续静音——**不是「射频永久坏了」**。

**翻表路径**：总索引「迟后进入 / 主叫识别」→ 速览 **§2 / §7** →（外壳）详表 SYNC/EMB → 需要认证再回 Part1 PDF（late entry 指针在库内已桥接）。  
**本课只要会在跟读轴上标出「CP3 可与 CP2 重叠」**；确认几次嵌入才锁定、与扫描如何配合——回第 26 课，不在此展开。

### 4.5 CP4 · Terminator with LC：下车广播

**空口上你应看见**：Data SYNC + **Data Type = `0010`（Terminator with LC）**；载荷通常仍是同一份 Voice Channel User LC。

**翻表路径**：速览 **§8**（语音 Terminator 要点）→ §2 过程表「语音结束」→ 详表 Data Type / FULL LC。  

**防晕三句**：

1. 源 MS 发 Terminator → 对端静音（EOT）。  
2. **语音 Terminator ≠ 数据 TD_LC**：后者 FLCO=`110000`，属 Part3（第 27 课指针）——本课跟读语音轴上别串台。  
3. 中继可能在 Hangtime 里**继续**发 Terminator with LC——那是 CP5，不是「用户又按了一次 PTT」。

### 4.6 CP5–CP6 · Hangtime vs EOC：留灯与放空

| 概念 | 直觉 | 空口可能看见 | 别混成 |
|------|------|--------------|--------|
| **Hangtime** | EOT 后短暂「本组优先」 | BS 继续 Terminator with LC / 活动指示；CACH AT 可仍 busy | Late Entry；射频卡死 |
| **TxHang** | 实现参数：保留后再挂载波多久 | 载波还在，但已不一定强占「刚才那组」 | 规范 Hangtime 本身 |
| **EOC / Idle** | 真正放空，别组可新开 | Idle 或无业务；CACH 可走 Nul_Msg | 「还在通话中」 |

**跟读口令**：同事喊「占着组不放」→ 先问 **Hangtime 定时是否在正常窗口**，再查射频与干扰。翻：速览 **§8**；实现侧 CallHang/TxHang 名称只对齐语义，**不要背成 ETSI 条款号**。

### 4.7 组呼 vs 个呼：OACSU 何时插入

- **组呼**：多数系统 CP0 可省略，直接 CP1（`Grp_V_Ch_Usr`）→ CP2 → CP4 → …  
- **个呼**：可能多一步 CP0 的 UU_V_Req/Ans；**只有 Proceed 才进 CP1（`UU_V_Ch_Usr`）**。  
- 不是每一次个呼空口都看得到 Req——取决于终端与系统策略。岗位直觉：**看见 UU_V_Req ≠ 已经在说话；看见 Voice LC Header(UU) 才算语音段开闸。**

### 4.8 边界钉死：Tier II 常规 ≠ Tier III Grant

本课跟读轴是 **Tier II 常规（业务信道上 Header/嵌入/Terminator 门牌）**。

**不是本课主线（留给第 31+ 课）**：

- 控制信道 vs 业务信道分工；  
- Aloha / 登记 / **Grant** 变体；  
- 「语音可以不靠前面的 LC Header、门牌改由控制信令告知」的集群变体。

看见「Grant」字样时，先问自己：**这是集群控制信道故事，还是常规中继 Header 故事？** 两套时间线别画在同一条轴上硬对齐。

### 4.9 一页「跟读速查卡」（可贴显示器边）

| CP | 先认壳 | 再认 Opcode/字段 | 打开 |
|----|--------|------------------|------|
| 0 | Data SYNC + DT=CSBK | CSBKO | 速览 §1.2 / §4 |
| 1 | Data SYNC + DT=`0001` | FLCO + 地址 + SO | 速览 §2 / §3.1–3.2 |
| 2A | **Voice SYNC** | 超帧相位 | 详表 §8；总索引「超帧」 |
| 2B–E | EMB + 嵌入 | 同 FLCO 碎片 / 可选 Alias | 详表 §2；速览 §7 |
| 3 | 同 2A→2B–E | Late Entry 两步 | 总索引「迟后进入」；速览 §2/§7 |
| 4 | Data SYNC + DT=`0010` | 同 Voice Channel User LC | 速览 §8 |
| 5–6 | Terminator 重复 / Idle | Hangtime vs EOC | 速览 §8 |

冲突规则回唤：**TS > TR > 博客/幻灯/课文**。课文是跟读脚手架，**实现与认证以 ETSI PDF 为准**。

---

## 5. 对照表：先前各课 → 本课时间线角色

| 时间线位置 | 空口形态 | 你用哪一课的眼镜 + 本课翻哪 |
|------------|----------|------------------------------|
| CP0 可选唤醒 | CSBK `BS_Dwn_Act` | 第 23 + 速览 §4.1 |
| CP0 可选个呼检查 | `UU_V_Req` / `UU_Ans` / `NACK` | 第 23/25 + 速览 §4.2–4.4 |
| CP0 可选前导 | `Pre_CSBK` | 第 23/26 + 速览 §4.5 |
| CP1 门牌 | Voice LC Header，DT=`0001` | 第 21–22/25 + 速览 §3 + 详表 §4 |
| CP2 列车 | 超帧 A–F；A=Voice SYNC；B–E 嵌入 | 第 17/21 + 详表 §2/§8 |
| CP3 半路上车 | Late Entry 两步 | 第 17/26 + 速览 §2/§7 |
| 加料乘客 | Talker Alias / GPS / SO 贴纸 | 第 26 + 速览 §3.3–3.5/§6–§7 |
| CP4 下车 | Terminator，DT=`0010` | 第 21–22/25 + 速览 §8 |
| CP5 留灯 | Hangtime 侧 Terminator | 第 25/26 + 速览 §8 |
| CP6 放空 | EOC / Idle | 第 25 + 速览 §8 |
| 查表肌肉 | 三层书架 | **第 29**（本课每个 CP 当场用） |
| **本课** | **把上表串成跟读清单** | — |
| 下一站边界 | 控制信道 / Grant | **第 31+**（本课只钉「别混」） |

---

## 6. 现场岗位对照 / 分诊

| 岗位现象 | 先做的跟读动作 | 常翻 | 别一上来就 |
|----------|----------------|------|------------|
| 「跟一下这通组呼」 | 从当前屏回放：有没有 Header？在哪一列超帧？有没有 Terminator？ | 速览 §2；本课速查卡 | 拆天线 / 改频率 |
| 只有 Voice SYNC、没有 Header | 标 CP3：等 A → 拼嵌入 → 比对组/CC | 总索引「迟后进入」；速览 §7 | 断言「没这通呼叫」 |
| 看见 UU_V_Req 就说「在通话」 | 停在 CP0：等 Ans 或等 Header(UU) | 速览 §4.2–4.3 | 按语音故障单处理 |
| FLCO=`000100` 当组呼 | 辨加料：Talker Alias header | 速览 §1.1 / §3.4 | 改组号乱试 |
| 「占着组不放」 | 问 Hangtime 窗口；看是否仍在发 Terminator with LC | 速览 §8 | 判发射机硬件卡死 |
| Data Type=`0010` 且 FLCO=`110000` | 这是数据 TD_LC 轴，不是本课语音跟读 | Part3 指针；第 27 课 | 硬套语音 Hangtime |
| 同事把 Grant 画进常规轴 | 停：问是不是 Tier III 控制信道 | 总索引「集群」；第 31 预告 | 用 Header 时间线硬解 Grant |
| 弱场开头坏、后面能听 | 可能 Header 丢、嵌入仍拼得动（Late Entry） | 详表 SYNC/EMB；第 26 | 只加功放不解时间线 |
| 两时隙串台感 | 确认跟的是 TS1 还是 TS2；各有 Hangtime | 第 15/18；调制钩子 | 当成单时隙模拟机 |

分诊口诀：**先定检查点 → 再认壳 → 再读 Opcode → 再翻速览 → 最后才碰射频与写频。**

---

## 7. 工作例子（7 则）

**例 1 · 直通组呼「干净跟读」**  
空口：Voice LC Header（FLCO=`000000`）→ 两列超帧 → Terminator。  
跟读：CP0 缺省；CP1 翻 §3.1；CP2 认 Voice SYNC@A；CP4 翻 §8。直通通常无中继 Hangtime 层。

**例 2 · 中继组呼带唤醒**  
先见 CSBKO=`111000`（BS_Dwn_Act）→ 再 Header → 超帧 → Terminator → BS 继续若干 Terminator（Hangtime）→ Idle。  
跟读：CP0 翻 §4.1（**还不是说话**）→ CP1–CP6 按速查卡。向领导一句话：「先敲门，再发车，再留灯。」

**例 3 · 个呼 OACSU 被拒**  
UU_V_Req → UU_Ans_Rsp(Deny) 或 NACK → **没有** Voice LC Header。  
跟读：停在 CP0；翻 §4.3/§4.4；不要按「语音超帧丢了」开单。

**例 4 · 扫描台半路上车**  
用户拧到谈组时，呼叫已在第二列超帧。屏上先锁 Voice SYNC@A，再拼出组地址，约半拍～约一个超帧量级后开声。  
跟读：标 CP3；翻总索引「迟后进入」+ 速览 §2/§7；回唤第 26 课两步，不重讲全文。

**例 5 · Hangtime 被当成故障**  
松 PTT 后中继仍占组约数秒，同组回一句很顺；别组硬上忙。  
跟读：CP5 正常；翻 §8；把 CallHang/TxHang 配置名对齐「先保留通话、再挂载波」，不要发明条款号。

**例 6 · 嵌入里出现 Talker Alias**  
超帧 B–E 拼出的不全是 Grp_V_Ch_Usr，间或 FLCO=`000100`…  
跟读：仍在同一趟组呼车上；加料乘客翻 §3.4–3.5；**不要**改 FLCO 当「换了个呼」。

**例 7 · 新人把 Tier III Grant 时间戳贴到常规录波**  
录波是常规中继，笔记却写「等 Grant」。  
跟读：用 §4.8 边界叫停；本课轴是 Header/嵌入/Terminator；Grant 留给第 31 课控制信道故事。

---

