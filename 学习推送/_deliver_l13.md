# 第 13 课 · 业务全景：语音 / 数据 / 补充业务

> DMR 深入学习 · 阶段 B 全貌（业务种类专课）  
> 适合：已能分清 L1/L2/L3 与 U-plane/C-plane，但一听到「承载 / 电信业务 / 补充业务」「个呼组呼全呼」「确认 PDP / 短数据」就晕——分不清用户要的是哪一类、该翻 Part2 还是 Part3 的人  
> 阅读量：约 30–40 分钟 · 几乎不推公式 · 要把「业务三层分类」「语音过程阶段」「补充业务与 Service Options」「数据 PDP/短数据/Tier 差异」钉死  
> 若频率/带宽/调制仍糊：只提醒一句——坏射频常**看起来像**语音/数据失败，其实是 L1；详见 `学习推送/加餐_频率带宽与调制解调.md`。本课主线是**业务种类全景**，不重讲频谱。

---

## 1. 为什么本课重要（动机）

第 12 课钉死了协议分层：L1 管电波、L2 管打包保护、L3 管呼叫控制；语音主载荷走 U-plane，信令走 C-plane。下一关不是再背「三层电梯」，而是学会**把用户体验钉到业务种类上**：

- 调度员说「要个呼确认接通再说话」，你却只配了组呼信道——规范里个呼可走 **OACSU**（先问对方在不在），组呼通常不走同一套存在性检查。  
- 现场抱怨「迟了半句才听到」，有人去拧天线；其实更像 **Late Entry（迟后进入）** 是否生效、超帧同步与嵌入地址 LC 是否可读。  
- 产品说「要发状态码和 GPS」，研发去翻 Part2 语音过程——状态/预编码、原始短数据、已定义短数据、IP over PDP 的主战场在 **Part3**。  
- 集群同事说「控制信道也能发短数据」，常规模式同事说「短数据都走 PDP」——两边都对，但 **Tier I/II 与 Tier III 路径不同**。  
- 听到「补充业务」，以为是另一套完全独立的呼叫；其实它是**依附在语音/数据之上的附加能力**（紧急、优先级、广播、主叫别名等）。

若只背「DMR 能语音也能数据」七个字，后面会卡在同一处：

> **业务按电信习惯分：承载（Bearer）、电信业务（Tele-service）、补充业务（Supplementary）。语音过程在 Part2；数据 PDP/短数据在 Part3；集群控制信道短数据还要看 Part4。排障先问「用户要的是哪一类业务」，再选书。**

本课目标是让你能自己讲清十件事：

1. **为什么**要用餐厅菜单/快递业务种类来记业务全景；  
2. 一张总图：Bearer / Tele-service / Supplementary + 网络规程/特性；  
3. 白话术语：个呼、组呼、未编址、全呼、广播、OACSU、PDP、DPF、短数据等；  
4. 现场岗位与故障如何映射到「该查哪类业务」；  
5. 语音业务地图：五种呼叫形态 + 过程阶段表（含关键数字）；  
6. 补充业务地图 + **Service Options 8 bit** 整表；  
7. 数据业务地图：确认/非确认 PDP、短数据三类、IP、Tier 差异；  
8. 书架怎么叠：Part2 / Part3 / Part4 / TR clause 6；  
9. 三到四个正反完整例子 + 误区 + 自测；  
10. 为第 14 课「互操作 SFID/MFID/FLCO」留下钩子（本课只点名，不深挖）。

---

## 2. 总图 / 故事：餐厅菜单 + 快递业务种类

先把整课装进「餐厅点菜 / 快递下单」故事，再落到规范里的真实分类。精神与 `DMR整合学习手册.md` **§5**、TR 102 398 **clause 6 Services Overview** 一致。

### 2.1 餐厅菜单故事（直觉）

想象你走进一家专业对讲「餐厅」，菜单分三栏：

