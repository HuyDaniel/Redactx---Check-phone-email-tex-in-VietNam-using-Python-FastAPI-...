import re
from .registry import Pattern, register

EMAIL = r"""
(?P<email>
  [a-z0-9._%+\-]+
  @
  [a-z0-9.\-]+
  \.[a-z]{2,}
)
"""
register(Pattern("email", EMAIL, re.IGNORECASE | re.VERBOSE, "Email address"))
