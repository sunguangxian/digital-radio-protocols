
## 5. 完整例子：跟一通组呼从发车到到站

场景：Tier II 中继，某组呼在 **Slot1** 发起。时间数字取常见教学量级；实现细节以 Part1 **5.1.2** / **7.1** 为准。

### 5.1 发车前：数据壳先报门牌（Voice LC Header）

常规系统里，真正进超帧哼歌之前，空口上常先出现**数据/控制形态**突发：

```text
Voice LC Header（数据壳 264 bit）：
  Info 98 | SLOT 10 | Data SYNC 48 | SLOT 10 | Info 98
                 └─ Data Type = Voice LC Header
  196 bit Info（经 FEC）里带着：FLCO、FID、组地址、源地址、业务选项…
```

可选再跟 **PI Header**（隐私相关初始化）。口诀：

> **先贴工卡（Header），再进会议室连续发言（超帧）。**

注意：Header 的中心是 **Data SYNC**，不是 Voice SYNC。有人口误「语音头中间也是 Voice SYNC」——那是把 Header 和 Burst A 搞混了（见误区）。

### 5.2 第一节：Burst A = 车头灯

```text
Burst A（语音壳）：
  Voice 108 | Voice SYNC 48 | Voice 108
              └─ 超帧边界；迟后进入上车点
```

左右 216 bit ≈ 约 60 ms 压缩话。听感：会场开始有人声。

### 5.3 第二～五节：Burst B–E = 四片嵌入拼 Full LC

```text
Burst B（典型）：
  Voice 108 | EMB + 碎片(32) + EMB 共 48 | Voice 108
Burst C、D、E：同结构，碎片用 LCSS 标「首/续/续/末」
```

拼装直觉（不必背矩阵）：

```text
  B 碎片 ─┐
  C 碎片 ─┼─→ 经 BPTC 等 FEC 拼回 → Full LC（72 bit 信息叙事）
  D 碎片 ─┤         └─ 谁呼谁、FLCO、业务选项…
  E 碎片 ─┘
```

现场翻译：

- 语音左右不停；  
- 中间四拍把「门牌」拼齐；  
- 迟后进入若错过 Header，仍可能靠这四拍认出组号。

Full LC 的字段外壳（PF/FLCO/FID/地址…）第 14、22 课已有/将有专篇；本课只要建立：**一条 Full LC ↔ 四个嵌入场（B–E）** 的肌肉记忆。

### 5.4 第六节：Burst F

```text
Burst F（语音壳）：
  Voice 108 | 嵌入窗口 48 | Voice 108
```

资料库摘要（与 Part1 出/入站嵌入规则一致的方向感）：

- **出站**：F 的嵌入位置可承载 RC / Privacy / Null 等（视特性与对端需要）；  
- **入站**：常为 **Null** 嵌入。  

本课要求：知道 **F 仍是超帧的第六节**，但**不要默认 F 还在继续拼同一条 Full LC**。RC 细节以后课再展开。

### 5.5 到站：Terminator with LC

语音尾常跟数据壳：

```text
Terminator with LC：
  数据壳 + Data SYNC + Slot Type（Data Type = Terminator with LC）
  并可再带一次 LC（散会公文）
```

听感：话停了；空口上还可能闪一下控制型突发。规范还强调：数据 SYNC 本身就足以提示「语音段结束」——实现是否深解 LC 由产品决定。

### 5.6 一张时间轴总表（建议能默画）

```text
时间 →

[Voice LC Header] (可选 [PI Header])
        ↓
   ┌────超帧 360 ms────┐
   A(SYNC) B C D E F
   └───────────────────┘
        ↓  （可重复多列超帧）
   A B C D E F
        ↓
[Terminator with LC]
```