```text
┌─────────────────────────────────────────────────────────────┐
│  ① 主菜 = 电信业务（Tele-service）                            │
│     「我要吃一顿完整的饭」——语音个呼/组呼、完整用户通信能力     │
│                                                             │
│  ② 餐具/送餐能力 = 承载业务（Bearer）                         │
│     「厨房到餐桌的传送能力」——低层信息传送，如个呼承载、确认 PDP │
│                                                             │
│  ③ 小料/加料 = 补充业务（Supplementary）                      │
│     「加辣、加葱、加急单」——迟后进入、紧急、优先级、主叫别名…   │
│                                                             │
│  另有：店规（网络规程）、招牌特色（Feature，如站址地址）         │
└─────────────────────────────────────────────────────────────┘
```

类比要落地到机制：

| 餐厅说法 | 真实机制（请用这句对外讲） |
|----------|----------------------------|
| 「主菜」 | Tele-service：含终端功能的完整用户通信能力（如组呼语音对话） |
| 「餐具/传送」 | Bearer：低层信息传送能力（如确认分组数据承载） |
| 「加料」 | Supplementary：依附于上述业务的附加能力（Late Entry、Emergency 等） |
| 「店规 / 招牌」 | 网络规程、特性（Feature）；互操作时还要看 SFID/MFID/FLCO（第 14 课） |

### 2.2 快递业务种类故事（加深）

再换一个现场更爱用的比喻——**快递柜下单**：

```text
用户意图：「把话 / 把状态码 / 把 IP 包送到对端」
        │
        ▼
   ┌──────────── 选业务种类 ────────────┐
   │  语音件：个呼 / 组呼 / 全呼 / 广播… │
   │  数据件：确认 PDP / 非确认 PDP / 短数据 / IP │
   │  加急贴纸：Emergency / Priority / Late Entry… │
   └────────────────┬───────────────────┘
                    │
        空口仍走同一栈：L3 意图 → L2 打包 → L1 电波
        （12.5 kHz 信道 · 30 ms 时隙 · 60 ms TDMA 帧）
```

口诀：**先问「送的是语音件还是数据件、要不要加急贴纸」，再问「卡在哪一层」。** 第 12 课解决后半句，本课解决前半句。

### 2.3 规范总图（请在脑子里贴墙上）

```text
                    ┌──────────────────────────────┐
                    │   用户体验：说话 / 发状态 / 传 IP │
                    └──────────────┬───────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
   Bearer 承载              Tele-service 电信业务      Supplementary 补充
   （传送能力）              （完整用户通信）            （依附加料）
         │                         │                         │
         │              ┌──────────┴──────────┐              │
         │              ▼                     ▼              │
         │         语音类（Part2）        数据类（Part3）      │
         │         个呼/组呼/…           PDP / 短数据 / IP    │
         │              │                     │              │
         └──────────────┴──────────┬──────────┴──────────────┘
                                   │
                    Tier III 另见 Part4（控制信道短数据等）
                    导读总览：TR 102 398 clause 6
```

互操作预告（**本课不深挖**）：标准特性应通过 **SFID + FLCO** 暴露；厂商私有走 **MFID**。细节留给第 14 课。

关键数字（贯穿语音超帧与空口舞台，阶段 C 还会深挖）：

| 项 | 值 | 业务直觉 |
|----|-----|----------|
| 信道间隔 | **12.5 kHz** | 一条「地皮」上可跑两路 TDMA 业务 |
| 时隙 | **30 ms** | 一次突发舞台 |
| TDMA 帧 | **60 ms**（2×30 ms） | 双时隙一帧 |
| Traffic burst | **264 bit ≈ 27.5 ms** | 业务突发本体 |
| 语音超帧 | **A–F 共 6 突发 = 360 ms** | 语音「一句话的节奏格子」 |

---

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

## 7. 数据业务地图

主战场：**TS 102 361-3 V1.3.1（Part3）**；头字段与 DPF/SAP 枚举与 **Part1** 表衔接。集群控制信道短数据另见 **Part4**。

### 7.1 PDP：确认 vs 非确认

