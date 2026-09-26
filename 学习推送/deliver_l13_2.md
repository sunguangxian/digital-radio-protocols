## 3. 白话术语表

| 术语 | 白话 | 现场你会碰到 |
|------|------|----------------|
| **Bearer（承载业务）** | 低层「能把信息送过去」的能力 | 「确认 PDP 承载」「个呼承载」 |
| **Tele-service（电信业务）** | 含终端功能的完整用户通信 | 「组呼语音业务」「个呼语音」 |
| **Supplementary（补充业务）** | 依附在主业务上的加料 | 迟后进入、紧急、优先级、广播位 |
| **Individual Call 个呼** | 一对一语音 | UU_V_Ch_Usr；可能先 OACSU |
| **Group Call 组呼** | 一对多（组地址） | Grp_V_Ch_Usr；调度最常用 |
| **Unaddressed 未编址语音** | 不靠常规目的地址那套路的语音形态 | 过程见 Part2；与编址组呼对照记 |
| **All Call 全呼** | 面向「所有人」类广播意图 | 常与 Broadcast 位 / 全呼地址约定一起出现 |
| **Broadcast 广播呼叫** | Service Options 里 Broadcast=1（**仅组呼**） | 「只听不回」类产品说法要对照规范位 |
| **OACSU** | 个呼前「对方在不在」的存在性检查直觉 | UU_V_Req → UU_Ans_Rsp / NACK |
| **Voice LC Header** | 语音开始时带地址的 LC 头 | Data Type 语音头；含 FLCO/地址/Service Options |
| **Terminator with LC** | 语音结束/挂起时的终结 LC | 与通话中 Voice Channel User LC 同家族 |
| **Late Entry 迟后进入** | 中途开机/入网仍能跟上正在进行的组呼 | Voice SYNC + 嵌入地址 LC（Part1 5.1.2） |
| **Talker Alias** | 主叫别名（可读名字） | FLCO 000100–000111 嵌入超帧 |
| **Service Options** | 语音 LC/CSBK 里 8 bit「加料开关」 | Emergency / Privacy / Broadcast / OVCM / Priority |
| **OVCM** | Open Voice Call Mode | Service Options 中 1 bit |
| **Emergency Interrupt** | 紧急打断正在发射的台 | Part2 过程条款（补充能力） |
| **PDP** | Packet Data Protocol 分组数据协议 | 确认 / 非确认；Part3 |
| **DPF** | Data Packet Format 包格式 | UDT/Response/确认/非确认/短数据/专有 |
| **短数据 Short Data** | 状态/预编码、原始、已定义 | DPF 1101 / 1110 家族 |
| **IP over PDP** | 在 PDP 上跑 IP（常配 UDP/IPv4 头压缩） | SAP 指示压缩/IP |
| **SFID / MFID / FLCO** | 标准特性集 / 厂商特性集 / 功能码 | **第 14 课主战场**；本课只认门牌 |

---

## 4. 现场对照（岗位 / 故障 → 业务种类）

把「谁在抱怨什么」映射到业务抽屉，避免一上来就拆射频：

