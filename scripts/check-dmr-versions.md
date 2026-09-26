# Helper notes for the version-check routine (human-readable)

Known ETSI deliver URL patterns (replace version path segments when a newer release appears):

- TR 102 398: https://www.etsi.org/deliver/etsi_tr/102300_102399/102398/
- TS 102 361-1: https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/
- TS 102 361-2: https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/
- TS 102 361-3: https://www.etsi.org/deliver/etsi_ts/102300_102399/10236103/
- TS 102 361-4: https://www.etsi.org/deliver/etsi_ts/102300_102399/10236104/

After downloading a newer PDF into the matching folder under `dmr/`, update:
1. `dmr/官方版本状态.md`
2. `dmr/DMR协议学习导航.md` §3
3. Any lesson/handbook version anchors if they hard-code the old version
4. Sync Markdown + PDFs to GitHub via `scripts/sync-to-github.sh`
