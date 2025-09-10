import re
from .registry import Pattern, register

# Visa/Master/Amex (đơn giản, không Luhn)
CREDIT = r"""
(?P<card>
  (?:4\d{12}(?:\d{3})?)                # Visa
  |
  (?:5[1-5]\d{14})                     # MasterCard
  |
  (?:3[47]\d{13})                      # AmEx
)
"""
register(Pattern("credit_card", CREDIT, re.VERBOSE, "Credit card (simple)"))
