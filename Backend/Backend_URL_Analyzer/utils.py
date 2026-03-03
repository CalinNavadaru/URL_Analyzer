def validate_url(url: str) -> bool:
    from urllib.parse import urlparse
    parsed = urlparse(url.strip())
    return  parsed.scheme in ('http', 'https') and bool(parsed.netloc)