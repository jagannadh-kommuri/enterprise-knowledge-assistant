"""Initialize an empty deployment database with your configured embedding identity."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.settings import load_local_env
load_local_env()
os.environ['INIT_SCHEMA'] = 'true'
from app.main import create_app
create_app()
print('Atlas database initialized successfully.')
