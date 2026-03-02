import json
import re
import urllib.parse as up

SAFE_CHARS = "-._~:/?#[]@!$&'()*+,;=%"
ALLOWED = set("abcdefghijklmnopqrstuvwxyz0123456789" + SAFE_CHARS)


def clean_url(raw: str) -> str:
    raw = raw.strip()
    if not re.match(r'^[a-z]+://', raw):
        raw = "http://" + raw
    u = up.unquote(raw).lower()
    u = re.sub(r'^(https?://)www\.', r'\1', u)
    u = re.sub(r':(80|443)(?=/)', '', u)
    if u.endswith('/') and u.count('/') > 2:
        u = u[:-1]
    u = ''.join(c if c in ALLOWED else '_' for c in u)

    return u


CHARS = list(ALLOWED)
PAD, UNK = 0, 1
MAX_LEN = 200

with open("Backend_URL_Analyzer/URL_model/url_char_vocab.json", "r") as f:
    char2idx = json.load(f)


def encode_url(url: str) -> list[int]:
    ids = [char2idx.get(c, UNK) for c in url[:MAX_LEN]]
    return ids + [PAD] * (MAX_LEN - len(ids))

def process_url(url: str) -> list[int]:
    return encode_url(clean_url(url))