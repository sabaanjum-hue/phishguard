"""URL feature extraction for PhishGuard."""

import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = {
    "login", "verify", "verification", "secure", "account", "update",
    "confirm", "banking", "signin", "password", "credential", "wallet",
}


def _normalise_url(url: str) -> str:
    url = str(url).strip()
    if not url:
        return ""
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url
    return url


def _is_ip_address(hostname: str | None) -> int:
    if not hostname:
        return 0
    return int(bool(re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", hostname)))


def extract_features(url: str) -> dict[str, int]:
    """Convert a URL into simple, explainable numerical features."""
    raw = str(url).strip()
    parsed = urlparse(_normalise_url(raw))
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    full = raw.lower()

    return {
        "url_length": len(raw),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "num_dots": raw.count("."),
        "num_hyphens": raw.count("-"),
        "num_slashes": raw.count("/"),
        "num_question_marks": raw.count("?"),
        "num_equals": raw.count("="),
        "num_at_symbols": raw.count("@"),
        "num_ampersands": raw.count("&"),
        "num_percent_symbols": raw.count("%"),
        "num_digits": sum(ch.isdigit() for ch in raw),
        "has_https": int(parsed.scheme.lower() == "https"),
        "has_ip_address": _is_ip_address(hostname),
        "has_port": int(parsed.port is not None) if parsed.hostname else 0,
        "num_subdomains": max(0, len(hostname.split(".")) - 2),
        "has_punycode": int("xn--" in hostname.lower()),
        "has_suspicious_word": int(any(word in full for word in SUSPICIOUS_WORDS)),
        "has_double_slash_path": int("//" in path),
    }


if __name__ == "__main__":
    for example in [
        "https://www.google.com",
        "http://secure-login-example.com/verify/account",
    ]:
        print(f"\nURL: {example}")
        print(extract_features(example))