| 模式 | 直觉 | 头形态直觉 | 适合 |
|------|------|------------|------|
| **Confirmed 确认** | 要回执、可按块/消息重传 | C_HEAD；可有响应窗、SARQ | 重要报文、配置下发 |
| **Unconfirmed 非确认** | 发完就走，不谈 ACK | U_HEAD；A 位固定 0 等 | 周期遥测、容许丢包 |

类比：确认像「挂号信+回执」；非确认像「塞进邮筒就走」。两者都是 **PDP 承载能力**，上面可以跑短数据或 IP。

### 7.2 DPF（包格式）速记表

来自 Part1 Table **9.30**（数据速览已摘）：

| DPF | 含义 |
|-----|------|
| **0000** | UDT（Unified Data Transport） |
| **0001** | Response packet 响应包 |
| **0010** | Unconfirmed data 非确认数据 |
| **0011** | Confirmed data 确认数据 |
| **1101** | Short Data: **Defined** 已定义短数据 |
| **1110** | Short Data: **Raw or Status/Precoded** 原始或状态/预编码 |
| **1111** | Proprietary 专有 |

### 7.3 短数据三姐妹

| 种类 | 白话 | 头直觉 |
|------|------|--------|
| **Status / Precoded** | 预约定状态码（到位、告警、请求支援…） | SP_HEAD；常 DPF=`1110` |
| **Raw** | 原始比特/字节短载荷 | R_HEAD |
| **Defined** | 带字符集约定的短数据（Binary/BCD/UTF…） | DD_HEAD；DPF=`1101` |

口诀：**状态码先查预编码表；自由短报文看 Raw/Defined；别和语音 LC 混成一张抓包。**

### 7.4 IP over PDP

- 在 PDP 上承载 IP 包；常用 **UDP/IPv4 头压缩**（Part3 正文展开 UDP/IPv4；TCP HC 有 SAP 预留但 V1.3.1 未给对等完整字段表——**不要编造**）。  
- SAP 指示上层：如 IP based Packet data、UDP/IP header compression、Short Data、ARP、Proprietary 等（Part1 Table 9.31）。  
- 产品说「DMR 上网传定位」：先问确认还是非确认、压缩开没开、地址/端口怎么映射——再谈应用层 JSON。

### 7.5 Tier I/II vs Tier III（最易吵错的一张表）

| 能力 | Tier I / II（常规等） | Tier III（集群） |
|------|----------------------|------------------|
| **PDP** | 有（确认 / 非确认） | **业务信道**上可用 PDP |
| **IP over PDP** | 有 | 有（业务信道） |
| **短数据** | 多经 **PDP**（状态/原始/已定义等） | **控制信道有自有短数据业务**；业务信道亦可走 PDP |

```text
常规（I/II）：  短数据 / IP  ──►  信道上的 PDP
集群（III）：   短状态等     ──►  控制信道自有短数据  和/或  业务信道 PDP
               大包 IP      ──►  业务信道 PDP
```

现场吵架仲裁句：

> 「集群控制信道短数据是 Part4 的故事；常规模式下短数据走 Part3 PDP。两边都对，路径不同。」

---

## 8. 书架映射：Part2 / Part3 / Part4 / TR clause 6

| 书 | 版本锚点 | 本课读什么 | 不读什么（留给后课） |
|----|----------|------------|---------------------|
| **TR 102 398** | V1.5.1 | **clause 6 Services Overview** 业务总览导读 | 当法律条文覆盖 TS |
| **Part1** | V2.7.1 | 突发/超帧数字；Late Entry 指针 5.1.2；DPF/SAP/Data Header 壳 | 本课不重讲整栈（见第 12 课） |
| **Part2** | V2.5.1 | 语音过程 clause 5–6；Service Options；FLCO 语音家族 | MFID 私有深挖 → 第 14 课 |
| **Part3** | V1.3.1 | PDP 确认/非确认；短数据；IP/压缩概述 | 逐比特重传窗刷题可后置 |
| **Part4** | V1.12.1 | Tier III：控制信道短数据 vs 业务信道 PDP 的「分家」 | 登记/Grant/Reason 全表 → 集群专课 |
| **手册 §5** | 中文合成 | Bearer/Tele/Supplementary 分类与 Tier 对照表 | 冲突时让位给 TS |

