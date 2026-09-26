# Part 2：Annex A 定时器与常数（Layer 3）

> **学习用整理，冲突以 ETSI 原文为准；非全文复制。**  
> 源：ETSI **TS 102 361-2 V2.5.1** Annex **A**（normative）。  
> Opcode 表见 [`语音业务字段速览.md`](./语音业务字段速览.md) §1（= Annex B）。  
> 覆盖清单：[`../附录覆盖清单.md`](../附录覆盖清单.md)

---

## A.1 Layer 3 timers

| 定时器 | 用途 | 量级 |
|--------|------|------|
| **T_AckWait** | 发 CSBK 后等对端响应；超时且未超重试则重发 | 建议 **360 ms**（UU_Ans_Rsp）；同播建议 min **2,0 s** |
| **T_TO** | 总超时 | Tier I = **180 s**；II/III 实现选 **0…180 s**（0=禁用） |
| **CT_RHOT** | CT_CSBK 随机 holdoff，减碰撞 | Leader 时序未知：0…**3,24 s**，步进 60 ms；已知：发后 **2,16…3,24 s**，每取消一次计划 CT 则范围减 120 ms |
| **NoLeader** | 上电/换台后，发请求前监听广域时序 | **4,5 min** |
| **SyncAge** | 广域时序信息有效期 | **10 min**；步进 SAIncr=**500 ms**（与 Part1 10.1.4 钟漂要求相关） |
| **SyncAgeWarning** | 超时前主动求更新 | **9 min**（= 2×BeaconInterval） |
| **T_MS_ChanAuth** | 信道授权等待 | 单站建议 **180 ms**；多站 **360 ms** |
| **T_BS_ChanAuthRsp** | BS 信道授权响应 | 语音单/多站建议 **720 ms**；CSBK/数据单站 **900 ms**、多站 **1140 ms** |
| **T_BS_ChanAuthSel** | 多站授权选择 | 建议 **240 ms** |
| **T_RCtimer** | Tier II RC 命令：等目标结束发射再重试 | 建议 **600 ms**（同播或需更大） |

---

## A.2 Layer 3 constants

| 常数 | 含义 | 量级 |
|------|------|------|
| **N_CSBKRetry** | CSBK 重试上限 | 实现/应用相关；UU_V_Req 建议 **1** |
| **BeaconDuration** | CT_CSBK_Beacon / Prop 时长 | min **600 ms** |
| **BeaconInterval** | 广域 Leader 两 Beacon 起始间隔 | **4,5 min** |
| **CTDuration** | CT_CSBK_Req / Resp 时长 | min **180 ms** |

---

## 与 Part 1 Annex F 的分工
- Part 1 F：**L2** 监测/hangtime/Wakeup/礼貌接入 RSSI 等。
- Part 2 A：**L3** 呼叫/CT 时序/信道授权/CSBK 重试。
