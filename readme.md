# RedactX — Scan & Redact PII (Regex) · CLI + API

Công cụ quét và ẩn thông tin nhạy cảm (PII) trong file bằng **regex nâng cao**. Có **CLI** và **REST API** (FastAPI).

## Features
- Patterns builtin: `email`, `phone_vn`, `cccd_vn`, `credit_card`, `ipv4`, `url`
- Scan thư mục (include/exclude), export JSON/CSV
- Redact in-place (ghi đè)
- API: `/scan/text`, `/scan/file`

## Install (dev)
```bash
python -m venv .venv && . .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