冲突规则再次钉死：**TS > TR > 手册笔记**。厂商白皮书/网页科普一律当「入门导读」，数字与过程以 TS 为准。

书架叠层复习（接第 12 课）：

```text
业务种类（本课）          协议层（第12课）         书
语音 Tele-service    →   L3/C-plane + U-plane  → Part2（+Part1 壳）
补充 Supplementary   →   多落在 LC/CSBK/Options → Part2
数据 PDP/短数据/IP   →   数据呼叫控制 + 承载    → Part3（+Part1 头）
集群控制信道短数据   →   仍坐同一空口栈上       → Part4
```

---

## 9. 完整例子（正反对照）

### 例 A（正）· 班组组呼 + 迟后进入

**场景**：巡检组正在组呼；队员小王中途开机。  
**正确理解**：这是 **Group Call Tele-service** + **Late Entry 补充**。空口靠 Voice SYNC 与嵌入/头中的地址 LC，让小王对齐超帧并确认「这是我们组」。  
**不该做**：一上来换天线、改频率表，却从不查组地址/色码/是否支持迟后进入。  
**分层**：业务种类对了仍听不清 → 再查 L1 覆盖与同步。

### 例 B（正）· 个呼 OACSU 再通话

**场景**：调度要「确认张三在席再下达」。  
**正确理解**：个呼过程可先 **UU_V_Req / UU_Ans_Rsp**（OACSU 直觉），Proceed 后再 Voice LC Header（UU_V_Ch_Usr）进超帧。  
**不该做**：用组呼地址「假装个呼」，或指望 Broadcast 位解决一对一确认。  
**书**：Part2；FLCO 000011。

### 例 C（反）· 把短状态当成「语音补充业务」

**场景**：产品要「一键发状态码 0x12」。  
**错误路径**：只在 Part2 Service Options 里找「状态码比特」——找不到就骂规范不全。  
**正确路径**：这是 **短数据 Status/Precoded（Part3）**；集群若走控制信道，还要看 **Part4**。Service Options 管的是紧急/广播/优先级等，不是预编码状态表。

### 例 D（反）· 集群/常规短数据路径混谈

**场景**：常规网优说「短数据必须上 PDP」；集群网优说「控制信道天天发短数据」。  
**错误**：互指对方不懂规范。  
**正确**：对照手册 §5.3 / 本课 §7.5——**I/II 短数据多经 PDP；III 控制信道有自有短数据，业务信道仍可 PDP**。先问 Tier，再问路径。

---

## 10. 常见误区

1. **把 Bearer / Tele-service / Supplementary 当成三层协议栈** —— 不对。那是**业务分类**；协议栈仍是 L1/L2/L3（第 12 课）。  
2. **以为补充业务可以单独「打一通补充电话」** —— 多数补充是依附主呼叫的加料（迟后进入、别名、紧急位等）。  
3. **Broadcast 套到个呼上** —— 规范明确 Broadcast **仅组呼**。  
4. **Privacy=1 就等于标准加密算法已规定** —— Part2 NOTE：本规范未定义隐私算法；位存在≠算法互操作已保证。  
5. **Late Entry 失败 = 一定是射频坏了** —— 先查是否支持迟后进入、地址 LC/SYNC 是否可读，再查 L1。  
6. **所有短数据都去 Part2 找** —— 短数据主战场 Part3；集群控制信道另见 Part4。  
7. **IP over PDP = 一定要确认模式** —— 确认/非确认是产品与可靠性选择，不是「上了 IP 就自动确认」。  
8. **SFID/MFID/FLCO 本课就能讲透** —— 只能认门牌；互操作专课是第 14 课。  
9. **厂商网页写「全呼=广播=组呼」就混成一个开关** —— 产品营销词要映射回 All Call 地址约定、Broadcast 位、Grp_V_Ch_Usr；冲突以 TS 为准。  
10. **业务配置都对仍全网哑 = 继续改 Part2 定时器** —— 回忆加餐：频率/调制混乱常**表现为**业务失败，根因可能在 L1。

