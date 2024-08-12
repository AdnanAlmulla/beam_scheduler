import sys  # noqa: D100
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent

# Add the project root and SRC directories to sys.path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "SRC"))
