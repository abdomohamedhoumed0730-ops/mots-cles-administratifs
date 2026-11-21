"""Configuration pytest : rend le dossier src/ importable, comme dans les scripts."""
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