---

## 11. 自测（闭卷先想，再对答案）

1. **填空**：电信习惯下，业务分 ______（承载）、______（电信业务）、______（补充业务）；互操作门牌预告是 ______ / ______ / ______（第 14 课）。  
2. **选择**：Service Options 中 Broadcast=1 适用于？  
   - A. 仅个呼  
   - B. 仅组呼  
   - C. 个呼与组呼都行  
   - D. 仅数据 PDP  
3. **判断**：Tier III 短数据只能走业务信道 PDP。（对 / 错）  
4. **连线**：  
   - Grp_V_Ch_Usr FLCO → ?  
   - UU_V_Ch_Usr FLCO → ?  
   - Talker Alias FLCO 范围 → ?  
   - GPS_Info FLCO → ?  
5. **排序**：把语音过程排成时间线：Voice LC Header；Terminator with LC；可选 BS_Dwn_Act；语音超帧 A–F；可选 UU_V_Req/Ans。  
6. **简答**：为什么说「短数据状态码不应到 Service Options 里找」？请用两句话说明该翻哪本书、DPF 家族大概是什么。

### 参考答案

1. **Bearer；Tele-service；Supplementary；SFID；MFID；FLCO。**  
2. **B。**  
3. **错。** Tier III 控制信道有自有短数据业务；业务信道亦可走 PDP。  
4. **000000；000011；000100–000111；001000。**  
5. **可选 BS_Dwn_Act → 可选 UU_V_Req/Ans → Voice LC Header → 超帧 A–F → Terminator with LC。**  
6. **状态/预编码短数据属 Part3（短数据头，DPF 常为 1110 家族）；Service Options（Part2 Table 7.11）管紧急/广播/OVCM/优先级等语音加料，不管预编码状态表。**

---

## 12. 资料库加深阅读

按「先手册分类、再语音速览、再数据速览、再官方 PDF」：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `DMR整合学习手册.md` **§5** | Bearer / Tele / Supplementary + Tier 数据对照（本课骨架） |
| 2 | `02-语音业务/语音业务字段速览.md` | FLCO/CSBK、过程阶段、Service Options Table 7.11 |
| 3 | `03-数据协议/数据协议字段速览.md` | DPF/SAP、确认/非确认头、短数据三头 |
| 4 | `00-入门/DMR术语与帧结构速查卡.md` | 突发、超帧、墙上词热身 |
| 5 | `学习推送/第07课.md` | 寻址直觉：个呼/组呼（本课语音前置） |
| 6 | `学习推送/第12课.md` | 分层 L1/L2/L3（本课「种类之上还要分层」） |
| 7 | `学习推送/加餐_频率带宽与调制解调.md` | 弱项加餐；业务症状背后的 L1 |
| 8 | `总索引.md` | 关键词→文档 |
| 9 | `02-语音业务/TS102361-2_V2.5.1.pdf` | 官方 Part2；对照 clause 5–6、Service Options |
| 10 | `03-数据协议/TS102361-3_V1.3.1.pdf` | 官方 Part3；先读目录与概述再下钻 |
| 11 | `DMR协议学习导航.md` | 版本表与官方链接入口 |

官方版本锚点：**TR V1.5.1**；**Part1 V2.7.1**；**Part2 V2.5.1**；**Part3 V1.3.1**；**Part4 V1.12.1**。冲突：**TS > TR > 手册笔记**。

---

## 13. 推荐阅读与视频

本课外链为指定核验清单（2026-09-24）；**不编造地址**。策略 = **中文业务综述 + TR clause 6 + Part2/Part3 正文 + Tait 呼叫类型课 + 产业白皮书**。

