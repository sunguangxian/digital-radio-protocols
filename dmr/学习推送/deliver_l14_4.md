## 12. 常见误区

1. **「都是 DMR，一定互通」**  
   错。互通的是 **SFID 下的标准特性**；MFID 私有不保证。

2. **「FID 就是设备 ID / 电台号」**  
   错。电台号是 24 bit 地址；FID 是 8 bit 特性集门牌。

3. **「FLCO 和 CSBKO 是同一个表」**  
   错。都是 6 bit，但分属 Full LC 与 CSBK，枚举不同。

4. **「把标准组呼改成 MFID 更有利于绑定客户」**  
   错，且违规于互操作设计：标准化特性必须经 SFID 暴露。

5. **「对端忽略我的私有 LC，就是协议栈有 Bug」**  
   通常不是。无对应 MFID 时忽略是正常行为。

6. **「FNS 等于呼叫失败因为信道忙」**  
   不必然。FNS 更接近「功能不支持」；忙/拒绝还有其他 Reason/NACK 语义（集群侧更复杂，后课再讲）。

7. **「Colour Code 不同也能靠 SFID 互通」**  
   Colour Code 管同频系统区分；门牌对了但色码不对，照样不该进错系统。两者都要满足。

8. **「Part3 数据没有互操作问题」**  
   有。标准化数据走规定头；非标准化走 MFID 路径。别用私有头冒充标准 PDP。

---

## 13. 自测（4–6 题）

**题 1.** SFID 的典型取值是什么？它代表什么？  
<details><summary>参考答案</summary>
`00000000`（0x00）。表示 TS 102 361-2 的标准默认特性集（Standards Feature ID）。
</details>

**题 2.** 规范要求：设备已实现的、Part2 已标准化的特性，应如何在空口上暴露？  
<details><summary>参考答案</summary>
只能通过 **默认 SFID + 对应的标准 FLCO（或同类标准 Opcode）** 访问；不得改挂 MFID 来「重包装」标准特性。
</details>

**题 3.** 抓包见 Full LC：`FID=0x00`，`FLCO=000011`。这最可能是什么业务？  
<details><summary>参考答案</summary>
标准个呼语音信道用户 LC（UU_V_Ch_Usr）。
</details>

**题 4.** A 厂私有巡更功能，B 厂终端完全无反应，但标准组呼正常。最可能的原因？  
<details><summary>参考答案</summary>
巡更走 **MFID**，B 厂无该特性集；组呼走 SFID 故仍通。属于预期的私有特性不互通，不是「DMR 坏了」。
</details>

**题 5.** FID 落在 `00000100`…`01111111` 区间意味着什么？  
<details><summary>参考答案</summary>
**MFID 厂商区**（学习摘要）。应按厂商特性集解释；他厂设备通常不保证理解。
</details>

**题 6.** 什么是 FNS？它和「进错 MFID 商场」有何不同？  
<details><summary>参考答案</summary>
FNS = Feature Not Supported：门牌仍是 **SFID**，但该标准 Opcode 本机未实现，礼貌拒绝。  
「进错 MFID」则是对端根本不在你的私有门牌体系里，往往直接忽略，而不是按标准 FNS 语义应答。
</details>

---

## 14. 本节钉死的句子（可直接对外讲）

1. **FID 是特性集门牌；FLCO/CSBKO 是门牌下的功能码。**  
2. **SFID=0x00 是标准馆；标准业务必须开在标准馆。**  
3. **MFID 是厂商私密馆；不通往往是预期，不是天线锅。**  
4. **禁止把已标准化特性改挂 MFID；禁止用 SFID 冒充私有语义。**  
5. **同频、同色码、同地址只保证「能听见比特」；FID+Opcode 一致才谈得上「听懂业务」。**  
6. **IOP 认证对齐的是标准特性清单；私有特性要在方案里单列。**  
7. **Service Options 是加料，FID/FLCO 是词典；两者都对才算一次标准呼叫完整。**  
8. **排障先分流：L1 不稳先修射频；门牌不对再吵厂家。**

---

## 15. 资料库加深阅读

按「先 Annex H → 外壳字段 → 语音 Opcode → 手册互操作段 → 官方 PDF」：

| 顺序 | 路径 | 读什么 |
|------|------|--------|
| 1 | `01-空中接口/AnnexA编址与AnnexH_FID.md` | Annex H：FID 分区与 SFID/MFID 模型（本课骨架） |
| 2 | `01-空中接口/CSBK与LC字段详表.md` §4 / §6 | Full LC / CSBK 外壳：FLCO、FID、CSBKO 在哪一字节 |
| 3 | `02-语音业务/语音业务字段速览.md` §1–§3 | FLCO/CSBKO 表与 Grp/UU LC 字段 |
| 4 | `DMR整合学习手册.md` §5.1 | 互操作四行金句 |
| 5 | `00-入门/DMR术语与帧结构速查卡.md` | SFID/MFID/FLCO 墙上词 |
| 6 | `学习推送/第13课.md` | 业务全景（本课前置） |
| 7 | `学习推送/第07课.md` | 个呼/组呼寻址直觉 |
| 8 | `学习推送/加餐_频率带宽与调制解调.md` | 弱项加餐；别把 L1 当互操作 |
| 9 | `总索引.md` | 关键词 Colour Code、FID、FLCO |
| 10 | `01-空中接口/TS102361-1_V2.7.1.pdf` | 官方 Annex **H** Feature interoperability |
| 11 | `02-语音业务/TS102361-2_V2.5.1.pdf` | 官方 clause **4.3**；Annex B Opcode 表 |

官方版本锚点：**TR V1.5.1**；**Part1 V2.7.1**；**Part2 V2.5.1**；**Part3 V1.3.1**；**Part4 V1.12.1**。冲突：**TS > TR > 手册笔记**。

---

