（第25课 · 推送 part 2/3）

## 4. 机制拆解：时间线上发生什么

Canonical 来源：`02-语音业务/语音业务字段速览.md` **§2（过程表）/ §3–4（PDU）/ §6（Service Options）/ §8（Terminator）**；Part 2 clause **5.2**；Part 1 Data Type 与 late entry 指针（Part 1 **5.1.2**）。下列**故意不画完整 SDL**。

### 4.1 组呼路径（直通 + 中继）

**直通（MS↔MS）直觉**：

1. 主叫按 PTT → 发 **Voice LC Header**（`Grp_V_Ch_Usr`：组地址 + 源地址 + Service Options）；  
2. 紧接 **语音超帧 A–F**（可多列）；  
3. 松 PTT → **Terminator with LC**（同门牌）；  
4. 对端静音。直通场景通常**没有**「中继 Hangtime 留灯」那一层（没有 BS 替你占信道）。

**中继（MS→BS→MS）直觉**：

1. （可选）BS 休眠时先发 **BS_Dwn_Act** 唤醒出站；  
2. 上行 Header → BS 校验后下行转发同门牌；  
3. 语音超帧双向转发（你仍按「同一时间线」理解）；  
4. 源 MS 发 Terminator → BS 可在 **Hangtime** 内继续发 Terminator with LC，表示「这组还留着」；  
5. Hangtime 结束 → 进入 Idle / 关载波（实现上可能还有 TxHang）。

现场口语对照：「占着组不放」常常是 **Hangtime 正常工作**，不是射频卡死。

### 4.2 个呼路径：可选 OACSU 检查

个呼 Full LC 用 **UU_V_Ch_Usr**（FLCO=`000011`：目标个号 + 源地址）。

许多系统在进语音前可先做 **OACSU** 式存在性检查（资料库 §2 / §4.2–4.4）：

1. 主叫发 **UU_V_Req**（CSBK）；  
2. 被叫（或经 BS）回 **UU_Ans_Rsp**：Proceed=`00100000` 继续；Deny=`00100001` 拒绝；  
3. 也可能收到 **NACK_Rsp**（不支持/无法提供等）；  
4. 只有 Proceed 路径才进入 **Voice LC Header（UU）→ 超帧 → Terminator**。

不是每一次个呼空口上都看得到 Req/Ans——取决于终端配置与系统策略。你的岗位直觉应是：**看见 UU_V_Req 不代表已经在说话；看见 Voice LC Header(UU) 才算语音段开闸。**

### 4.3 三份门牌：Header / 嵌入 / Terminator 复用同一 Full LC

第 22 课已钉死：Full LC 门牌正文约 72 bit 信息（PF|Reserved|FLCO|FID|Data56）。语音呼叫里它至少出现三次「运载形态」：

| 形态 | 壳 | 校验直觉（第 22/24 课） | 作用 |
|------|----|------------------------|------|
| Voice LC Header | 数据壳 + Data Type=`0001` | RS(12,9) 24-bit + BPTC | **发车门牌**（最完整的一次「整包」） |
| 嵌入 LC（超帧 B–E） | 语音壳 + EMB/LCSS | CS5 + 变长 BPTC | **中途上车**仍能拼出谁呼谁 |
| Terminator with LC | 数据壳 + Data Type=`0010` | 同 Header 路径（RS24+BPTC） | **下车广播**；中继 Hangtime 也可继续发 |

同一通话中，组呼就一直是 `Grp_V_Ch_Usr`；个呼就一直是 `UU_V_Ch_Usr`——**别在中途把 FLCO 换成别的业务还以为是「同一趟车」**（Talker Alias / GPS 是嵌入里的「另一类乘客」，见资料库 §3.3–3.5，细讲留给补充业务课）。

### 4.4 超帧在时间线上的位置（复习 + 钉角色）

一列超帧 = Burst **A–F** = **6 × 30 ms ≈ 360 ms**：

```text
  … → [Voice LC Header] → A B C D E F → A B C D E F → … → [Terminator] → …
                              │         │
                              │         └─ B–E：嵌入 Full LC 碎片（迟到拼门牌）
                              └─ A：Voice SYNC（边界 + late entry 上车点）
```

- **A**：中心多为 **Voice SYNC**（不是 Data SYNC）；  
- **B–E**：EMB + 嵌入碎片，拼回与 Header 同类的 Full LC；  
- **F**：本超帧收尾；下一列再从 A 开始。

话越长，超帧列数越多；**门牌不会只在开头出现一次**——这正是迟后进入能成立的原因。

