"""Root conftest for all tests - configures Python path."""

import os
import sys
from pathlib import Path

os.environ["ENVFILE"] = ".env.example"

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
