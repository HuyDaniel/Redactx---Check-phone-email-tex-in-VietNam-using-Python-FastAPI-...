from __future__ import annotations
import argparse
from .scanner import scan_paths, print_findings, write_json, write_csv, redact_file_inplace
from .patterns import registry  # load patterns

def main():
    ap = argparse.ArgumentParser("redactx", description="Scan & redact sensitive data (regex).")
    ap.add_argument("paths", nargs="+", help="File/thư mục để quét")
    ap.add_argument("-p", "--patterns", default="email,phone_vn,url",
                    help="Danh sách pattern, ví dụ: email,phone_vn,cccd_vn,credit_card,ipv4,url")
    ap.add_argument("--no-recursive", action="store_true", help="Không quét đệ quy")
    ap.add_argument("--include", action="append", help="Chỉ quét file khớp pattern (vd: *.log)")
    ap.add_argument("--exclude", action="append", help="Bỏ qua pattern file (vd: *.min.js)")
    ap.add_argument("--json", help="Ghi kết quả ra JSON")
    ap.add_argument("--csv", help="Ghi kết quả ra CSV")
    ap.add_argument("--color", action="store_true", help="Tô màu match khi in ra")
    ap.add_argument("--redact", action="store_true", help="Redact (ghi đè) thay vì chỉ scan")
    args = ap.parse_args()

    pats = [x.strip() for x in args.patterns.split(",") if x.strip()]

    if args.redact:
        # redact từng file
        total = 0
        from .utils import iter_paths
        for p in iter_paths(args.paths, recursive=not args.no_recursive, include=args.include, exclude=args.exclude):
            total += redact_file_inplace(p, pats)
            print(f"{p}: redacted {total} match(es) so far")
        print(f"Done. Total redacted: {total}")
        return

    findings = scan_paths(args.paths, pats, recursive=not args.no_recusive if hasattr(args, 'no_recusive') else not args.no_recursive,
                          include=args.include, exclude=args.exclude)
    print_findings(findings, color=args.color)

    if args.json:
        write_json(findings, args.json)
        print(f"Saved JSON -> {args.json}")
    if args.csv:
        write_csv(findings, args.csv)
        print(f"Saved CSV -> {args.csv}")

if __name__ == "__main__":
    main()