| 岗位 / 现象 | 先怀疑哪类业务 | 该翻哪本 | 分层提醒 |
|-------------|----------------|----------|----------|
| 调度：A 台打 B 台，要先确认接通 | **个呼 + OACSU** | Part2 | L3/C-plane；不是「再加个组号」 |
| 班组：全组听指挥 | **组呼** | Part2 | 最常见 Tele-service |
| 中途开机听不到正在讲的组 | **Late Entry** 补充 | Part2 + Part1 5.1.2 | 常被误判成「天线坏了」 |
| 屏幕要显示主叫名字/别名 | **Talker Alias** | Part2 FLCO 000100–000111 | 嵌入超帧，不是另开一路模拟音 |
| 紧急键红了、要插队 | **Emergency / Priority / Interrupt** | Part2 Service Options + 过程 | 补充业务位 + 过程，不是只改音量 |
| 只要「全员听、少回传」 | **Broadcast / All Call** | Part2 Broadcast 位 + 地址约定 | Broadcast **仅组呼** |
| 发「到位/告警」状态码 | **短数据 Status/Precoded** | Part3 | 别在 Part2 语音过程里找状态码表 |
| 传一段自定义短报文 | **短数据 Raw / Defined** | Part3 | DPF 1110 / 1101 |
| 传定位/传感器 IP 包 | **IP over PDP** | Part3 | 确认还是非确认要产品先定 |
| 集群：控制信道刷短状态 | **Tier III 控制信道短数据** | Part4（+TR） | 与常规「事事走 PDP」不同 |
| 语音破、同步花、覆盖怪 | **先别改业务种类** | 加餐文 + Part1 | 常是 **L1**；见加餐 `学习推送/加餐_频率带宽与调制解调.md` |

排障口诀：**症状像业务，先确认业务种类与配置；种类对了仍坏，再分层（L1/L2/L3）。**

---

## 5. 语音业务地图

主战场：**TS 102 361-2 V2.5.1（Part2）**。空口壳与时序数字仍来自 Part1；冲突时 **TS > TR > 手册**。

### 5.1 五种形态（先认脸）

| 形态 | 直觉 | 典型空口记号 |
|------|------|----------------|
| **个呼 Individual** | 一对一 | FLCO **000011** UU_V_Ch_Usr；可先 UU_V_Req/Ans |
| **组呼 Group** | 一对多（组地址） | FLCO **000000** Grp_V_Ch_Usr |
| **未编址 Unaddressed** | 不走常规「目的地址那套路」的语音形态 | 与编址组呼对照 Part2 过程条款 |
| **全呼 All Call** | 「所有人」类意图 | 常配合全呼地址约定 + 组呼 LC 家族 |
| **广播 Broadcast** | Service Options.Broadcast=1 | **仅组呼**；产品「只听不回」要对照此位 |

记忆钉：组呼/全呼/广播多落在 **Grp_V_Ch_Usr**；个呼落在 **UU_V_Ch_Usr**。二者都是 Full LC 业务 PDU，公共前缀含 FLCO 与 FID（标准时 FID=SFID）。

### 5.2 OACSU 直觉（个呼「先敲门」）

类比：打内线电话前，总机先问「对方在不在席」。

```text
可选：BS_Dwn_Act（唤醒/激活中继出站）
        │
        ▼
个呼存在性：UU_V_Req  ──►  UU_Ans_Rsp（Proceed / Deny）
                │              或 NACK_Rsp
                ▼
        对方允许 → 再进 Voice LC Header + 语音超帧
```

- **UU_V_Req** CSBKO=`000100`；**UU_Ans_Rsp** CSBKO=`000101`；拒绝还可走 **NACK_Rsp**。  
- 组呼通常**不走**这套「先问在不在」——所以调度「个呼要确认、组呼要秒通」是两种产品语义，对应两套过程。  
- OACSU 是**直觉名**；现场以 Part2 个呼过程与 CSBK 为准，不要 invent 厂商黑话当规范。

### 5.3 过程阶段表（请背成时间线）

| 阶段 | 空口大概模样 | 典型 PDU / 记号 |
|------|--------------|-----------------|
| 0. 可选唤醒 BS | CSBK | **BS_Dwn_Act**（CSBKO 111000） |
| 1. 个呼存在性（可选） | CSBK | **UU_V_Req → UU_Ans_Rsp / NACK** |
| 2. 语音开始 | Voice LC Header | **Grp_V_Ch_Usr** 或 **UU_V_Ch_Usr**（含 Service Options、地址） |
| 3. 语音进行 | 超帧 A–F | Voice + SYNC(A)；B–F 可嵌 LC（别名/GPS 等） |
| 4. 语音结束 / 挂起 | Terminator with LC | 同 Voice Channel User LC 家族；BS 可在 hangtime 续发 |

