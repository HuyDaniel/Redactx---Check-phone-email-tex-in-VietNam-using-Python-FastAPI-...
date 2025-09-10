from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from . import patterns  # <-- chỉ cần import package để auto-register
from .patterns.registry import get as get_pattern  # <-- dùng hàm get


# nạp registry để đăng ký pattern builtin
from .patterns import registry  # noqa
from .patterns.registry import get as get_pattern

app = FastAPI(title="RedactX API") 

class ScanRequest(BaseModel):
    text: str
    patterns: List[str] = ["email", "phone_vn", "url"]

@app.get("/")
def root():
    return {"ok": True, "service": "RedactX"}

@app.post("/scan/text")
def scan_text(req: ScanRequest):
    findings = []
    for name in req.patterns:
        pat = get_pattern(name)
        for m in pat.finditer(req.text):
            findings.append(
                {
                    "file": "<inline>",
                    "pattern": name,
                    "start": m.start(),
                    "end": m.end(),
                    "text": m.group(0),
                }
            )
    return {"findings": findings}

