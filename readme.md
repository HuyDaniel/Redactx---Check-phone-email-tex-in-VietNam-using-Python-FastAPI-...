# 🕵️‍♂️ RedactX — Scan & Redact Sensitive Data (PII)

**RedactX** là một công cụ viết bằng Python để **phát hiện và ẩn thông tin nhạy cảm (PII)** trong file, sử dụng **Regex nâng cao**.  
Nó hỗ trợ chạy qua **CLI (command line)** và cả **REST API (FastAPI)** để dễ dàng tích hợp vào hệ thống khác.  

---

## ✨ Tính năng
- 🚀 CLI: quét file hoặc thư mục, hỗ trợ include/exclude glob (`--include "*.log"`).
- 🛡️ Redact: che thông tin nhạy cảm trực tiếp trong file (ghi đè).
- 📂 Export: xuất kết quả ra JSON/CSV.
- 🌐 API: FastAPI endpoint (`/scan/text`, `/scan/file`).
- 🔌 Patterns có sẵn:
  - `email`
  - `phone_vn` (số điện thoại Việt Nam)
  - `cccd_vn` (CMND/CCCD 12 số)
  - `credit_card` (Visa/Master/Amex – simple)
  - `ipv4`
  - `url`

---

## 📦 Cài đặt

Tạo virtualenv (tuỳ chọn):

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
## Cách cài đặt môi trường:
pip install -r requirements.txt

# Linux/Mac
source venv/bin/activate


CẤu trúc thư mục:
redactx/
├─ __init__.py
├─ cli.py
├─ api.py
├─ scanner.py
└─ patterns/
   ├─ __init__.py
   ├─ registry.py
   ├─ email.py
   ├─ phone_vn.py
   ├─ cccd_vn.py
   ├─ credit_card.py
   └─ ip_url.py
sample/
│  └─ data.txt
tests/
   └─ test_patterns.py