| 阶段 | 外壳 | 中心 48 | 你在找什么 |
|------|------|---------|------------|
| Voice LC Header | 数据壳 | Data SYNC | 地址/FLCO（完整门牌） |
| Burst A | 语音壳 | **Voice SYNC** | 超帧边界 / 迟入上车 |
| Burst B–E | 语音壳 | 嵌入碎片 | 拼 Full LC |
| Burst F | 语音壳 | 嵌入（用途可变） | 别误当成第二个 A |
| Terminator | 数据壳 | Data SYNC | 散会 |

### 5.7 集群补充一句（防定势）

Part1 写明：集群场景下语音**可以**不带前面的 LC Header（靠集群控制信令告知源/目的）；常规系统则 Voice LC Header 更「标配」。本课例子按**常规中继组呼**讲；你遇到 Tier III 时，把「门牌从哪来」换成控制信道叙事即可，**超帧 A–F 本身不变**。

---

## 6. 数字账本（建议钉在速查卡旁）

| 项 | 值 | 备注 |
|----|-----|------|
| Timeslot | **30 ms** | 第 15 课 |
| TDMA frame | **60 ms** | 两时隙 |
| Traffic 内容窗 | **≈ 27.5 ms** | 264 bit |
| Traffic 总比特 | **264 = 108+48+108** | 第 16 课 |
| 语音载荷 / 突发 | **216 bit** | ≈ 60 ms 压缩话 |
| **Voice superframe** | **6 × 30 ms = 360 ms** | 仅语音；标号 A–F |
| Burst A 中心 | **Voice SYNC（48）** | 超帧边界；迟入 |
| Burst B–E 中心 | **嵌入（EMB+碎片）** | 典型拼一条 Full LC |
| Full LC 嵌入拼装 | **4** 个嵌入场 | 72 bit LC + FEC → BPTC（Annex B.2.1） |
| 语音 SYNC 机会（每逻辑信道） | 约每 **360 ms** | 在 Burst A |
| 入站数据/控制 SYNC | 可至约每 **60 ms** | 无超帧 |
| 出站数据/控制 SYNC（双时隙可见） | 可至约每 **30 ms** | clause 4.3 |
| 出站语音最坏 SYNC 等待 | 约 **330 ms** | 两路超帧错 30 ms |
| 符号率 / 比特率 | **≈ 4800 baud / 9.6 kbps** | 4FSK；超帧不改 |

口算口诀：

> **三十窗、二六四箱、六箱一列三百六；A 亮灯、B 到 E 拼门牌、SYNC 不按三十贴。**

---

## 7. 常见误区

1. **「超帧 = TDMA frame。」**  
   错。TDMA frame = **60 ms**（两时隙）；超帧 = **360 ms**（六语音突发）。

2. **「超帧 = 六个时隙编号。」**  
   错。时隙仍是 **1/2**；A–F 是**同一逻辑信道上**连续六次业务突发的名字。

3. **「每个语音突发中间都是 Voice SYNC。」**  
   错。通常只有 **Burst A**；B–F 中心多为嵌入。

4. **「Voice LC Header 中间也是 Voice SYNC。」**  
   错。Header 是**数据壳**，中心是 **Data SYNC**；Voice SYNC 在超帧 **A**。

5. **「迟后进入靠每个 30 ms 重新对一次完整地址。」**  
   错。先等 **A** 的 Voice SYNC 上车，再靠嵌入/头拼 LC；所以会有短暂等待。

6. **「B–F 五个突发各自携带完整 Full LC。」**  
   错。典型是 **B–E 四个碎片**拼一条；F 另有用途叙事。

7. **「数据突发也有 A–F 超帧。」**  
   错。Part1 定义：superframe **仅用于语音**；数据/控制无此编组。

8. **「360 ms 是 RF 换频或换带宽的周期。」**  
   错。频率/带宽不变；只是时间轴上的编组长度。

9. **「听到语音就一定已经解出组号。」**  
   错。左右货仓可先出声，门牌可能仍在 B–E 拼装中——「有声无地址」时期存在。

10. **「两时隙共享同一超帧相位。」**  
    错。两逻辑信道的 SYNC/超帧位置**相互独立**；可以错开。

---
