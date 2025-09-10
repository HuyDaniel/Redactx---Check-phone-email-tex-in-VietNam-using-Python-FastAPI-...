import re
from .registry import Pattern, register

IPV4 = r"(?P<ipv4>(?:\d{1,3}\.){3}\d{1,3})"

URL = r"""
(?P<url>
 (?:https?|ftp)://
 [^\s/$.?#].[^\s]*
)
"""

register(Pattern("ipv4", IPV4, 0, "IPv4 (simple)"))
register(Pattern("url", URL, re.VERBOSE | re.IGNORECASE, "URL"))
