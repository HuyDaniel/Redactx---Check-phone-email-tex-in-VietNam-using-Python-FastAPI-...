import re
from .registry import Pattern, register

# 0xxxxxxxxx hoặc +84xxxxxxxxx (10 số sau 0/+84)
PHONE_VN = r"(?P<phone>(?:\+?84|0)(?:\d){9})"
register(Pattern("phone_vn", PHONE_VN, re.VERBOSE, "Vietnam phone number"))