### 4.5 迟后进入直觉（本课只开窗，细讲归第 26 课）

你已经在第 17 / 22 课见过「半路上车」：

1. 抓到某个 Burst **A** 的 Voice SYNC → 对齐超帧；  
2. 用 **B–E 嵌入**（或若还能看见后续 Header 副本）拼出组号/个号与源地址；  
3. 确认色码、时隙、组匹配后开声。

本课只要记住：**错过开头 Header ≠ 这通呼叫对你永久不可见**。如何「确认几次嵌入才算锁定」、与扫描/补充业务如何配合——**第 26 课**展开。

### 4.6 Hangtime vs TxHang（现场高频混淆）

| 概念 | 直觉 | 空口上可能看见 |
|------|------|----------------|
| **Hangtime（呼叫保留）** | EOT 后短暂「本组优先」；别人换组硬上会忙 | BS 继续下发 Terminator with LC / 活动指示 |
| **TxHang（实现用语）** | Hangtime 结束后，发射机载波还可再挂一会儿再关 | 载波还在，但已不再为「刚才那组」强占业务 |
| **Idle / EOC** | 真正空闲，别组可新开呼叫 | Idle 或无业务；CACH 可走 Nul_Msg 等 |

业余中继（如 MMDVM 系）常用 **CallHang / TxHang / ModeHang** 等参数名描述类似层次——名称是实现配置，**语义要对齐「先保留通话、再挂载波、再释放模式」**，不要背成 ETSI 条款号。

### 4.7 范围钉死：Tier II 常规 ≠ Tier III Grant

本课时间线是 **常规（Tier II）语音呼叫**：门牌主要靠 Voice LC Header / 嵌入 / Terminator；可选 CSBK 做唤醒与个呼检查。

**不是**本课主线：

- Tier III 控制信道上的 **Grant / Aloha / 登记**（阶段 E，约第 31–34 课）；  
- 集群里「语音可以不带前面的 LC Header、门牌改由控制信令告知」的变体（第 17 课已提过指针）。

看见「Grant」字样时，先问自己：**这是集群控制信道故事，还是常规中继 Header 故事？** 两套别混。

### 4.8 Service Options / OVCM / Broadcast（门牌上的「贴纸」）

Full LC 里常有 **Service Options（8 bit）**（资料库 Table 7.11）：Emergency / Privacy / **Broadcast（仅组呼）** / **OVCM** / Priority…  
岗位顺序：先认 **FLCO（组还是个）** → 再读 Service Options → 最后读地址数字。细节字段表回资料库 §6，不在本课背满。

---

## 5. 对照表：先前各课 → 本课时间线角色

| 时间线位置 | 空口形态 | 你用哪一课的眼镜看 |
|------------|----------|-------------------|
| 可选唤醒 | CSBK `BS_Dwn_Act` | 第 23 |
| 可选个呼检查 | CSBK `UU_V_Req` / `UU_Ans_Rsp` / `NACK` | 第 23 |
| 可选前导 | CSBK `Pre_CSBK` | 第 23 |
| BOT/BOC 门牌 | Voice LC Header，DT=`0001`，Full LC | 第 21 Data Type + 第 22 Full LC |
| 语音列车 | 超帧 A–F，A=Voice SYNC，B–E 嵌入 | 第 17 + 第 21 EMB |
| 门牌碎片保护 | 嵌入 CS5 + 变长 BPTC；头/终止 RS24+BPTC | 第 24（原则）+ 第 22 |
| 色码 / 同频 | CC 在 SLOT/EMB | 第 20–21 |
| EOT 下车 | Terminator with LC，DT=`0010` | 第 21–22；资料库 §8 |
| Hangtime 留灯 | BS 侧 Terminator with LC 等 | 本课 §4.6；资料库 §8 |
| 缝里活动广播 | CACH Short LC `Act_Updt` | 第 18 + 第 22 Short LC |
| EOC / 空闲 | Idle 等 | 第 23/24 提过 Idle 无 CRC 等原则 |
| 寻址是组还是个 | FLCO `000000` / `000011` | 第 7 + 第 14 + 资料库 §1.1 |

---

## 6. 现场岗位对照

