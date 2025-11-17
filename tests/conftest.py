"""Pytest configuration for Shannon tests"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Also set PYTHONPATH
os.environ['PYTHONPATH'] = parent_dir + ':' + os.environ.get('PYTHONPATH', '')
