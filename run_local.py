"""Launch a loopback-only review server. Run after installing requirements."""
import os
import secrets
from pathlib import Path

root = Path(__file__).resolve().parent
os.chdir(root)
config = root / '.env'
if not config.exists():
    config.write_text('ADMIN_PASSWORD=' + secrets.token_urlsafe(24) + '\nREADER_PASSWORD=' + secrets.token_urlsafe(24) + '\nAI_MODE=preview\nCOOKIE_SECURE=false\nDATABASE_PATH=./data/atlas.sqlite3\n')
    config.chmod(0o600)
for line in config.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith('#') and '=' in line:
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('\"\''))
print('Atlas local review: http://127.0.0.1:8000')
print('Your workspace passwords are in .env. Never upload that file.')
import uvicorn
uvicorn.run('app.main:create_app', factory=True, host='127.0.0.1', port=8000)
