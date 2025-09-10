from __future__ import annotations
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
import re

from .scanner import scan_file, redact_file_inplace, Finding
from .patterns import registry  # noqa
from .patterns.registry import get as get_pattern

app = FastAPI(title="RedactX API")

class ScanRequest(BaseModel):
    text: str
    patterns: List[str] = ["email", "phone_vn", "url"]

class ScanResponse(BaseModel):
    findings: List[dict]

@app.post("/scan/text", response_model=ScanResponse)
def scan_text(req: ScanRequest):
    text = req.text
    findings: List[Finding] = []
    for name in req.patterns:
        pat = get_pattern(name)
        for m in pat.finditer(text):
            findings.append(Finding(file="<inline>", pattern=name, start=m.start(), end=m.end(), text=m.group(0)))
    return {"findings": [f.__dict__ for f in findings]}

@app.post("/scan/file")
async def scan_upload(patterns: str = Form("email,phone_vn,url"), file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")
    names = [x.strip() for x in patterns.split(",") if x.strip()]
    res = []
    for name in names:
        pat = get_pattern(name)
        for m in pat.finditer(content):
            res.append({"file": file.filename, "pattern": name, "start": m.start(), "end": m.end(), "text": m.group(0)})
    return {"findings": res}
