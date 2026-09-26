# DMR 官方版本检查 / ETSI PDF 自动更新

## GitHub Action（推荐）

仓库已配置工作流 [`.github/workflows/update-dmr-pdfs.yml`](../.github/workflows/update-dmr-pdfs.yml)：

| 项 | 说明 |
|----|------|
| 定时 | 每周一 **01:29 UTC**（= **09:29 Asia/Shanghai**），cron `29 1 * * 1` |
| 手动 | Actions → **Update DMR ETSI PDFs** → Run workflow，或见下方 `gh` |
| 逻辑 | 运行 [`scripts/update-dmr-pdfs.py`](./update-dmr-pdfs.py) |
| 有更新 | 下载新 PDF → 更新 `dmr/官方版本状态.md`（及导航版本锚点）→ bot commit `chore(dmr): update ETSI PDFs` 推到 `main` |
| 无更新 | exit 0，不产生 commit |
| 拉取失败 | exit 1，Actions 显示失败（不静默） |

### 手动触发

```bash
gh workflow run update-dmr-pdfs.yml --repo sunguangxian/digital-radio-protocols
# 或
gh workflow run "Update DMR ETSI PDFs" --repo sunguangxian/digital-radio-protocols
```

查看最近运行：

```bash
gh run list --workflow=update-dmr-pdfs.yml --repo sunguangxian/digital-radio-protocols
```

## 本地运行（可测）

在仓库根目录：

```bash
# 仅探测版本（不改文件）
python3 scripts/update-dmr-pdfs.py --check-only

# 探测但不写入
python3 scripts/update-dmr-pdfs.py --dry-run

# 实际下载并更新 Markdown / PDF
python3 scripts/update-dmr-pdfs.py
```

脚本会带浏览器式 `User-Agent` 访问 ETSI deliver 目录；裸 curl 可能被 Cloudflare 拦成 403。

## ETSI deliver URL 模式

版本目录形如 `MM.mm.pp_60`（对应 `V{M}.{m}.{p}`），PDF 在其子目录：

- TR 102 398: https://www.etsi.org/deliver/etsi_tr/102300_102399/102398/
- TS 102 361-1: https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/
- TS 102 361-2: https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/
- TS 102 361-3: https://www.etsi.org/deliver/etsi_ts/102300_102399/10236103/
- TS 102 361-4: https://www.etsi.org/deliver/etsi_ts/102300_102399/10236104/

参考（可能滞后）：https://www.dmrassociation.org/dmr-standards.html  
**以 ETSI deliver 可下载发布版为准。**

更新 PDF 后请同步核对：

1. `dmr/官方版本状态.md`
2. `dmr/DMR协议学习导航.md` §3
3. 课程/手册里硬编码的旧版本号（如有）
4. 需要时用 `scripts/sync-to-github.sh` 把本地资料库整树推上 GitHub
