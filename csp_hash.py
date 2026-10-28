"""Пересчитывает sha256 инлайн-скриптов в meta CSP index.html.

GitHub Pages не даёт ставить заголовки, поэтому CSP живёт в meta, а скрипты
разрешены по хешу. Правка любого скрипта без пересчёта = браузер молча его
не запустит. Запуск: python csp_hash.py
"""
import base64
import hashlib
import re
from pathlib import Path

page = Path(__file__).with_name("index.html")
raw = page.read_bytes()
# комментарии вырезаем: литерал <script> в комментарии однажды сошёл за скрипт
body = re.sub(rb"<!--.*?-->", b"", raw, flags=re.S)
scripts = re.findall(rb"<script>(.*?)</script>", body, flags=re.S)
hashes = " ".join(
    "'sha256-" + base64.b64encode(hashlib.sha256(s).digest()).decode() + "'" for s in scripts
)
new, n = re.subn(rb"script-src [^;]*;", f"script-src {hashes};".encode(), raw, count=1)
if not n:
    raise SystemExit("script-src в CSP не найден")
page.write_bytes(new)
print(f"скриптов: {len(scripts)}, CSP обновлён")
