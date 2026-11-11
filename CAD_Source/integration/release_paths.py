"""Paths shared by the FreeCAD and CadQuery export interpreters."""
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = WORK.parent
RELEASE = ROOT / 'dist' / 'Hexfellow_External_Drum_Leader'
