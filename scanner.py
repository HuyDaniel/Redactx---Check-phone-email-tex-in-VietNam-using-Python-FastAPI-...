from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, List, Dict, Any
from pathlib import Path
import json
import csv
import re

from .utils import iter_paths, colorize
from .patterns.registry import get as get_pattern

@dataclass
class Finding:
    file: str
    pattern: str
    start: int
    end: int
    text: str

def scan_file(path: Path, pattern_names: List[str]) -> List[Finding]:
    findings: List[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"⚠️ Không đọc được {path}: {e}")
        return findings

    for name in pattern_names:
        try:
            pat: re.Pattern = get_pattern(name)
        except Exception as e:
            print(f"❌ Pattern '{name}' lỗi: {e}")
            continue

        for m in pat.finditer(text):
            findings.append(Finding(
                file=str(path), pattern=name,
                start=m.start(), end=m.end(),
                text=m.group(0)
            ))
    return findings

def redact_file_inplace(path: Path, pattern_names: List[str]) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"⚠️ Không đọc được {path}: {e}")
        return 0

    replaced = 0

    def mask(name: str, s: str) -> str:
        # rule mask tùy loại
        if name == "email":
            return re.sub(r"(^.).*(@.*$)", r"\1***\2", s)
        if name in ("phone_vn", "cccd_vn", "credit_card"):
            return s[:4] + "*" * (len(s) - 8) + s[-4:] if len(s) >= 8 else "*" * len(s)
        if name == "ipv4":
            return "***.***.***." + s.split(".")[-1]
        if name == "url":
            return s.split("://")[0] + "://***"
        return "*" * len(s)

    for name in pattern_names:
        pat = get_pattern(name)
        def _repl(m: re.Match):
            nonlocal replaced
            replaced += 1
            return mask(name, m.group(0))
        text = pat.sub(_repl, text)

    try:
        path.write_text(text, encoding="utf-8")
    except Exception as e:
        print(f"❌ Không ghi được {path}: {e}")
        return 0
    return replaced

def scan_paths(
    roots: Iterable[str], pattern_names: List[str],
    recursive: bool = True, include=None, exclude=None
) -> List[Finding]:
    results: List[Finding] = []
    for p in iter_paths(roots, recursive=recursive, include=include, exclude=exclude):
        results.extend(scan_file(p, pattern_names))
    return results

def print_findings(findings: List[Finding], color=False, context: int = 0):
    # In nhanh; có thể mở rộng thêm context
    for f in findings:
        s = f"{f.file}:{f.start}-{f.end} [{f.pattern}] "
        s += colorize(f.text) if color else f.text
        print(s)

def write_json(findings: List[Finding], out: str):
    with open(out, "w", encoding="utf-8") as f:
        json.dump([asdict(x) for x in findings], f, ensure_ascii=False, indent=2)

def write_csv(findings: List[Finding], out: str):
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["file", "pattern", "start", "end", "text"])
        w.writeheader()
        for x in findings:
            w.writerow(asdict(x))