时间肌肉记忆：

- 一个时隙 **30 ms**；两时隙一帧 **60 ms**。  
- 业务突发约 **264 bit ≈ 27.5 ms**。  
- 语音超帧 **A–F = 6 突发 = 360 ms**——别名、GPS 等信息是「嵌在超帧节奏里」送的，不是另开一条模拟副载波给你听。

### 5.4 和分层的接线（复习第 12 课）

- **谁跟谁说、建没建起来、紧急/广播位**：C-plane + L3/L2 信令（Voice LC Header、CSBK）。  
- **嗓音比特本身**：U-plane，经 L2 声码器接口进突发。  
- **飞不出去 / 同步花**：先看 L1（12.5 kHz、4FSK、收发切换）——再回来查业务配置。

---

## 6. 补充业务地图 + Service Options

补充业务不是「第三种主菜」，而是**贴在语音（或相关过程）上的加料**。字段落点见 `02-语音业务/语音业务字段速览.md` §6–§7。

### 6.1 常见补充 / 特性（本课必认）

| 名称 | 白话 | 主要落点 |
|------|------|----------|
| **Late Entry 迟后进入** | 中途加入仍能解码正在进行的呼叫 | Voice SYNC + 嵌入/头中的地址 LC（Part1 **5.1.2**） |
| **Talker Alias 主叫别名** | 显示可读名字而不只是号码 | FLCO **000100–000111**（头 + block1/2/3） |
| **GPS_Info** | 嵌入位置信息 | FLCO **001000** |
| **Emergency 紧急** | 紧急呼叫标记 | Service Options.Emergency=1；Act_Updt 亦可反映紧急语音活动 |
| **Priority 优先级** | P1/P2/P3 | Service Options 低 2 bit |
| **Broadcast** | 广播（仅组） | Service Options.Broadcast=1 |
| **OVCM** | Open Voice Call Mode | Service Options.OVCM |
| **Emergency Interrupt** | 请求打断正在发射的台 | Part2 过程（如 clause 6.3.4 一带）；本课记「有这件事」 |

### 6.2 Service Options（Table 7.11）— 8 bit 整表

这是本课**必须能默写**的一张表（Part2 Table **7.11**）：

| 子域 | 比特宽 | 取值 |
|------|--------|------|
| **Emergency** | 1 | `0` 非紧急；`1` 紧急 |
| **Privacy** | 1 | 本规范未定义具体隐私算法（NOTE）；位存在≠算法已标准化 |
| **Reserved** | 2 | 固定 **`00`** |
| **Broadcast** | 1 | `0` 非广播；`1` 广播（**仅组呼**） |
| **OVCM** | 1 | `0` / `1` |
| **Priority level** | 2 | `00` 无；`01` P1；`10` P2；`11` P3（最高） |

位序直觉（从高到低记「紧急→隐私→保留→广播→OVCM→优先级」）：

```text
  [ Emergency | Privacy | Reserved(00) | Broadcast | OVCM | Priority(2) ]
       1            1           2            1         1         2
```

现场口播模板：

> 「这通组呼 Service Options：非紧急、未开广播、优先级 P2——对应 bit 模式要能在抓包/日志里对上 Table 7.11。」

### 6.3 补充业务与「主业务」的关系（防晕）

```text
组呼 Tele-service
   ├─ 可加 Late Entry（别人中途进来）
   ├─ 可加 Talker Alias（显示谁在说）
   ├─ 可加 Emergency / Priority（加急贴纸）
   └─ 可加 Broadcast=1（广播语义，仅组）

个呼 Tele-service
   ├─ 可走 OACSU（先敲门）
   ├─ 可加 Emergency / Priority
   └─ Broadcast 位对个呼不适用（规范：仅组呼）
```

---

