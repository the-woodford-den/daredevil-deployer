"""Root conftest for all tests - configures Python path."""

import os
import sys
from pathlib import Path

# Set DB_ENV to test BEFORE any imports that use settings
os.environ["DB_ENV"] = ".env.test"

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
