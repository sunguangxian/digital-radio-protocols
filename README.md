> **GitHub 镜像**：本仓库同步本地多体制数字对讲协议资料库（Markdown + 官方 PDF + `学习推送/` + `codex/` 等）。
>
> **Codex 更新**：后续产出放在 [`codex/`](./codex/) 目录，随同步推送。

# 数字无线电协议资料库（digital-radio-protocols）

多协议数字对讲 / 集群学习资料库。当前 **DMR** 内容完整；其余体制为占位，逐步扩充。

## 怎么导航

| 目录 | 说明 |
|------|------|
| [`dmr/`](./dmr/) | **DMR（ETSI）** 全部现有资料：入门、空口、语音、数据、集群、课程推送、手册与总索引 |
| [`shared/`](./shared/) | 各体制共用的通信基础笔记（占位） |
| [`dpmr/`](./dpmr/) | dPMR（待建设） |
| [`nxdn/`](./nxdn/) | NXDN（待建设） |
| [`pdt/`](./pdt/) | PDT（待建设） |
| [`compare/`](./compare/) | 体制对比（占位） |
| [`codex/`](./codex/) | Codex / 工具产出更新目录 |
| [`scripts/`](./scripts/) | 同步与版本检查辅助脚本 |

### DMR 快速入口

- **总索引（检索）**：[`dmr/总索引.md`](./dmr/总索引.md)
- **新人全貌**：[`dmr/DMR整合学习手册.md`](./dmr/DMR整合学习手册.md)
- **学习导航 / 版本**：[`dmr/DMR协议学习导航.md`](./dmr/DMR协议学习导航.md)
- **附录覆盖清单**：[`dmr/附录覆盖清单.md`](./dmr/附录覆盖清单.md)
- **官方版本状态**：[`dmr/官方版本状态.md`](./dmr/官方版本状态.md)
- DMR 分册：`dmr/00-入门` … `dmr/04-集群协议`（含官方 PDF）
- 课程推送：[`dmr/学习推送/`](./dmr/学习推送/)

## 本地路径

- 主路径：`/workspace/digital-radio-protocols`
- 兼容软链：`/workspace/dmr-protocol` → 同上（旧脚本过渡用）

## 同步到 GitHub

```bash
/workspace/digital-radio-protocols/scripts/sync-to-github.sh
```
