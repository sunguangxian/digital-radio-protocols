## 8. 对照表：你会在哪些 PDU 里看见 FID

把「门牌」钉到具体 PDU，避免只会背名词。

| PDU / 路径 | Opcode 字段名 | FID 在哪 | 典型用途 |
|------------|---------------|----------|----------|
| Voice LC Header | FLCO | Octet1 | 语音开始：组呼/个呼用户 LC |
| Terminator with LC | FLCO | Octet1 | 语音结束；常与通话中同一 Voice Channel User LC |
| 嵌入 LC（超帧 B–F） | FLCO | Octet1 | 迟后进入可读地址；Talker Alias / GPS 等 |
| CSBK | CSBKO | Octet1 | 个呼请求/应答、BS 激活、前导、NACK/FNS 等 |
| Short LC（经 CACH） | SLCO | （Short LC 结构不同，本课不展开） | 活动更新等；互操作主矛盾仍在 Full LC/CSBK |
| Part3 数据头 | （数据格式字段） | 非标准化时第二数据头带 MFID | 标准 PDP vs 厂商数据 |

现场抓包顺序建议：

1. 先认 Data Type（这是 Voice LC Header？CSBK？Terminator？）。  
2. 读 Octet0 低 6 bit → FLCO 或 CSBKO。  
3. 读 Octet1 → FID。  
4. `FID==0`：查 Part2 Annex B；否则查厂商文档/MFID 表。  
5. 再解后面的地址与 Service Options。

---

## 9. 和服务选项、补充业务怎么分工（防混淆）

第 13 课讲过 **Service Options（8 bit）**：紧急、广播、优先级、OVCM、双时隙等「加料」。本课的 FID/FLCO 是另一轴线：

| 轴线 | 回答的问题 | 典型字段 |
|------|------------|----------|
| 特性集互操作 | 「这是哪一套字典里的哪一个词？」 | FID + FLCO/CSBKO |
| 补充业务加料 | 「这次标准呼叫要不要加急/广播/…？」 | Service Options 等 |
| 寻址 | 「谁跟谁说？」 | 24 bit Source / Dest 或 Group |

三者同时正确，一次标准组呼才「又认得、又找对人、又加对料」：

```text
FID=SFID  +  FLCO=Grp_V_Ch_Usr  +  Group ID 对  +  Service Options（如 Emergency）
```

私有特性往往**自己重定义**整段 LC 数据含义，不能假设 Service Options 比特还按 Table 7.11 解释。

---

## 10. 排障剧本（把课用到明天的工单）

### 剧本 1 ·「两家手台组呼正常，一键告警对面没反应」

1. 确认告警是标准 Emergency（Service Options）还是厂商「一键告警应用」。  
2. 抓空口：若告警 PDU 的 FID≠0x00 → 按 MFID 特性排查，换他厂机本来就不该通。  
3. 若 FID=0x00 且 FLCO/CSBKO 为标准紧急相关路径 → 查对端是否实现该**可选**标准特性、是否回 FNS。

### 剧本 2 ·「写着 DMR 的车载台，个呼 OACSU 无应答」

1. 查是否发出 UU_V_Req（CSBKO=`000100`）且 FID=SFID。  
2. 对端是否实现 OACSU（有的部署只用 PATCS 直接讲）。  
3. 若对端回 NACK/FNS → 读原因；若完全无 CSBK → 查信道/时隙/色码/礼貌接入，先排除 L1。

### 剧本 3 ·「升级固件后，他厂中继不认我们的某某功能」

1. 列出该功能是标准还是私有。  
2. 私有：查 MFID 是否变更、对端是否曾特制支持旧 MFID。  
3. 标准：查是否误把 FID 改非零（回归缺陷）；IOP 证书是否绑旧软件版本。

### 剧本 4 ·「仪表能解语音，却解不出别名」

1. Talker Alias 是 SFID 下 FLCO `000100`–`000111` 的嵌入 LC。  
2. 若发送端用私有格式塞「名字」→ 标准仪表/他厂机只认标准 Alias FLCO。  
3. 别把「没有别名」说成「组呼失败」——组呼 LC 与 Alias LC 是不同 FLCO。

---

## 11. 产业侧：IOP 认证在测什么（建立语感）

DMR Association 维护自愿的 **IOP（互操作）认证**流程：针对 Tier II / Tier III 的**强制与可选标准特性**做厂间对测，并保存空口日志。证书按硬件平台与软件版本管理。

对你有用的三句话：

1. **IOP 测的是标准特性清单**，不是某厂全部私有功能。  
2. 招投标写「多厂家互通」时，应对齐证书上的 **强制项**（如组呼、个呼 PATCS/OACSU、全呼等——以协会现行清单为准）。  
3. 私有特性可以卖点很亮，但要在方案书里**单独标注「仅本厂/本 MFID」**。

再补两条现场常用判断：

4. 证书通常**绑定硬件平台 + 软件版本**；大版本升级后旧证书不能想当然沿用。  
5. 「可选特性」即便是标准的，对端也可以不做；此时更常见的是能力不齐或 FNS，而不是「DMR 假冒」。

详细流程与清单见本课「推荐阅读」中的协会材料。

---

