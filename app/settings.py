"""Load simple local key=value settings without evaluating shell expressions."""
import os
from pathlib import Path

def load_local_env():
    path=Path(__file__).resolve().parents[1]/'.env'
    if not path.exists():return
    for line in path.read_text().splitlines():
        line=line.strip()
        if line and not line.startswith('#') and '=' in line:
            key,value=line.split('=',1)
            os.environ.setdefault(key.strip(),value.strip().strip('\"\''))
