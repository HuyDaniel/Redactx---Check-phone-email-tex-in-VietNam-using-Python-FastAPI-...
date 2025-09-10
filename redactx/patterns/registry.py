# redactx/patterns/registry.py
from __future__ import annotations
import re
from functools import lru_cache
from typing import Dict

class Pattern:
    def __init__(self, name: str, regex: str, flags: int = 0, description: str = ""):
        self.name = name
        self.regex = regex
        self.flags = flags
        self.description = description

    def compile(self) -> re.Pattern:
        return re.compile(self.regex, self.flags)

_REGISTRY: Dict[str, Pattern] = {}

def register(p: Pattern) -> None:
    if p.name in _REGISTRY:
        raise ValueError(f"Pattern '{p.name}' đã tồn tại")
    _REGISTRY[p.name] = p

@lru_cache
def get(name: str) -> re.Pattern:
    if name not in _REGISTRY:
        raise KeyError(f"Pattern '{name}' chưa được đăng ký")
    return _REGISTRY[name].compile()

def all_names() -> list[str]:
    return list(_REGISTRY.keys())