1. **[什么是数字对讲机？DMR 数字无线通信原理（海川通）](https://www.hacton.com/newsinfo/1174391.html)**  
   - **为什么值得看**：中文业务综述，覆盖单呼/组呼/全呼、迟后进入、短数据/IP 等直觉。  
   - **适合哪一段**：第 2–7 节。  
   - **注意**：厂商科普；**冲突以 ETSI TS 为准**。  
   - **基础**：入门；中文。

2. **[ETSI TR 102 398 V1.5.1｜DMR General System Design](https://www.etsi.org/deliver/etsi_tr/102300_102399/102398/01.05.01_60/tr_102398v010501p.pdf)**  
   - **为什么值得看**：clause **6 Services Overview** 权威导读（语音/数据分类总览）。  
   - **适合哪一段**：第 2、8 节后作对照。  
   - **基础**：进阶；英文 PDF；本课先读 clause 6，不必一次读完全文。

3. **[ETSI TS 102 361-2 V2.5.1｜Part 2 语音与通用业务](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/02.05.01_60/ts_10236102v020501p.pdf)**  
   - **为什么值得看**：语音过程与补充业务规范正文；Service Options 终审文本。  
   - **适合哪一段**：第 5–6 节后精读 clause 5–6 / Table 7.11。  
   - **基础**：进阶；收藏。

4. **[ETSI TS 102 361-3 V1.3.1｜Part 3 数据协议](https://www.etsi.org/deliver/etsi_ts/102300_102399/10236103/01.03.01_60/ts_10236103v010301p.pdf)**  
   - **为什么值得看**：PDP / 短数据 / IP 权威定义。  
   - **适合哪一段**：第 7 节后先读目录与概述，再下钻确认/非确认与短数据。  
   - **基础**：进阶；英文 PDF。

5. **[Introduction to DMR｜Tait Radio Academy（Call Types and Features）](https://www.taitradioacademy.com/courses/introduction-to-digital-mobile-radio/)**  
   - **为什么值得看**：英文结构化课；Lesson 4 专讲呼叫类型与特性，和本课语音/补充地图同频。  
   - **适合哪一段**：第 5–6 节；通勤复习。  
   - **基础**：入门；英文课程/视频。

6. **[DMR Association｜Benefits and Features of DMR White Paper](https://www.dmrassociation.org/public-downloads/documents/White-Papers/DMR-Association-White-Paper_Benefits-and-Features-of-DMR_160512.pdf)**  
   - **为什么值得看**：产业白皮书列举 Late Entry、Talking Party ID、数据应用等，适合建立「特性清单」语感。  
   - **适合哪一段**：第 6–7 节；与 TS 对照着看。  
   - **注意**：版本可能偏旧；**细节以最新 TS 为准**。  
   - **基础**：入门～进阶；英文 PDF。

**说明**：专门只讲「DMR 业务分类」的优质长篇中文视频不好找；本课用 **中文综述 + TR/TS + Tait 课程** 补充。业务边界、Service Options 与 DPF 以本课与语音/数据字段速览、ETSI TS 为准。

---

## 14. 下一课预告

**第 14 课 · 互操作：SFID / MFID / FLCO**

你已经能说出：业务按 Bearer / Tele-service / Supplementary 分类；语音个呼/组呼等走 Part2，补充加料看 Service Options 与 Late Entry/别名等；数据看 Part3 的 PDP/短数据/IP，集群控制信道短数据还要看 Part4。下一课会把「特性怎么在空口上被认出、标准与厂商如何共存」钉死——**SFID、MFID、FLCO** 是互操作的门牌与功能码，仍然少公式，多现场对照：为什么同频同色码仍可能「各说各话」。

---

*推送说明：本课为阶段 B「业务全景：语音 / 数据 / 补充业务」专课。不加长篇频率加餐，只保留一句指向加餐文的提醒，并点明坏射频常表现为语音/数据失败。主文加厚覆盖动机、餐厅/快递总图、术语、现场对照、语音过程与 OACSU、补充业务与 Service Options 8 bit 表、数据 PDP/短数据/Tier 差异、书架映射、正反例、误区、自测与六条核验外链。读完应能向同事讲清「用户要的是哪类业务、该翻 Part2 还是 Part3/4」，并为第 14 课 SFID/MFID/FLCO 打好业务全景地基。*