| 现场现象 | 时间线解释 | 先查什么 |
|----------|------------|----------|
| 晚半拍才按进组，开头几秒听不见 | 错过 Header；在等下一列 Burst **A** + 嵌入拼门牌（late entry） | 组号/时隙/色码是否本就错；再看是否弱场导致嵌入拼失败 |
| 「没人说话了」却占着组，换组呼不进去 | **Hangtime** 保留；礼貌接入下别组会忙 | 是否同组回传；中继 CallHang/Hangtime 配置；终端礼貌/不礼貌 |
| 同组有人能回、异组一直忙 | Hangtime 按「当前通话/组」保留（时隙独立） | 别把 TS1 的保留当成整机坏了 |
| 终端设「不礼貌」才能强上 | 部分机型对 Hangtime/色码忙检测不友好；或不想等保留 | 培训上优先教**礼貌接入**；强上可能打断正在进行的组 |
| 对端一直开着静噪尾、分析仪偶发无 Terminator | 漏收 Terminator；靠 Hangtime/超时收尾 | 弱场、错 CC、错时隙；不要只骂「对方没松键」 |
| Header CRC/RS 失败，但稍后仍听到声音 | 头没赶上，**嵌入 late entry** 仍可能上车 | 第 22/24 课：头 RS24 vs 嵌入 CS5 是两条路 |
| 以为是组呼，其实是个呼（或相反） | FLCO 看错；或只看了源地址没看目的类型 | 先看 FLCO=`000000` vs `000011`，再看地址场语义 |
| 语音进行中 CACH 里刷 Activity | **Act_Updt**：广播 TS1/TS2 活动类型与哈希地址 | 第 18/22 课；Activity ID 如 Group voice=`1000` 等（资料库 §5.2） |
| 个呼一直失败，空口只有 UU_V_Req/NACK | 卡在 OACSU，**还没进 Voice Header** | 被叫是否开机/同系统；Deny/NACK 原因；别在语音超帧里找 |
| 双时隙一个在说话一个空闲 | Tier II 两时隙独立；Hangtime 也按时隙 | 不要用「整机载波还在」判断两个时隙都忙 |

---

## 7. 工作例子（6 则）

### 例子 A · 中继组呼「最常见幸福路径」

```text
MS(主叫) --BS_Dwn_Act?--> BS 唤醒
MS --Voice LC Header(Grp, DT=0001)--> BS --转发 Header--> 组内 MS
MS --A B C D E F-- A B C D E F-- …（语音）-->
MS --Terminator(Grp, DT=0010)--> BS
BS --Hangtime 内继续 Terminator with LC--> 组内
BS --Hangtime/TxHang 结束--> Idle
```

要点：门牌三次形态（Header / 嵌入 / Terminator）；Hangtime 不是故障。

### 例子 B · 直通组呼（无 Hangtime 留灯）

```text
MS1 --Header(Grp)--> MS2
MS1 --超帧 A–F…--> MS2
MS1 --Terminator--> MS2（静音）
（无 BS → 通常无「站台留灯」层）
```

### 例子 C · 个呼 OACSU：Proceed 才进语音

```text
MS_A --UU_V_Req--> MS_B
MS_B --UU_Ans_Rsp(Proceed)--> MS_A
MS_A --Header(UU_V_Ch_Usr)--> …
MS_A --超帧…--> Terminator
```

若 `Deny` 或 `NACK_Rsp`：时间线在 CSBK 段结束，**不会出现** Voice LC Header(UU)。

### 例子 D · 迟后进入：错过 Header，仍从超帧中途上车

```text
时间线真实存在：
  [Header] A B C D E F  A B C D E F  A B C D E F  [Term]

你开机太晚，只赶上：
                 ↑从这里听
                 A B C D E F …
  1) 锁定 Voice SYNC@A
  2) B–E 拼出 Grp/Src
  3) 组匹配 → 开声（细节确认策略 → 第 26 课）
```

### 例子 E · Hangtime 挡别组（礼貌 vs 不礼貌）

```text
t0  组9 通话结束，EOT Terminator
t0–tH  Hangtime：组9 同组可礼貌回传；组10 礼貌接入 → 忙
tH  Hangtime 结束
tH–tX  （实现）TxHang：载波或仍开，但业务保留已放
tX  Idle：组10 可新开
```

口语：「等中继掉载波才能说话」——有时是 TxHang/Idle 等待，有时是终端对 Hangtime 处理不友好。

### 例子 F · Header 校验失败，但嵌入救场

```text
[Header RS/BPTC 挂了] → 你没锁定门牌
        A B C D E F → 嵌入 CS5 通过 → 拼出组9
        A B C D E F → 再确认一次（实现策略各异）
        → 开声
[Terminator] → 正常下车
```

对照第 24 课：这是「保护链不同层」，不是「天线一会儿好一会儿坏」的唯一解释。

---

