#!/usr/bin/env python3
"""Check ETSI for newer DMR PDFs and update the local library.

Discovers published versions by listing ETSI deliver directories
(https://www.etsi.org/deliver/...), downloads newer PDFs when found,
and updates dmr/官方版本状态.md (and navigation version anchors when
straightforward).

Exit codes:
  0 — success (updated files, or nothing newer)
  1 — failure to fetch ETSI / download / parse (CI should go red)
  2 — usage / local path error
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

USER_AGENT = (
    "Mozilla/5.0 (compatible; digital-radio-protocols-bot/1.0; "
    "+https://github.com/sunguangxian/digital-radio-protocols) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
TIMEOUT_S = 60

REPO_ROOT_DEFAULT = Path(__file__).resolve().parents[1]
STATUS_REL = Path("dmr") / "官方版本状态.md"
NAV_REL = Path("dmr") / "DMR协议学习导航.md"

VERSION_DIR_RE = re.compile(r"(\d{2})\.(\d{2})\.(\d{2})_60")
STATUS_ROW_RE = re.compile(
    r"^\|\s*(TR 102 398|TS 102 361-[1-4])\s*\|\s*(V\d+\.\d+\.\d+)\s*\|\s*`([^`]+)`\s*\|",
    re.MULTILINE,
)
PDF_VERSION_RE = re.compile(r"_V(\d+\.\d+\.\d+)(?:_|\.pdf)", re.IGNORECASE)


@dataclass(frozen=True)
class DocSpec:
    key: str  # e.g. "TR 102 398"
    folder: str  # under dmr/
    deliver_base: str  # directory listing URL ending with /
    pdf_stem: str  # local filename stem prefix, e.g. "TR102398"
    etsi_pdf_prefix: str  # e.g. "tr_102398"
    etsi_doc_id: str  # path segment e.g. "102398" or "10236101"
    local_suffix: str  # extra suffix for TR only, e.g. "_系统设计总览"
    nav_label: str  # bold label in nav table


DOCS: list[DocSpec] = [
    DocSpec(
        key="TR 102 398",
        folder="00-入门",
        deliver_base="https://www.etsi.org/deliver/etsi_tr/102300_102399/102398/",
        pdf_stem="TR102398",
        etsi_pdf_prefix="tr_102398",
        etsi_doc_id="102398",
        local_suffix="_系统设计总览",
        nav_label="TR 102 398",
    ),
    DocSpec(
        key="TS 102 361-1",
        folder="01-空中接口",
        deliver_base="https://www.etsi.org/deliver/etsi_ts/102300_102399/10236101/",
        pdf_stem="TS102361-1",
        etsi_pdf_prefix="ts_10236101",
        etsi_doc_id="10236101",
        local_suffix="",
        nav_label="TS 102 361-1",
    ),
    DocSpec(
        key="TS 102 361-2",
        folder="02-语音业务",
        deliver_base="https://www.etsi.org/deliver/etsi_ts/102300_102399/10236102/",
        pdf_stem="TS102361-2",
        etsi_pdf_prefix="ts_10236102",
        etsi_doc_id="10236102",
        local_suffix="",
        nav_label="TS 102 361-2",
    ),
    DocSpec(
        key="TS 102 361-3",
        folder="03-数据协议",
        deliver_base="https://www.etsi.org/deliver/etsi_ts/102300_102399/10236103/",
        pdf_stem="TS102361-3",
        etsi_pdf_prefix="ts_10236103",
        etsi_doc_id="10236103",
        local_suffix="",
        nav_label="TS 102 361-3",
    ),
    DocSpec(
        key="TS 102 361-4",
        folder="04-集群协议",
        deliver_base="https://www.etsi.org/deliver/etsi_ts/102300_102399/10236104/",
        pdf_stem="TS102361-4",
        etsi_pdf_prefix="ts_10236104",
        etsi_doc_id="10236104",
        local_suffix="",
        nav_label="TS 102 361-4",
    ),
]


def version_tuple(v: str) -> tuple[int, int, int]:
    s = v.lstrip("Vv")
    parts = s.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"bad version: {v!r}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def format_version(t: tuple[int, int, int]) -> str:
    return f"V{t[0]}.{t[1]}.{t[2]}"


def dir_to_version(dirname: str) -> tuple[int, int, int] | None:
    m = VERSION_DIR_RE.fullmatch(dirname.strip("/"))
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def version_to_dir(t: tuple[int, int, int]) -> str:
    return f"{t[0]:02d}.{t[1]:02d}.{t[2]:02d}_60"


def version_to_etsi_pdf_name(spec: DocSpec, t: tuple[int, int, int]) -> str:
    return f"{spec.etsi_pdf_prefix}v{t[0]:02d}{t[1]:02d}{t[2]:02d}p.pdf"


def local_pdf_name(spec: DocSpec, t: tuple[int, int, int]) -> str:
    return f"{spec.pdf_stem}_{format_version(t)}{spec.local_suffix}.pdf"


def http_get(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            status = getattr(resp, "status", 200)
            if status >= 400:
                raise RuntimeError(f"HTTP {status} for {url}")
            data = resp.read()
            ctype = (resp.headers.get("Content-Type") or "").lower()
            # Cloudflare / HTML challenge pages must not look like success
            if "text/html" in ctype and url.lower().endswith(".pdf"):
                raise RuntimeError(f"got HTML instead of PDF for {url}")
            return data
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} for {url}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"network error for {url}: {e.reason}") from e


def list_version_dirs(html: str) -> list[tuple[int, int, int]]:
    found: set[tuple[int, int, int]] = set()
    for m in VERSION_DIR_RE.finditer(html):
        found.add((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return sorted(found)


def latest_published(spec: DocSpec) -> tuple[tuple[int, int, int], str]:
    """Return (version_tuple, pdf_url) for the newest published edition."""
    html = http_get(spec.deliver_base).decode("utf-8", errors="replace")
    versions = list_version_dirs(html)
    if not versions:
        raise RuntimeError(f"no version directories found at {spec.deliver_base}")
    latest = versions[-1]
    vdir = version_to_dir(latest)
    # Confirm PDF exists inside version dir listing
    sub_url = f"{spec.deliver_base}{vdir}/"
    sub_html = http_get(sub_url).decode("utf-8", errors="replace")
    pdf_name = version_to_etsi_pdf_name(spec, latest)
    if pdf_name not in sub_html:
        # Fall back: any .pdf link in the version folder
        pdfs = re.findall(r'href="[^"]+/([^"/]+\.pdf)"', sub_html, re.I)
        pdfs += re.findall(r'HREF="[^"]+/([^"/]+\.pdf)"', sub_html, re.I)
        if not pdfs:
            raise RuntimeError(f"no PDF listed under {sub_url}")
        pdf_name = pdfs[0]
    pdf_url = f"{spec.deliver_base}{vdir}/{pdf_name}"
    return latest, pdf_url


def read_local_versions(repo: Path) -> dict[str, tuple[int, int, int]]:
    """Prefer 官方版本状态.md; fall back to PDF filenames in folders."""
    out: dict[str, tuple[int, int, int]] = {}
    status = repo / STATUS_REL
    if status.is_file():
        text = status.read_text(encoding="utf-8")
        for m in STATUS_ROW_RE.finditer(text):
            out[m.group(1)] = version_tuple(m.group(2))
    for spec in DOCS:
        if spec.key in out:
            continue
        folder = repo / "dmr" / spec.folder
        if not folder.is_dir():
            continue
        best: tuple[int, int, int] | None = None
        for pdf in folder.glob(f"{spec.pdf_stem}_V*.pdf"):
            m = PDF_VERSION_RE.search(pdf.name)
            if not m:
                continue
            t = version_tuple(m.group(1))
            if best is None or t > best:
                best = t
        if best is not None:
            out[spec.key] = best
    return out


def shanghai_today() -> str:
    # Asia/Shanghai = UTC+8 (no DST)
    now = dt.datetime.utcnow() + dt.timedelta(hours=8)
    return now.strftime("%Y-%m-%d")


def update_status_md(
    repo: Path,
    versions: dict[str, tuple[int, int, int]],
    log_note: str,
) -> bool:
    path = repo / STATUS_REL
    text = path.read_text(encoding="utf-8")
    changed = False

    def repl_row(m: re.Match[str]) -> str:
        nonlocal changed
        key = m.group(1)
        if key not in versions:
            return m.group(0)
        new_v = format_version(versions[key])
        spec = next(s for s in DOCS if s.key == key)
        new_path = f"{spec.folder}/{local_pdf_name(spec, versions[key])}"
        old = m.group(0)
        new = f"| {key} | {new_v} | `{new_path}` |"
        if old != new:
            changed = True
        return new

    text2 = STATUS_ROW_RE.sub(repl_row, text)

    # Append check log row
    today = shanghai_today()
    log_line = f"| {today} | {log_note} | 自动检查（GitHub Actions / scripts/update-dmr-pdfs.py） |"
    # Insert after header separator of 核对日志 table if not already today+same note
    if log_line not in text2:
        # Find 核对日志 table body end — append before ## 检查来源
        marker = "## 检查来源"
        if marker in text2:
            # Find last log row before marker
            head, tail = text2.split(marker, 1)
            if not head.rstrip().endswith("|"):
                head = head.rstrip() + "\n"
            head = head.rstrip() + "\n" + log_line + "\n\n"
            text2 = head + marker + tail
            changed = True
        else:
            text2 = text2.rstrip() + "\n\n" + log_line + "\n"
            changed = True

    if text2 != text:
        path.write_text(text2, encoding="utf-8")
        changed = True
    return changed


def update_nav_md(repo: Path, versions: dict[str, tuple[int, int, int]]) -> bool:
    """Update §3 table version cells and download links when present."""
    path = repo / NAV_REL
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    original = text
    for spec in DOCS:
        if spec.key not in versions:
            continue
        t = versions[spec.key]
        vstr = format_version(t)
        vdir = version_to_dir(t)
        pdf = version_to_etsi_pdf_name(spec, t)
        pdf_url = f"{spec.deliver_base}{vdir}/{pdf}"

        # Replace version in table row for this doc: **V...** or V...
        # Match line containing the nav label and update version + link
        line_re = re.compile(
            rf"(\|\s*\*\*{re.escape(spec.nav_label)}\*\*.*?\|\s*)"
            rf"(\*\*)?(V\d+\.\d+\.\d+)(\*\*)?"
            rf"([^*|\n]*)"
            rf"(\|\s*\[下载\]\()([^)]+)(\))",
            re.MULTILINE,
        )

        def line_repl(m: re.Match[str], _vstr: str = vstr, _url: str = pdf_url) -> str:
            star_l = m.group(2) or ""
            star_r = m.group(4) or ""
            # Preserve star markers around version if they existed
            if star_l and star_r:
                ver = f"**{_vstr}**"
            else:
                ver = _vstr
            # Keep trailing note (e.g. date / star emoji) if any, but refresh bare version
            trail = m.group(5)
            # If trail was only " (YYYY-MM)" or " ⭐ ...", leave it; strip old version dates lightly
            return f"{m.group(1)}{ver}{trail}{m.group(6)}{_url}{m.group(8)}"

        text, n = line_re.subn(line_repl, text, count=1)
        if n == 0:
            # Softer fallback: replace known old V in row containing key
            for line in text.splitlines():
                if spec.nav_label in line and "V" in line:
                    new_line = re.sub(r"V\d+\.\d+\.\d+", vstr, line, count=1)
                    new_line = re.sub(
                        r"https://www\.etsi\.org/deliver/[^)\s]+",
                        pdf_url,
                        new_line,
                        count=1,
                    )
                    if new_line != line:
                        text = text.replace(line, new_line, 1)
                    break

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def download_pdf(url: str, dest: Path) -> None:
    data = http_get(url)
    if len(data) < 1000 or not data.startswith(b"%PDF"):
        raise RuntimeError(f"download does not look like a PDF ({url}, {len(data)} bytes)")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(dest)


def remove_old_pdfs(folder: Path, spec: DocSpec, keep: Path) -> None:
    for pdf in folder.glob(f"{spec.pdf_stem}_V*.pdf"):
        if pdf.resolve() != keep.resolve():
            pdf.unlink()


def run(repo: Path, *, check_only: bool, dry_run: bool) -> int:
    print(f"repo: {repo}")
    local = read_local_versions(repo)
    if not local:
        print("ERROR: could not read any local versions", file=sys.stderr)
        return 2

    print("local versions:")
    for spec in DOCS:
        v = local.get(spec.key)
        print(f"  {spec.key}: {format_version(v) if v else '(missing)'}")

    remote: dict[str, tuple[int, int, int]] = {}
    pdf_urls: dict[str, str] = {}
    errors: list[str] = []

    for spec in DOCS:
        try:
            latest, url = latest_published(spec)
            remote[spec.key] = latest
            pdf_urls[spec.key] = url
            print(f"ETSI {spec.key}: {format_version(latest)} -> {url}")
        except Exception as e:  # noqa: BLE001 — surface any fetch failure
            errors.append(f"{spec.key}: {e}")
            print(f"ERROR fetching {spec.key}: {e}", file=sys.stderr)

    if errors:
        print(f"FAILED to fetch {len(errors)}/{len(DOCS)} standards from ETSI", file=sys.stderr)
        return 1

    updates: list[DocSpec] = []
    for spec in DOCS:
        loc = local.get(spec.key)
        rem = remote[spec.key]
        if loc is None or rem > loc:
            updates.append(spec)
            print(
                f"NEWER: {spec.key} "
                f"{format_version(loc) if loc else '?'} -> {format_version(rem)}"
            )
        elif rem < loc:
            print(
                f"WARN: local {spec.key} {format_version(loc)} "
                f"is newer than ETSI listing {format_version(rem)} (keeping local)"
            )
        else:
            print(f"up-to-date: {spec.key} {format_version(loc)}")

    if check_only:
        return 0

    if not updates:
        print("No newer PDFs.")
        return 0

    new_versions = dict(local)
    for spec in updates:
        new_versions[spec.key] = remote[spec.key]

    if dry_run:
        print("dry-run: would download/update:")
        for spec in updates:
            print(f"  {pdf_urls[spec.key]}")
        return 0

    for spec in updates:
        t = remote[spec.key]
        folder = repo / "dmr" / spec.folder
        dest = folder / local_pdf_name(spec, t)
        print(f"downloading {spec.key} -> {dest}")
        try:
            download_pdf(pdf_urls[spec.key], dest)
        except Exception as e:  # noqa: BLE001
            print(f"ERROR downloading {spec.key}: {e}", file=sys.stderr)
            return 1
        remove_old_pdfs(folder, spec, dest)

    note = "已更新: " + ", ".join(
        f"{s.key}→{format_version(remote[s.key])}" for s in updates
    )
    update_status_md(repo, new_versions, note)
    update_nav_md(repo, new_versions)
    print(f"Updated {len(updates)} document(s).")
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--repo",
        type=Path,
        default=REPO_ROOT_DEFAULT,
        help="repository root (default: parent of scripts/)",
    )
    p.add_argument(
        "--check-only",
        action="store_true",
        help="only report versions; do not download or edit files",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="detect updates but do not write files",
    )
    args = p.parse_args(list(argv) if argv is not None else None)
    repo = args.repo.resolve()
    if not (repo / "dmr").is_dir():
        print(f"ERROR: {repo}/dmr not found", file=sys.stderr)
        return 2
    return run(repo, check_only=args.check_only, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
