import re
from .registry import Pattern, register

# CCCD 12 số (đơn giản hóa)
CCCD = r"(?P<cccd>(?:\d{12}))"
register(Pattern("cccd_vn", CCCD, 0, "Vietnam citizen ID (simplified)"))
