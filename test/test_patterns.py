from redactx.patterns.registry import get
from redactx.patterns import email, phone_vn, ip_url  # noqa

def test_email():
    pat = get("email")
    assert pat.search("liên hệ a@b.com") is not None

def test_phone_vn():
    pat = get("phone_vn")
    assert pat.search("Gọi 0912345678 nhé") is not None
    assert pat.search("SĐT +84912345678 cũng hợp lệ") is not None

def test_url():
    pat = get("url")
    assert pat.search("https://example.org/page") is not None
